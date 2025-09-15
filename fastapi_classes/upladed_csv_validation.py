from Network_Security.exception.exception import NetworkSecurityException
from Network_Security.logging.logger import logger
import os 
import sys 
import pandas as pd
import numpy as np
from Network_Security.constants.training_pipeline import PREDECTION_SCHEMA_FILE_PATH
from Network_Security.utils.main_utils.utils import read_yaml_file




class DataValidation:
    def __init__(self , file_path):
        
        try:
            self.file_path = file_path
            self._schema_config = read_yaml_file(PREDECTION_SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
        
    
    def validate_number_of_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            number_of_columns = len(self._schema_config['columns'])
            logger.info(f"Required number of columns: {number_of_columns}")
            logger.info(f"Dataframe has columns: {len(dataframe.columns)}")
            if len(dataframe.columns) == number_of_columns:
                return True
            else:
                return False
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    
    def validate_is_numerical_column_exist(self,dataframe:pd.DataFrame)->bool:
        try:
            numerical_columns = self._schema_config['numerical_columns']
            logger.info(f"Number of Numerical columns required: {len(numerical_columns)}")
            logger.info(f"Number of Numerical columns present in dataframe: {len(dataframe.select_dtypes(include=['int64','float64']).columns)}")
            if len(numerical_columns) == len(dataframe.select_dtypes(include=['int64','float64']).columns):
                return True
            else:
                return False
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

    def initiate_csv_data_validation(self):
        try:
            df = self.read_data(self.file_path)
            status = self.validate_number_of_columns(df)
            if not status:
                raise Exception(f"Dataframe does not have required number of columns")
            status = self.validate_is_numerical_column_exist(df)
            if not status:
                raise Exception(f"Dataframe does not have all the numerical columns")
            return True
        except Exception as e:
            raise NetworkSecurityException(e,sys)