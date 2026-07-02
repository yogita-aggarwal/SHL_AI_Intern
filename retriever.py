# # # # # # import faiss
# # # # # # import pickle
# # # # # # from sentence_transformers import SentenceTransformer

# # # # # # # Load model
# # # # # # model = SentenceTransformer("all-MiniLM-L6-v2")

# # # # # # # Load FAISS index
# # # # # # index = faiss.read_index("vector_db/catalog.index")

# # # # # # # Load catalog
# # # # # # with open("vector_db/catalog.pkl", "rb") as f:
# # # # # #     catalog = pickle.load(f)

# # # # # # for item in catalog:
# # # # # #     if "link" in item:
# # # # # #         link = item["link"]

# # # # # #         if "(" in link and ")" in link:
# # # # # #             item["link"] = link.split("(")[1].split(")")[0]


# # # # # # def search_catalog(query, top_k=5):
# # # # # #     """
# # # # # #     Search the SHL catalog using semantic similarity.
# # # # # #     """

# # # # # #     embedding = model.encode([query])

# # # # # #     distances, indices = index.search(embedding, top_k)

# # # # # #     results = []

# # # # # #     for idx in indices[0]:
# # # # # #         if idx == -1:
# # # # # #             continue

# # # # # #         results.append(catalog[idx])

# # # # # #     return results
# # # # # import faiss
# # # # # import pickle
# # # # # from sentence_transformers import SentenceTransformer

# # # # # # Load model
# # # # # model = SentenceTransformer("all-MiniLM-L6-v2")

# # # # # # Load FAISS index
# # # # # index = faiss.read_index("vector_db/catalog.index")

# # # # # # Load catalog
# # # # # with open("vector_db/catalog.pkl", "rb") as f:
# # # # #     catalog = pickle.load(f)


# # # # # # -----------------------------
# # # # # # CLEAN LINK FUNCTION
# # # # # # -----------------------------
# # # # # def clean_link(link):
# # # # #     if not link:
# # # # #         return ""

# # # # #     # remove markdown-style links if present
# # # # #     if "(" in link and ")" and "[" in link:
# # # # #         try:
# # # # #             link = link.split("(")[1].split(")")[0]
# # # # #         except:
# # # # #             pass

# # # # #     return link.strip()


# # # # # # -----------------------------
# # # # # # MAIN SEARCH FUNCTION
# # # # # # -----------------------------
# # # # # def search_catalog(query, top_k=5):

# # # # #     embedding = model.encode([query])

# # # # #     distances, indices = index.search(embedding, top_k)

# # # # #     results = []

# # # # #     for idx in indices[0]:
# # # # #         if idx == -1:
# # # # #             continue

# # # # #         item = catalog[idx].copy()   # IMPORTANT: avoid mutating original

# # # # #         # normalize link safely
# # # # #         if "link" in item:
# # # # #             item["link"] = clean_link(item["link"])

# # # # #         results.append(item)

# # # # #     return results
# # # # import faiss
# # # # import pickle
# # # # import re
# # # # from sentence_transformers import SentenceTransformer

# # # # # Load embedding model
# # # # model = SentenceTransformer("all-MiniLM-L6-v2")

# # # # # Load FAISS index
# # # # index = faiss.read_index("vector_db/catalog.index")

# # # # # Load catalog
# # # # with open("vector_db/catalog.pkl", "rb") as f:
# # # #     catalog = pickle.load(f)


# # # # # -----------------------------
# # # # # CLEAN LINK FUNCTION (FIXED)
# # # # # -----------------------------
# # # # def clean_link(link):
# # # #     if not link:
# # # #         return ""

# # # #     link = str(link).strip()

# # # #     # Case 1: Markdown format [text](url)
# # # #     match = re.search(r'\((https?://[^\s\)]+)\)', link)
# # # #     if match:
# # # #         return match.group(1)

# # # #     # Case 2: Already clean URL
# # # #     if link.startswith("http"):
# # # #         return link

# # # #     return link


# # # # # -----------------------------
# # # # # CLEAN ENTIRE CATALOG ON LOAD
# # # # # -----------------------------
# # # # for item in catalog:
# # # #     if isinstance(item, dict) and "link" in item:
# # # #         item["link"] = clean_link(item["link"])


# # # # # -----------------------------
# # # # # SEARCH FUNCTION
# # # # # -----------------------------
# # # # def search_catalog(query, top_k=5):

