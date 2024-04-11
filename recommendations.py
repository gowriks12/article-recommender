import pickle
import pandas as pd
# import streamlit as st
# from streamlit import session_state as session
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize
from sklearn.decomposition import NMF

class Recommendations:
    def __init__(self):
        self.df = pd.read_csv("data/medium_data.csv", index_col="id")
        self.df = self.df.drop_duplicates()

    def fix_titles(self, title):
        # Define a pattern to match HTML tags
        html_tags_pattern = re.compile(r'<.*?>')

        # Replace HTML tags with an empty string
        cleaned_title = re.sub(html_tags_pattern, '', title)

        return cleaned_title

    def preprocess_data(self):
        self.df['date'] = pd.to_datetime(self.df['date'], dayfirst=True)
        self.df['title'] = self.df['title'].apply(self.fix_titles)
        self.df["claps"] = self.df["claps"].fillna(0)
        self.df["subtitle"] = self.df["subtitle"].fillna(self.df["title"])
        return self.df

    def top_content(self):
        pub_popularity = self.df.groupby('publication')[['claps', 'responses']].mean().round().astype(int).sort_values(
            by='claps', ascending=False)
        top_three_publications = pub_popularity['claps'].nlargest(3).index
        channels = top_three_publications.tolist()
        top_articles = pd.DataFrame()  # Initialize an empty DataFrame to store top articles

        for channel in channels:
            cont = self.df[self.df['publication'] == channel]
            top_n_articles = cont.nlargest(3, 'claps')  # Select top 3 articles for the channel
            top_articles = pd.concat([top_articles, top_n_articles])  # Concatenate with previous top articles

        return top_articles

    # print(top_content(df))

    def trending_article(self):
        latest_date = self.df['date'].max()
        latest_week = latest_date - pd.Timedelta(days=6)
        latest_articles = self.df[self.df['date'] >= latest_week]
        top_three = self.df.loc[latest_articles['claps'].nlargest(3).index]
        top_three_trending = top_three['title'].tolist()
        return top_three

    # print(trending_article(df))

    def popular_quick_reads(self):
        quick_reads = self.df[self.df['reading_time'] <= 5.0]
        quick_reads_df = self.df.loc[quick_reads['claps'].nlargest(3).index]
        #     popular_quick_reads = quick_reads_df['title'].tolist()
        return quick_reads_df

    def similarity_matrix(self):
        # Create a new feature article which is combination of both title and subtitle
        self.df['article'] = self.df['title'] + self.df['subtitle']
        # Sort Data by number of claps
        self.df = self.df.sort_values(by="claps", ascending=False)
        # Now, we have to vectorize the articles using Tf-IDF vecotizer.
        # Pre processing and NMF
        vectorizer = TfidfVectorizer()
        articles = vectorizer.fit_transform(self.df["article"])
        # Now we can apply NMF on our data and create the recommender. I choose 10 as number of components.
        model = NMF(n_components=10, random_state=0)
        nmf_features = model.fit_transform(articles)
        #     model.components_
        normalized = normalize(nmf_features)
        recom_df = pd.DataFrame(data=normalized)
        recom_df.set_index(self.df['title'], inplace=True)
        recom_df.to_csv("data/recom_df.csv")

    def content_based_recommendation(self, recom_df, article, count):
        similarities = recom_df.dot(article)
        sims = pd.DataFrame(similarities.nlargest(count+1))
        sims = sims.merge(self.df[["title", "claps", "url", "publication"]], how='inner', on="title")
        sims.set_index("title", drop=True, inplace=True)
        sims.sort_values(by="claps", ascending=False)
        return sims

    def recommend_articles(self, article, count):
        print("In recommend articles---------------")
        self.df = self.preprocess_data()
        print("Data Preprocessed-------------------")
        recom_df = pd.read_csv("data/recom_df.csv", index_col=0)
        # a = self.df[self.df['title'] == article[0]]
        art = recom_df.loc[article]
        # print(art)
        top_publication_content = self.top_content()
        trending_articles = self.trending_article()
        top_quick_reads = self.popular_quick_reads()
        recommended = self.content_based_recommendation(recom_df=recom_df, article=art, count=count)
        # recomms = recommended.loc[1:]
        recommended = recommended.drop(recommended.index[0])
        recommended = recommended[["url","publication","claps"]]
        print(recommended)

        return top_publication_content, trending_articles, top_quick_reads, recommended


if __name__=="__main__":
    recommender = Recommendations()
    count =10
    article = ["How ChatGPT Works: The Model Behind The\xa0Bot"]
    top_publication_content, trending_articles, top_quick_reads, recommended = recommender.recommend_articles(article, count)
    print("-----------------------------------------------")
    print("----------------Recommendations----------------")
    print("-----------------------------------------------")
    print(" ")
    print("----Top Publication Content Recommendations----")
    print(top_publication_content['title'])
    print("-------Trending Content Recommendations--------")
    print(trending_articles['title'])
    print("-----------Quick Read Recommendations----------")
    print(top_quick_reads['title'])
    print("----Because You read ", article[0], "----")
    print(recommended.index)
    print("-----------------------------------------------")

