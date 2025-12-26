"""Tradingengine.py Main Trading Engine Module"""
import time
import pandas as pd

from BrokerAPI.FinvasiaAPI import interfacefinvasia
from Master.MasterFinvasia.mastersymbolfinvasia import MasterSymbolFinvasia, MasterTypeVar
from Utility.relativepath import Path
import settings
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
        # self.df_fno = pd.DataFrame()

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
        """
        Function to take new entry based on strategy signal.
        SAFE MODE: No order will be placed unless valid data is supplied.
        """
        try:
            print("Taking New Entry...")

            # --------------------------------------------------
            # 🚫 ORDER PLACEMENT DISABLED (DEVELOPMENT MODE)
            # --------------------------------------------------

            # buy_or_sell = ""
            # product_type = ""
            # exchange = ""
            # tradingsymbol = ""
            # quantity = ""
            # discloseqty = ""
            # price_type = ""
            # price = ""
            # trigger_price = None
            # retention = 'DAY'
            # amo = None
            # remarks = None
            # bookloss_price = 0.0
            # bookprofit_price = 0.0
            # trail_price = 0.0

            # rec_orderid = self.__shoonyafinvasia.transmitordertobroker_oms(
            #     buy_or_sell,
            #     product_type,
            #     exchange,
            #     tradingsymbol,
            #     quantity,
            #     discloseqty,
            #     price_type,
            #     price,
            #     trigger_price,
            #     retention,
            #     amo,
            #     remarks,
            #     bookloss_price,
            #     bookprofit_price,
            #     trail_price
            # )
            # if rec_orderid != -1:
            #     print(F"Order Placed Successfully. Order ID: {rec_orderid}")
            # else:
            #     print("Order Placement Failed.")

        except (ValueError, TypeError, RuntimeError, ConnectionError) as e:
            print(F"Error Occured while taking new entry... : {e}")

    # 5. Function to get market data and streaming data from broker API
    def activatemarketfeed(self):
        """Function to activate market data feed from broker API."""
        try:
            print("Getting Market Data...")
            # Implement market data retrieval here
            self.__shoonyafinvasia.startstreamingusingwebsocket()

            print("Waiting 5 seconds for initial market data...")
            # 🔹 NEW: Give time for initial ticks to populate df_feed
            time.sleep(5)

            print('Client Dynamic Requirements for Tokens subscription...')
            # example token list
            clientcallinglist = ['NSE|22', 'NSE|3456']
            self.__shoonyafinvasia.subscribetokentobroker(clientcallinglist)

            self.subcribe_live_feed_cash()
            # self.subcribe_live_feed_fno()

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
            # self.df_fno = __master.getfnomasterdata()

            self.applyinstrumentsfilter_cash()
            # self.applyinstrumentsfilter_fno()
            # self.subcribe_live_feed()

        except (ConnectionError, TimeoutError, RuntimeError) as e:
            print(
                F"Error Occured while downloading master symbol database... : {e}")

    # 10. Function to filter on the basis of Cluster [EQ, SM, BE etc]
    def applyinstrumentsfilter_cash(self):
        """Filter cash master data for EQ Instruments"""
        try:
            if self.df_cash is None or self.df_cash.empty:
                raise ValueError("Cash dataframe is empty or not initiatlized")

            # Filter by instrument type
            self.df_cash = self.df_cash[
                self.df_cash['Instrument'].isin(settings.instrument_list)]

            # Filter valid equity symbols (optional but safer)
            self.df_cash = self.df_cash[
                self.df_cash['Symbol'].str.match('^[^0-9]')]

            self.df_cash = self.df_cash.reset_index(drop=True)

        except ValueError as e:
            print(F"Pattern matching failed : {e}")

        except KeyError as e:
            print(F"Column: missing from dataframe:{e}")

    # 11. Function to suscribe to live feeds from the cluster dataframe
    def subcribe_live_feed_cash(self) -> None:
        """This function assist to subscribe to live market feeds from dataframe (NSE, BSE, MCX)"""
        try:
            if not isinstance(self.__shoonyafinvasia, interfacefinvasia.InterfaceFinvasia):
                raise AttributeError(
                    "This method must be accessed through an instance of the class")
            if (self.df_cash).empty:
                raise ValueError("No data in cash DataFrame")
            token_list = list(self.df_cash['Token'])
            formatted_token_list = ["{}|{}".format(
                'NSE', token) for token in token_list]

            self.__shoonyafinvasia.subscribetokentobroker(formatted_token_list)

        except (ValueError, KeyError) as e:
            print(F"Error occured while subscribing to live feeds : {e}")

    # 12. Function to filter on the basis of Cluster Option
    # def applyinstrumentsfilter_fno(self):
    #     """Filter FNO master data for EQ Instruments"""
    #     try:
    #         if self.df_fno is None or self.df_fno.empty:
    #             raise ValueError("F&O dataframe is empty or not initiatlized")

    #         # Filter by instrument type
    #         option = ['CE', 'PE']

    #         # Include Trading Symbol for Future list
    #         future = ['XX']

    #         # combining both Option and Future data
    #         self.df_fno = self.df_fno[
    #             (
    #                 self.df_fno['Symbol'].isin(settings.option_list) &
    #                 self.df_fno['OptionType'].isin(option)
    #             )
    #             |
    #             (
    #                 self.df_fno['Symbol'].isin(settings.future_list) &
    #                 self.df_fno['OptionType'].isin(future)
    #             )
    #         ]

    #         # Filter on expiry (optional but safer)
    #         self.df_fno = self.df_fno[
    #             self.df_fno['Expiry'].isin(settings.expiry_list)]
    #         # rest index from 0 again
    #         self.df_fno = self.df_fno.reset_index(drop=True)

    #     except ValueError as e:
    #         print(F"Pattern matching failed : {e}")

    #     except KeyError as e:
    #         print(F"Column: missing from dataframe:{e}")

    # # 13. Function to suscribe to live feeds from the cluster dataframe
    # def subcribe_live_feed_fno(self) -> None:
    #     """Subscribe to FNO live market feeds from Cluster dataframe"""
    #     try:
    #         if not isinstance(self.__shoonyafinvasia, interfacefinvasia.InterfaceFinvasia):
    #             raise AttributeError(
    #                 "This method must be accessed through an instance of the class")

    #         if (self.df_fno).empty:
    #             raise ValueError("No data in F&O DataFrame")

    #         token_list = list(self.df_fno['Token'])
    #         formatted_token_list = ["{}|{}".format(
    #             'NFO', token) for token in token_list]

    #         # This is bulk token streaming approach
    #         self.__shoonyafinvasia.subscribetokentobroker(formatted_token_list)
    #         # self.__shoonyafinvasia.subscribetokentobroker(
    #         #     [f"NFO|,{token}" for token in self.df_fno['Token'].tolist()])

    #     except (ValueError, KeyError) as e:
    #         print(F"Error occured while subscribing to live feeds : {e}")

    # 14. Start strategy
    def start(self):
        """Start function for strategy"""
        # waiting Block
        print("start function is called....")
        count = 0
        while True:  # Infinite Loop to keep the streaming alive
            count += 1
            if count > 50000000:
                count = 0
            # self.conditional_strategy()
            # self.conditional_stategy_doji()
            # self.conditional_stategy_hammer()
            self.conditional_strategy_shootingstar()

    # 15. Conditional Strategy for Stocks and FNO
    def conditional_strategy(self):
        """Start conditional strategy review """
        try:
            if self.__shoonyafinvasia.is_connected():
                # # 🔹 NEW: skip if df_feed is empty
                # if self.__shoonyafinvasia.df_feed.empty:
                #     print("No market data yet, skipping Conditional strategy.")
                #     return

                for idx, row in self.__shoonyafinvasia.df_feed.iterrows():
                    # LTP > High --> cs 1
                    # ['TradingSymbol', 'Open', 'High', 'Low', 'Close', 'Ltp', 'Vol']
                    _lpt = row['Ltp']
                    _high = row['High']
                    _low = row['Low']
                    stockname = row['TradingSymbol']

                    if _lpt > _high:
                        print(
                            F"Stocks under Bullish category : {stockname} {_lpt} {_high}")
                    if _lpt < _high:
                        print(
                            F"Stocks under Bearish category : {stockname} {_lpt} {_low}")

        except KeyError as e:
            print(f"Column missing in CS : {e}")
        except TypeError as e:
            print(f"Invalid type in CS : {e}")

    # 16. Function - DOJI candle pattern implementation
    def conditional_stategy_doji(self):
        """Doji pattern"""
        try:
            if self.__shoonyafinvasia.is_connected():

                for idx, row in self.__shoonyafinvasia.df_feed.iterrows():
                    # ['TradingSymbol', 'Open', 'High', 'Low', 'Close', 'Ltp', 'Vol']
                    # print("Executing Doji Validation condition")
                    _token = idx
                    _open = row['Open']
                    _high = row['High']
                    _low = row['Low']
                    _close = row['Close']
                    _ltp = row['Ltp']
                    stockname = row['TradingSymbol']

                    # Skip invalid candles
                    if _high <= _low or _open <= 0 or _close <= 0:
                        continue

                    candle_range = _high - _low
                    if candle_range == 0:
                        continue

                    body_size = abs(_open - _close)
                    upper_wick = _high - max(_open, _close)
                    lower_wick = min(_open, _close) - _low

                    # Doji conditions
                    small_body = body_size <= (0.1 * candle_range)
                    balanced_wicks = abs(
                        upper_wick - lower_wick) <= (0.2 * candle_range)

                    if small_body and balanced_wicks:
                        print(
                            f"DOJI detected: {stockname} | "
                            f"O:{_open} H:{_high} L:{_low} C:{_close}"
                        )

        except KeyError as e:
            print(f"Column missing in Doji Strategy : {e}")
        except TypeError as e:
            print(f"Invalid type in Doji Strategy : {e}")

    # 17. Function - Hammer candle pattern implementation
    def conditional_stategy_hammer(self):
        """Hammer pattern"""
        try:
            if self.__shoonyafinvasia.is_connected():
                for idx, row in self.__shoonyafinvasia.df_feed.iterrows():
                    _token = idx
                    _open = row['Open']
                    _high = row['High']
                    _low = row['Low']
                    _close = row['Close']
                    _ltp = row['Ltp']
                    stockname = row['TradingSymbol']

                    # Skip invalid candles
                    if _high <= _low or _open <= 0 or _close <= 0:
                        continue

                    candle_range = _high - _low
                    body_size = abs(_open - _close)

                    upper_wick = _high - max(_open, _close)
                    lower_wick = min(_open, _close) - _low

                    # Avoid divide-by-zero or bad candles
                    if candle_range == 0:
                        continue

                    # Hammer conditions
                    small_body = body_size <= (0.3 * candle_range)
                    long_lower_wick = lower_wick >= (2 * body_size)
                    small_upper_wick = upper_wick <= (0.1 * candle_range)

                    # Hammer condition: body is very small compared to range
                    if small_body and long_lower_wick and small_upper_wick:
                        print(
                            f"HAMMER detected: {stockname} | "
                            f"O:{_open} H:{_high} L:{_low} C:{_close}"
                        )

        except KeyError as e:
            print(f"Column missing in Hammer Strategy : {e}")
        except TypeError as e:
            print(f"Invalid type in Hammer Strategy : {e}")

    # 18. Function - Shooting star candle pattern implementation
    def conditional_strategy_shootingstar(self):
        """Shooting Star (Bearish) candle pattern"""
        try:
            if self.__shoonyafinvasia.is_connected():
                df_feed = self.__shoonyafinvasia.df_feed

                for pos in range(len(df_feed)):
                    row = df_feed.iloc[pos]
                    _token = df_feed.index[pos]       # Token from index
                    _open = row['Open']
                    _high = row['High']
                    _low = row['Low']
                    _close = row['Close']
                    stockname = row['TradingSymbol']

                    # Skip invalid candles
                    if _high <= _low or _open <= 0 or _close <= 0:
                        continue

                    candle_range = _high - _low
                    if candle_range == 0:
                        continue

                    body_size = abs(_open - _close)
                    upper_wick = _high - max(_open, _close)
                    lower_wick = min(_open, _close) - _low

                    # Shooting Star conditions
                    small_body = body_size <= (0.3 * candle_range)
                    long_upper_wick = upper_wick >= (2 * body_size)
                    small_lower_wick = lower_wick <= (0.1 * candle_range)

                    # Optional: trend confirmation (previous candle bullish)
                    if pos > 0:
                        prev_row = df_feed.iloc[pos - 1]
                        uptrend = prev_row['Close'] > prev_row['Open']
                    else:
                        uptrend = False

                    if uptrend and small_body and long_upper_wick and small_lower_wick:
                        print(
                            f"SHOOTING STAR detected: {stockname} | "
                            f"O:{_open} H:{_high} L:{_low} C:{_close} | Token:{_token}"
                        )

        except KeyError as e:
            print(f"Column missing in Shooting Star Strategy : {e}")
        except TypeError as e:
            print(f"Invalid type in Shooting Star Strategy : {e}")
