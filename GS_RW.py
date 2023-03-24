import pygsheets


def upload_to_google(file, sheet, df):
    try:
        gc = pygsheets.authorize(service_file='PythonUpload-cfde37284cdc.json')
    except:
        return filename
    
    sh = gc.open(file)

    try:
        wks = sh.worksheet_by_title(sheet)
    except:
        wks = sh.add_worksheet(sheet,rows=1,cols=30,index=0)    
     
    wks.set_dataframe(df, (1, 1))
    '''
    sh = gc.open('Translation_Symptom')

    try:
        wks = sh.worksheet_by_title('data in')
    except:
        wks = sh.add_worksheet(gh_name,rows=510,cols=80,index=0)    
     
    wks.set_dataframe(En_df, (1, 1))
    '''
    return wks    

def download_from_google(file, sheet):
    try:
        gc = pygsheets.authorize(service_file='PythonUpload-cfde37284cdc.json')
    except:
        log("can not find json file")
    
    sh = gc.open(file)

    try:
        wks = sh.worksheet_by_title(sheet)
    except:
        wks = sh.add_worksheet(sheet,rows=1,cols=30,index=0)    
     
    df = wks.get_as_df()

    return df 

def clear_sheet(file, sheet):
    try:
        gc = pygsheets.authorize(service_file='PythonUpload-cfde37284cdc.json')
    except:
        log("can not find json file")
    
    sh = gc.open(file)

    try:
        wks = sh.worksheet_by_title(sheet) 
        wks.clear() 
    except:
        log("can not open sheet")
    
    

    
if __name__ == '__main__':
    clear_sheet("Stock_PythonUpload_analysis","corporation")
    
    #config_df=download_from_google("Stock_PythonUpload_analysis","config")
    #print('config_df=',config_df)
    #print('config_df[00]=',config_df.iloc[0][0])
    #print('config_df[01]=',config_df.iloc[0][1])


