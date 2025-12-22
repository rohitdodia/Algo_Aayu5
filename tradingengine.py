"""Tradingengine.py Main Trading Engine Module"""
import pandas as pd

from BrokerAPI.FinvasiaAPI import interfacefinvasia
from Master.MasterFinvasia.mastersymbolfinvasia import MasterSymbolFinvasia, MasterTypeVar
from Utility.relativepath import Path
# from BrokerAPI.FyersAPI import InterfaceFyers

# Trading Engine Class


class TradingEngine:
    """Trading Engine Class to manage trading operations with broker APIs."""

    # 1. Function to initialize the trading engine
    def __init__(self):  # Initialize the trading engine
        print("Welcome to Trading Engine...")
        # Process initialization here
        self.__shoonyafinvasia = interfacefinvasia.InterfaceFinvasia()
        # self.__fyers = InterfaceFyers.InterfaceFyers()

        self.df_cash = pd.DataFrame()
        self.df_fno = pd.DataFrame()

    # 2. Function to connect to the broker API

    def connecttobroker(self):
        """Establish a connection to the broker API."""
        # Connect to the broker API
        try:
            self.__shoonyafinvasia.login_panel()
        except (ConnectionError, TimeoutError, RuntimeError) as e:
            print(F"Failed to Connect to Broker API... : {e}")

    # 3. Function to start the trading engine
    def startengine(self):
        """Start the engine."""
        if self.__shoonyafinvasia.is_connected() is True:
            # if self._fyers.is_connected() == True:
            # Do Work Here
            # self._fyers.requesttobroker()
            # self._shoonyafinvasia.requesttobroker()
            self.takenewentry()
            self.requestorderbook()
            self.requestexecutedtradebook()
            self.requestnetpositionlive()
            self.activatemarketfeed()
        else:
            print("Request to Broker Failed. Not Connected to Broker API.")

        self.__shoonyafinvasia.close_api()  # Close the API connection
        # self._fyers.close_api()  # Close the API connection

    # 4. Function Take Entruy Signal from Strategy Module
    def takenewentry(self):
        """Function to take new entry based on strategy signal."""
        try:
            print("Taking New Entry...")
            buy_or_sell = ""
            product_type = ""
            exchange = ""
            tradingsymbol = ""
            quantity = ""
            discloseqty = ""
            price_type = ""
            price = ""
            trigger_price = None
            retention = 'DAY'
            amo = None
            remarks = None
            bookloss_price = 0.0
            bookprofit_price = 0.0
            trail_price = 0.0

            rec_orderid = self.__shoonyafinvasia.transmitordertobroker_oms(
                buy_or_sell,
                product_type,
                exchange,
                tradingsymbol,
                quantity,
                discloseqty,
                price_type,
                price,
                trigger_price,
                retention,
                amo,
                remarks,
                bookloss_price,
                bookprofit_price,
                trail_price
            )
            if rec_orderid != -1:
                print(F"Order Placed Successfully. Order ID: {rec_orderid}")
            else:
                print("Order Placement Failed.")

        except (ValueError, TypeError, RuntimeError, ConnectionError) as e:
            print(F"Error Occured while taking new entry... : {e}")

    # 5. Function to get market data and streaming data from broker API
    def activatemarketfeed(self):
        """Function to activate market data feed from broker API."""
        try:
            print("Getting Market Data...")
            # Implement market data retrieval here
            self.__shoonyafinvasia.startstreamingusingwebsocket()

            print('Client Dynamic Requirements for Tokens subscription...')
            # example token list
            clientcallinglist = ['NSE|22', 'NSE|3456']
            self.__shoonyafinvasia.subscribetokentobroker(clientcallinglist)

            # waiting Block
            count = 0
            while True:  # Infinite Loop to keep the streaming alive
                count += 1
                if count > 50000000:
                    count = 0

            rg_meme_quotes = "Khatma Bye Bye Tata good Bye Gaya"
            print(rg_meme_quotes)

        except (ConnectionError, TimeoutError, RuntimeError) as e:
            print(F"Error Occured while getting market data... : {e}")

    # 6. Function to Request order book from Broker
    def requestorderbook(self):
        """Function to request order book from broker API."""
        print("Requesting Order Book from Broker...")
        self.__shoonyafinvasia.getcompleteorderbookfrombroker()

    # 7. Fundction to request trade book from Broker
    def requestexecutedtradebook(self):
        """Function to request trade book from broker API."""
        print("Requesting Trade Book from Broker...")
        self.__shoonyafinvasia.getexecutedtradebookfrombroker()

    # 8. Fundction to request Position book from Broker
    def requestnetpositionlive(self):
        """Function to request trade book from broker API."""
        print("Requesting Trade Book from Broker...")
        self.__shoonyafinvasia.getnetpositionfrombroker()

    # 9. Function to download Matser Symbol Database from Broker
    def activatemastyersymboldownloader(self):
        """Function to download master symbol database from broker API."""
        try:

            print("Processing Master...")
            print("Please wait while downloading master symbol database...")

            getfullpath = Path.getcurrentdirectory()
            print(F"Current Working Directory is : {getfullpath}")

            __master = MasterSymbolFinvasia(getfullpath)

            # filtering capability
            __master.downloadmasterfile(MasterTypeVar.with_both)
            __master.loadallmastertextfile(str(MasterTypeVar.with_both))

            self.df_cash = __master.getcashmasterdata()
            self.df_fno = __master.getfnohmasterdata()

        except (ConnectionError, TimeoutError, RuntimeError) as e:
            print(
                F"Error Occured while downloading master symbol database... : {e}")