# # # #     if not query:
# # # #         return []

# # # #     embedding = model.encode([query])

# # # #     distances, indices = index.search(embedding, top_k)

# # # #     results = []

# # # #     for idx in indices[0]:
# # # #         if idx == -1:
# # # #             continue

# # # #         if idx >= len(catalog):
# # # #             continue

# # # #         item = catalog[idx]

# # # #         results.append({
# # # #             "name": item.get("name", ""),
# # # #             "link": item.get("link", ""),
# # # #             "score": float(distances[0][list(indices[0]).index(idx)]) if len(distances[0]) > 0 else None
# # # #         })

# # # #     return results
# # # import faiss
# # # import pickle
# # # from sentence_transformers import SentenceTransformer

# # # model = SentenceTransformer("all-MiniLM-L6-v2")

# # # index = faiss.read_index("vector_db/catalog.index")

# # # with open("vector_db/catalog.pkl", "rb") as f:
# # #     catalog = pickle.load(f)


# # # def search_catalog(query, top_k=5):

# # #     query_embedding = model.encode([query])
# # #     distances, indices = index.search(query_embedding, top_k * 3)

# # #     results = []
# # #     q = query.lower()

# # #     for idx in indices[0]:
# # #         if idx == -1:
# # #             continue

# # #         item = catalog[idx].copy()

# # #         tags = item.get("tags", [])

# # #         # -----------------------
# # #         # INTENT BOOSTING
# # #         # -----------------------
# # #         score = 0

# # #         if "personality" in q and "personality" in tags:
# # #             score += 10

# # #         if "cognitive" in q or "aptitude" in q:
# # #             if "cognitive" in tags:
# # #                 score += 10

# # #         if "behavior" in q and "behavior" in tags:
# # #             score += 8

# # #         item["score"] = score
# # #         results.append(item)

# # #     # sort by score (important fix)
# # #     results = sorted(results, key=lambda x: x["score"], reverse=True)

# # #     return results[:top_k]
# # import faiss
# # import pickle
# # from sentence_transformers import SentenceTransformer

# # model = SentenceTransformer("all-MiniLM-L6-v2")

# # index = faiss.read_index("vector_db/catalog.index")

# # with open("vector_db/catalog.pkl", "rb") as f:
# #     catalog = pickle.load(f)

# # def clean_link(link):
# #     if not link:
# #         return ""

# #     # fix markdown links like [text](url)
# #     if "(" in link and ")" in link:
# #         try:
# #             link = link.split("(")[1].split(")")[0]
# #         except:
# #             pass

# #     return link.strip()

# # def search_catalog(query, top_k=5):
# #     embedding = model.encode([query])

# #     distances, indices = index.search(embedding, top_k)

# #     results = []

# #     for idx in indices[0]:
# #         if idx == -1:
# #             continue

# #         item = catalog[idx].copy()

# #         if "link" in item:
# #             item["link"] = clean_link(item["link"])

# #         results.append(item)

# #     return results
# import faiss
# import pickle
# from sentence_transformers import SentenceTransformer

# # -------------------------
# # Lazy-loaded singletons
# # -------------------------
# model = None
# index = None
# catalog = None


# def load_resources():
#     global model, index, catalog

#     if model is None:
#         model = SentenceTransformer("all-MiniLM-L6-v2")

#     if index is None:
#         index = faiss.read_index("vector_db/catalog.index")

#     if catalog is None:
#         with open("vector_db/catalog.pkl", "rb") as f:
#             catalog = pickle.load(f)


# def clean_link(link):
#     if not link:
#         return ""

#     if "(" in link and ")" in link:
#         try:
#             link = link.split("(")[1].split(")")[0]
#         except:
#             pass

#     return link.strip()


# def search_catalog(query, top_k=5):
#     load_resources()   # 🔥 FIX: prevents reload crash

#     embedding = model.encode([query])
#     distances, indices = index.search(embedding, top_k)

#     results = []

#     for idx in indices[0]:
#         if idx == -1:
#             continue

#         item = catalog[idx].copy()

#         if "link" in item:
#             item["link"] = clean_link(item["link"])

#         results.append(item)

#     return results
import faiss
import pickle
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

index = faiss.read_index("vector_db/catalog.index")

with open("vector_db/catalog.pkl", "rb") as f:
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