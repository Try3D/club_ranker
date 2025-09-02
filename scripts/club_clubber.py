from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans

from clubs import CLUBS


model = SentenceTransformer("nomic-ai/nomic-embed-text-v1", trust_remote_code=True)

files = []
for d in CLUBS:
    files.append(open(f"reports/{d}.md", "r").read())

embeddings = [model.encode(files[i], convert_to_tensor=True) for i in range(len(files))]

for i in range(len(embeddings)):
    embeddings[i] = embeddings[i].to("cpu")

kmeans = KMeans(n_clusters=5, random_state=42, n_init="auto")

fit = kmeans.fit(embeddings)


clusters = {}
for i in range(len(CLUBS)):
    if fit.labels_[i] in clusters:
        clusters[fit.labels_[i]].append(CLUBS[i])
    else:
        clusters[fit.labels_[i]] = [CLUBS[i]]

print(clusters)
