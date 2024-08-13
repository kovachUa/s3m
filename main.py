import argparse
from minio_library import MinioClient

def main():
    parser = argparse.ArgumentParser(description="MinIO Client Command Line Interface")
    
    subparsers = parser.add_subparsers(dest="command")
    
    # Команда для створення бакета
    subparsers.add_parser("create", help="Create a bucket")
    
    # Команда для видалення бакета
    subparsers.add_parser("delete", help="Delete a bucket")
    
    # Команда для перегляду списку бакетів
    subparsers.add_parser("buckets", help="List all buckets")

    # Команда для переліку об'єктів у бакеті
    list_parser = subparsers.add_parser("ls", help="List objects in a bucket")
    list_parser.add_argument("bucket", help="Bucket name")

    # Команда для завантаження об'єкта
    get_parser = subparsers.add_parser("get", help="Get an object to local")
    get_parser.add_argument("bucket", help="Bucket name")
    get_parser.add_argument("object", help="Object name")
    get_parser.add_argument("file", help="Local file path")

    # Команда для виведення вмісту об'єкта
    cat_parser = subparsers.add_parser("cat", help="Display object contents")
    cat_parser.add_argument("bucket", help="Bucket name")
    cat_parser.add_argument("object", help="Object name")

    # Команда для підрахунку розміру бакета
    du_parser = subparsers.add_parser("du", help="Summarize disk usage in a bucket")
    du_parser.add_argument("bucket", help="Bucket name")

    # Команда для переміщення об'єкта
    mv_parser = subparsers.add_parser("mv", help="Move an object")
    mv_parser.add_argument("bucket", help="Bucket name")
    mv_parser.add_argument("src_object", help="Source object name")
    mv_parser.add_argument("dst_object", help="Destination object name")

    args = parser.parse_args()

    client = MinioClient("key.json")

    if args.command == "create":
        bucket_name = input("Enter bucket name to create: ")
        client.mb(bucket_name)
        print(f"Bucket '{bucket_name}' created.")
    
    elif args.command == "delete":
        bucket_name = input("Enter bucket name to delete: ")
        client.rb(bucket_name)
        print(f"Bucket '{bucket_name}' deleted.")
    
    elif args.command == "buckets":
        buckets = client.ls()
        print("Available buckets:")
        for bucket in buckets:
            print(bucket)

    elif args.command == "ls":
        objects = client.ls(args.bucket)
        for obj in objects:
            print(obj)

    elif args.command == "get":
        client.get(args.bucket, args.object, args.file)
        print(f"Object '{args.object}' from bucket '{args.bucket}' downloaded to '{args.file}'.")

    elif args.command == "cat":
        client.cat(args.bucket, args.object)

    elif args.command == "du":
        client.du(args.bucket)

    elif args.command == "mv":
        client.mv(args.bucket, args.src_object, args.dst_object)
        print(f"Object '{args.src_object}' moved to '{args.dst_object}' in bucket '{args.bucket}'.")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
