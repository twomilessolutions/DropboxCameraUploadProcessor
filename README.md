# Dropbox Camera Upload Processor
## Overview
Python scripts to process iPhone camera uploads into folders.

iPhones save files in the format: "YYYY-mm-dd HH.MM.ss.{jpg|jpeg|png|mov|mp4}", then Dropbox moves them to a folder called *Camera Uploads*.

This set of python scripts does the following:
* **CameraUploadsConfig.py**: This file reads/creates a config file to ask the user where the Dropbox Camera Uplods file is.
* **CameraUploadsProcessor.py**: This file instantiates a **CameraUploadsConfig** and a **FileProcessor** and processes the Dropbox *Camera Uploads* directory.
* **CameraUploadsWatchdog.py**: This file instantiates a **CameraUploadsConfig** and a **FileProcessor** and watches the Dropbox  *Camera Uploads* directory for new files and processes them.
* **FileProcessor.py**: This file defines the workhorse class that processes files. It looks for files of the format YYYY-mm-dd HH.MM.ss.{jpg|jpeg|png|mov|mp4} and sorts them into folders by year and month.

to be continued...

© 2021 [Two Miles Solutions](https://www.twomilessolutions.com), All Rights Reserved.