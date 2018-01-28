from group_ids import group_ids
import pandas as pd
from pathlib import Path
import sys
pd.options.mode.chained_assignment = None  # default='warn' (to turn off pandas warning text)
phppath="C:/wamp64/www/auto_hash_update.php"

#%% generate php script to update entries
def generate_php(group,post_id):
    print("Generating php script to update {0} in {1}".format(post_id,group),end="...")
    with open(phppath,"a") as phpout:
        phpout.write("$sql=$sql.\"UPDATE g{0} SET display=0 WHERE id=\'{1}\';\";\n".format(group,post_id))
    print("Done.")

#%% find duplicates & set older entry's 'show' to 0
def finddupe(filename,message,from_id,key):
    read_path = "hashfiles/" + str(filename) +".csv"
    print("Reading from",read_path,"...")
    df = pd.read_csv(read_path,encoding='utf-8',index_col=None,na_filter=False)
    found_msg = df['message'].apply(lambda x: x.replace(' ','')) == message.replace(' ','')
    found_frid = df['from_id'] == from_id
    found_key = df['key'] == key
    print("Looking for entry with key =",key)
    found_df = df[found_msg & found_frid & found_key]
    if found_df.empty: # can't find dupe
        print("No dupe found.")
        return False
    else:
        for index,dfs in found_df.iterrows(): # found dupe(s)!
            print("Found dupe:",dfs['id'])
            if dfs['show'] == 1:
                group=str(dfs["id"]).split('_')[0]
                #%% generate php to update this entry's 'show' value to 0
                generate_php(group,dfs["id"])
                #%% update 'show' value in g-xxx.csv
                updatepath = dfs['date'] + "/g-" + group + ".csv"
                print(dfs['id'],"in",updatepath,"will be set to 0...",end='')
                updatedt = pd.read_csv(updatepath,encoding='utf-8',index_col=0,na_filter=False)
                updatedt['show'][updatedt['id']==dfs['id']] = 0
                updatedt.to_csv(updatepath,index_label='index_i',encoding='utf-8')
                print("Done.")
                #%% update 'show' value in hashfile
                df['show'][df['id']==dfs['id']] = 0
                df.to_csv(read_path,encoding='utf-8',index=False)
        return True
#%%        

def main(datestr):
    hashnum = 100 # how many buckets
    
    #%% prepare php update script 
    with open(phppath,"w") as phpout:
        phpout.write("<?php\n")
        phpout.write("$servername=\"localhost\";\n")
        phpout.write("$username=\"root\";\n")
        phpout.write("$password=\"\";\n")
        phpout.write("$dbname=\"by_group\";\n")
        phpout.write("$conn=new mysqli($servername,$username,$password,$dbname);\n")
        phpout.write("if($conn->connect_error){\n\tdie(\"Connection failed: \".$conn->error);\n}\n")
        phpout.write("$sql=\"\";\n")
    #%%
    for gid in group_ids:
        #   read file
        read_path = datestr + '/g-' + gid + '.csv'
        read_path_c= datestr + '/g-' + gid + '-c.csv'
        print("Reading from",read_path,"...")
        df = pd.read_csv(read_path,encoding='utf-8',index_col=0,na_filter=False)
        dfc = pd.read_csv(read_path_c,encoding='utf-8',index_col=0,na_filter=False)
        
        #%%   get hash id/filename
        for dtf,dtm,dtid,dtfrid,dtclass in zip(dfc.feature,df.message,dfc.id,df.from_id,df.classification):
            if(dtclass != 0):
                ft = dtf.split(" ")
                totalft = 0
                for idx,fts in enumerate(ft):
                    if int(fts) > 0:
                        totalft += idx*int(fts) # sum of feature
                filename = totalft % hashnum
                
                new_entry=pd.DataFrame({'key':[str(totalft)],'id':[dtid],'from_id':[str(dtfrid)],'message':[dtm],'date':[datestr],'show':['1']})
                hashpath = Path("hashfiles/" + str(filename) + '.csv')                
                filepath = "hashfiles/" + str(filename) + ".csv"
                if hashpath.is_file():
                    # find dupe
                    finddupe(filename,dtm,dtfrid,totalft)
                    app = pd.read_csv(filepath,encoding='utf-8',index_col=None,na_filter=False)
                    app.append(new_entry,ignore_index=True).to_csv(filepath,encoding='utf-8',index=False)

                else:
                    new_entry.to_csv(filepath,encoding='utf-8',index=False)

                    print("Created file",hashpath)
                    
    #%% generate foot of php script
    with open(phppath,"a") as phpout:
        phpout.write("if($sql!=\"\"){\n")
        phpout.write("\tif($conn->query($sql)===TRUE){\n\techo \"Record updated successfully.\";\n}\n")
        phpout.write("\telse{\n\techo \"Error updating record: \".$conn->error;\n}\n}\n")
        phpout.write("$conn->close();\n")
        phpout.write("?>")
                    
#%% main
if __name__=='__main__':
    main(sys.argv[1])
    #%% bulk hashing    
#    from datetime import date,timedelta
#    for days in range(3,3+97):
#        yesterday = date.today() - timedelta(days=days)
#        datestring = yesterday.strftime("%Y-%m-%d")
#        main(datestring)        
    
    #%%
#        main("2017-12-03")