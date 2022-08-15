import datetime
import pandas as pd
import os
from pathlib import Path
class LogAnalyzer():
    """
    Process of automaticaly generate logfile by EOL in readable format.

    Methods:

        values(file, skip_rows=9, use_cols = [0,2],
        names = ["Inspections","Values"])
        - process one file by reading measurment values

        Return: pandas.dataframe with header as list of inspections
                and their values.
        #
        header(file, read_rows=14,skip_rows=1,use_col=[0,2],
                names=["Inspections","Values"])
        - process one file and return head information as SW version,
          Firmware version, etc.
        - Add information from file name, such as PN,Date,Time,etc.

        Return: pandas.DataFrame
        #
        check_file(df,method="Header")

        - old function, used to identify file format version.
        - will be deleted in future.

        Return: bool value
        #
        check_file2(self,file,use_cols = [0,2],
                names = ['Inspections','Values'],
            dtype={"Inspections":"string"})
        - method that check what kind of inspections and where are they
        in log file.
        - return values are dict. with index number of specific inspections,
        common or specific for each EOL

        Return: tuple
        df => pandas.DataFrame
        common_index => Dict.
        EOL6_index => Dict.
        #
        creat_file(file="")
        - create excel file with name as
        - <Teste names> + <today date>
        - all files are saved in /<application folder>/Reports

        Return: pandas.ExcelWriter object
        #
        process_data(file=[])
         /Useable for ZBE EOL 2,3,4/
        - process all given EOL log files.
        - read all files, separete Header and Values
        - merge all into one DataFrame
        - write final DataFrame into ExcelFile

        Return: pandas.DataFrame
        #
        process_data_Haptic(self,file=[])
        /Usable for ZBE EOL 6/
        - same purpose as method process_data()

        Return: pandas.DataFrame

    """
    def __init__(self,file):

        """
        """
        self.file = file
        #self.PATH_TO_SAVE = "E:/EOL_Summary/"
        self.PATH_TO_SAVE = "F:/EOL_Summary/"
        
    #
    #
    #
    def get_info(self,file,station=-8,station_name=-6,pn=-5,ecu_id=-4,date=-3,
                time=-2,error_code=-1):
        """
        Get necessary data info from file name.Such as PN,Date,Time,etc.
        Ver. 0.0.2
        Changed indexing from positive to negative,
        to increase robustness.
        """
        self.file = file
        self.partInfo = file.split('_')
        self.STATION = self.partInfo[station]
        self.STATION_NAME = self.partInfo[station_name]
        self.PN = self.partInfo[pn]
        self.ECU_ID = self.partInfo[ecu_id]
        self.DATE = self.partInfo[date]
        self.TIME = self.partInfo[time]
        self.ERROR_CODE = self.partInfo[error_code].split('.')


        pass
    #
    #
    #
    def values(self,skip_rows = 9, use_cols = [0,2],
                               names = ["Inspections","Values"]):
        '''
        Process of automaticaly generate logfile by EOL
        file:  adress of one csv file that will be proceed
        skip_rows:  number rows in csv from top that will be skipped
        '''
        #import csv file into dataframe
        #df = pd.read_csv(self.file,skiprows = skip_rows, usecols = use_cols,
        #                names = names)
        #debug
        #print (self.df.iloc[skip_rows:,:])
        self.df_values = self.df.iloc[skip_rows:,:]
        #get list names of inspections that will be use as Header
        new_names = self.df_values.Inspections
        #Transpose dataframe (change rows and columns)
        self.df_values = self.df_values.T
        #delete unnecessary data
        self.df_values = self.df_values.drop(["Inspections"],axis=0)
        #assign new header as names of inspections
        self.df_values.columns = new_names


        return self.df_values
    #
    #
    #
    def header(self,read_rows = 14,skip_rows = 1,use_cols = [0,2],
              names=["Inspections","Values"]):
        """
        ToDo:
        1.Add docstrings
        2.list of arguments
        3.Return values description

        Version:
        ver. 0.0.2
        """
        self.df_header = self.df.iloc[skip_rows:skip_rows+2,:]
        #Transform dataframe
        self.df_header = self.df_header.T
        #assign new header names
        self.df_header.columns = names
        #get ic and sw version info and copy to temp.
        main_ic_name = str(self.df_header.iloc[0,0])
        main_ic_version = str(self.df_header.iloc[1,0])
        pic_ic_name = self.df_header.iloc[0,1]
        pic_ic_version = self.df_header.iloc[1,1]
        #update DF based on info from file name
        self.df_header.insert(0,'P/N',self.PN)
        self.df_header.insert(1,'ECU Unique ID',self.ECU_ID)
        self.df_header.insert(2,'Date',self.DATE)
        self.df_header.insert(3,'Time',self.TIME)
        self.df_header.insert(4,main_ic_name,main_ic_version)
        self.df_header.insert(5,pic_ic_name,pic_ic_version)
        self.df_header.insert(6,'Error code',self.ERROR_CODE[0])
        #drop unnecessary columns, keep only first 7 count from 0
        self.df_header = self.df_header.drop(self.df_header.columns[7:],axis=1)
        #drop inspections row
        self.df_header = self.df_header.drop(["Inspections"])
        #
        return self.df_header
    #
    #
    #
    def check_file(self,df2,method="Header"):
        """
        Function depracapted! Will be deleted in future.
        """
        if method == "Header":
            if self.df2.iloc[0][0] == "Inspection information":
                return True
            else:
                return False
        elif method == "Haptic":
            if self.df2.iloc[0][0] == "Active Haptic Vibration Inspection":
                return True
            else:
                return False
        else:
            if self.df2.iloc[0][0] == "Power inspection":
                return True
            else:
                return False
    #
    #
    #
    def check_file2(self,file,use_cols = [0,2],
                    names = ['Inspections','Values'],
                    dtype={"Inspections":"string"}):
        """
        ToDo:
         - Docstring
         - List of arguments and return values
        """
        self.df = pd.read_csv(file, usecols = use_cols,names = names, dtype=dtype)
        #
        """
        Co hledat a najit index, pak kolik preskocit od zacatku +1 => skiprows
        Kolik radku precist aby data davali smysl => nrows (after skiprows)
        Skontrolovat jestli hledani vyraz(nazev mereni) existuje a kde(ktory radek)
        """
        #Define common structures:
        self.II = "Inspection information"
        self.PI = "Power inspection"
        self.CI = "Communication inspection"
        #Define structures for each EOL
        self.EOL2_TSC = "Tilt switch Calibration" #First tests in LogFile
        self.EOL2_TSI = "Tilt switch inspection"
        self.EOL2_MAF = "Measurement Actual Force"
            #
        self.EOL3_PIC = "PIC inspection" #First tests in LogFile
        self.EOL3_MAF = "Measurement Actual Force"
            #
        self.EOL4_CDP = "Calibration Dimming Parameter" #First tests in LogFile
        self.EOL4_LI = "Luminance inspection"
        self.EOL4_SII = "Symbol image inspection"
        self.EOL4_CGP = "Calibration Gain Parameter"
        self.EOL4_LI_IS = "Luminance inspection (Initial state)"
        self.EOL4_LI_DMax = "Luminance inspection (Day Max)"
        self.EOL4_LI_DMin = "Luminance inspection (Day Min)"
        self.EOL4_LI_NMax = "Luminance inspection (Nnight Max)"
            #
        self.EOL5_ASI = "Audio Switch inspection" #First tests in LogFile
        self.EOL5_CAI = "COMET AD inspection"
            #
        self.EOL6_AHVI = 'Active Haptic Vibration Inspection' #First tests in LogFile
            #
            #Dictionary of CONST. define upper == COMMON
        self.common_inspections = {1:self.II,2:self.PI,3:self.CI}
            #Dictionay of CONST. for EOL6
        self.EOL6_inspections = {1:self.EOL6_AHVI}
            #Decitionary of index's for each constant (make sens???) => YES!
        self.common_index = {self.II:0,self.PI:0,self.CI:0}
            #Dictionary of index's for each constant(EOL6)
        self.EOL6_index = {self.EOL6_AHVI:0}
            #
        """
        And following code put into cycle??? => YES!
        Go through dict of CONSTANTS and update index for each CONSTANT => YES!
        """
            #Genereting index for all EOL logs
        for index_key,index_value in self.common_inspections.items():
            index = self.df[self.df['Inspections'] == self.common_inspections[index_key]].index
            if index.size > 0:
                self.common_index[self.common_inspections[index_key]] = index[0]
            else:
                 self.common_index[self.common_inspections[index_key]] = 0
                #
            #Generating index for EOL6 logs
        for index_key,index_value in self.EOL6_inspections.items():
            index = self.df[self.df['Inspections'] == self.EOL6_inspections[index_key]].index
            if index.size > 0:
                self.EOL6_index[self.EOL6_inspections[index_key]] = index[0]
            else:
                self.EOL6_index[self.EOL6_inspections[index_key]] = 0
                #
            #
        """
        ToDo:
        Here add other EOL index's
        """
        return self.df,self.common_index,self.EOL6_index

    #
    #
    #
    def create_file(self,path=""):
        """
        Create file/excelwriter as inital return file,
        with all sheets. One sheet per station/tester.
        ToDo:
        1. finish docstrings
        2. Check if file exist or not
        """
        # Create Reports folder in script directory if it does not exists
        #reports_dir = os.path.dirname(os.path.realpath(__file__)) + '/Reports/'
        #Path(reports_dir).mkdir(parents=True, exist_ok=True)
        #
        #change in ver.0.5 file name as today change to file name as yesterday
        file_name = self.PATH_TO_SAVE+str(self.STATION_NAME)+"_"+(datetime.date.today()-datetime.timedelta(1)).strftime("%y%m%d")+".xlsx"
        writer = pd.ExcelWriter(file_name)

        return writer
    #
    #
    #
    def change_header(self, x):
        """ 
        Change values in series so there are no duplicates
        Used in process_data_Tilt
        """
        if "   " in x:
            x = self.last + x.replace("   ","-")
        else:
            self.last = x        
        return x
    #
    #
    #
    def process_data(self,file=[]):
        """
        Process all given data and save result in excel.
        ToDo:
         - Docstrings
         - describe arguments
         - describe return values
        """
        data = []
        file_number = 0
        for i in file:
            #!!!Add test if i is not empty!!!
            if i == "": break
            #Read values from name of file
            file_number = file_number + 1
            self.get_info(i)
            #Get index numbers and DF from file
            self.df,self.common_index,a = self.check_file2(i)
            #call first part of DF, contains P/N,ECU,Date,Time,SW Version,etc.
            firstDf = self.header(skip_rows = self.common_index[self.CI]+1)
            #call second part of DF, contains measured values
            secondDf = self.values(skip_rows = self.common_index[self.CI]+4)
            #merge first and second part of DF into one
            result = pd.concat([firstDf,secondDf],axis=1)
            result.insert(0,"No.",file_number)
            result.set_index("No.", inplace=True)
            #append sorted and cleaned DF into list
            data.append(result)

        try:
            #merge all DF into one and export to excel
            data = pd.concat(data, axis=0)
            self.writer = self.create_file()
            data.to_excel(self.writer, sheet_name=self.STATION_NAME)
            self.writer.save()
        except ValueError as e:
            print (e)
            return False
        except:
            raise ValueError("No files to concat!")


        return data
    #
    #
    #
    def process_data_Tilt(self,file=[]):
        """
        Process all given data and save result in excel.
        ToDo:
         - Docstrings
         - describe arguments
         - describe return values
        """
        data = []
        file_number = 0
        for i in file:
            #!!!Add test if i is not empty!!!
            if i == "": break
            #Read values from name of file
            file_number = file_number + 1
            self.get_info(i)
            #Get index numbers and DF from file
            self.df,self.common_index,a = self.check_file2(i)
            #call first part of DF, contains P/N,ECU,Date,Time,SW Version,etc.
            firstDf = self.header(skip_rows = self.common_index[self.CI]+1)
            #print ("This is first:",firstDf)
            #call second part of DF, contains measured values
            secondDf = self.values(skip_rows = self.common_index[self.CI]+4)
            #print ("This is second:",secondDf)
            #merge first and second part of DF into one
            result = pd.concat([firstDf,secondDf],axis=1)
            result.insert(0,"No.",file_number)
            result.set_index("No.", inplace=True)
            #Rename columns, so there are no duplicates
            result.columns = result.columns.to_series().apply(lambda x: self.change_header(x))
            
            data.append(result)
        
        #for debug only
        try:
            data = pd.concat(data, axis=0)
            self.writer = self.create_file()
            data.to_excel(self.writer, sheet_name=self.STATION_NAME)
            self.writer.save()
        except ValueError as e:
            print (e)
            return False
        except:
            print (i)
            raise ValueError("No files to concat!")
    
        return data
    #
    #
    #
    def process_data_Haptic(self,file=[]):
        """
        Process all given data and save result in excel.
        ToDo:
         - Merge in common function?
        """
        data = []
        file_number = 0
        for i in file:
        #!!!Add test if i is not empty!!!
            if i == "": break
            #Read values from name of file
            file_number = file_number + 1
            self.get_info(i)
            #Get index numbers from DF
            self.df, self.common_index,self.EOL6_index = self.check_file2(i)
            #call first part of DF, contains P/N,ECU,Date,Time,SW Version,etc.
            firstDf = self.header(skip_rows = self.common_index[self.CI]+1)
            #call second part of DF, contains measured values
            secondDf = self.values(skip_rows = self.EOL6_index[self.EOL6_AHVI])
            #merge first and second part of DF into one
            result = pd.concat([firstDf,secondDf],axis=1)
            result.insert(0,"No.",file_number)
            result.set_index("No.", inplace=True)
            #append sorted and cleaned DF into list
            data.append(result)

        try:
            #merge all DF into one and export to excel
            data = pd.concat(data, axis=0)
            final_data = pd.DataFrame()
            self.writer = self.create_file()
            data.to_excel(self.writer, sheet_name=self.STATION_NAME)
            self.writer.save()
        except ValueError as e:
            print (e)
            return False
        except:
            raise ValueError("No files to concat!")

        return data
    #
    #
    #
