import numpy as np
from sklearn.decomposition import PCA
from scipy.spatial.distance import cdist
import pandas as pd
import csv

# Load the courses
with open("../courses.csv", newline="") as f:
    courses = [row[0] for row in csv.reader(f)]
print(len(courses))

# Load the categories
with open("categories.csv", newline="") as f:
    categories = [row[0] for row in csv.reader(f)]
print(len(categories))

# Embeddings
embeddings_array = np.loadtxt("courses_embeddings_full.csv", delimiter=",")
categories_embeddings_array = np.loadtxt(
    "categories_embeddings_full.csv", delimiter=","
)

# PCA
pca = PCA(n_components=8)
pca_embeddings = pca.fit_transform(embeddings_array)
print(pca_embeddings.shape)

# Category PCA
pca_categories = pca.transform(categories_embeddings_array)

# Save the embeddings
np.savetxt("courses_embeddings.csv", pca_embeddings, delimiter=",")
np.savetxt("categories_embeddings.csv", pca_categories, delimiter=",")

# Distances
subject_distances = cdist(embeddings_array, categories_embeddings_array)
df = pd.DataFrame(subject_distances, columns=categories, index=courses)
df.to_csv("subject_distances.csv")
