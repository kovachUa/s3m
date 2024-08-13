from minio import Minio
import json
import os

class MinioClient:
    def __init__(self, config_file):
        with open(config_file, 'r') as file:
            config = json.load(file)

        self.client = Minio(
            config['url'].replace("http://", ""),
            access_key=config['accessKey'],
            secret_key=config['secretKey'],
            secure=config['url'].startswith("https")
        )

    def cp(self, bucket_name, object_name, file_path):
        # Copy object from bucket to local file
        self.client.fget_object(bucket_name, object_name, file_path)
    
    def cat(self, bucket_name, object_name):
        # Display object contents
        response = self.client.get_object(bucket_name, object_name)
        print(response.read().decode('utf-8'))

    def diff(self, bucket1, bucket2):
        # List differences in object name, size, and date between two buckets
        objs1 = {obj.object_name: obj for obj in self.client.list_objects(bucket1, recursive=True)}
        objs2 = {obj.object_name: obj for obj in self.client.list_objects(bucket2, recursive=True)}

        all_objs = set(objs1.keys()).union(set(objs2.keys()))
        for obj in all_objs:
            obj1 = objs1.get(obj)
            obj2 = objs2.get(obj)

            if obj1 and not obj2:
                print(f"Only in {bucket1}: {obj}")
            elif obj2 and not obj1:
                print(f"Only in {bucket2}: {obj}")
            elif obj1 and obj2:
                if obj1.size != obj2.size:
                    print(f"Size difference in {obj}: {bucket1}({obj1.size}) vs {bucket2}({obj2.size})")

    def du(self, bucket_name):
        # Summarize disk usage recursively
        total_size = 0
        for obj in self.client.list_objects(bucket_name, recursive=True):
            total_size += obj.size
        print(f"Total size in bucket {bucket_name}: {total_size} bytes")

    def encrypt(self):
        # Manage bucket encryption config
        pass

    def event(self):
        # Manage object notifications
        pass

    def find(self, bucket_name, prefix):
        # Search for objects
        objects = self.client.list_objects(bucket_name, prefix=prefix)
        return [obj.object_name for obj in objects]

    def get(self, bucket_name, object_name, file_path):
        # Get S3 object to local
        self.client.fget_object(bucket_name, object_name, file_path)

    def head(self, bucket_name, object_name, lines=10):
        # Display first 'n' lines of an object
        response = self.client.get_object(bucket_name, object_name)
        content = response.read().decode('utf-8').splitlines()
        print("\n".join(content[:lines]))

    def ilm(self):
        # Manage bucket lifecycle
        pass

    def idp(self):
        # Manage MinIO IDentity Provider server configuration
        pass

    def license(self):
        # License related commands
        pass

    def legalhold(self):
        # Manage legal hold for object(s)
        pass

    def ls(self, bucket_name=None):
        # List buckets and objects
        if bucket_name:
            objects = self.client.list_objects(bucket_name)
            return [obj.object_name for obj in objects]
        else:
            buckets = self.client.list_buckets()
            return [bucket.name for bucket in buckets]

    def mb(self, bucket_name):
        # Make a bucket
        self.client.make_bucket(bucket_name)

    def mv(self, bucket_name, src_object_name, dst_object_name):
        # Move objects
        src = self.client.get_object(bucket_name, src_object_name)
        self.client.put_object(bucket_name, dst_object_name, src, src.size)
        self.client.remove_object(bucket_name, src_object_name)

    def mirror(self):
        # Synchronize object(s) to a remote site
        pass
