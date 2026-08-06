import os, re
from datetime import datetime
from colorama import init, Fore
init()

class FileProcessor:
    directory = ""
    filename = ""

    # Extensions this tool will organize.
    VALID_EXTENSIONS = {".jpg", ".jpeg", ".png", ".mov", ".mp4"}

    MONTH_NAME_TO_NUM = {
        "jan": 1, "january": 1,
        "feb": 2, "february": 2,
        "mar": 3, "march": 3,
        "apr": 4, "april": 4,
        "may": 5,
        "jun": 6, "june": 6,
        "jul": 7, "july": 7,
        "aug": 8, "august": 8,
        "sep": 9, "sept": 9, "september": 9,
        "oct": 10, "october": 10,
        "nov": 11, "november": 11,
        "dec": 12, "december": 12,
    }
    MONTH_NAME_ALTERNATION = "|".join(
        sorted(MONTH_NAME_TO_NUM.keys(), key=len, reverse=True)
    )

    # Date patterns to look for in a filename, in priority order.
    # Each pattern must expose named groups: year, month, day
    # (month name patterns expose "monthname" instead of "month").
    # Separator between numeric components can be "-", "_", "." or nothing,
    # but must be consistent within a single match (handled via backreference).
    DATE_PATTERNS = [
        # YYYY-MM-DD / YYYY_MM_DD / YYYY.MM.DD / YYYYMMDD
        re.compile(
            r"(?P<year>(19|20)\d{2})(?P<sep>[-_.]?)(?P<month>0[1-9]|1[0-2])(?P=sep)(?P<day>0[1-9]|[12]\d|3[01])"
        ),
        # MM-DD-YYYY / MM_DD_YYYY / MM.DD.YYYY / MMDDYYYY
        re.compile(
            r"(?P<month>0[1-9]|1[0-2])(?P<sep>[-_.]?)(?P<day>0[1-9]|[12]\d|3[01])(?P=sep)(?P<year>(19|20)\d{2})"
        ),
    ]

    # Month spelled out by name, e.g. "Jul 30", "July 30th", "30 Jul".
    # Year is looked for separately since it's often missing (e.g. "Photo Jul 30, 5 07 40 PM.jpg").
    MONTH_NAME_DAY_PATTERN = re.compile(
        r"\b(?P<monthname>" + MONTH_NAME_ALTERNATION + r")\.?\s+(?P<day>\d{1,2})(?:st|nd|rd|th)?\b",
        re.IGNORECASE,
    )
    MONTH_NAME_DAY_PATTERN_REVERSED = re.compile(
        r"\b(?P<day>\d{1,2})(?:st|nd|rd|th)?\s+(?P<monthname>" + MONTH_NAME_ALTERNATION + r")\b",
        re.IGNORECASE,
    )
    YEAR_PATTERN = re.compile(r"(19|20)\d{2}")

    def setDirectory(self, directory):
        self.directory = directory
        print(Fore.WHITE + "Directory set to " + self.directory)

    def findDateMatch(self, filename):
        """Search the filename (excluding extension) for a recognizable date.
        Returns a dict with 'year' and 'month' (both strings, zero-padded)
        if found, otherwise None."""
        name, _ext = os.path.splitext(filename)

        for pattern in self.DATE_PATTERNS:
            match = pattern.search(name)
            if match:
                return {"year": match.group("year"), "month": match.group("month")}

        for pattern in (self.MONTH_NAME_DAY_PATTERN, self.MONTH_NAME_DAY_PATTERN_REVERSED):
            match = pattern.search(name)
            if not match:
                continue

            monthNum = self.MONTH_NAME_TO_NUM.get(match.group("monthname").lower())
            day = int(match.group("day"))
            if monthNum is None or not (1 <= day <= 31):
                continue

            # The filename itself might not contain a year (e.g. "Photo Jul 30, 5 07 40 PM.jpg").
            # Prefer a year found in the filename; otherwise fall back to the file's
            # last-modified date on disk.
            yearMatch = self.YEAR_PATTERN.search(name)
            if yearMatch:
                year = yearMatch.group(0)
            else:
                year = self.getFallbackYear(filename)
                if year is None:
                    continue
                print(Fore.YELLOW + "No year found in filename " + filename + ", using file's last-modified year (" + year + ") instead.")

            return {"year": year, "month": "{:02d}".format(monthNum)}

        return None

    def getFallbackYear(self, filename):
        """Best-effort fallback: use the file's last-modified date to determine
        the year when the filename itself doesn't contain one."""
        if not self.directory:
            return None
        path = os.path.join(self.directory, filename)
        try:
            mtime = os.path.getmtime(path)
        except OSError:
            return None
        return str(datetime.fromtimestamp(mtime).year)

    def testFilename(self, filename):
        _name, extension = os.path.splitext(filename)

        if extension.lower() not in self.VALID_EXTENSIONS:
            return False

        return self.findDateMatch(filename) is not None

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

        dateInfo = self.findDateMatch(filename)
        if not self.testFilename(filename) or dateInfo is None:
            print(Fore.YELLOW + "Filename " + filename + " does not match pattern.")
            return

        try:
            year = dateInfo["year"]
            month = dateInfo["month"]
            newDirectory = os.path.join(self.directory, year, month)

            if not os.path.isdir(newDirectory):
                print(Fore.BLUE + "Directory " + newDirectory + " does not exist, creating...")
                os.makedirs(newDirectory)

            print(Fore.BLUE + "moving file: " + filename)
            self.moveFile(self.directory, filename, newDirectory)
        except Exception as ex:
            print(Fore.RED + "Error processing file: " + filename + "\nException: " + str(ex))
            choice = input(Fore.RED + "Press <Enter> to exit...")

    def moveFile(self, oldDirectory, filename, newDirectory):
        try:
            if not os.path.exists(os.path.join(newDirectory, filename)):
                 os.rename(os.path.join(oldDirectory, filename), os.path.join(newDirectory, filename))
                 print(Fore.BLUE + "Moved file: " + os.path.join(oldDirectory, filename) + " to: " + os.path.join(newDirectory, filename))
            else:
                base, extension = os.path.splitext(filename)
                ii = 1
                while True:
                    newFilename = base + "_" + str(ii) + extension
                    if not os.path.exists(os.path.join(newDirectory, newFilename)):
                        os.rename(os.path.join(oldDirectory, filename), os.path.join(newDirectory, newFilename))
                        print(Fore.BLUE + "Moved file: " + os.path.join(oldDirectory, filename) + " to: " + os.path.join(newDirectory, newFilename))
                        break
                    ii += 1
        except Exception as ex:
            print(Fore.RED + "Error processing file: " + filename + "\nException: " + str(ex))
            choice = input(Fore.RED + "\n\nPress <Enter> to acknowledge...")