#this script determines model features
import nltk
import pandas as pd
from group_ids import group_ids
#group_ids = ['979903922059977','1612153615732604','349760251870471']

data = []
for g_id in group_ids:    
    read_path = g_id+'/g-'+g_id+'-c.csv'
    df = pd.read_csv(read_path,encoding='cp950',index_col=0,na_filter=False ) #讀檔
    for msg in df['message']:
        data = data + msg.split(' ') #空格分開單字

fdist = nltk.FreqDist(data) #所有貼文拿來統計 單字出現的次數
cout = open("features.txt","w+")
cout.write("key,value\n")
for word in fdist:
    sentence = word + "," + str(fdist[word]) + "\n"
    cout.write(sentence)