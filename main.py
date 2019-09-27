import tosdb
import time

tosdb.init(dllpath= r"C:\TOSDataBridge\bin\Release\x64\tos-databridge-0.9-x64.dll")

# Bool value to check if its connected: True
# print(tosdb.connected())

# Bool value to check if the engine is connected
# print(tosdb.connection_state()== tosdb.CONN_ENGINE_TOS)

block = tosdb.TOSDB_DataBlock(100000, True)

block.add_items('/ES:XCME')
block.add_topics('bid', 'ask', 'volume')

### NOTICE WE ARE SLEEPING TO ALLOW DATA TO GET INTO BLOCK ###
print("sleeping for 1.5 seconds")
time.sleep(1.5)

# ['ASK', 'BID', 'VOLUME']
# print(block.topics())

print(block.get('/ES:XCME', 'ask'))
time.sleep(.1)

# tosdb.clean_up()

if __name__ == '__main__':
    pass