from Network_Security.cloud.s3_syncer import S3Sync
from Network_Security.exception.exception import NetworkSecurityException
from Network_Security.constants.training_pipeline import CSV_UPLOADING_BUCKET_NAME
import sys
import os

class SyncCSVS3:
    def __init__(self , file_path): 
        try:
            self.s3_sync = S3Sync()
            self.file_path = file_path
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def upload_csv_s3(self):
        try:
            aws_bucket_url = f"s3://{CSV_UPLOADING_BUCKET_NAME}"
            # Use cp command for single file upload instead of sync
            abs_file_path = os.path.abspath(self.file_path)
            filename = os.path.basename(self.file_path)
            command = f"aws s3 cp {abs_file_path} {aws_bucket_url}/{filename}"
            print(f"Executing S3 upload command: {command}")
            os.system(command)
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)