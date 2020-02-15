from google.cloud import storage


class StorageService:
    def __init__(self, bucket_name: str):
        self.client = storage.Client()
        self.bucket_name = bucket_name
        self.bucket = self.client.bucket(bucket_name)

    def upload(self, source: str, destination: str):
        blob = self.bucket.blob(destination)

        blob.upload_from_filename(source)

        return "gs://{}/{}".format(self.bucket_name, destination)
