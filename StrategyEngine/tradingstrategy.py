""" Building Trading Strategy to support Algo trading"""
import pandas as pd


class StrategyHeader:
    """ To support Strategy listing """
    STRATEGYNAME = "Strategy"
    SPOT = "Spot"
    EXPIRYDATE = "ExpiryDate"
    STRIKEPRICE = "StrikePrice"
    OPTIONTYPE = "OptionType"
    QUANTITY = "Qty"
    ATMITMOTM = "AtmOtmItm"


class StrategyEngine:
    """Class to support Algo Trading Strategy"""

    def __init__(self):
        try:
            print('reading trading strategy ...')
            col = [StrategyHeader.STRATEGYNAME, StrategyHeader.SPOT, StrategyHeader.EXPIRYDATE,
                   StrategyHeader.STRIKEPRICE, StrategyHeader.OPTIONTYPE, StrategyHeader.QUANTITY, StrategyHeader.ATMITMOTM]

            self.__df = pd.DataFrame(columns=col)  # _StrategyEngine__df

            self.read_input()

        except Exception as e:
            print(F"Error generated while init...trading engine : {e} ")

    def read_input(self):
        """Reading the trading strategy input"""
        strategy_data = [['Bull Call Spread', 'NIFTY',
                         '30-Dec-2025', '25700', 'CE', '100', 'ATM']]

        for strategy in strategy_data:
            self.__df.loc[len(self.__df)] = strategy

        print(self.__df)

    def get_tradingstrategy(self):
        """Getting ready for trade strategy"""
        return self.__df
