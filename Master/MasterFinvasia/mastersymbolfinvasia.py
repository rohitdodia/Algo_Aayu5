"""Class representing a financial symbol in the Finvasia master database."""

import urllib.request
import zipfile


class MasterTypeVar:
    """Set the segment type"""
    with_cash = "1"
    with_fno = "2"
    with_both = "3"


class MasterSymbolFinvasia:
    """Class representing a financial symbol in the Finvasia master database."""

    # 1. Function constructor
    def __init__(self, pathcwd):
        print("Activating Master Symbol Finvasia Module...")
        self.__nse = None
        self.__nfo = None
        self.__cds = None
        self.__mcx = None
        self.__bse = None
        self.__bfo = None
        self.__ncx = None
        self.__pathcwd = pathcwd
        self.__init()
        self.__prepareurls()

    # 2. Function to prepare URLs with destination paths

    def __prepareurls(self):
        """Prepare URLs for downloading master symbol data."""
        self.__nse = "https://api.shoonya.com/NSE_symbols.txt.zip"
        self.__nfo = "https://api.shoonya.com/NFO_symbols.txt.zip"
        self.__cds = "https://api.shoonya.com/CDS_symbols.txt.zip"
        self.__mcx = "https://api.shoonya.com/MCX_symbols.txt.zip"
        self.__bse = "https://api.shoonya.com/BSE_symbols.txt.zip"
        self.__bfo = "https://api.shoonya.com/BFO_symbols.txt.zip"
        self.__ncx = "https://api.shoonya.com/NCX_symbols.txt.zip"

    # 3. Function as Engine to download master symbol file using prepared URLs
    def __downloadmatserfileusingurl(self, urladdress):
        """Download master symbol file using prepared URLs."""
        try:
            folderextension = self.getfileextension(urladdress)
            if folderextension is None:
                print("Url input is incorrect or short as expected")
                return

            outpath = self.__actualpath + "\\" + folderextension

            with urllib.request.urlopen(urladdress) as response:
                with open(outpath, "wb") as out_file:
                    out_file.write(response.read())

            # Call unzip function
            self.__autounzipmaster(outpath)

        except (ConnectionError, TimeoutError, OSError) as e:
            print(
                F"Error Occured while downloading master symbol file... : {e}")

    # 4. Function about knowledge of the writing direction of master symbol file
    def __init(self):
        """Get information about the master symbol file."""
        self.__initfolder = "INIT"
        self.__destinationfolder = "MasterFinvasia"
        self.__actualpath = self.__pathcwd + "\\" + \
            self.__initfolder + "\\" + self.__destinationfolder

    # 5. Function to get file extension from URL
    def getfileextension(self, urladdress: str):
        """Get information of file extension from URL"""
        file_extension = None
        try:
            datalist = urladdress.split('/')

            if len(datalist) == 4:
                file_extension = datalist[3]

        except IndexError as e:
            print(F"Error generated while extracting file extension: {e}")
        return file_extension

    # 6. Function to handler different Master file symbol
    def downloadmasterfile(self, signal: str) -> None:
        """Get different market segment master file symbols"""
        try:
            if signal == MasterTypeVar.with_cash:
                self.__downloadmatserfileusingurl(self.__nse)
            elif signal == MasterTypeVar.with_fno:
                self.__downloadmatserfileusingurl(self.__nfo)
            elif signal == MasterTypeVar.with_both:
                self.__downloadmatserfileusingurl(self.__nse)
                self.__downloadmatserfileusingurl(self.__nfo)
            # elif signal == "CCY":
            #     self.__downloadmatserfileusingurl(self.__cds)
            # elif signal == "MCX":
            #     self.__downloadmatserfileusingurl(self.__mcx)
            # elif signal == "BSE":
            #     self.__downloadmatserfileusingurl(self.__bse)
            # elif signal == "BFO":
            #     self.__downloadmatserfileusingurl(self.__bfo)
            # elif signal == "NCX":
            #     self.__downloadmatserfileusingurl(self.__ncx)
            else:
                return
        except IndexError as e:
            print(
                F"Error generated while processing other segment master file: {e}")

    # 7. Function unzip Segment Master file
    def __autounzipmaster(self, pathofmaster: str) -> None:
        """Unzip various segment master file"""
        try:
            # unzip file from given path
            # print(F"Unziping master :{pathofmaster}")
            extract_path = pathofmaster
            extract_path = pathofmaster.replace(".zip", '')

            with zipfile.ZipFile(pathofmaster, mode='r') as zip_ref:
                zip_ref.extractall(extract_path)
            # print("Completed Unziping master")

        except (OSError, zipfile.BadZipFile) as e:
            print(
                F"Failed to unzip master for path : {pathofmaster} with err {e}")
