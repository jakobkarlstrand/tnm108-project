from joblib import load

def classify_articles(article_array):

    clf = load("newsclassifier.joblib")

    return clf.predict_proba(article_array)

    

