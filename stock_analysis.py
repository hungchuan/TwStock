import tw_stock
import datetime
import pygsheets
import time
import os
import sys
from datetime import datetime, date
import csv
import numpy as np
import pandas as pd
import threading
import pdb

def DF2List(df_in):
    train_data = np.array(df_in)#np.ndarray()
    df_2_list=train_data.tolist()#list
    return df_2_list
    
# 子執行緒的工作函數
def job(num):
  for i in range(5):
    print("Child thread:", num)
    time.sleep(num)

  
def main (args):

    twse_list = tw_stock.get_twse_list() #download TWSE list

    try:
        if (args[1]=="1"):
            print("下載精選股資料")
            download_stock(1)
        else:
            download_single_stock(args[1])			
    except:    
        print("下載上市櫃待分析股資料")  
        # 建立 2 個子執行緒
        threads = []
        for i in range(2):
          threads.append(threading.Thread(target = download_stock, args = (i+2,)))
          threads[i].start()

        # 等待所有子執行緒結束
        for i in range(2):
          threads[i].join()      
       
    print('Done')
    
    
def download_stock(input):    
    print(input)	
    sel = str(input)

    PACKAGE_DIRECTORY = os.path.abspath('.')
    PACKAGE_DIRECTORY = PACKAGE_DIRECTORY + '\data'

    #twse_list = tw_stock.get_twse_list() #download TWSE list

    download_months = 12

    today_date = datetime.now() #現在時間
    #year_from = today_date.year
    this_year = today_date.year
    #month_from = today_date.month
    this_month = today_date.month

    month_end = str (this_year-1911)+'/'+ "{0:0=2d}".format(this_month)+'/' +'01' ## format is yyyy/mm/dd 轉民國

    #year_list = range (2015,year_from+1) #since 2015 to this year
    #month_list = range(1,13)  # 12 months


    if (this_month<=download_months):
        month_from = this_month+12-download_months
        year_from = this_year-1
    else:
        month_from = this_month-download_months
        year_from = this_year

    month_begin = str (this_year-1-1911)+'/'+ "{0:0=2d}".format(this_month)+'/' +'01' ## format is yyyy/mm/dd 轉民國

    gc = pygsheets.authorize(service_file='PythonUpload-cfde37284cdc.json')

    sh_good = gc.open('Stock_PythonUpload2')
    print('Stock_PythonUpload2 Open')
    Good_Stock_wks = sh_good.worksheet_by_title("list")
    Good_Stock_list = Good_Stock_wks.get_values(start=(2,1), end=(500,2), returnas='matrix')

    df_Good_Stock = pd.DataFrame(Good_Stock_list, columns=['股票代號','股票名稱']) 

    # Open spreadsheet and then workseet
    if (sel=='2' or sel=='3'): 
        sh = gc.open('Stock_PythonUpload_analysis')
        print('Stock_PythonUpload_analysis Open')
    else:    
        sh = gc.open('Stock_PythonUpload2')
        print('Stock_PythonUpload2 Open')

    wks_list = sh.worksheets()

    if (sel=='2'): 
        wks=sh.worksheet_by_title("twse list")	
    elif (sel=='3'):
        wks=sh.worksheet_by_title("tpex list")
    else:    
        wks = sh.worksheet_by_title("list")


    Stock_list = wks.get_values(start=(2,1), end=(999,2), returnas='matrix')
    print(Stock_list)

    array_row=len(Stock_list)
    stock_zero = [['' for i in range(9)] for j in range(300)]
    df_empty = pd.DataFrame(columns=['date','volume','amount','open','high','low','close','spread','Quantity'])

    emptyfile = os.path.join(PACKAGE_DIRECTORY,'empty.csv')
    df_analysis = pd.read_csv(emptyfile)
    df_analysis = df_analysis.dropna()
    
    analysis_list=[['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0']]
    analysis_list_0=analysis_list    
    
    for i in range(0,array_row):#array_row
        print('i=',i)
        print('Stock_Name = ',Stock_list[i][1]) 
		
        if (i<(array_row-1)):
            analysis_list=analysis_list+analysis_list_0
			
        print("len=",len(analysis_list))
        #wks = sh.worksheet_by_title("123")    
        writefile = os.path.join(PACKAGE_DIRECTORY, Stock_list[i][0]+Stock_list[i][1]+'.csv')
        #print(writefile)
        
        if (os.path.isfile(writefile)==True):
            df_csv = pd.read_csv(writefile)
            year_from_new = this_year
            month_from_new = this_month
            #print(year_from)
            #print(month_from)
            df_csv2 = df_csv[ df_csv['date'] > month_begin]
            df_csv3 = df_csv2[ df_csv2['date'] < month_end]        
        else:
            print("===============================creat new file===============================")
            df_csv3 = df_empty
            year_from_new = year_from
            month_from_new = month_from

        #print('df_csv3 = ',df_csv3)
        #pdb.set_trace()
        
        if (sel=='2'): 
            wks=sh.worksheet_by_title("Analyze_twse")	
        elif (sel=='3'):
            wks=sh.worksheet_by_title("Analyze_tpex")
        else:    
            try:
                wks = sh.worksheet_by_title(Stock_list[i][1])
            except:
                wks = sh.add_worksheet(Stock_list[i][1],rows=300,cols=10,index=0)    
        
        #print('wks=',wks)
        
        print(year_from_new,month_from_new,Stock_list[i][0])
        
        print('download.................')
        try:
            #stock_No = twstock.Stock(Stock_list[i][0])	
            stock_data = tw_stock.fetch_from(year_from_new,month_from_new,Stock_list[i][0])     # 獲取至今日之股票資料
        except KeyboardInterrupt:
            break
        except:
            continue

        #print('stock_data = ',stock_data)
        #stock_No = twstock.Stock(Stock_list[i][0])
        #stock_data = tw_stock.fetch_from(year_from_new,month_from_new,Stock_list[i][0])     # 獲取至今日之股票資料
        df_new = pd.DataFrame(stock_data, columns=['date','volume','amount','open','high','low','close','spread','Quantity']) 
        df_new2=pd.concat([df_csv3,df_new],ignore_index=True)  
        df_new2.to_csv(writefile,index=0)
        print("writefile=",writefile)
        #print('df_new2 = ',df_new2)
        #pdb.set_trace()
        
        '''
        stock_data_row=len(df_new2)
        stock_data_len=len(df_new2[0])
        print(stock_data_row)
        print(stock_data_len)        
        stock_array = [['' for i in range(stock_data_len)] for j in range(stock_data_row)]
        '''
        #stock_array = stock_data
        #wks = sh.worksheet_by_title("123")  
        try:        
            wks.update_values(crange='A2:I310', values=stock_zero) # update a range of values with a cell list or matrix 
        except:
            continue
            
        time.sleep(1)		
        
        df_new2_2_list=DF2List(df_new2)
        #print(df_new2_2_list)    
        try:          
            wks.update_values(crange='A2:I290', values=df_new2_2_list) # update a range of values with a cell list or matrix 
        except:
            continue
            
        if (sel=='2' or sel=='3'):
            result_list = wks.get_values(start=(300,34), end=(300,64), returnas='matrix')
            analysis_list[i]=result_list[0]
            #df_Stock_result = pd.DataFrame(analysis_list, columns=['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30']) 
            #df_analysis=pd.concat([df_analysis,df_Stock_result],ignore_index=True)  
            #print(df_analysis)
            #df_analysis_2_list=DF2List(df_analysis)
            if (sel=='2'):
                wks=sh.worksheet_by_title("twse list")	
            else:
                wks=sh.worksheet_by_title("tpex list")	
                
            wks.update_values(crange='D2:AI999', values=analysis_list) # update a range of values with a cell list or matrix 
                    
            
            sid = str(Stock_list[i][0])
            print('sid=',sid)
            df_Good_Stock2= df_Good_Stock[df_Good_Stock['股票代號'] == sid]
            if (len(df_Good_Stock2)==1):
                print('In good list......................................')
                try:
                    Good_Stock_wks = sh_good.worksheet_by_title(Stock_list[i][1])
                except:
                    Good_Stock_wks = sh_good.add_worksheet(Stock_list[i][1],rows=300,cols=10,index=0)    
                
                try:        
                    Good_Stock_wks.update_values(crange='A2:I310', values=stock_zero) # update a range of values with a cell list or matrix 
                except:
                    continue
            
                time.sleep(1)		   
                
                try: 
                    Good_Stock_wks.update_values(crange='A2:I310', values=df_new2_2_list) # update a range of values with a cell list or matrix        
                except:
                    continue

        
        print('Time = ',datetime.now())	
        '''
        cvs_file=os.path.join(PACKAGE_DIRECTORY, writefile)
        outputfile = open(cvs_file,'w', newline='')
        outputwriter = csv.writer(outputfile)  
        outputwriter.writerow(['date','volume','amount','open','high','low','close','spread','Quantity'])
        #outputwriter.writerow(stock_data)
        for row in stock_data:
            outputwriter.writerow(row)
        outputfile.close()
            
        print('Time = ',datetime.now())	
        #if (i<array_row-1):
        #    time.sleep(40) 
        '''
    #print('Done')

    
