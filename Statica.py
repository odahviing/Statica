# Build by Idan Cohen
# Version 0.01 - Only Alpha

# Imports
import sys, time
import Helper, Threat
from datetime import datetime
from Scanner import Scanner
from optparse import OptionParser
from Threat import Url, Xss
from multiprocessing.dummy import Pool as ThreadPool

# Globals
objFile = Helper.StoreFile


# Main function that will preform the search in files
def search_for_threats(filename):
    lines = [line.rstrip('\n') for line in open(filename)]

    num_of_lines = Helper.Counter()
    for line in lines:
        num_of_lines.add()
        result = Xss.detect(filename, line.lower(), num_of_lines)
        if result is True:
            Xss.FoundFile = True

        result = Url.detect(filename, line.lower(), num_of_lines)
        if result is True:
            Url.FoundFile = True

    Xss.count_files()
    Url.count_files()
    Threat.count_files()


# Printer
def print_summary(TimeStarted):
    TimeStarted = datetime.now() - TimeStarted
    print "\nFound " + Xss.OverallAmount.string() + " Hits In " + \
          Xss.OverallFiles.string() + " Files With domXSS Potential"
    print "Found " + Url.OverallAmount.string() + " Urls In " + \
          Url.OverallFiles.string() + " Files With External Urls"
    print "Found overall: " + Threat.OverallIssuesAmount.string() + " Issues In " \
          + Threat.overallFilesAmount.string() + " Files" \
          + " (" + str(TimeStarted)+ ")\n"


def Menu():
    options = OptionParser()
    options.add_option("-f", "--filename", help="Save to file", dest="filename", metavar="FILE")
    options.add_option("-u", "--url", action="store_true", help="Do online static analysis [Future Use]", default=False)
    (options, args) = options.parse_args()

    if options.url is True:
        print "Online Scanning not available"
        sys.exit(2)

    return options

# Main function
def main():
    # Arguments Care
    Threads = ThreadPool(10)
    result = Menu()

    if len(sys.argv) < 2:
        print "Missing Argument: Statica.py folder_name"
        sys.exit(0)

    Helper.FileHandler = Helper.StoreFile(result.filename)

    # Get Suspicious File List
    main_scanner = Scanner(sys.argv[len(sys.argv) - 1])
    files_to_scan = main_scanner.FileLists

    # Set Up Counters
    file_finished = Helper.Counter()
    time.sleep(1)

    TimeStarted = datetime.now()
    for file_name in files_to_scan:
        Threads.map(search_for_threats,(file_name,))
        file_finished.add()

    print_summary(TimeStarted)
    Helper.FileHandler.close()

if __name__ == "__main__":
    main()