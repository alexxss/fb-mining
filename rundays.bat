@ECHO off
>multidaysLog.txt 2>&1(
FOR /L %%A IN (0,1,52) DO (
automate.py %%A
)
)