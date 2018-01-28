訓練模型：
1. Crawler.R
	從FB抓貼文 //要再分開寫一個
	儲存在id/g-id.csv
2. prettify.py
	前處理
	儲存在id/g-id-c.csv
3. features.py
	定義模型特徵值
	儲存在features.txt
4. get_features.py
	定義貼文特徵值
	儲存在id/g-id-n.csv
5. train.py
	訓練模型
	儲存在model.m

使用分類器：
1. Crawler.R
	從FB抓貼文 -> {id}.csv (cp950)
2. preprocess.py
	前處理     -> {id}-c.csv (utf8)
3. classify.py
	定義貼文特徵值 -> {id}-c.csv (utf8)
	丟分類器       -> {id}.csv (utf8)

其他：
autoscript.bat：呼叫automate.py並設定參數0
automate.py：接受一參數n，指定日期為當前日期的第前n-1天
	呼叫Crawler.R,preprocess.py,classify.py,new_hashing.py
	例：執行日期為9/11，n=0，則抓取並處理9/10的貼文
rundays.bat：抓取並處理20天內的貼文

文件格式：
{id}.csv: 貼文原始資料, classification
{id}-c.csv: id, prettified-message, feature