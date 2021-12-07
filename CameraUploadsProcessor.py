import os
from configparser import ConfigParser
from FileProcessor import FileProcessor
from CameraUploadsConfig import CameraUploadConfig

from colorama import init, Fore
init()

# C:\Users\Jeff Miles\OneDrive\Desktop\test folder - will be different on different computers

def main():
    camera_upload_config = CameraUploadConfig()
    camera_uploads_directory = camera_upload_config.GetDirectory()
    
    file_processor = FileProcessor()
    file_processor.setDirectory(camera_uploads_directory)
    file_processor.processDirectory()

if __name__ == "__main__":
    main()