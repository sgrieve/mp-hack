from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import matplotlib.pyplot as plt

from io import BytesIO
import base64


app = FastAPI(title="MP Hack API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
    allow_credentials=True,
)

@app.get("/")
def test():
    return {"API": 'Working'}

@app.get("/mp")
def mp():
    data = pd.read_csv('database/mp.csv')
    return data.to_dict(orient='records')

@app.get("/subject")
def subject():
    data = pd.read_csv('database/subject.csv')
    return data.to_dict(orient='records')

@app.get("/university")
def university():
    data = pd.read_csv('database/university.csv')
    return data.to_dict(orient='records')

@app.get("/relationship")
def relationship():
    df1 = pd.read_csv('database/mp.csv')
    df2 = pd.read_csv('database/subject.csv')
    df3 = pd.read_csv('database/university.csv')
    relationship_df = pd.read_csv('database/relationship.csv')

    merged_df = pd.merge(relationship_df, df1, left_on='MP', right_on='ID', how='left')
    merged_df = pd.merge(merged_df, df2, left_on='Subject', right_on='ID', how='left')
    merged_df = pd.merge(merged_df, df3, left_on='University', right_on='ID', how='left')
    merged_df = merged_df.replace([float('inf'), float('-inf'), float('NaN')], None)    
    merged_df[['lat', 'lng']] = merged_df['UniLocation'].str.split(',', expand=True)
    merged_df['lat'] = pd.to_numeric(merged_df['lat'])
    merged_df['lng'] = pd.to_numeric(merged_df['lng'])
    return merged_df.to_dict(orient='records')


def create_graph():
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv('courses.csv')
    degrees = df.iloc[:, 0]

    # Convert text data into a matrix of token counts
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(degrees)

    # Store feature names
    feature_names = vectorizer.get_feature_names_out()

    # Define the number of topics
    num_topics = 5  # You can adjust this based on your data and requirements

    # Fit LDA model
    lda_model = LatentDirichletAllocation(n_components=num_topics, random_state=42)
    lda_model.fit(X)

    # Function to display top words for each topic
    def display_topics(model, feature_names, n_top_words):
        topics = []
        for topic_idx, topic in enumerate(model.components_):
            topic_words = [feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]]
            topics.append((topic_idx, topic_words))
        return topics

    # Set the number of top words to display for each topic
    num_top_words = 10

    # Get top words for each topic
    topics = display_topics(lda_model, feature_names, num_top_words)

    # Plotting
    plt.figure(figsize=(12, 8))  # Increase figure size
    # Extract topic distribution for each document
    topic_dist = lda_model.transform(X)

    # Count the number of documents associated with each topic
    topic_counts = pd.DataFrame(topic_dist).idxmax(axis=1).value_counts().sort_index()

    # Plotting the distribution of topics
    plt.bar(range(num_topics), topic_counts.values)
    plt.xlabel('Major Theme', fontsize=14)  # Increase font size
    plt.ylabel('Number of Degrees', fontsize=14)  # Increase font size
    plt.title('Distribution of Major Themes in Degrees', fontsize=16)  # Increase font size

    # Update x-axis labels with major themes
    plt.xticks(range(num_topics), [f'Theme {i+1}: {" ".join(topics[i][1])}' for i in range(num_topics)], rotation=45, ha='right', fontsize=12)  # Increase font size

    # Save the plot to a BytesIO object
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')  # Adjust bounding box
    buf.seek(0)  # Move to the start of the BytesIO buffer
    plt.close()  # Close the plot to release resources

    return buf.getvalue()

@app.get("/plot/")
async def get_plot():
    plot_bytes = create_graph()
    return StreamingResponse(BytesIO(plot_bytes), media_type="image/png")
