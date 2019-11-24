import tosdb
import time
from tosdb.intervalize import ohlc
from threading import Thread

tosdb.init(dllpath=r"C:\TOSDataBridge\bin\Release\x64\tos-databridge-0.9-x64.dll")

class TradeBot(Thread):
    def __init__(self, ticker):
        Thread.__init__(self)
        self.ticker = ticker
        self.block = tosdb.TOSDB_DataBlock(100000, True)
        self.ohlcblock = ohlc.tosdb.TOSDB_ThreadSafeDataBlock(100000)
        self.block.add_items(ticker)
        self.block.add_topics(
            "OPEN",
            "HIGH",
            "LOW",
            "bid",
            "ask",
            "volume",
            "LAST",
            "LASTX",
            "BIDX",
            "ASKX",
            "LAST_SIZE",
            "CUSTOM5",
            "CUSTOM9",
        )

    def getLastPrice(self):
        return self.block.get(self.ticker, "LAST", date_time=True)

    def tosDBohlc(self):
        self.intrv = ohlc.TOSDB_OpenHighLowCloseIntervals(self.ohlcblock, 60)
        return self.intrv.get(self.ticker, "OPEN")

    def tosOHLCMinute(self):
        self.val = self.block.get(self.ticker, "CUSTOM9", date_time=False)
        open, high, low, close = val.split("|")
        open = float(open.replace(",", ""))
        high = float(high.replace(",", ""))
        low = float(low.replace(",", ""))
        close = float(close.replace(",", ""))
        return open, high, low, close

    def tosVolTrailingStopSTUDY(self):
        val, times = self.block.get(self.ticker, "CUSTOM5", date_time=True)
        if val == "1.0":
            return True
        elif val == "-1.0":
            return False
        tosdb.clean_up()

    def tosPlotChart(self):
        pass

    def buyPos(self):
        pass

    def sellPos(self):
        pass

    def reversePos(self):
        pass

    def flattenPos(self):
        pass

MES = TradeBot("/MES:XCME")
MYM = TradeBot("/MYM:XCBT")
MES.start()
MYM.start()

print(MES.getLastPrice())
print(MYM.getLastPrice())
