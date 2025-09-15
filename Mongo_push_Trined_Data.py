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



class Predicted_JSON_Uplaoder(): 
    def __init__(self): 
        try:
            pass 
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
            logger.info(f"Data inserted to mongoDB database {self.database} and collection {self.collection}")
            return(len(self.records))
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
