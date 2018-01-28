#this script extracts previously obtained features for model training
import nltk
import pandas as pd
import numpy as np
#from sklearn import svm
from sklearn.externals import joblib #"儲存"model用
from group_ids import group_ids
#from datetime import date, timedelta
import sys

def main(date):
    clf = joblib.load("model.m")
    features = pd.read_csv('features.txt',encoding='cp950')['key']
    #yesterday = date.today() - timedelta(days=1)
    #date = yesterday.strftime("%Y-%m-%d")
    
    for group_id in group_ids:
        read_path = date+'/g-'+group_id+'-c.csv'
        #讀檔
        print("Reading from",read_path+"...")
        df = pd.read_csv(read_path,encoding='utf-8',index_col=0,na_filter=False )
        genfeatr = [] #準備一個list做為新的欄位
        print("Generating features...",end=" ")
        for msg in df['message']:
            postfeatr = [] #準備一list儲存這篇貼文的feature
            data = msg.split(' ') #以空格split出一個個單字
            fdist = nltk.FreqDist(data) #統計單字出現的次數
            for word in features: 
                postfeatr.append(str(fdist[word]) if word in fdist else '0')
            pf_tostr = " ".join(postfeatr) #串成一個str以便儲存
            genfeatr.append(pf_tostr) #塞進新的"column"
        print("done")
        #寫檔: 每篇貼文的feature及其分類 
        df.assign(feature = genfeatr).to_csv(read_path,index='index',encoding='utf-8')
        print("Feature generation done. Written to",read_path)
    
    for group_id in group_ids:
        read_path = date+'/g-'+group_id+'-c.csv'
        write_path = date+'/g-'+group_id+'.csv'
        #讀檔
        print("Reading from",read_path+"...")
        df = pd.read_csv(read_path,encoding='utf-8',index_col=0,na_filter=False )
        d = pd.read_csv(write_path,encoding='cp950',index_col=0,na_filter=False )
        classcol = []
        showcol = []
        print("Classifying...")
        for feature in df['feature']:
            ftr = feature.split(' ')
            classval = clf.predict(np.array(ftr).reshape(1,-1))
            classcol.append(classval[0])
            showcol.append(1)
        d.assign(classification = classcol).assign(show = showcol).to_csv(write_path,index_label='index_i',encoding='utf-8')
        print("Classification done. Written to",write_path)
        
if __name__=='__main__':
    main(sys.argv[1])
#    main('2017-10-16')