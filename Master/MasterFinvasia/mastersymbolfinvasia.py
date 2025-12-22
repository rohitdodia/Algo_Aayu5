"""Class representing a financial symbol in the Finvasia master database."""

import urllib.request
import zipfile
import pandas as pd


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
        # path
        self.__nse = None
        self.__nfo = None
        # self.__cds = None
        # self.__mcx = None
        # self.__bse = None
        # self.__bfo = None
        # self.__ncx = None
        self.__pathcash = None
        self.__pathfno = None

        self.__pathcwd = pathcwd
        self.__init()
        self.__prepareurls()

        # DataFrames
        self.__df_cash = None
        self.__df_fno = None

    # 2. Function to prepare URLs with destination paths

    def __prepareurls(self):
        """Prepare URLs for downloading master symbol data."""
        self.__nse = "https://api.shoonya.com/NSE_symbols.txt.zip"
        self.__nfo = "https://api.shoonya.com/NFO_symbols.txt.zip"
        # self.__cds = "https://api.shoonya.com/CDS_symbols.txt.zip"
        # self.__mcx = "https://api.shoonya.com/MCX_symbols.txt.zip"
        # self.__bse = "https://api.shoonya.com/BSE_symbols.txt.zip"
        # self.__bfo = "https://api.shoonya.com/BFO_symbols.txt.zip"
        # self.__ncx = "https://api.shoonya.com/NCX_symbols.txt.zip"

    # 3. Function as Engine to download master symbol file using prepared URLs
    def __downloadmatserfileusingurl(self, urladdress):
        """Download master symbol file using prepared URLs."""
        path = None
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
            path = self.__autounzipmaster(outpath)

        except (ConnectionError, TimeoutError, OSError) as e:
            print(
                F"Error Occured while downloading master symbol file... : {e}")

        return path

    # 4. Function about knowledge of the writing direction of master symbol file
    def __init(self):
        """Get information about the master symbol file."""
        self.__initfolder = "INIT"
        self.__destinationfolder = "MasterFinvasia"
        self.__actualpath = self.__pathcwd + "\\" + \
            self.__initfolder + "\\" + self.__destinationfolder

        # store all master folder path
        self.__pathcash = None
        self.__pathfno = None
        self.__df_cash = pd.DataFrame()
        self.__df_fno = pd.DataFrame()

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
                self.__pathcash = self.__downloadmatserfileusingurl(self.__nse)
            elif signal == MasterTypeVar.with_fno:
                self.__pathfno = self.__downloadmatserfileusingurl(self.__nfo)
            elif signal == MasterTypeVar.with_both:
                self.__pathcash = self.__downloadmatserfileusingurl(self.__nse)
                self.__pathfno = self.__downloadmatserfileusingurl(self.__nfo)
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
        path = None
        try:
            # unzip file from given path
            # print(F"Unziping master :{pathofmaster}")
            extract_path = pathofmaster
            extract_path = extract_path.replace(".zip", '').replace('.txt', '')

            with zipfile.ZipFile(pathofmaster, mode='r') as zip_ref:
                zip_ref.extractall(extract_path)
            # print("Completed Unziping master")

            path = extract_path

        except (OSError, zipfile.BadZipFile) as e:
            print(
                F"Failed to unzip master for path : {pathofmaster} with err {e}")
        return path

    # 8 . Function to load all segment data to Internal memory [RAM] via dataframe
    def loadallmastertextfile(self, signal: str) -> None:
        """load all segment data to system memory"""
        try:
            if signal == MasterTypeVar.with_cash:
                if self.__pathcash is not None:  # verify
                    print("*** Reading Cash Master ***")
                    self.__cashmasteronly()
                # self.__downloadmatserfileusingurl(self.__nse)

            elif signal == MasterTypeVar.with_fno:
                print("*** Reading FNO Master ***")
                if self.__pathfno is not None:  # verify
                    self.__fnomasteronly()
                # self.__downloadmatserfileusingurl(self.__nfo)

            elif signal == MasterTypeVar.with_both:
                print("*** Reading Cash & FNO Master ***")
                if self.__pathcash is not None:  # verify
                    self.__cashmasteronly()
                if self.__pathfno is not None:  # verify
                    self.__fnomasteronly()
                # self.__downloadmatserfileusingurl(self.__nse)
                # self.__downloadmatserfileusingurl(self.__nfo)

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

        except (FileNotFoundError, pd.errors.EmptyDataError) as e:
            print(
                F"Error occured while reading file from localm with err: {e}")

    # 9. Function read F&O Master text file
    def __fnomasteronly(self):
        """Read F&O Master data"""
        try:
            path = self.__pathfno + "\\" + "NFO_symbols.txt"
            print(path)
            self.__df_fno = pd.read_csv(path)
            print(F"Rows in master file : {len(self.__df_fno)}")
        except FileNotFoundError as e:
            print(f"FNO file not found: {e}")
        except pd.errors.EmptyDataError as e:
            print(f"FNO file is empty: {e}")

    # 10. Function to read Cash Master text file
    def __cashmasteronly(self):
        """Read Cash Master data"""
        try:
            path = self.__pathcash + "\\" + "NSE_symbols.txt"
            print(path)
            self.__df_cash = pd.read_csv(path)
            print(F"Rows in master file : {len(self.__df_cash)}")
        except FileNotFoundError as e:
            print(f"Cash file not found: {e}")
        except pd.errors.EmptyDataError as e:
            print(f"Cash file is empty: {e}")
