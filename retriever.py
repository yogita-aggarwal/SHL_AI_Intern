import faiss
import pickle
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

index = faiss.read_index("catalog.index")

with open("catalog.pkl", "rb") as f:
    catalog = pickle.load(f)
def clean_link(link):
    if not link:
        return ""
    link = str(link).strip()

    if "(" in link and ")" in link:
        try:
            link = link.split("(")[1].split(")")[0]
        except:
            pass

    return link

def search_catalog(query, top_k=10):
    embedding = model.encode([query])
    distances, indices = index.search(embedding, top_k)

    results = []

    for idx in indices[0]:
        if idx == -1 or idx >= len(catalog):
            continue

        item = catalog[idx].copy()
        item["link"] = clean_link(item.get("link", ""))

        results.append(item)

    return results
