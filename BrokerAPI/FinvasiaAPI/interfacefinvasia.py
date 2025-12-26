"""interfacefinvasia.py - Interface module for Finvasia Broker API interaction."""

# import time
import pandas as pd

from BrokerAPI.FinvasiaAPI.api_helper import ShoonyaApiPy
from CredentialTo.credentialtobroker import CredentialFinvasia


class InterfaceFinvasia:
    """Interface for finvasia Broker API interaction"""

    # 1. Function to initialize the Finvasia interface
    def __init__(self):  # constructor
        print("Connecting to Finvasia Broker API...")
        # process initialization here
        # acting as private member
        self.__shoonyapi = ShoonyaApiPy()
        self.__isconnected = False  # Broker login state
        self.__iswebsocketconnected = False  # WebSocket connection status flag
        self.__set_up_feed()

    # 2. Function to setup dataframe to store feeds
    # self=<BrokerAPI.FinvasiaAPI.interfacefinvasia.InterfaceFinvasia object at 0x000001B0BE052F90>
    def __set_up_feed(self):
        # feed_col = ['Token', 'TradingSymbol', 'Open',
        #             'High', 'Low', 'Close', 'Ltp', 'Vol']
        # self.df_feed = pd.DataFrame(columns=feed_col)
        feed_col = ['TradingSymbol', 'Open',
                    'High', 'Low', 'Close', 'Ltp', 'Vol']
        self.df_feed = pd.DataFrame(columns=feed_col)
        self.df_feed.index.name = 'Token'

    # 3. Function to display login panel

    def login_panel(self):
        """Function to handle login to Finvasia Broker API"""
        # 6 digit code from 2FA app as per broker requirement
        totp = self.__get_totp_factor()

        if totp == -1:
            print("Login aborted due to TOTP generation error..")
            return

        # Implement login panel logic here
        # Converting totp factor from int to string for better readability
        totp = str(totp)
        try:
            ret = self.__shoonyapi.login(userid=CredentialFinvasia.Uid,
                                         password=CredentialFinvasia.Password,
                                         twoFA=totp,
                                         vendor_code=CredentialFinvasia.VendorCode,
                                         api_secret=CredentialFinvasia.APIKEY,
                                         imei=CredentialFinvasia.IMEI)
        except (ConnectionError, TimeoutError, OSError, ValueError, KeyError) as e:
            print(f"Exception occurred during broker login: {e}")
            return

        print(F"Broker Replied: {ret} ")

        # Validate response
        if not ret or not isinstance(ret, dict):
            print("Invalid response from broker login. Check credentials and network.")
            return

        stat = ret.get('stat')
        if stat is None:
            print("Broker response missing 'stat' field. Full response: {ret}")
            return

        print(F"Connection Establised to Broker : {stat}")

        if stat == "Ok":
            print("Successfully Logged in to Finvasia Broker API")
            self.__sucessfully_connected()
        else:
            print("Login Failed.")

    # 4. Function to get TOTP factor for 2FA
    def __get_totp_factor(self):  # private method to get TOTP factor
        try:  # try block to handle exceptions
            print("Please Enter TOTP (6 digit) Numeric Character")  # prompt user
            result = input()  # get user input and CPU wait for user input

            check_length_of_input = len(result)  # check length of input
            if check_length_of_input != 6:  # validate length
                print("Invalid TOTP Length. It should be 6 digits.")  # log error
                return self.__get_totp_factor()  # recursive call to re-prompt
            result = int(result)  # convert input to integer

            return result  # return the entered TOTP

        except ValueError:  # handle exception
            # log error
            print("Error in generating TOTP factor: Invalid input provided")
            return -1  # indicate failure

    # 5. Function Connection Establishment == "OK"
    def __sucessfully_connected(self):
        try:
            self.__isconnected = True  # implement connection check logic here
        except (ConnectionError, OSError) as e:
            print(f"Error in connection establishment: {e}")

    # 6. Function to Confirm client about connection status {Ok, NOT OK}
    def is_connected(self):
        """This public method"""
        return self.__isconnected  # False

    # 7. Function to Requseting Data from broker Server
    def requesttobroker(self):
        """Function to request data from Finvasia Broker API"""

        if self.is_connected() is False:  # check connection status
            print("Please Connect to broker server first.")
            return  # early return

    # 8. Function to close connection forecefully - Logout
    def close_api(self):
        """Function to close API connection to Finvasia Broker"""
        try:
            if self.is_connected() is False:
                print("Already Disconnected from Broker API.")
                return

            result = self.__shoonyapi.logout()  # call logout method from ShoonyaApiPy
            if result['stat'] == "Ok":
                print("Successfully logged out from Broker API.")
            else:
                print("Logout Failed from Broker API.")
        except (ConnectionError, TimeoutError, OSError, KeyError) as e:
            print(f"Error in logging out: {e}")

    # 9. Function to Transmit Order to Broker API
    def transmitordertobroker_oms(self, buy_or_sell, product_type, exchange,
                                  tradingsymbol, quantity, discloseqty,
                                  price_type, price, trigger_price, retention,
                                  amo, remarks, bookloss_price,
                                  bookprofit_price, trail_price):
        """
        Transmit order to Finvasia OMS with validation
        """
        try:
            # 🚨 VALIDATION BLOCK Transmit order to broker API
            print('sending trader(signla) to broker OMS')

            order_message = self.__shoonyapi.place_order(buy_or_sell, product_type, exchange,
                                                         tradingsymbol, quantity, discloseqty,
                                                         price_type, price, trigger_price,
                                                         retention, amo, remarks, bookloss_price,
                                                         bookprofit_price, trail_price)

            # print(F"Order Transmit Result from Broker API: {order_message}")

            if order_message['stat'] == "Ok":
                # Order Transmitted Successfully to Broker API
                return int(order_message['norenordno'])  # return order number
            else:
                return -1

        except (ConnectionError, TimeoutError, OSError, KeyError, ValueError) as e:
            print(
                F"Error Occured while transmitting Order to Broker API... : {e}")
            return -1

    # Application callbacks
    # Critical heart of Algo Trading System and ownership of calling is with broker
    # CF = Critical Function - Heart of Algo Trading System
    # NP2U = Non Preemptive to User
    # OWN = Ownership of Calling is with Broker Server
    # TOTP = Run on Thread Pool

    # 10. Function used by Broker calling back for order update | CF | NP2U | OWN | ROTP
    def __event_handler_order_update(self, message):
        print("order event: " + str(message))

    # 11. Function used by Broker calling back for quote update | CF | NP2U | OWN | ROTP
    def __event_handler_quote_update(self, message):
        """Handle broker quote updates safely without FutureWarning"""
        try:
            # TBT :{ 't': 'tf', 'e': 'NSE', 'tk': '22', 'lp': '2324.85', 'pc': '-1.01', 'ft': ...'}
            token = message['tk']

            # Extract & convert values safely
            def get_float(key):
                return float(message[key]) if key in message else None

            ltp = get_float('lp')
            op_pre = get_float('o')
            hi_pre = get_float('h')
            lw_pre = get_float('l')
            cl_pre = get_float('c')
            vol = get_float('v')

            # 🔴 Skip incomplete ticks
            if None in (ltp, op_pre, hi_pre, lw_pre, cl_pre):
                return   # skip incomplete tick safely

            # volume = 1  # tick volume

            # 🔴 -------- EXPLICIT INSERT / UPDATE --------
            is_new = token not in self.df_feed.index

            if is_new:
                # INSERT
                self.df_feed.loc[token] = pd.Series({
                    'TradingSymbol': 'NA',  # TradingSymbol
                    'Open': op_pre,          # Open
                    'High': hi_pre,          # High
                    'Low': lw_pre,           # Low
                    'Close': cl_pre,         # Close
                    'Ltp': ltp,              # Ltp
                    'Vol': vol               # Volume
                }, name=token)
            else:
                # UPDATE: Existing Token
                # .loc for updating multiple columns.
                self.df_feed.loc[token, [
                    'Open', 'High', 'Low', 'Close', 'Ltp'
                ]] = [
                    op_pre, hi_pre, lw_pre, cl_pre, ltp
                ]
                # .at only works for a single cell, not multiple columns at once.
                self.df_feed.at[token, 'Vol'] += vol

                # self.df_feed.loc[token, 'Vol'] += volume

            # Insert function - if Key (Token) Absent
            # if token not in self.df_feed['Token'].values:
            #     nw_recd = {'Token': token, 'TradingSymbol': 'NA', 'Open': op_pre,
            #                'High': hi_pre, 'Low': lw_pre, 'Close': cl_pre, 'Ltp': ltp, 'Vol': vol}
            #     self.df_feed = self.df_feed.append(nw_recd, ignore_index=True)

            # else:  # Update function - if key is present
            #     # print('Code entered to block part')
            #     self.df_feed.loc[self.df_feed['Token'] == token, [
            #         'Open', 'High', 'Low', 'Close', 'Ltp', 'Vol']] = [op_pre, hi_pre, lw_pre, cl_pre, ltp, vol]

                # # ONE unified insert/update operation
            # self.df_feed.loc[token, [
            #     'TradingSymbol',
            #     'Open',
            #     'High',
            #     'Low',
            #     'Close',
            #     'Ltp',
            #     'Vol'
            # ]] = [
            #     self.df_feed.loc[token, 'TradingSymbol']
            #     if token in self.df_feed.index else 'NA',
            #     op_pre,
            #     hi_pre,
            #     lw_pre,
            #     cl_pre,
            #     ltp,
            #     self.df_feed.loc[token, 'Vol'] + volume
            #     if token in self.df_feed.index else volume
            # ]

        except KeyError as e:
            print(f"Key Error: {e}")
        except ValueError as e:
            print(f"Value Error: {e}")

        # print(self.df_feed.tail(3))

    # 12. Function used by Broker calling back when socket is opened | CF | NP2U | OWN | ROTP
    def __open_callback(self):
        """🔹 Socket Open (Broker-owned callback)"""
        print("🔌 WebSocket opened")

        # self.ws_started = True

        # top priority function to manage websocket connection status
        self.__iswebsocketconnected = True

        # Initial subscriptions (if any) brokercallinglist = ['NSE|22', 'NSE|3456']  # example token list
        brokercallinglist = []
        if brokercallinglist:
            self.subscribetokentobroker(brokercallinglist)
        # end of callbacks

    # 13. Function from client to streaming data from broker server

    def startstreamingusingwebsocket(self):
        """
        Start WebSocket streaming safely.
        Prevents multiple WebSocket connections.
        """
        try:
            # ❌ Broker not connected → do nothing
            if self.is_connected() is False:  # False
                print(
                    "❌ Web Socket Streaming Connection Failed to Establish. Broker not connected.")
                return None

            # ❌ WebSocket already open
            if self.__iswebsocketconnected:
                print("⚠ WebSocket already connected.")
                return

            print("Starting Web Socket for Streaming Data from Broker Server...")
            # Executing Web Socket Start Function
            self.__shoonyapi.start_websocket(
                order_update_callback=self.__event_handler_order_update,
                subscribe_callback=self.__event_handler_quote_update,
                socket_open_callback=self.__open_callback,
                socket_close_callback=self.__close_callback,
                socket_error_callback=self.__error_callback
            )

            print("WebSocket start request sent to broker.")
            # wait for 5 seconds to ensure connection is established
            # time.sleep(5)

            print("Streaming Request Completed from Broker Server.")

        except (ConnectionError, TimeoutError, OSError, RuntimeError) as e:
            print(f"Error occured while starting Web Socket with Err: {e}")

    def __close_callback(self):
        """🔹 Socket Close"""
        print("🔌 WebSocket closed")
        self.__iswebsocketconnected = False

    def __error_callback(self, error):
        """🔹 Socket Error"""
        print(f"❌ WebSocket error: {error}")
        self.__iswebsocketconnected = False

    # 14. Function from client to Dynamic request data from broker server and Main Thread + ROTP

    def subscribetokentobroker(self, tokenlist):
        """Function to subscribe tokens to Finvasia Broker API for market data."""
        try:
            if self.iswebsocketconnectionopened() is False:
                print("Web Socket Connection is not opened. Cannot subscribe tokens.")
                return

            if isinstance(tokenlist, list):
                # handle this function to List collection
                print("Bulk Subscribe to Broker")
                self.__shoonyapi.subscribe(tokenlist)
            else:
                # This is the costly function as we have to same time, money, speed
                print("One by One Subscribe to Broker")
                self.__shoonyapi.subscribe(tokenlist)

        except (ConnectionError, TimeoutError, OSError, RuntimeError) as e:
            print(
                f"Error occured while subscribing tokens to broker with Err: {e}")

    # 15. Function to check Web Socket connection status from broker server
    def __managewebsocketconnection(self):
        try:
            self.__iswebsocketconnected = True
        except (ConnectionError, TimeoutError, OSError) as e:
            print(
                f"Error occured while checking Web Socket connection status with Err: {e}")
            return False

    # 16. Function allow Trading Engine to know the Web Socket connection status (like Open/Close)
    def iswebsocketconnectionopened(self):
        """Function to check if Web Socket connection is opened."""
        return self.__iswebsocketconnected

    # 17. Function to Get complete Order Book from Broker API
    def getcompleteorderbookfrombroker(self):
        """Function to get complete order book from Finvasia Broker API."""
        try:
            if self.is_connected() is False:
                print("Connection Failure...Please Connect to broker server first.")
                return None

            # Successfully connected to broker API
            getorderbook = self.__shoonyapi.get_order_book()

            if getorderbook is None:
                print("No packet received from broker.")
                return

            # actual processing of order book
            # print(F"Order Book from Broker API: {getorderbook}")
            for order in getorderbook:
                print(F"Order Details: {order}")

        except (ConnectionError, TimeoutError, OSError, RuntimeError) as e:
            print(
                f"Error occured while getting order book from broker with Err: {e}")

    # 18. Function to get executed (completed) trade book from broker
    def getexecutedtradebookfrombroker(self):
        """Function to get complete order book from Finvasia Broker API."""
        try:
            if self.is_connected() is False:
                print(
                    "Connection Failure. Please connect to broker server trade bookfirst.")
                return None

            # Successfully connected to broker API
            gettradebook = self.__shoonyapi.get_trade_book()

            if gettradebook is None:
                print("No packet received from broker.")
                return

            # actual processing of trade book
            # print(F"Order Book from Broker API: {gettradebook}")
            for order in gettradebook:
                print(F"Trade Details: {order}")

            # Count of Trades available in Trade Book
            trade_count = len(gettradebook)
            print(F"Total Trades Executed till now: {trade_count}")
        except (ConnectionError, TimeoutError, OSError, RuntimeError) as e:
            print(
                f"Error occured while getting trade book from broker with Err: {e}")

    # 19. Function to get Net Position (Live) from broker
    def getnetpositionfrombroker(self):
        """Function to get net position from Finvasia Broker API."""
        try:
            if self.is_connected() is False:
                print("Connection Failure...Please Connect to broker server first.")
                return None

            # Successfully connected to broker API
            getnetposition = self.__shoonyapi.get_positions()
            if getnetposition is None:
                print("No packet received from broker.")
                return

            # actual net position
            print(F"Net Position from Broker API: {getnetposition}")
            for position in getnetposition:
                print(F"Position Details: {position}")

            # count of net positions
            totalpositioncount = len(getnetposition)
            print(F"Total Net Positions till now: {totalpositioncount}")

        except (ConnectionError, TimeoutError, OSError, RuntimeError) as e:
            print(
                f"Error occured while getting net position from broker with Err: {e}")
