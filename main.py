import argparse
import json
import os
import gnupg
from minio import Minio
from urllib.parse import urlparse

class MinioClient:
    def __init__(self, url, access_key, secret_key, api):
        # Розбираємо URL
        parsed_url = urlparse(url)
        base_url = f"{parsed_url.hostname}:{parsed_url.port}"
        
        # Визначаємо, чи використовувати HTTPS
        secure = (parsed_url.scheme == "https")

        # Ініціалізуємо клієнт MinIO
        self.client = Minio(
            base_url,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure
        )

        # Ініціалізуємо GPG
        self.gpg = gnupg.GPG()

    def encrypt_file(self, file_path, recipient):
        """Шифрує файл за допомогою GPG"""
        with open(file_path, 'rb') as f:
            encrypted_data = self.gpg.encrypt_file(f, recipients=[recipient], always_trust=True)
            if encrypted_data.ok:
                with open(file_path + '.gpg', 'wb') as ef:
                    ef.write(encrypted_data.data)
                print(f"File '{file_path}' encrypted successfully.")
            else:
                print(f"Error encrypting file '{file_path}': {encrypted_data.stderr}")

    def decrypt_file(self, file_path, output_path):
        """Дешифрує файл за допомогою GPG"""
        with open(file_path, 'rb') as f:
            decrypted_data = self.gpg.decrypt_file(f)
            if decrypted_data.ok:
                with open(output_path, 'wb') as df:
                    df.write(decrypted_data.data)
                print(f"File '{file_path}' decrypted successfully.")
            else:
                print(f"Error decrypting file '{file_path}': {decrypted_data.stderr}")

    def mb(self, bucket_name):
        """Створює новий bucket"""
        try:
            self.client.make_bucket(bucket_name)
            print(f"Bucket '{bucket_name}' created successfully.")
        except Exception as e:
            print(f"Error creating bucket '{bucket_name}': {e}")

    def rb(self, bucket_name):
        """Видаляє існуючий bucket"""
        try:
            self.client.remove_bucket(bucket_name)
            print(f"Bucket '{bucket_name}' removed successfully.")
        except Exception as e:
            print(f"Error removing bucket '{bucket_name}': {e}")

    def ls(self):
        """Перелічує всі buckets"""
        try:
            buckets = self.client.list_buckets()
            for bucket in buckets:
                print(bucket.name)
        except Exception as e:
            print(f"Error listing buckets: {e}")

    def bucket_exists(self, bucket_name):
        """Перевіряє, чи існує bucket"""
        try:
            return bucket_name in [bucket.name for bucket in self.client.list_buckets()]
        except Exception as e:
            print(f"Error checking if bucket exists '{bucket_name}': {e}")
            return False

    def get(self, bucket_name, object_name, file_path):
        """Завантажує файл з bucket"""
        try:
            self.client.fget_object(bucket_name, object_name, file_path)
            print(f"File '{object_name}' downloaded successfully from bucket '{bucket_name}' to '{file_path}'.")
        except Exception as e:
            print(f"Error downloading file '{object_name}' from bucket '{bucket_name}': {e}")

    def cat(self, bucket_name, object_name):
        """Виводить вміст файлу"""
        try:
            response = self.client.get_object(bucket_name, object_name)
            print(response.read().decode())
            response.close()
            response.release_conn()
        except Exception as e:
            print(f"Error displaying object contents '{object_name}' from bucket '{bucket_name}': {e}")

    def du(self, bucket_name):
        """Підраховує розмір бакета"""
        try:
            objects = self.client.list_objects(bucket_name, recursive=True)
            total_size = sum(obj.size for obj in objects)
            print(f"Total size of bucket '{bucket_name}': {total_size} bytes")
        except Exception as e:
            print(f"Error summarizing disk usage in bucket '{bucket_name}': {e}")

    def mv(self, bucket_name, src_object, dst_object):
        """Переміщує файл"""
        try:
            self.client.copy_object(bucket_name, dst_object, f"{bucket_name}/{src_object}")
            self.client.remove_object(bucket_name, src_object)
            print(f"Object '{src_object}' moved to '{dst_object}' in bucket '{bucket_name}'.")
        except Exception as e:
            print(f"Error moving object '{src_object}' to '{dst_object}' in bucket '{bucket_name}': {e}")

    def upload(self, bucket_name, file_path):
        """Завантажує файл в bucket з оригінальним ім'ям"""
        try:
            object_name = os.path.basename(file_path)
            self.client.fput_object(bucket_name, object_name, file_path)
            print(f"File '{file_path}' uploaded successfully to bucket '{bucket_name}' as '{object_name}'.")
        except Exception as e:
            print(f"Error uploading file '{file_path}' to bucket '{bucket_name}': {e}")

    def upload_file(self, bucket_name, file_path):
        """Завантажує файл в bucket з оригінальним ім'ям"""
        try:
            object_name = os.path.basename(file_path)
            self.client.fput_object(bucket_name, object_name, file_path)
            print(f"File '{file_path}' uploaded successfully to bucket '{bucket_name}' as '{object_name}'.")
        except Exception as e:
            print(f"Error uploading file '{file_path}' to bucket '{bucket_name}': {e}")

    def upload_directory(self, bucket_name, directory_path):
        """Завантажує каталог в bucket"""
        try:
            for root, dirs, files in os.walk(directory_path):
                for file_name in files:
                    file_path = os.path.join(root, file_name)
                    object_name = os.path.relpath(file_path, start=directory_path)
                    self.client.fput_object(bucket_name, object_name, file_path)
            print(f"Directory '{directory_path}' uploaded successfully to bucket '{bucket_name}'.")
        except Exception as e:
            print(f"Error uploading directory '{directory_path}' to bucket '{bucket_name}': {e}")

