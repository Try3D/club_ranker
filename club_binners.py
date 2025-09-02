import os
from google import genai
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans

from clubs import CLUBS

mapping = ["" for _ in range(len(CLUBS))]

for i in range(len(CLUBS)):
    club = CLUBS[i]
    out = ""
    if os.path.exists(f"logs_linkedin/{club}.txt"):
        lines = open(f"logs_linkedin/{club}.txt").read()

        out += "Linkedin summary:"
        out += lines

    if os.path.exists(f"logs_whatsapp/{club}.txt"):
        lines = open(f"logs_whatsapp/{club}.txt").read()

        out += "Linkedin summary:"
        out += lines

    if os.path.exists(f"logs_instagram/{club}.txt"):
        lines = open(f"logs_instagram/{club}.txt").read()

        out += "Linkedin summary:"
        out += lines

    if os.path.exists(f"club_reports/{club}.md"):
        lines = open(f"club_reports/{club}.md").read()

        out += "Linkedin summary:"
        out += lines

    mapping[i] = out


client = genai.Client(api_key="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

for i in range(len(CLUBS)):
    prompt = """
    You are a embedding-optimized summarizer for clubs part of shiv nadar university chennai
    Given structured input, generate one compact paragraph with high semantic density, suitable for vector embeddings.

    Include explicit information such as domain, activities conducting, purpose, reception, etc.

    Use direct language with minimal stop words. Avoid headings, label phrases, repetition, or list formatting.
    Retain only relevant narrative elements.
    Ensure the paragraph uses consistent structure and maximizes keyword richness for semantic search. Output must be a single, unbroken paragraph.
    """
    response = client.models.generate_content(
        model="gemini-2.5-pro",
        contents=f"{prompt}\n\nInput:{mapping[i]}",
    )
    mapping[i] = response.text

model = SentenceTransformer("nomic-ai/nomic-embed-text-v1", trust_remote_code=True)

embeddings = [
    model.encode(mapping[i], convert_to_tensor=True) for i in range(len(mapping))
]

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
