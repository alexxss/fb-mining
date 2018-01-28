@echo off
>>"C:\Users\OWNER\Documents\R crawler\log.txt" 2>&1(
echo ========= %date% %time% =========
cd C:\Users\OWNER\Documents\R crawler
automate.py 0
net start wampmysqld64 
cd C:\wamp64\www
C:\wamp64\bin\php\php5.6.31\php.exe auto_bygroup.php #update
C:\wamp64\bin\php\php5.6.31\php.exe auto_hash_update.php
net stop wampmysqld64 
)