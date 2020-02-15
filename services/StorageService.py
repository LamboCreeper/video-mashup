from google.cloud import storage


class StorageService:
    def __init__(self, bucket: str):
        self.client = storage.Client()
        self.bucket = self.client.bucket(bucket)

    def upload(self, source: str, destination: str):
        blob = self.bucket.blob(destination)

        blob.upload_from_filename(source)
