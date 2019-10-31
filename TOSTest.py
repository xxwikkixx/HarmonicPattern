import tosdb
import time
import numpy as np
import pandas as pd
from datetime import datetime 
from tosdb.intervalize import ohlc
from timeit import default_timer
from xlwings import *

tosdb.init(dllpath=r"C:\TOSDataBridge\bin\Release\x64\tos-databridge-0.9-x64.dll")
block = tosdb.TOSDB_DataBlock(100000, True)
block.add_items('/MES:XCME', '/MYM:XCBT')
block.add_topics('OPEN', 'HIGH', 'LOW', 'bid', 'ask', 'volume', 'LAST', 'LASTX', 'BIDX', 'ASKX', 'LAST_SIZE', 'CUSTOM5', 'CUSTOM9')
### NOTICE WE ARE SLEEPING TO ALLOW DATA TO GET INTO BLOCK ###
print("Sleeping for 2 second")
time.sleep(2)

position_taken = 0 # Position is open or closed
trades_taken = 0
current_trade = '' # Current position of long or trade closed

def getLastPrice(symbol):
    # Bool value to check if its connected: True
    # print(tosdb.connected())

    # Bool value to check if the engine is connected
    # print(tosdb.connection_state()== tosdb.CONN_ENGINE_TOS)

    # block = tosdb.TOSDB_DataBlock(100000, True)

    # block.add_items('/ES:XCME')
    # block.add_topics('OPEN', 'HIGH', 'LOW', 'bid', 'ask', 'volume', 'LAST')

    # ### NOTICE WE ARE SLEEPING TO ALLOW DATA TO GET INTO BLOCK ###
    # print("sleeping for 1.5 seconds")
    # time.sleep(1.5)

    # ['ASK', 'BID', 'VOLUME']
    # print(block.topics())

    # while True:
    #     print(block.get('/ES:XCME', 'LAST'))
    #     time.sleep(.5)
    # tosdb.clean_up()
    return block.get(symbol, 'LAST')


def tosDBohlc():
    block = ohlc.tosdb.TOSDB_ThreadSafeDataBlock(10000)
    intrv = ohlc.TOSDB_OpenHighLowCloseIntervals(block, 60)
    print(intrv.get('/ES:XCME', 'OPEN'))
    tosdb.clean_up()


def tosOHLC():
    val = block.get("/MES:XCME", "CUSTOM9", date_time=False)
    op,hi,lo,cl = val.split("|")
    print(op, hi, lo, cl)


def tosCustomStudyData(symbol):
    val, times = block.get(symbol, 'CUSTOM5', date_time=True)
    if val == "1.0":
        return True
    elif val == "0.0":
        return False
    tosdb.clean_up()


if __name__ == '__main__':
    # # tosDBohlc()

    # while True:
    #     # print(getLastPrice('/ES:XCME'))
    #     data, times = block.get('/ES:XCME', 'LAST', date_time=True)
    #     print(data, times)
    #     time.sleep(.5)

    # tosOHLC()

    # tosCustomStudyData('/MES:XCME')
    while True:
        current_price = getLastPrice('/MES:XCME')
        '''
        if signal is long(True) and postion is not taken
        Increase trade count
        Take position
        Set the trade Long
        '''
        if tosCustomStudyData('/MES:XCME') == True and position_taken != 1:
            trades_taken += 1
            position_taken = 1
            current_trade = 'Long'
            print("Trade Taken ")
            print(trades_taken, position_taken, current_trade)

        '''
        if signal is long(true) and postion is already taken
        output the positions
        '''
        if tosCustomStudyData('/MES:XCME') == True and position_taken == 1:
            print("Existing Positions ")
            print(trades_taken, position_taken, current_trade)

        '''
        if signal is Short(False) and position is taken
        set position taken to closed 
        '''
        if tosCustomStudyData('/MES:XCME') == False and position_taken == 1:
            position_taken = 0
            current_trade = 'Trade Closed'
            print("Short signal sent, Trade Closed ")
            print(trades_taken, position_taken, current_trade)

        '''
        if signal is Short(False) and position is not taken
        output the positions 
        '''
        if tosCustomStudyData('/MES:XCME') == False and position_taken != 1:
            print("No Trade ")
            print(trades_taken, position_taken, current_trade)

        time.sleep(5)