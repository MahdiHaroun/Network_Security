from Network_Security.components.data_ingestion import DataIngestion 
from Network_Security.components.data_validation import DataValidation 
from Network_Security.components.data_transformation import DataTransformation

from Network_Security.exception.exception import NetworkSecurityException
from Network_Security.logging.logger import logger
from Network_Security.entity.config_entity import TrainingPipelineConfig,DataIngestionConfig , DataValidationConfig , DataTransformationConfig


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
        data_validation_config=DataValidationConfig(training_pipeline_config)
        data_validation=DataValidation(dataingestionartifact, data_validation_config)
        logger.info("Starting data validation")
        data_validation_artifact = data_validation.initiate_data_validation()
        logger.info("Data validation completed")
        print(data_validation_artifact)
        data_transformation_config = DataTransformationConfig(training_pipeline_config)
        logger.info("Starting data transformation")
        data_transformation = DataTransformation(data_validation_artifact, data_transformation_config)
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        logger.info("Data transformation completed")
        print(data_transformation_artifact)

    except Exception as e:
        raise NetworkSecurityException(e,sys)
