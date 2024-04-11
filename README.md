# Medium Article Recommender
Content Based Recommendation System to recommend medium articles to users based on what they read earlier.

![Logo](https://github.com/gowriks12/article-recommender/main/static/article-recommender-demo.gif)

## Steps to Setup

Clone the repository
```bash
  git clone https://github.com/gowriks12/article-recommender.git
```
Go to the project directory

```bash
  cd article-recommender
```

Create a new environment (with pip)
```bash
pip install virtualenv
virtualenv myenv
.\myenv\Scripts\activate
```
Alternatively can use conda environment as well

Install dependencies
```bash
pip install -r requirements.txt
```

Start the App Server
```bash
streamlit run article-recommend-app.py
```

Select the article and click on recommend button to get personalized and generalized article recommendations
