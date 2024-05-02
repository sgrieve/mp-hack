import csv
import numpy as np
from sentence_transformers import SentenceTransformer

# Load the model
model = SentenceTransformer("paraphrase-MiniLM-L6-v2")

# Load the courses
with open("../courses.csv", newline="") as f:
    courses = [row for row in csv.reader(f)]
print(len(courses))

# Compute the embeddings
embeddings = []
for course in courses:
    embeddings.append(model.encode(course)[0])
embeddings_array = np.array(embeddings)
print(embeddings_array.shape)
np.savetxt("courses_embeddings_full.csv", embeddings_array, delimiter=",")

# Load the categories
with open("categories.csv", newline="") as f:
    reader = csv.reader(f)
    categories = list(reader)
print(len(categories))

# Category embeddings
embeddings = []
for category in categories:
    embeddings.append(model.encode(category)[0])
embeddings_array = np.array(embeddings)
print(embeddings_array.shape)
np.savetxt("categories_embeddings_full.csv", embeddings_array, delimiter=",")
