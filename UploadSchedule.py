from io import BytesIO
from zipfile import ZipFile
import urllib.request
from datetime import date,timedelta
import pandas as pd
import schedule
import time
import datetime
import requests

def uploadData():
    url = "http://localhost:8000/upload/"    
    files = {'file' : open("bse.csv","rb")}
    r = requests.post(url,files=files)
    print("file status code: ",r.status_code)

def getData():
    class AppURLopener(urllib.request.FancyURLopener):
        version = "Mozilla/5.0"
    
    opener = AppURLopener()
    weekdayNum=datetime.datetime.now().weekday()
    
    crntTime=time.strftime("%H:%M")
    
    if weekdayNum<5:
        if crntTime < '18:00':
            if(weekdayNum==0):
                dateUsed = (date.today() - timedelta(days = 3)).strftime("%d%m%y")
            else:
                dateUsed = (date.today() - timedelta(days = 1)).strftime("%d%m%y")
            url = 'https://www.bseindia.com/download/BhavCopy/Equity/EQ'+dateUsed+'_CSV.ZIP'
            response = opener.open(url)
            
            zipfile = ZipFile(BytesIO(response.read()))
            dateFile='EQ'+dateUsed+'.CSV'
            
            df = pd.read_csv(zipfile.open(dateFile))
            df.to_csv('bse.csv',index=False)            
            uploadData()                        
        else:                      
            dateUsed = date.today().strftime("%d%m%y")
            url = 'https://www.bseindia.com/download/BhavCopy/Equity/EQ'+dateUsed+'_CSV.ZIP'
            response = opener.open(url)
            
            zipfile = ZipFile(BytesIO(response.read()))
            
            dateFile='EQ'+dateUsed+'.CSV'
            
            df = pd.read_csv(zipfile.open(dateFile))

            df.to_csv('bse.csv',index=False)
            
            uploadData()
            

            
    else:
          dateUsed = (date.today() - timedelta(days = weekdayNum-4)).strftime("%d%m%y")
          url = 'https://www.bseindia.com/download/BhavCopy/Equity/EQ'+dateUsed+'_CSV.ZIP'
          response = opener.open(url)
         
          zipfile = ZipFile(BytesIO(response.read()))
          dateFile='EQ'+dateUsed+'.CSV'
         
          df = pd.read_csv(zipfile.open(dateFile))
          df.to_csv('bse.csv',index=False)
          uploadData()
         

    
getData()

schedule.every().day.at("18:00").do(getData)

while True:
    schedule.run_pending()
    time.sleep(60)
    