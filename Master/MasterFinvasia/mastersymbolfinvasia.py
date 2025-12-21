"""Class representing a financial symbol in the Finvasia master database."""

import urllib.request


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
    def downloadmasterfile(self):
        """Get different market segment master file symbols"""
        try:
            self.__downloadmatserfileusingurl(self.__nse)
            self.__downloadmatserfileusingurl(self.__nfo)
            self.__downloadmatserfileusingurl(self.__cds)
            self.__downloadmatserfileusingurl(self.__mcx)
            self.__downloadmatserfileusingurl(self.__bse)
            self.__downloadmatserfileusingurl(self.__bfo)
            self.__downloadmatserfileusingurl(self.__ncx)
        except IndexError as e:
            print(
                F"Error generated while processing other segment master file: {e}")
