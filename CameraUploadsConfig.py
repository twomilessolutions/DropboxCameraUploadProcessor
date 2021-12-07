import os
from configparser import ConfigParser
from colorama import init, Fore
init()

class CameraUploadConfig:
    config_directory = "C:\\python_config\\"
    config_filename = "CameraUploadsProcessor.ini"
    config_file_full_path = config_directory + config_filename
    camera_uploads_directory = ""
    config_section_name = "FILEPROCESSORCONFIGS"
    config_name = "camera_uploads_directory"

    def GetDirectory(self):
        if self.camera_uploads_directory == "":
            config_parser = ConfigParser()
            
            if not os.path.isdir(self.config_directory):
                os.mkdir(self.config_directory)
            
            if os.path.isfile(self.config_file_full_path):
                print(Fore.WHITE + "Config file exists:" + self.config_file_full_path) 
                
                print(Fore.WHITE + "reading config file")
                config_parser.read(self.config_file_full_path)
                print(Fore.WHITE + "config file read")

                file_processor_configs = config_parser[self.config_section_name]
                self.camera_uploads_directory = file_processor_configs[self.config_name]
            else:
                self.camera_uploads_directory = input(Fore.GREEN + "Please enter the full path to the camera uploads directory: ").strip()
                config_parser[self.config_section_name] = {
                    self.config_name: self.camera_uploads_directory
                }
                with open(self.config_file_full_path, 'w') as conf:
                    config_parser.write(conf)

        return self.camera_uploads_directory            
