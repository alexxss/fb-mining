#this script extracts previously obtained features for model training
import pandas as pd
from sklearn.cross_validation import train_test_split
from sklearn import svm
from sklearn.externals import joblib #"儲存"model用
from group_ids import group_ids
#group_ids = ['979903922059977','1612153615732604','349760251870471']

data=[]
label=[]
for g_id in group_ids:
    read_path = g_id+'/g-'+g_id+'-n.csv'
    print("reading data from ",read_path,"...",end="")
    df = pd.read_csv(read_path,index_col=0,na_filter=False)
    print("done")
    for i,d in df.iterrows(): #把所有檔案的data合在一起
        data.append(d['feature'].split(' '))
        label.append(pd.to_numeric(d['class'], errors='coerce'))

#分割訓練資料及測試資料(測資:訓練資料 = 3:7)
print("splitting train/test sets...",end="")    
X_train,X_test,y_train,y_test = train_test_split(data,label,test_size=0.5,random_state=0)
print("done")

#定義一個svc
svc_model = svm.SVC(gamma=0.001,C=100.,kernel='linear')

#fitting
print("fitting model...",end="")
svc_model.fit(X_train,y_train)
print("done")

#顯示score
print("score: ",svc_model.score(X_test,y_test))

#儲存model
joblib.dump(svc_model,"model.m")
print("model saved: model.m")