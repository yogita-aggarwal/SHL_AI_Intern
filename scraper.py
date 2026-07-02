# # # # import requests
# # # # from bs4 import BeautifulSoup

# # # # url = "https://www.shl.com/solutions/products/product-catalog/"

# # # # headers = {
# # # #     "User-Agent": "Mozilla/5.0"
# # # # }

# # # # response = requests.get(url, headers=headers)

# # # # print("Status Code:", response.status_code)

# # # # soup = BeautifulSoup(response.text, "html.parser")

# # # # print("Page Title:", soup.title.text)

# # # # # Print first 10 links from the page
# # # # links = soup.find_all("a")

# # # # print("\nFirst 10 Links:\n")

# # # # for link in links[:10]:
# # # #     print(link.get("href"))
# # # import requests
# # # from bs4 import BeautifulSoup
# # # import re
# # # from urllib.parse import urljoin

# # # url = "https://www.shl.com/solutions/products/product-catalog/"

# # # headers = {"User-Agent": "Mozilla/5.0"}

# # # response = requests.get(url, headers=headers)
# # # soup = BeautifulSoup(response.text, "html.parser")


# # # def clean_link(link):
# # #     if not link:
# # #         return None

# # #     # convert relative links to absolute
# # #     link = urljoin(url, link)

# # #     # extract valid URL
# # #     match = re.search(r'https?://[^\s\)\]\}"]+', link)
# # #     return match.group(0) if match else None


# # # links = soup.find_all("a")

# # # cleaned_links = []

# # # for link in links:
# # #     href = link.get("href")
# # #     clean = clean_link(href)

# # #     if clean and "shl.com" in clean:
# # #         cleaned_links.append(clean)

# # # print(cleaned_links[:10])
# # import requests
# # from bs4 import BeautifulSoup
# # from urllib.parse import urljoin

# # url = "https://www.shl.com/solutions/products/product-catalog/"

# # headers = {"User-Agent": "Mozilla/5.0"}

# # response = requests.get(url, headers=headers)
# # soup = BeautifulSoup(response.text, "html.parser")

# # base = "https://www.shl.com"

# # products = []

# # for a in soup.find_all("a"):
# #     href = a.get("href")
# #     name = a.text.strip()

# #     if not href:
# #         continue

# #     # convert relative links to absolute
# #     full_url = urljoin(base, href)

# #     # KEEP ONLY product catalog links
# #     if "/product" in full_url and "shl.com" in full_url:
# #         if name:  # ensure it has a title
# #             products.append({
# #                 "name": name,
# #                 "link": full_url
# #             })

# # print("Total clean products:", len(products))
# # print(products[:10])
# import requests
# from bs4 import BeautifulSoup
# from urllib.parse import urljoin

# url = "https://www.shl.com/solutions/products/product-catalog/"

# headers = {"User-Agent": "Mozilla/5.0"}

# response = requests.get(url, headers=headers)
# soup = BeautifulSoup(response.text, "html.parser")

# base = "https://www.shl.com"

# products = []

# seen = set()

# for a in soup.find_all("a"):
#     href = a.get("href")
#     name = a.text.strip()

#     if not href or not name:
#         continue

#     full_url = urljoin(base, href)

#     # ONLY keep assessment pages
#     if "/products/assessments/" not in full_url:
#         continue

#     # remove junk labels
#     if name.lower() in ["products", "assessments", "view all", ""]:
#         continue

#     # remove duplicates
#     if full_url in seen:
#         continue

#     seen.add(full_url)

#     products.append({
#         "name": name,
#         "link": full_url
#     })

# print("Final clean assessments:", len(products))
# print(products[:10])
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

url = "https://www.shl.com/solutions/products/product-catalog/"

headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

base = "https://www.shl.com"

products = []
seen = set()


def clean_link(link):
    if not link:
        return None

    # remove markdown artifacts
    link = link.replace("[", "").replace("]", "")

    # extract real URL
    match = re.search(r'https?://[^\s\)\]\}"]+', link)

    return match.group(0) if match else None


for a in soup.find_all("a"):
    href = a.get("href")
    name = a.text.strip()

    if not href or not name:
        continue

    full_url = urljoin(base, href)

    clean_url = clean_link(full_url)

    if not clean_url:
        continue

    # keep only assessment pages
    if "/products/assessments/" not in clean_url:
        continue

    # remove junk labels
    if name.lower() in ["products", "assessments", "view all", ""]:
        continue

    # remove duplicates
    if clean_url in seen:
        continue

    seen.add(clean_url)

    products.append({
        "name": name,
        "link": clean_url
    })

print("Final clean assessments:", len(products))
print(products[:10])