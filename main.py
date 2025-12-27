"main.py - Entry point for the trading application as Main module and thread."

import tradingengine as te

# https://shoonya.com/api-documentation
# https://github.com/Shoonya-Dev/ShoonyaApi-py
# https://cdn.sanity.io/files/3n8bfe6i/production/ff63049ecd3370926c77fca0ed82f1e960273367.pdf

if __name__ == "__main__":  # Main entry point
    handler = te.TradingEngine()
    handler.activatemastyersymboldownloader()
    handler.connecttobroker()
    handler.startengine()
    handler.start()
