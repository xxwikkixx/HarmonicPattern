import tosdb
import time
from tosdb.intervalize import ohlc
from timeit import default_timer

def tosDB():
    tosdb.init(dllpath=r"C:\TOSDataBridge\bin\Release\x64\tos-databridge-0.9-x64.dll")
    # Bool value to check if its connected: True
    # print(tosdb.connected())

    # Bool value to check if the engine is connected
    # print(tosdb.connection_state()== tosdb.CONN_ENGINE_TOS)

    block = tosdb.TOSDB_DataBlock(100000, True)

    block.add_items('/ES:XCME')
    block.add_topics('OPEN', 'HIGH', 'LOW', 'bid', 'ask', 'volume', 'LAST')

    ### NOTICE WE ARE SLEEPING TO ALLOW DATA TO GET INTO BLOCK ###
    print("sleeping for 1.5 seconds")
    time.sleep(1.5)

    # ['ASK', 'BID', 'VOLUME']
    # print(block.topics())

    while True:
        print(block.get('/ES:XCME', 'LAST'))
        time.sleep(.5)
    # tosdb.clean_up()


def tosDBohlc():
    block = ohlc.tosdb.TOSDB_ThreadSafeDataBlock(10000)
    intrv = ohlc.TOSDB_OpenHighLowCloseIntervals(block, 60)
    intrv.add_items('/ES:XCME')
    intrv.add_topics('OPEN', 'HIGH', 'LOW')
    print(intrv.get('/ES:XCME', 'OPEN'))

    tosdb.clean_up()


def test():
    buffer = []
    block = tosdb.TOSDB_DataBlock(10000, True)
    block.add_items('/ES:XCME')
    block.add_topics('LASTX', 'BIDX', 'ASKX', 'LAST_SIZE')
    time.sleep(3)  # allow block time to load the cache
    buffer.append(block.get('/ES:XCME', 'BIDX', date_time=True,
                            indx=0))  # update marker
    time.sleep(5)  # wait perhaps for transactions to occur
    timer = 0
    while (timer < 5):  # get transactions for 5 seconds
        data = block.get('/ES:XCME', 'BIDX', date_time=True) # this works
        # data = block.stream_snapshot_from_marker('/ES:XCME', 'BIDX', date_time=True, beg=0)
        print(data)  # => prints None
        buffer.append(data)
        timer = default_timer()
    tosdb.clean_up()
    print(buffer)

if __name__ == '__main__':
    tosDB()