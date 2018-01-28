import sys
import pandas as pd
import subprocess
from datetime import date, timedelta, datetime

stepback = int(sys.argv[1]) # get command line input: number of days to stepback
pd.options.mode.chained_assignment = None  # default='warn' (to turn off pandas warning text)

yesterday = date.today() - timedelta(days=stepback)
datestr = yesterday.strftime("%Y-%m-%d")

logpath = datestr+'\log.txt'
#f = open(logpath,"a")
#orig = sys.stdout
#sys.stdout = f

### call R script from Python ###
command = 'C://Program Files//R//R-3.4.1//bin//Rscript'
path2Rscript = 'Crawler.R'
cmd = [command,path2Rscript] + [sys.argv[1]]
#subprocess.call(cmd,stdout=f,shell=False)
subprocess.call(cmd,shell=False) 
#################################

datevar = date.today() - timedelta(days=stepback+1)
datestr = datevar.strftime("%Y-%m-%d")
print(datetime.now(),datestr) 
import preprocess
preprocess.main(datestr)
import classify
classify.main(datestr)
import new_hashing
new_hashing.main(datestr)
#f.close()
#sys.stdout = orig