
import os


class S3Sync:
    def sync_folder_to_s3(self,folder,aws_bucket_url):
        # Convert to absolute path to ensure correct directory
        abs_folder = os.path.abspath(folder)
        command = f"aws s3 sync {abs_folder} {aws_bucket_url} "
        print(f"Executing S3 sync command: {command}")
        os.system(command)

    def sync_folder_from_s3(self,folder,aws_bucket_url):
        # Convert to absolute path to ensure correct directory
        abs_folder = os.path.abspath(folder)
        command = f"aws s3 sync  {aws_bucket_url} {abs_folder} "
        print(f"Executing S3 sync command: {command}")
        os.system(command)
