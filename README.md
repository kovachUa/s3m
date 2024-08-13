---

# MinIO Multi-Server Bucket Scanner and Management Tool

MinIO Multi-Server Bucket Scanner and Management Tool is a Python-based solution for interacting with multiple MinIO servers. It includes commands for scanning buckets, searching objects, and downloading objects locally.

## Features

- **Bucket Scanning**: Indexes all buckets and objects on a specified MinIO server.
- **Object Search**: Quickly find objects in the local index.
- **Object Download**: Download objects from MinIO servers to a local machine.
- **Multi-Server Support**: Work with multiple MinIO servers, selected via command-line arguments.

## Installation and Configuration

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/minio-multi-server-scanner.git
   cd minio-multi-server-scanner
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the servers:**

   Edit the `key.json` file to include your MinIO server details:

   ```json
   {
       "servers": [
           {
               "name": "server1",
               "url": "http://192.168.1.1:9000",
               "accessKey": "accesskey1",
               "secretKey": "secretkey1",
               "api": "s3v4"
           },
           {
               "name": "server2",
               "url": "http://192.168.1.2:9000",
               "accessKey": "accesskey2",
               "secretKey": "secretkey2",
               "api": "s3v4"
           }
       ]
   }
   ```

## Usage

- **Scan Buckets on a Server:**

   ```bash
   python3 main.py scan --server server1
   ```

- **Search for an Object on a Specific Server:**

   ```bash
   python3 main.py search --server server1 --bucket my-bucket --object some-object
   ```

- **Download an Object from a Specific Server:**

   ```bash
   python3 main.py get --server server1 --bucket my-bucket --object some-object --file /path/to/local/file
   ```

## Project Structure

- `main.py`: The main script for interacting with MinIO servers via command line.
- `bucket_scanner.py`: The library that handles core logic for interacting with the MinIO API.
- `key.json`: Configuration file containing details of MinIO servers.
- `requirements.txt`: Python dependencies.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

---

