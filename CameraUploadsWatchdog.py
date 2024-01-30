from os import truncate
import time
from configparser import ConfigParser
from FileProcessor import FileProcessor
from CameraUploadsConfig import CameraUploadConfig
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from colorama import init, Fore
init()

class Watcher:
    camera_uploads_config = CameraUploadConfig()
    camera_uploads_directory = camera_uploads_config.GetDirectory()
    
    def __init__(self):
        self.observer = Observer()
    
    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.camera_uploads_directory, recursive=False)
        self.observer.start()

        try:
            while True:
                time.sleep(5)
        except:
                self.observer.stop()
                print(Fore.RED + "ERROR")
        
        self.observer.join()
    

class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            print(Fore.BLUE + "Received created event for: " + event.src_path)
            camera_upload_config = CameraUploadConfig()
            camera_uploads_directory = camera_upload_config.GetDirectory()

            file_processor = FileProcessor()
            file_processor.setDirectory(camera_uploads_directory)
            truncated_filename = event.src_path.replace(camera_uploads_directory, "")
            print(Fore.BLUE + "truncated filename: " + truncated_filename)
            processed = False
            while not processed:
                try:
                    file_processor.processFile(truncated_filename)
                    processed = True
                except Exception as ex:
                    print(Fore.RED + "Error processing file: " + truncated_filename + "\nwaiting to retry...")
                    time.sleep(5)
                    print(Fore.YELLOW + "Retrying file: " + truncated_filename)

        elif event.event_type == 'modified':
            print(Fore.CYAN + "Received modified event for: " + event.src_path)

        elif event.event_type == 'deleted':
            print(Fore.MAGENTA + "Received deleted event for: " + event.src_path)

if __name__ == '__main__':
    w = Watcher()
    w.run()