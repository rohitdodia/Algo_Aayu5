""" Building Trading Strategy to support Algo trading"""
import pandas as pd


class StrategyEngine:
    """Class to support Algo Trading Strategy"""

    def __init__(self):
        try:
            self.__df = pd.DataFrame()

            self.read_input()

        except Exception as e:
            print(F"Error generated while init...trading engine : {e} ")

    def read_input(self):
        """Reading the trading strategy input"""
        pass

    def get_tradingstrategy(self):
        """Getting ready for trade strategy"""
        return self.__df
