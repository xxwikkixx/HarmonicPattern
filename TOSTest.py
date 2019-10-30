import tosdb
import time
import numpy as np
import pandas as pd
from tosdb.intervalize import ohlc
from timeit import default_timer
from xlwings import *

tosdb.init(dllpath=r"C:\TOSDataBridge\bin\Release\x64\tos-databridge-0.9-x64.dll")
block = tosdb.TOSDB_DataBlock(100000, True)
block.add_items('/MES:XCME', '/MYM:XCBT')
block.add_topics('OPEN', 'HIGH', 'LOW', 'bid', 'ask', 'volume', 'LAST', 'LASTX', 'BIDX', 'ASKX', 'LAST_SIZE', 'CUSTOM5')
### NOTICE WE ARE SLEEPING TO ALLOW DATA TO GET INTO BLOCK ###
print("Sleeping for 2 second")
time.sleep(2)

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


def test():
    buffer = []
    time.sleep(3)  # allow block time to load the cache
    buffer.append(block.get('/ES:XCME', 'BIDX', date_time=True,
                            indx=0))  # update marker
    time.sleep(5)  # wait perhaps for transactions to occur
    timer = 0
    while (timer < 5):  # get transactions for 5 seconds
        data,data2= block.get('/ES:XCME', 'BIDX', date_time=True) # this works
        # data = block.stream_snapshot_from_marker('/ES:XCME', 'BIDX', date_time=True, beg=0)
        print(data)
        print(data2)
        buffer.append(data)
        timer = default_timer()
    tosdb.clean_up()
    print(buffer)

def RTDdata():
    pass

def tosCustomStudyData():
    while True:
        esval, estimes = block.get('/MES:XCME', 'CUSTOM5', date_time=True)
        ymval, ymtimes = block.get('/MYM:XCBT', 'CUSTOM5', date_time=True)
        if esval == "1.0":
            print("ES LONG")
        elif esval == "0.0":
            print("ES SHORT")
    # tosdb.clean_up()

if __name__ == '__main__':
    # # tosDBohlc()

    # while True:
    #     # print(getLastPrice('/ES:XCME'))
    #     data, times = block.get('/ES:XCME', 'LAST', date_time=True)
    #     print(data, times)
    #     time.sleep(.5)

    tosStudyData()