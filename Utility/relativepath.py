"""Module to get the current working directory"""

import os


class Path:
    """Class to get the current working directory"""

    @staticmethod
    def getcurrentdirectory():
        """Get the current working directory."""
        try:
            abspath = os.getcwd()
            return abspath
        except OSError as e:
            print(
                F"Error Occured while getting current working directory... : {e}")
            return None
