from Network_Security.components.data_ingestion import DataIngestion
from Network_Security.exception.exception import NetworkSecurityException
from Network_Security.logging.logger import logger
from Network_Security.entity.config_entity import TrainingPipelineConfig,DataIngestionConfig

import sys 

if __name__=="__main__":
    try: 
        training_pipeline_config=TrainingPipelineConfig()
        data_ingestion_config=DataIngestionConfig(training_pipeline_config)
        data_ingestion=DataIngestion(data_ingestion_config)
        logger.info("Starting data ingestion")  
        dataingestionartifact = data_ingestion.initiate_data_ingestion()
        print(dataingestionartifact)
        logger.info("Data ingestion completed")
    except Exception as e:
        raise NetworkSecurityException(e,sys)
