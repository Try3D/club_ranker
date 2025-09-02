from sentence_transformers import SentenceTransformer, util
from clubs import CLUBS


model = SentenceTransformer("nomic-ai/nomic-embed-text-v1", trust_remote_code=True)

files = []
for d in CLUBS:
    files.append(open(f"reports/{d}.md", "r").read())

similarity_matrix = [[0] * len(CLUBS) for _ in range(len(CLUBS))]

for i in range(len(CLUBS)):
    for j in range(i + 1, len(CLUBS)):
        embedding_1 = model.encode(files[i], convert_to_tensor=True)
        embedding_2 = model.encode(files[j], convert_to_tensor=True)

        similarity_matrix[i][j] = util.pytorch_cos_sim(embedding_1, embedding_2)

used = [False] * len(CLUBS)
pairs = []
for _ in range(len(CLUBS) // 2):
    max_sim = -1
    max_i, max_j = -1, -1
    for i in range(len(similarity_matrix)):
        if used[i]:
            continue
        for j in range(i + 1, len(similarity_matrix)):
            if used[j]:
                continue
            if similarity_matrix[i][j] > max_sim:
                max_sim = similarity_matrix[i][j]
                max_i, max_j = i, j
    if max_i != -1 and max_j != -1:
        pairs.append((CLUBS[max_i], CLUBS[max_j], max_sim))
        used[max_i] = True
        used[max_j] = True

print(pairs)
