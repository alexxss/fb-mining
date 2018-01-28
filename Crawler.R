library(Rfacebook)
library(RJSONIO)
library(rjson)
#### execute on first run only  ####
#fb_oauth <- fbOAuth( app_id = "1586829294666696",
#                   app_secret = "cd4481ffc97e24974a46678c30f49e7a")
dir_fb_oauth = "C:\\Users\\OWNER\\Documents\\R crawler\\fboauth.RData"
#workspace = "C:\\Users\\OWNER\\Documents\\R crawler\\.RData"
#save(dir_fb_oauth, file = dir_fb_oauth)
####################################
#load(workspace)
load(dir_fb_oauth)

#list of group ids
ids <- c(979903922059977,1612153615732604,349760251870471)
wd <- ""
fpath <- ""
args <- commandArgs(trailingOnly = TRUE)
stepBackDays <- as.integer(args[1])

#### get dates ####
gettoday <- Sys.Date() - stepBackDays
today <- ""
today = format.Date(gettoday,"%Y/%m/%d") 

getyesterday <- gettoday -1
yesterday <- ""
yesterday = format.Date(getyesterday,"%Y/%m/%d")
##################

print(paste("Crawling on ",yesterday,"..."))

# creat & set working directory #
wd = paste("C:\\Users\\OWNER\\Documents\\R crawler\\",as.character(getyesterday),sep="")
dir.create(wd)
setwd(wd)
  
# crawl  
for(id in ids){
  attempt <- 0
  while(1){
    attempt <- attempt + 1
    try(
      fb_page <- getGroup(group_id=id,
                         token = fb_oauth,
                         since = yesterday,
                       until = today)
    )
    if(nrow(fb_page)>0 || attempt < 5) break
  }
  if(nrow(fb_page)>0){  
    fpath = paste("g-",as.character(id),".csv",sep="")
    rownames(fb_page) <- 1:nrow(fb_page) # reindex rows
    write.csv(fb_page,fpath) # write file
    print(sprintf("Crawl %s successful on attempt #%d.",id,attempt))
  }
  else
    print(sprintf("Crawl %s unsuccessful. Attempts: %d",id,attempt))
}
# reset working directory
setwd("C:\\Users\\OWNER\\Documents\\R crawler\\")