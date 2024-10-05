import boto3
import os

class S3Sink:
    def __init__(self):
        self.s3 = boto3.client('s3',
                               aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                               aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
        self.bucket = os.getenv('S3_BUCKET')

    def upload_file(self, file_path, s3_key):
        try:
            self.s3.upload_file(file_path, self.bucket, s3_key)
            print(f"File {file_path} uploaded to {self.bucket}/{s3_key}")
        except Exception as e:
            print(f"Error uploading file: {str(e)}")

# Usage example after processing
if __name__ == "__main__":
    sink = S3Sink()
    sink.upload_file("/path/to/processed_data.parquet", "processed/2024/10/05/data.parquet")
