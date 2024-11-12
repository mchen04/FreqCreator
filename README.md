# FreqCreator

FreqCreator is a tool to automate the creation and upload of frequency-based audio files to Google Drive.

## Setup

1. **Install Dependencies**:

pip install -r requirements.txt


2. **Google Drive API Setup**:
- Enable the Google Drive API in your [Google Cloud Console](https://console.cloud.google.com/).
- Create a service account and download the `credentials.json` file.
- Place `credentials.json` in the root of this project.

3. **Specify Google Drive Folder ID**:
- In `upload_to_drive.py`, replace `'YOUR_GOOGLE_DRIVE_FOLDER_ID'` with your actual Google Drive folder ID.

## Usage

1. **Generate Audio Files**:
- Run the following command to generate 5-minute audio files for each specified frequency:
  ```
  python generate_frequencies.py
  ```

2. **Upload Audio Files to Google Drive**:
- Run the following command to upload generated files to your specified Google Drive folder:
  ```
  python upload_to_drive.py
  ```

## Automating the Process

To automate both scripts, create a batch file or shell script to run them in sequence, or schedule them using a task scheduler.

## License
MIT License

