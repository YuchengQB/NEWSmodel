"""
機器學習：文章標題-報社
"""

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
import pandas as pd

df = pd.read_csv("1018_00_03_新聞.csv") #記得改這邊，不然會讀同一個檔

news_x = df.loc[:,"NEWS"]
news_y = df.loc[:,"Writer"]

train_x,test_x,train_y,test_y = train_test_split(news_x, news_y,test_size=0.1) #0.2好像最高

model = make_pipeline(TfidfVectorizer(), MultinomialNB())
model.fit(train_x,train_y)
predicted_label= model.predict(test_x)


'''
print(predicted_label)
print(test_y)
'''
from sklearn import metrics
import matplotlib.pyplot as plt
import seaborn as sns;sns.set()

accuracy = metrics.accuracy_score(test_y,predicted_label)
print(accuracy)

mat = metrics.confusion_matrix(test_y,predicted_label)

sns.heatmap(mat.T,square=True,annot=True,fmt='d',cbar='F',
            xticklabels=["CHDTV","LTN","TVBS","UDN"],yticklabels=["CHDTV","LTN","TVBS","UDN"])



