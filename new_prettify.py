#this script pre-processes each dataset
import re
import jieba
import pandas as pd
from group_ids import group_ids

jieba.set_dictionary('dict.txt.big') #使用繁中字典
stp = pd.read_csv('stopwords.txt',encoding='utf-8-sig') # 自訂義stopwords，windows注意encoding
stopwords = {}.fromkeys(stp['words']) #把讀出來的stopwords串成dict

#一串id一個個run
for group_id in group_ids:
    read_path = group_id+'/g-'+group_id+'.csv'
    write_path = group_id+'/g-'+group_id+'-c.csv'
    #讀檔，注意encoding
    df = pd.read_csv(read_path,usecols=['index','message','class'],encoding='cp950',index_col=0,na_filter=False)
    #各種regex
    RemoveEmoji = re.compile(r"<[eU][d\+][\w]*>") #去除表情符號編碼
    RemoveUrl = re.compile(r"https?://([a-zA-Z0-9]+[.?&#_=/]*)+")#去除網址連結
    RemoveNonChar = re.compile(r"[a-zA-Z0-9]+")
    RemovePunct = re.compile(r"[^\w]")#去除標點符號
    RemoveSpace = re.compile(r" +")#去除多餘空格
    
    df['message'] = [RemoveUrl.sub('',msg) for msg in df['message']]
    df['message'] = [RemoveEmoji.sub('',msg) for msg in df['message']]
    df['message'] = [RemoveNonChar.sub('',msg) for msg in df['message']]
    df['message'] = [RemovePunct.sub('',msg) for msg in df['message']]
    df['message'] = ['NA' if (msg == '') else msg for msg in df['message']]    
    #開始斷句
    d = df['message']
    for i,msg in enumerate(d):
        words = jieba.cut(msg) #切
        words = ['' if word in stopwords else word for word in words]
        sentence = " ".join(words)#用空格把一串切好的字串起來
        sentence = RemoveSpace.sub(" ",sentence) #去掉多餘的空格
        d[i+1] = 'NA' if (sentence == " ") else sentence 
    
    #存檔    
    df['message'] = d    
    df.to_csv(write_path,index='index')