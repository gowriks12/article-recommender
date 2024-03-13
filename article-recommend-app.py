import pickle
import pandas as pd
import streamlit as st
from streamlit import session_state as session
import types
from recommendations import Recommendations

recommender = Recommendations()

def my_hash_func(func):
    # Custom hash function for functions
    return hash(func.__code__)

@st.cache_data(persist=True, show_spinner=False, hash_funcs={types.FunctionType: my_hash_func})
def load_data():
    """
    load and cache data
    :return: tfidf data
    """
    recom_df = pd.read_csv("data/recom_df.csv", index_col=0)
    article_list = recom_df.index.tolist()
    return recom_df, article_list

recom_df, article_list = load_data()

top_publication_content, trending_articles, top_quick_reads, recommended = None, None, None, None

st.title("""
Medium Article Recommendation System
This is an Content Based Recommender System based on claps and responses :smile:.
 """)

st.text("")
st.text("")
st.text("")
st.text("")

session.options = st.multiselect(label="Select Article", options=article_list)

st.text("")
st.text("")

session.slider_count = st.slider(label="Article Count", min_value=5, max_value=10)

st.text("")
st.text("")

buffer1, col1, buffer2 = st.columns([1.45, 1, 1])

is_clicked = col1.button(label="Recommend")

if is_clicked:
    # dataframe = recommender.recommend_articles(recom_df=recom_df, article = session.options)
    top_publication_content, trending_articles, top_quick_reads, recommended = recommender.recommend_articles(article=session.options)

st.text("")
st.text("")
st.text("")
st.text("")

st.text("Top Publication Content Recommendations")
if top_publication_content is not None:
    st.table(top_publication_content['title'])

st.text("Trending Content Recommendations")
if trending_articles is not None:
    st.table(trending_articles['title'])

st.text("Quick Read Recommendations")
if top_quick_reads is not None:
    st.table(top_quick_reads['title'])

st.text("Because You read ", session.option)
if recommended is not None:
    st.table(recommended.index)