def download_single_stock(input):    
    print("download_single_stock=",input)	
    stock_no = str(input)

    PACKAGE_DIRECTORY = os.path.abspath('.')
    PACKAGE_DIRECTORY = PACKAGE_DIRECTORY + '\data'

    download_months = 12

    today_date = datetime.now() #現在時間
    this_year = today_date.year
    this_month = today_date.month

    month_end = str (this_year-1911)+'/'+ "{0:0=2d}".format(this_month)+'/' +'01' ## format is yyyy/mm/dd 轉民國

    if (this_month<=download_months):
        month_from = this_month+12-download_months
        year_from = this_year-1
    else:
        month_from = this_month-download_months
        year_from = this_year

    month_begin = str (this_year-1-1911)+'/'+ "{0:0=2d}".format(this_month)+'/' +'01' ## format is yyyy/mm/dd 轉民國

    gc = pygsheets.authorize(service_file='PythonUpload-cfde37284cdc.json')

    # Open spreadsheet and then workseet
    sh = gc.open('Stock_PythonUpload_analysis')
    print('Stock_PythonUpload_analysis Open')

    stock_zero = [['' for i in range(9)] for j in range(300)]
 
    year_from_new = year_from
    month_from_new = month_from 

    wks_list = sh.worksheets()
	
    wks=sh.worksheet_by_title("Analyze_twse")	 
    print(year_from_new,month_from_new,stock_no)        
    print('download.................')

    stock_data = tw_stock.fetch_from(year_from_new,month_from_new,stock_no)     # 獲取至今日之股票資料


    df_new = pd.DataFrame(stock_data, columns=['date','volume','amount','open','high','low','close','spread','Quantity']) 
    
    wks.update_values(crange='A2:I310', values=stock_zero) # update a range of values with a cell list or matrix 

    time.sleep(1)		
        
    df_new2_2_list=DF2List(df_new)
      
    wks.update_values(crange='A2:I290', values=df_new2_2_list) # update a range of values with a cell list or matrix 
    print('download_single_stock finish')                                
       


if __name__ == '__main__':
    main (sys.argv)


#if __name__ == '__main__':
#    print('Main')
    #print(tw_stock.get_twse(2019,6,2330))
    #print(tw_stock.get_tpex(2019,6,4939))