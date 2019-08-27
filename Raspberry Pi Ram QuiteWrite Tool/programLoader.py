import RPi.GPIO as G
import time
import binascii
from ctypes import c_ubyte

G.setmode(G.BCM)
G.setwarnings(True)

aO = 19
aC = 26

dO = 20
dC = 21
dOE = 5

fB = 16
gL = 13
wL = 6

d0 = 22
d1 = 27
d2 = 17
d3 = 12
d4 = 25
d5 = 24
d6 = 23
d7 = 18

G.setup(aO, G.OUT)
G.setup(aC, G.OUT)

G.setup(dO, G.OUT)
G.setup(dC, G.OUT)
G.setup(dOE, G.OUT)

G.setup(fB, G.OUT)
G.setup(gL, G.OUT)
G.setup(wL, G.OUT)

G.setup(d0 , G.IN)
G.setup(d1 , G.IN)
G.setup(d2 , G.IN)
G.setup(d3 , G.IN)
G.setup(d4 , G.IN)
G.setup(d5 , G.IN)
G.setup(d6 , G.IN)
G.setup(d7 , G.IN)

G.output(fB, 0)
G.output(gL, 1)
G.output(wL, 1)

G.output(dOE, 0)
G.output(dC, 1)
G.output(aC, 1)

def sendAddress(binary, delayTime):
    for x in range(7, -1, -1):
        G.output(aO, int(binary[x], 10))
        time.sleep(delayTime)
        G.output(aC, 0)
        time.sleep(delayTime)
        G.output(aC, 1)
        time.sleep(delayTime)
    G.output(aC, 0)
    time.sleep(delayTime)
    G.output(aC, 1)

def sendData(binary, delayTime):
    G.output(dC, 1)
    time.sleep(delayTime)
    for x in range(0, 8):
        G.output(dO, int(binary[x], 10))
        time.sleep(delayTime)
        G.output(dC, 0) #go low to get data
        time.sleep(delayTime)
        G.output(dC, 1) #go high
        time.sleep(delayTime)
    G.output(dC, 0)
    time.sleep(delayTime)
    G.output(dC, 1)

def pulseWriteCommand(delayTime):
    G.output(wL, 0)
    time.sleep(delayTime)
    G.output(wL, 1)

def writeInstruction(data, delayTime):
    sendData(data, delayTime)
    G.output(fB, 1)
    time.sleep(delayTime)
    pulseWriteCommand(delayTime)

def writeMemoryLoc(data, delayTime):
    sendData(data, delayTime)
    G.output(fB, 0)
    time.sleep(delayTime)
    pulseWriteCommand(delayTime)

def nToBin(hex_num, bit_length):
    bin_string= bin(int(hex_num))[2:]
    #print(bin_string)
    length = len(bin_string)
    #print(length)
    for x in range(0, bit_length - length):
        bin_string = "0" + bin_string
    #print(bin_string)
    return bin_string

def writeByte(address, data1, data0):
    delayTime = 0.0001
    sendAddress(address, delayTime)
    writeInstruction(data1, delayTime)
    writeMemoryLoc(data0, delayTime)


def sendCommands(commands):
    for x in range (0, len(commands)):
        address = nToBin(x, 8)
        writeByte(address, commands[x][0], commands[x][1])

def clearCommands():
    for x in range (0, 256):
        address = nToBin(x, 8)
        writeByte(address, "00000000", "00000000")

def readByte():
    string = ""
    string = string + str(G.input(d7))
    string = string + str(G.input(d6))
    string = string + str(G.input(d5))
    string = string + str(G.input(d4))
    string = string + str(G.input(d3))
    string = string + str(G.input(d2))
    string = string + str(G.input(d1))
    string = string + str(G.input(d0))
    return string

def readRAM():
    G.output(dOE, 1)
    G.output(gL, 0)
    delayTime = 0.0001
    for x in range(0, 256):
        string = ""
        address = nToBin(x, 8)
        sendAddress(address, delayTime)
        time.sleep(delayTime)
        G.output(fB, 1)
        time.sleep(delayTime)
        string = string + readByte() + " "
        time.sleep(delayTime)
        G.output(fB, 0)
        time.sleep(delayTime)
        string = string + readByte()
        print(string)
        time.sleep(delayTime)
    G.output(dOE, 0)
    G.output(gL, 1) 

NOP = "00000000"
LDA = "00010000"
ADD = "00100000"
SUB = "00110000"
STA = "01000000"
LDI = "01010000"
JMP = "01100000"
JZ  = "01110000"
HLT = "11110000"

commands = [
    [LDA , nToBin(2, 8)],
    [JMP , nToBin(3, 8)],
    ["11111111" , "11111111"],
    [NOP , nToBin(0, 8)],
    [NOP , nToBin(0, 8)],
    [NOP , nToBin(0, 8)],
    [NOP , nToBin(0, 8)],
    [NOP , nToBin(0, 8)],
    [NOP , nToBin(0, 8)],
    [NOP , nToBin(0, 8)],
    [NOP , nToBin(0, 8)],
    [NOP , nToBin(0, 8)],
    [NOP , nToBin(0, 8)],
    [NOP , nToBin(0, 8)],
    [NOP , nToBin(0, 8)],
    [NOP , nToBin(0, 8)]
    ]
    

#sendCommands(commands)
#clearCommands()
sendCommands(commands)
readRAM()
        
