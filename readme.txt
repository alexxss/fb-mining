�V�m�ҫ��G
1. Crawler.R
	�qFB��K�� //�n�A���}�g�@��
	�x�s�bid/g-id.csv
2. prettify.py
	�e�B�z
	�x�s�bid/g-id-c.csv
3. features.py
	�w�q�ҫ��S�x��
	�x�s�bfeatures.txt
4. get_features.py
	�w�q�K��S�x��
	�x�s�bid/g-id-n.csv
5. train.py
	�V�m�ҫ�
	�x�s�bmodel.m

�ϥΤ������G
1. Crawler.R
	�qFB��K�� -> {id}.csv (cp950)
2. preprocess.py
	�e�B�z     -> {id}-c.csv (utf8)
3. classify.py
	�w�q�K��S�x�� -> {id}-c.csv (utf8)
	�������       -> {id}.csv (utf8)

��L�G
autoscript.bat�G�I�sautomate.py�ó]�w�Ѽ�0
automate.py�G�����@�Ѽ�n�A���w�������e������īen-1��
	�I�sCrawler.R,preprocess.py,classify.py,new_hashing.py
	�ҡG��������9/11�An=0�A�h����óB�z9/10���K��
rundays.bat�G����óB�z20�Ѥ����K��

���榡�G
{id}.csv: �K���l���, classification
{id}-c.csv: id, prettified-message, feature