import requests
from io import StringIO
import pandas as pd
import json
import GS_RW as gs
from datetime import datetime, date, timedelta
import time
from print_log import log_print,Emptyprintf,printLineFileFunc

wait_time = 121

def wait(sec):
    for i in range(0,sec):
        time.sleep(1) 
        print ('delay: %d' % i)


def Is_weekend(date):
    if date.weekday() in [5,6]:
        return True
    else:
        return False

def add_date(date,df_in):
    #now = datetime.now()
    #now2=now+timedelta(1)
    #now2=now2-timedelta(2)
    #date= now.strftime("%Y")+now.strftime("%m")+now.strftime("%d")  
    df_in['date']=date
    cols = df_in.columns.tolist()
    cols.insert(0,cols.pop(cols.index('date')))
    df_final=df_in[cols]
    #print(df_final) 
    return df_final

def download_corporation():
    printLineFileFunc()
    gs.clear_sheet("Stock_PythonUpload_analysis","corporation")
    now = datetime.now()
    download_date = now
    
    i = 0
    while True:
        while (Is_weekend(download_date)==True):
            download_date=download_date-timedelta(1)
            
        str_date= download_date.strftime("%Y")+download_date.strftime("%m")+download_date.strftime("%d")              

        print ('i= %d' % i)
        print('str_date=',str_date)
        url = 'https://www.twse.com.tw/rwd/zh/fund/T86?response=csv&date='+str_date+'&selectType=ALLBUT0999'
        print('url=',url)
        
        try:
            res = requests.get(url)
        except:
            print('requests.get fail')
            
        try:
            df = pd.read_csv(StringIO(res.text), header=1,engine = "python").dropna(how='all', axis=1).dropna(how='any')
        except:
            download_date=download_date-timedelta(1)
            str_date= now.strftime("%Y")+now.strftime("%m")+now.strftime("%d")  
            #i = i+1
            wait(wait_time)
            continue          
            
        df = add_date(str_date,df)
        if (i==0):
            df_all=df                              
        else:    
            df_all=pd.concat([df_all,df],ignore_index=True)   
        
        download_date=download_date-timedelta(1)
        #str_date= download_date.strftime("%Y")+download_date.strftime("%m")+download_date.strftime("%d")  
        print(df_all) 
        i = i+1
        if(i>10):
            break        
        wait(wait_time)


    df_all.to_csv("test2022.csv",encoding='utf_8_sig')
    gs.upload_to_google('Stock_PythonUpload_analysis','corporation',df_all)


if __name__ == '__main__':
    printLineFileFunc()
    download_corporation()