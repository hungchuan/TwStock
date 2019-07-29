import requests
import time
import json
import pandas as pd
from datetime import datetime, date
import os
#import csv


def get_twse(year, month, stock_id):
    #print('get_twse')
    date = str (year) + "{0:0=2d}".format(month) +'01' ## format is yyyymmdd
    sid = str(stock_id)
    url= 'http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date='+date+'&stockNo='+sid
    #print('URL twse = ',url)
    res = requests.get(url)
    #print("get_twse res=",res)
    smt = json.loads(res.text)     #convert data into json
    if (smt['stat']=="OK"):
        return smt['data']
    else:
        return []

	
def get_tpex(year, month, stock_id):
    #print('get_tpex')
    year = year-1911
    date = str (year)+'/'+ "{0:0=2d}".format(month)+'/'+'01' ## format is yyyymmdd
    sid = str(stock_id)
    url = 'https://www.tpex.org.tw/web/stock/aftertrading/daily_trading_info/st43_result.php?l=zh-tw&d='+date+'&stkno='+sid
    #print('URL tpex= ',url)
    res = requests.get(url)
    smt = json.loads(res.text)     #convert data into json
    return smt['aaData']

def get_twse_list():
    global newdf
    global dt
    #global year_list
    #global month_list

    dt = datetime.now() #現在時間
    dt.year
    dt.month
	
    PACKAGE_DIRECTORY = os.path.abspath('.')
    PACKAGE_DIRECTORY = PACKAGE_DIRECTORY + '\data'
    #print('PACKAGE_DIRECTORY = ',PACKAGE_DIRECTORY)

    twse_list_file=os.path.join(PACKAGE_DIRECTORY, "twse_list.xlsx")
    #print('isfile = ',os.path.isfile(twse_list_file))
    
    if (os.path.isfile(twse_list_file)==True):
        newdf = pd.read_excel(twse_list_file)
        return (newdf)
    
    if not os.path.isdir(PACKAGE_DIRECTORY):
        os.makedirs (PACKAGE_DIRECTORY)  # os.makedirs able to create multi folders	
		
    print('Download TWSE list....')

    #today_date_year = dt.year
    #year_list = range (2015,dt.year+1) #since 2015 to this year
    #month_list = range(1,13)  # 12 months
	
    df=pd.read_html('http://isin.twse.com.tw/isin/C_public.jsp?strMode=2',encoding='big5hkscs',header=0)
    newdf=df[0][df[0]['產業別'] > '0']
    del newdf['國際證券辨識號碼(ISIN Code)'],newdf['CFICode'],newdf['備註']
    df2=newdf['有價證券代號及名稱'].str.split(' ', expand=True)
    df2 = df2.reset_index(drop=True)
    newdf = newdf.reset_index(drop=True)
    for i in df2.index:
        if '　' in df2.iat[i,0]:
            df2.iat[i,1]=df2.iat[i,0].split('　')[1]
            df2.iat[i,0]=df2.iat[i,0].split('　')[0]
    newdf=df2.join(newdf)
    newdf=newdf.rename(columns = {0:'股票代號',1:'股票名稱'})
    del newdf['有價證券代號及名稱']
    newdf.to_excel(twse_list_file, sheet_name='twse',index=False)
    time.sleep(5)
    print('Download Finish')
    return newdf
	
def Is_twse(stock_id):
    global newdf
    #print('Is_twse')
    sid = str(stock_id)
    newdf2= newdf[newdf['股票代號'] == sid]
    if (len(newdf2)==1):
        return True
    else:
        return False

def get_webmsg(year, month, stock_id):
    #print('get_webmsg stock_id=',stock_id)
    if (Is_twse(stock_id)==True):
        data = get_twse(year,month,stock_id)
    else:
        data = get_tpex(year,month,stock_id)		
    return data

def fetch_from(year_from, month_from, stock_id):
    global dt
    #global year_list
    #global month_list
    Year_month=year_from*100+month_from
    smt = []
    #print('fetch_from',year_from,month_from,stock_id)
    for year in range(year_from,dt.year+1):
        for month in range(1,13):
            #print('year=',year)
            #print('month=',month)
            if ((year*100+month)>=Year_month):
                if (dt.year == year and month > dt.month) :break  # break loop while month over current month
                sid = str(stock_id)
                smt = smt + get_webmsg(year ,month, stock_id)           #put the data into smt
                #print("stock_id=",stock_id,year,month)
                #print("smt fetch_from = ",smt)
                time.sleep(5)				
    return smt
	
		
if __name__ == '__main__':
    #global year_list
    #global month_list
    global dt

    get_twse_list()

    #dt = datetime.now()
    #today_date_year = dt.year
    #year_list = range (2015,today_date_year+1) #since 2015 to this year
    #month_list = range(1,13)  # 12 months
	
    #twse_data = get_twse(2019,6,2330)
    #twse_data = twse_data + get_twse(2019,7,2330)
    #print(fetch_from(2019,7,2330))
    print(fetch_from(2018,7,1616))
    #print('twse_data=',twse_data)
    #print('get_twse = ',get_twse(2019,7,2330))
    #print('get_tpex = ',get_tpex(2019,7,4939))

'''
url_twse ='http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&'
url_tpex ='https://www.tpex.org.tw/web/stock/aftertrading/daily_trading_info/st43_result.php?l=zh-tw'
res = requests.get(url_twse)
print(res)
s = json.loads(res.text)
'''