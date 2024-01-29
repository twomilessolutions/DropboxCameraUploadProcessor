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
        choice = input(Fore.GREEN + "\n\nPress <Enter> to exit...")

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
            self.moveFile(self.directory, filename, newDirectory)
        except Exception as ex:
            print(Fore.RED + "Error processing file: " + filename + "\nException: " + ex.__str__)
            choice = input(Fore.RED + "Press <Enter> to exit...")

    def moveFile(self, oldDirectory, filename, newDirectory):
        try:
            if not os.path.exists(os.path.join(newDirectory,filename)):
                 os.rename(os.path.join(oldDirectory, filename), os.path.join(newDirectory, filename))
                 print(Fore.BLUE + "Moved file: " + os.path.join(oldDirectory,filename) + " to: " + os.path.join(newDirectory, filename))
            else:
                base, extension = os.path.splitext(filename)
                ii = 1
                while True:
                    newFilename = base + "_" + str(ii) + extension
                    if not os.path.exists(os.path.join(newDirectory, newFilename)):
                        os.rename(os.path.join(oldDirectory,filename),os.path.join(newDirectory, newFilename))
                        print(Fore.BLUE + "Moved file: " + os.path.join(oldDirectory,filename) + " to: " + os.path.join(newDirectory, newFilename))
                        break
                    ii += 1
        except Exception as ex:
            print(Fore.RED + "Error processing file: " + filename + "\nException: " + ex.__str__)
            choice = input(Fore.RED + "\n\nPress <Enter> to acknowledge...")