import pandas as pd
from datetime import date,timedelta
from group_ids import group_ids

def main(datestr,gid):
    filepath = datestr + "/g-" + gid + ".csv"
    print("Reading from:", filepath,"...")
    
    df = pd.read_csv(filepath,encoding='utf-8',index_col=0,na_filter=False )
    count = len(df.from_id)
    showcol = []
    for x in range(count):
        showcol.append(1)
    print("Writing to:",filepath,end="...")
    df['show'] = showcol
    df.to_csv(filepath,index_label="index_i",encoding='utf-8')
    print("Success.")

if __name__=='__main__':
    stepback = 97
    for gid in group_ids:
        for i in range(3,3+stepback):
            yesterday = date.today() - timedelta(days=i)
            datestr = yesterday.strftime("%Y-%m-%d")
            main(datestr,gid)
#        main("2017-08-26",gid)
            
