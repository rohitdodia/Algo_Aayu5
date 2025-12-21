"""interfacefinvasia.py - Interface module for Finvasia Broker API interaction."""

import time

from BrokerAPI.FinvasiaAPI.api_helper import ShoonyaApiPy
from CredentialTo.credentialtobroker import CredentialFinvasia


class InterfaceFinvasia:
    """Interface for finvasia Broker API interaction"""

    # 1. Function to initialize the Finvasia interface
    def __init__(self):  # constructor
        print("Connecting to Finvasia Broker API...")
        # process initialization here
        # acting as private member
        self._shoonyapi = ShoonyaApiPy()
        self._isconnected = False  # connection status flag
        self._iswebsocketconnected = False  # WebSocket connection status flag

    # 2. Function to display login panel
    def login_panel(self):
        """Function to handle login to Finvasia Broker API"""
        # 6 digit code from 2FA app as per broker requirement
        totp = self._get_totp_factor()

        if totp == -1:
            print("Login aborted due to TOTP generation error..")
            return

        # Implement login panel logic here
        # Converting totp factor from int to string for better readability
        totp = str(totp)
        try:
            ret = self._shoonyapi.login(userid=CredentialFinvasia.Uid,
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
            self._sucessfully_connected()
        else:
            print("Login Failed.")

    # 3. Function to get TOTP factor for 2FA
    def _get_totp_factor(self):  # private method to get TOTP factor
        try:  # try block to handle exceptions
            print("Please Enter TOTP (6 digit) Numeric Character")  # prompt user
            result = input()  # get user input and CPU wait for user input

            check_length_of_input = len(result)  # check length of input
            if check_length_of_input != 6:  # validate length
                print("Invalid TOTP Length. It should be 6 digits.")  # log error
                return self._get_totp_factor()  # recursive call to re-prompt
            result = int(result)  # convert input to integer

            return result  # return the entered TOTP

        except ValueError:  # handle exception
            # log error
            print("Error in generating TOTP factor: Invalid input provided")
            return -1  # indicate failure

    # 4. Function Connection Establishment == "OK"
    def _sucessfully_connected(self):
        try:
            self._isconnected = True  # implement connection check logic here
        except (ConnectionError, OSError) as e:
            print(f"Error in connection establishment: {e}")

    # 5. Function to Confirm client about connection status {Ok, NOT OK}
    def is_connected(self):
        """This public method"""
        return self._isconnected  # False

    # 6. Function to Requseting Data from broker Server
    def requesttobroker(self):
        """Function to request data from Finvasia Broker API"""

        if self.is_connected() is False:  # check connection status
            print("Please Connect to broker server first.")
            return  # early return

    # 7. Function to close connection forecefully - Logout
    def close_api(self):
        """Function to close API connection to Finvasia Broker"""
        try:
            if self.is_connected() is False:
                print("Already Disconnected from Broker API.")
                return

            result = self._shoonyapi.logout()  # call logout method from ShoonyaApiPy
            if result['stat'] == "Ok":
                print("Successfully logged out from Broker API.")
            else:
                print("Logout Failed from Broker API.")
        except (ConnectionError, TimeoutError, OSError, KeyError) as e:
            print(f"Error in logging out: {e}")

    # 8. Function to Transmit Order to Broker API
    def transmitordertobroker_oms(self, buy_or_sell, product_type, exchange,
                                  tradingsymbol, quantity, discloseqty,
                                  price_type, price, trigger_price, retention,
                                  amo, remarks, bookloss_price,
                                  bookprofit_price, trail_price):
        """Function to transmit order to Finvasia Broker API OMS"""
        try:
            # Transmit order to broker API
            print('sending trader(signla) to broker OMS')

            order_message = self._shoonyapi.place_order(buy_or_sell, product_type, exchange,
                                                        tradingsymbol, quantity, discloseqty,
                                                        price_type, price, trigger_price, retention,
                                                        amo, remarks, bookloss_price,
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

    # 9. Function used by Broker calling back for order update | CF | NP2U | OWN | ROTP
    def _event_handler_order_update(self, message):
        print("order event: " + str(message))

    # 10. Function used by Broker calling back for quote update | CF | NP2U | OWN | ROTP
    def _event_handler_quote_update(self, message):
        print(F"TBT :{str(message)}")

    # 11. Function used by Broker calling back when socket is opened | CF | NP2U | OWN | ROTP
    def _open_callback(self):
        # top priority function to manage websocket connection status
        self._managewebsocketconnection()
        brokercallinglist = ['NSE|22', 'NSE|3456']  # example token list
        self.subscribetokentobroker(brokercallinglist)
        # end of callbacks

    # 12. Function from client to streaming data from broker server
    def startstreamingusingwebsocket(self) -> None:
        """Function to start Web Socket for streaming data from Finvasia Broker API."""
        try:
            print("Starting Web Socket for Streaming Data from Broker Server...")

            # Failback implementation if needed
            if self.is_connected() is False:
                print("Web Socket Streaming Connection Failed to Establish.")
                return None

            # Executing Web Socket Start Function
            self._shoonyapi.start_websocket(order_update_callback=self._event_handler_order_update,
                                            subscribe_callback=self._event_handler_quote_update,
                                            socket_open_callback=self._open_callback,
                                            socket_close_callback=None,
                                            socket_error_callback=None)

            # wait for 5 seconds to ensure connection is established
            time.sleep(5)

            print("Streaming Request Completed from Broker Server.")
        except (ConnectionError, TimeoutError, OSError, RuntimeError) as e:
            print(f"Error occured while starting Web Socket with Err: {e}")

    # 13. Function from client to Dynamic request data from broker server and Main Thread + ROTP
    def subscribetokentobroker(self, tokenlist):
        """Function to subscribe tokens to Finvasia Broker API for market data."""
        try:
            if self.iswebsocketconnectionopened() is False:
                print("Web Socket Connection is not opened. Cannot subscribe tokens.")
                return
            # This is the costly function as we have to same time, money, speed
            self._shoonyapi.subscribe(tokenlist)
        except (ConnectionError, TimeoutError, OSError, RuntimeError) as e:
            print(
                f"Error occured while subscribing tokens to broker with Err: {e}")

    # 14. Function to check Web Socket connection status from broker server
    def _managewebsocketconnection(self):
        try:
            self._iswebsocketconnected = True
        except (ConnectionError, TimeoutError, OSError) as e:
            print(
                f"Error occured while checking Web Socket connection status with Err: {e}")
            return False

    # 15. Function allow Trading Engine to know the Web Socket connection status (like Open/Close)
    def iswebsocketconnectionopened(self):
        """Function to check if Web Socket connection is opened."""
        return self._iswebsocketconnected

    # 16. Function to Get complete Order Book from Broker API
    def getcompleteorderbookfrombroker(self):
        """Function to get complete order book from Finvasia Broker API."""
        try:
            if self.is_connected() is False:
                print("Connection Failure...Please Connect to broker server first.")
                return None

            # Successfully connected to broker API
            getorderbook = self._shoonyapi.get_order_book()

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

    # 17. Function to get executed (completed) trade book from broker
    def getexecutedtradebookfrombroker(self):
        """Function to get complete order book from Finvasia Broker API."""
        try:
            if self.is_connected() is False:
                print(
                    "Connection Failure. Please connect to broker server trade bookfirst.")
                return None

            # Successfully connected to broker API
            gettradebook = self._shoonyapi.get_trade_book()

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

    # 18. Function to get Net Position (Live) from broker
    def getnetpositionfrombroker(self):
        """Function to get net position from Finvasia Broker API."""
        try:
            if self.is_connected() is False:
                print("Connection Failure...Please Connect to broker server first.")
                return None

            # Successfully connected to broker API
            getnetposition = self._shoonyapi.get_positions()
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
