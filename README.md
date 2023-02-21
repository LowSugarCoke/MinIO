# Minio Log Uploader

![flow chart](https://raw.githubusercontent.com/LowSugarCoke/MinIO/main/flow_chart.png)

This program automatically uploads log files from your local machine to the Minio object storage service. It performs the following functions:

- Import necessary packages (Minio uploader, log processor, log judge, etc.).
- Set up related parameters, including endpoint, bucket name, upload path, etc.
- Prompt the user to enter their Minio access and secret keys.
- Initialize Minio upload client, log judge, and log processor.
- Continuously check the size of the local log folder, select files that haven't been updated for more than two days, or select all files in the folder if the size exceeds 5GB.
- Read the tool name file, classify files based on tool name, and get files that need to be compressed and files that do not need to be compressed.
- Add files to the upload list and upload them to Minio.
- Wait for 60 seconds and repeat the process.

Note that the Minio uploader, log processor, and log judge used in this program are custom packages that may need to be installed or imported separately.

## Requirements

This program requires the following packages:

- `minio` (for the Minio uploader)
- `getpass` (for password input)
- `time` (for time management)

## Usage

1. Clone the repository to your local machine.
2. Install the required packages using pip.
3. Modify the parameters in the code to fit your Minio configuration and local log directory.
4. Run the program using the command `python main.py` in the terminal.

## License

This program is released under the TSMC license.
