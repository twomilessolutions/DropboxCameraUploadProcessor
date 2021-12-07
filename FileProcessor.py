import os, re
from colorama import init, Fore
init()

class FileProcessor:
    directory = ""
    filename = ""

    def setDirectory(self, directory):
        self.directory = directory
        print(Fore.WHITE + "Directory set to " + self.directory)
    
    def testFilename(self, filename):
        testPassed = False
        if re.match("[0-9]{4}-[0-9]{2}-[0-9]{2}.*?.jpg", filename) or re.match("[0-9]{4}-[0-9]{2}-[0-9]{2}.*?.jpeg", filename) or re.match("[0-9]{4}-[0-9]{2}-[0-9]{2}.*?.png", filename) or re.match("[0-9]{4}-[0-9]{2}-[0-9]{2}.*?.mov", filename) or re.match("[0-9]{4}-[0-9]{2}-[0-9]{2}.*?.mp4", filename):
            testPassed = True

        return testPassed

    def processDirectory(self):
        print(Fore.WHITE + "Processing directory: " + self.directory)

        files = os.listdir(self.directory)
        for filename in files:
            if self.testFilename(filename):
                self.processFile(filename)
            else:
                print(Fore.YELLOW + self.directory + filename + " skipped...")
        
        print(Fore.WHITE + "Processing directory: " + self.directory + " completed.")

    def processFile(self, filename):
        print(Fore.BLUE + "processFile() called for file " + self.directory + filename)

        if not self.testFilename(filename):
            print(Fore.YELLOW + "Filename " + filename + " does not match pattern.")
            return

        try:
            filenameArray = filename.split("-")
            year = filenameArray[0]
            month = filenameArray[1]
            newDirectory = self.directory + year + "\\" + month + "\\"

            if not os.path.isdir(newDirectory):
                print(Fore.BLUE + "Directory " + newDirectory + " does not exist, creating...")
                os.makedirs(newDirectory)
            
            print(Fore.BLUE + "moving file: " + filename)
            os.rename(self.directory + filename, newDirectory + filename)
        except Exception as ex:
            print(Fore.RED + "Error processing file: " + filename + "\nException: " + ex.__str__)