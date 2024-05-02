import csv
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.decomposition import PCA

# Load the courses
with open("courses.csv", newline="") as f:
    reader = csv.reader(f)
    courses = list(reader)
print(len(courses))

# Load the model
model = SentenceTransformer("paraphrase-MiniLM-L6-v2")

# Compute the embeddings
embeddings = []
for course in courses:
    embeddings.append(model.encode(course)[0])
embeddings_array = np.array(embeddings)
print(embeddings_array.shape)

# PCA
pca = PCA(n_components=8)
pca_embeddings = pca.fit_transform(embeddings_array)
print(pca_embeddings.shape)

# Save the embeddings
np.savetxt("courses_embeddings.csv", pca_embeddings, delimiter=",")
