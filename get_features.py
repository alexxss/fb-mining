#this script obtains features of each dataset
import nltk
import pandas as pd
from group_ids import group_ids

#group_ids = ['979903922059977','1612153615732604','349760251870471']
features = pd.read_csv('features.txt',encoding='cp950')['key']

for g_id in group_ids:
    read_path = g_id+'/g-'+g_id+'-c.csv'
    write_path = g_id+'/g-'+g_id+'-n.csv'
    #讀檔
    df = pd.read_csv(read_path,encoding='cp950',index_col=0,na_filter=False )
    genfeatr = [] #準備一個list做為新的欄位
    for msg in df['message']:
        postfeatr = [] #準備一list儲存這篇貼文的feature
        data = msg.split(' ') #以空格split出一個個單字
        fdist = nltk.FreqDist(data) #統計單字出現的次數
        for word in features: 
            postfeatr.append(str(fdist[word]) if word in fdist else '0')
        pf_tostr = " ".join(postfeatr) #串成一個str以便儲存
        genfeatr.append(pf_tostr) #塞進新的"column"
    #寫檔: 每篇貼文的feature及其分類 
    df.assign(feature = genfeatr).to_csv(write_path,index='index',columns=['feature','class'])