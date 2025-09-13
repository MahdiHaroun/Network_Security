import os
import  sys
from dotenv import load_dotenv
import json 

load_dotenv()

uri = "mongodb+srv://MahdiHaroun:"+os.getenv("MONGODB_PASSWORD")+"@cluster0.vgezfpm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
print(uri)


import certifi       # secure connection
ca = certifi.where()    


import pandas as pd
import numpy as np  
import pymongo
from Network_Security.exception.exception import NetworkSecurityException
from Network_Security.logging.logger import logger



class NetworkDataExtract(): 
    def __init__(self): 
        try:
            pass 
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

    def csv_to_json_convertor(self , file_path): 
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True,inplace=True)
            records = json.loads(data.T.to_json()).values()
            return list(records)

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def push_data_to_mongoDB(self , records , database , collection):
        try:
            self.database = database    
            self.collection = collection
            self.records = records  
            self.mongo_client = pymongo.MongoClient(uri)

            self.db = self.mongo_client[self.database]
            self.col = self.db[self.collection]
            self.col.insert_many(self.records)
            logger.logging.info(f"Data inserted to mongoDB database {self.database} and collection {self.collection}")
            return(len(self.records))
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

if __name__=='__main__':
    
        FILE_PATH = "Network_Data/phisingData.csv"
        DATABASE = "MahdiHaroun"
        COLLECTION = "NetworkData"
        networkobj = NetworkDataExtract()
        records = networkobj.csv_to_json_convertor(file_path=FILE_PATH)
        print(f"Total number of records to be inserted to mongoDB is {len(records)}")
        no_of_records =networkobj.push_data_to_mongoDB(records, DATABASE, COLLECTION)
        print(f"Total number of records inserted to mongoDB is {no_of_records}")

