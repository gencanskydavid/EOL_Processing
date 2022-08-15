from config import find_data_file
import log_analyzer2 as la
import glob
from datetime import date,timedelta
import sys
import logging
import os
from pathlib import Path

# Create sys_log folder in script directory if it does not exists
def find_data_file():
    if getattr(sys, 'frozen', False):
        # The application is frozen
        datadir = os.path.dirname(sys.executable) + '/sys_log/'
    else:
        # The application is not frozen
        datadir = os.path.dirname(os.path.realpath(__file__)) + '/sys_log/'
        # The following line has been changed to match where you store your data files:
    
    return datadir
#
#logger_dir = os.path.dirname(os.path.realpath(__file__)) + '/sys_log/'
logger_dir = find_data_file()
print (logger_dir)
#
Path(logger_dir).mkdir(parents=True, exist_ok=True)
# Initialization of logging
logging.basicConfig(filename=logger_dir + date.today().strftime("%y%m%d") + '.log', level=logging.DEBUG,
                    format='%(levelname)s %(asctime)s %(message)s')

try:
    logging.info("Loading configuration file")
    import config as cfg
except Exception as e:
    print("There was an error while opening config.yaml")
    logging.error("There was error with Config.yaml as {}".format(e))
    #input("Press Enter to Exit...")
    sys.exit()

'''
ToDo:
    1. Choose path where files are saved
    2. Select range since YYYYMM until YYYYMM
    3. Check if file name is correct, otherwise offer order of file name
    4. ???
    5. Inform user about sucess? - Done
    6. Choose where result is saved??? Needed???
'''
######
today = date.today()
current_year = today.strftime("%Y") #Get current year
current_month = today.strftime("%Y%m") #Get current month
current_day = today.strftime("%Y%m%d") #Get current day
yesterday = today - timedelta(days=1) #Get yesterday
yesterday = yesterday.strftime("%Y%m%d")#Correct format
#
if cfg.MODE == 'auto':
    logging.info("Automatic processing started")
    for i in cfg.PATHS:
        logging.info("Start processing of files for {} ".format(cfg.PATHS[i]))
        print ("Start processing of files for {} ".format(cfg.PATHS[i]))
        #
        #In case of ALCZ Backup server, yesterday data are latest one!
        path = cfg.PATHS[i]+current_year+"/"+current_month+"/"+yesterday+"/"
        #path = cfg.PATHS[i]+current_year+"/"+current_month+"/"

        #Exception for EOL1_Rotary
        if "EOL1_copy" in cfg.PATHS[i]:
            path += "**/BMW*_*_00.csv"
        else:
            path += "**/BMW*_*_??.csv"
        print (cfg.PATHS[i])    
        file = glob.glob(path, recursive=True)
    #file = glob.glob("2021/202104/**/BMW*_*_??.csv", recursive=True)
        try:
            #If there's no files, skip processing and try next folder/Tester
            analyzer = la.LogAnalyzer(file[0])
            if "EOL6_copy" in cfg.PATHS[i]:
                analyzer.process_data_Haptic(file)
            elif "EOL2_copy" in cfg.PATHS[i]:
                analyzer.process_data_Tilt(file)
            else:
                analyzer.process_data(file)
            logging.info("Finish processing of files for {} ".format(cfg.PATHS[i]))
            print ("Finish processing of files for {} ".format(cfg.PATHS[i]))
        except IndexError:
            logging.error("There's no files to process!")
            print ("There's no files to process!")
            continue
        except Exception:
            logging.exception(Exception)
else:
    logging.info("Manual processing started")
    manual_month = input("Write month(ex.202107/202103):")
    #check_month()
    manual_day = input("Write day(ex.20210712/20210305):")
    #check_day()
    #
    logging.debug("Month:"+manual_month)
    logging.debug("Day:"+manual_day)
    for i in cfg.PATHS:
        logging.info("Start processing of files for {} ".format(cfg.PATHS[i]))
        print ("Start processing of files for {} ".format(cfg.PATHS[i]))

        path = cfg.PATHS[i]+current_year+"/"+manual_month+"/"+manual_day+"/"
        #path = cfg.PATHS[i]+current_year+"/"+current_month+"/"
        #Exception for EOL1_Rotary
        if "EOL1_copy" in cfg.PATHS[i]:
            path += "**/BMW*_*_00.csv"
        else:
            path += "**/BMW*_*_??.csv"
        print (cfg.PATHS[i])    
        file = glob.glob(path, recursive=True)
    #file = glob.glob("2021/202104/**/BMW*_*_??.csv", recursive=True)
        try:
            #If there's no files, skip processing and try next folder/Tester
            analyzer = la.LogAnalyzer(file[0])
            if "EOL6_copy" in cfg.PATHS[i]:
                analyzer.process_data_Haptic(file)
            elif "EOL2_copy" in cfg.PATHS[i]:
            #added new function for EOL2_TILT due to duplicity value in log file
                analyzer.process_data_Tilt(file)
            else:
                analyzer.process_data(file)
            logging.info("Finish processing of files for {} ".format(cfg.PATHS[i]))
            print ("Finish processing of files for {} ".format(cfg.PATHS[i]))
        except IndexError:
            logging.error("There's no files to process!")
            print ("There's no files to process!")
            continue
        except Exception:
            logging.exception(Exception)
            
print("Finished")
logging.info("Processing finished")
#input("Press enter to exit")