def load_config(config_file):
    with open(config_file, 'r') as file:
        return json.load(file)

def main():
    parser = argparse.ArgumentParser(description="MinIO Client Command Line Interface")
    
    subparsers = parser.add_subparsers(dest="command")
    
    # Команди для MinIO
    subparsers.add_parser("create", help="Create a bucket")
    subparsers.add_parser("delete", help="Delete a bucket")
    subparsers.add_parser("buckets", help="List all buckets")
    
    list_parser = subparsers.add_parser("ls", help="List objects in a bucket")
    list_parser.add_argument("bucket", help="Bucket name")
    
    upload_parser = subparsers.add_parser("put", help="Upload a file to a bucket")
    upload_parser.add_argument("bucket", help="Bucket name")
    upload_parser.add_argument("file", help="Local file path")
    
    upload_dir_parser = subparsers.add_parser("put-dir", help="Upload a directory to a bucket")
    upload_dir_parser.add_argument("bucket", help="Bucket name")
    upload_dir_parser.add_argument("directory", help="Local directory path")
    
    # Команди для шифрування/дешифрування
    encrypt_parser = subparsers.add_parser("encrypt", help="Encrypt a file")
    encrypt_parser.add_argument("file", help="File path")
    encrypt_parser.add_argument("recipient", help="GPG recipient email")
    encrypt_parser.add_argument("--upload", help="Upload encrypted file to a bucket", action="store_true")
    encrypt_parser.add_argument("--bucket", help="Bucket name for uploading")

    decrypt_parser = subparsers.add_parser("decrypt", help="Decrypt a file")
    decrypt_parser.add_argument("file", help="File path")
    decrypt_parser.add_argument("output", help="Output file path")

    args = parser.parse_args()

    # Завантажити конфігурацію з key.json
    config = load_config("key.json")

    # Створити клієнта Minio з конфігурації
    client = MinioClient(config["url"], config["accessKey"], config["secretKey"], config["api"])

    if args.command == "create":
        bucket_name = input("Enter bucket name to create: ")
        client.mb(bucket_name)
    
    elif args.command == "delete":
        bucket_name = input("Enter bucket name to delete: ")
        client.rb(bucket_name)
    
    elif args.command == "buckets":
        client.ls()

    elif args.command == "ls":
        client.ls(args.bucket)

    elif args.command == "put":
        if not client.bucket_exists(args.bucket):
            client.mb(args.bucket)
            print(f"Bucket '{args.bucket}' created.")
        client.upload(args.bucket, args.file)

    elif args.command == "put-dir":
        if not client.bucket_exists(args.bucket):
            client.mb(args.bucket)
            print(f"Bucket '{args.bucket}' created.")
        client.upload_directory(args.bucket, args.directory)

    elif args.command == "encrypt":
        client.encrypt_file(args.file, args.recipient)
        if args.upload:
            if args.bucket and client.bucket_exists(args.bucket):
                encrypted_file = args.file + '.gpg'
                client.upload_file(args.bucket, encrypted_file)
            else:
                print("Bucket does not exist or not specified.")
                
    elif args.command == "decrypt":
        client.decrypt_file(args.file, args.output)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
