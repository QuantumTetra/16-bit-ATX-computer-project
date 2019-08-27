import RPi.GPIO as G
import time
import binascii
from ctypes import c_ubyte

G.setmode(G.BCM)
G.setwarnings(True)

d0 = 21
d1 = 20
d2 = 16
d3 = 12
d4 = 25
d5 = 24
d6 = 23
d7 = 18



clock = 27
address_data = 17

we = 13
prom_oe = 19
ce = 26

G.setup(clock, G.OUT)
G.setup(address_data, G.OUT)
G.setup(we, G.OUT)
G.setup(prom_oe, G.OUT)
G.setup(ce, G.OUT)

G.output(we, G.HIGH)

G.setup(d0, G.OUT)
G.setup(d1, G.OUT)
G.setup(d2, G.OUT)
G.setup(d3, G.OUT)
G.setup(d4, G.OUT)
G.setup(d5, G.OUT)
G.setup(d6, G.OUT)
G.setup(d7, G.OUT)

def wait(time):
    time.sleep(float(time))

def data_setup(binary):
    G.output(d7, int(binary[0], 10))
    G.output(d6, int(binary[1], 10))
    G.output(d5, int(binary[2], 10))
    G.output(d4, int(binary[3], 10))
    G.output(d3, int(binary[4], 10))
    G.output(d2, int(binary[5], 10))
    G.output(d1, int(binary[6], 10))
    G.output(d0, int(binary[7], 10))

def address_setup(binary):
    for x in range(12, -1, -1):
        if(int(binary[x]) == 1):
            G.output(address_data, G.HIGH)
        time.sleep(0.00001)
        G.output(clock, G.HIGH)
        time.sleep(0.00001)
        G.output(clock, G.LOW)
        time.sleep(0.00001)
        G.output(address_data, G.LOW)
        

def write_data(address, data_in):
    data_IO_out()
    disable_prom_output()
    address_setup(address)
    data_setup(data_in)
    time.sleep(0.001)
    G.output(ce, G.LOW)
    time.sleep(0.001)
    G.output(we, G.LOW)
    time.sleep(0.001)
    G.output(we, G.HIGH)
    time.sleep(0.001)
    G.output(ce, G.HIGH)
    time.sleep(0.001)

def enable_prom_output():
    G.output(prom_oe, G.LOW)

def disable_prom_output():
    G.output(prom_oe, G.HIGH)

def enable_prom():
    G.output(ce, G.LOW)

def disable_prom():
    G.output(ce, G.HIGH)

def data_IO_in():
    G.setup(d0, G.IN)
    G.setup(d1, G.IN)
    G.setup(d2, G.IN)
    G.setup(d3, G.IN)
    G.setup(d4, G.IN)
    G.setup(d5, G.IN)
    G.setup(d6, G.IN)
    G.setup(d7, G.IN)

def data_IO_out():
    G.setup(d0, G.OUT)
    G.setup(d1, G.OUT)
    G.setup(d2, G.OUT)
    G.setup(d3, G.OUT)
    G.setup(d4, G.OUT)
    G.setup(d5, G.OUT)
    G.setup(d6, G.OUT)
    G.setup(d7, G.OUT)

def disp_prom(bit_depth, disp_time):
    enable_prom()
    enable_prom_output()
    data_IO_in()
    aa = list("0000000000000")
    address = "".join(aa)
    #print(address)
    is_byte_full = False
    string = ":"
    num = 0
    while(is_byte_full == False):
        address = "".join(aa)
        address_setup(address)
        time.sleep(float(disp_time))
        current_byte = read_bin(address)
        #add one to address
        last_overflowed = True
        mini = 12 - bit_depth
        string = string + " " + hex_to_binary_bufferer(int(current_byte, 16), 8)
        num+=1
        if(num == 8):
            num = 0
            print(string)
            string = ":"
        for x in range(12, mini, -1):
            if(last_overflowed):
                if(aa[x] == '0'):
                    last_overflowed = False
                    aa[x] = '1'
                else:
                    last_overflowed = True
                    aa[x] = '0'
                    if(x == mini + 1):
                        is_byte_full = True
    data_IO_out()
    disable_prom()
    disable_prom_output()
        
def clear_prom(bit_depth, byte_hex):
    byte = hex_to_binary_bufferer(byte_hex, 8)
    enable_prom()
    disable_prom_output()
    aa = list("0000000000000")
    address = "".join(aa)
    #print(address)
    is_byte_full = False
    while(is_byte_full == False):
        address = "".join(aa)
        write_data(address, byte)
        print(address)
        #add one to address
        last_overflowed = True
        #highest number should be 12 and min should be -1 for full data write
        mini = 12 - bit_depth
        for x in range(12, mini, -1):
            if(last_overflowed):
                if(aa[x] == '0'):
                    last_overflowed = False
                    aa[x] = '1'
                else:
                    last_overflowed = True
                    aa[x] = '0'
                    if(x == mini + 1):
                        is_byte_full = True

def hex_to_binary_bufferer(hex_num, bit_length):
    bin_string= bin(int(hex_num))[2:]
    #print(bin_string)
    length = len(bin_string)
    #print(length)
    for x in range(0, bit_length - length):
        bin_string = "0" + bin_string
    #print(bin_string)
    return bin_string

def write(address_hex, data_hex):
    address = hex_to_binary_bufferer(address_hex, 13)
    data_out = hex_to_binary_bufferer(data_hex, 8)
    write_data(address, data_out)

def read_bin(address):
    address_setup(address)
    data_int = 0
    enable_prom()
    enable_prom_output()
    time.sleep(0.0001)
    data_int = data_int + (1 * G.input(d0))
    data_int = data_int + (2 * G.input(d1))
    data_int = data_int + (4 * G.input(d2))
    data_int = data_int + (8 * G.input(d3))
    data_int = data_int + (16 * G.input(d4))
    data_int = data_int + (32 * G.input(d5))
    data_int = data_int + (64 * G.input(d6))
    data_int = data_int + (128 * G.input(d7))
    data_out = hex(data_int)
    disable_prom_output()
    return(data_out)

def read(address_hex):
    data_IO_in()
    address = hex_to_binary_bufferer(address_hex, 13)
    address_setup(address)
    data_int = 0
    enable_prom()
    enable_prom_output()
    time.sleep(0.0002)
    data_int = data_int + (1 * G.input(d0))
    data_int = data_int + (2 * G.input(d1))
    data_int = data_int + (4 * G.input(d2))
    data_int = data_int + (8 * G.input(d3))
    data_int = data_int + (16 * G.input(d4))
    data_int = data_int + (32 * G.input(d5))
    data_int = data_int + (64 * G.input(d6))
    data_int = data_int + (128 * G.input(d7))
    data_out = hex(data_int)
    print(data_out)
    disable_prom_output()
    data_IO_out()
    return(data_out)

#this is the actual program down here \/

#1 = 7seg, 2 = conditional control chip 1, 3 = conditional control chip 2
data_seg = [0x7e, 0x30, 0x6d, 0x79, 0x33, 0x5b, 0x5f, 0x70, 0x7f, 0x7b, 0x77, 0x1f, 0x4e, 0x3d, 0x4f, 0x47]
digits = [0x7e, 0x30, 0x6d, 0x79, 0x33, 0x5b, 0x5f, 0x70, 0x7f, 0x7b]
#print(data_seg)
#print(digits)
program_number = 1

#print(hex_to_binary_bufferer(0x100, 13))

address = 0x100
print(address)
val = c_ubyte(-128).value
print(val)
hex_val = hex(int(val))[2:]
print(hex_val)
address = address + val
print(address)

HLT = 0b000000010000000000000000 #PROM #1
MI  = 0b000000100000000000000000
RI  = 0b000001000000000000000000
RO  = 0b000010000000000000000000
IO  = 0b000100000000000000000000
II  = 0b001000000000000000000000
AI  = 0b010000000000000000000000
AO  = 0b100000000000000000000000

SO  = 0b000000000000000100000000 #PROM #2
SU  = 0b000000000000001000000000
BI  = 0b000000000000010000000000
BO  = 0b000000000000100000000000
CE  = 0b000000000001000000000000
CO  = 0b000000000010000000000000
J   = 0b000000000100000000000000
FI  = 0b000000001000000000000000

A0I = 0b000000000000000000000001 #PROM #3
A0O = 0b000000000000000000000010
B0I = 0b000000000000000000000100
S0O = 0b000000000000000000001000
MB  = 0b000000000000000000010000
PP  = 0b000000000000000000100000


NOP = [MI+CO+MB, RO+II+MB, RO+BI+CE, 0     , 0        , 0          , 0          , 0         ] #0000 - NOP
LDA = [MI+CO+MB, RO+II+MB, RO+BI+CE, MI+BO , RO+A0I   , RO+AI+MB   , 0          , 0         ] #0001 - LDA
ADD = [MI+CO+MB, RO+II+MB, RO+BI+CE, MI+BO , RO+B0I   , RO+BI+MB   , AI+SO+FI   , A0I+S0O   ] #0010 - ADD
SUB = [MI+CO+MB, RO+II+MB, RO+BI+CE, MI+BO , RO+SU+B0I, RO+SU+BI+MB, AI+SO+SU+FI, SU+A0I+S0O] #0011 - SUB
STA = [MI+CO+MB, RO+II+MB, RO+BI+CE, MI+BO , RI+A0O   , RI+AO+MB   , 0          , 0         ] #0100 - STA
LDI = [MI+CO+MB, RO+II+MB, RO+BI+CE, BO+A0I, AI       , 0          , 0          , 0         ] #0101 - LDI
JMP = [MI+CO+MB, RO+II+MB, RO+BI+CE, BO+J  , 0        , 0          , 0          , 0         ] #0110 - JMP
JZ  = [MI+CO+MB, RO+II+MB, RO+BI+CE, BO+J  , 0        , 0          , 0          , 0         ] #0111 - JZ
HLT = [MI+CO+MB, RO+II+MB, RO+BI+CE, HLT   , 0        , 0          , 0          , 0         ] #1111 - HLT


data_prom_JZ  = [
    NOP, #0000 - NOP
    LDA, #0001 - LDA
    ADD, #0010 - ADD
    SUB, #0011 - SUB
    STA, #0100 - STA
    LDI, #0101 - LDI
    JMP, #0110 - JMP
    JZ , #0111 - JZ
    NOP, #1000 - NOP
    NOP, #1001 - NOP
    NOP, #1010 - NOP
    NOP, #1011 - NOP
    NOP, #1100 - NOP
    NOP, #1101 - NOP
    NOP, #1110 - NOP
    HLT  #1111 - HLT
        ]

data_prom_NOP = [
    NOP, #0000 - NOP
    LDA, #0001 - LDA
    ADD, #0010 - ADD
    SUB, #0011 - SUB
    STA, #0100 - STA
    LDI, #0101 - LDI
    JMP, #0110 - JMP
    NOP, #0111 - JZ (NOP)
    NOP, #1000 - NOP
    NOP, #1001 - NOP
    NOP, #1010 - NOP
    NOP, #1011 - NOP
    NOP, #1100 - NOP
    NOP, #1101 - NOP
    NOP, #1110 - NOP
    HLT  #1111 - HLT
        ]
prom_id = 1

for iterator in range(0,4):
    if(True):
        data_IO_out()
        #clear_prom(9,0x0)
        #print(str(bin(MI + CO))[2:])
        G.output(we, G.HIGH)
        disable_prom()
        disable_prom_output()
        time.sleep(1)
        for i in range(0,4):
            for j in range(0, 16):
                for k in range(0,8):
                    address = "0000" + hex_to_binary_bufferer(i, 2) + hex_to_binary_bufferer(j, 4) + hex_to_binary_bufferer(k, 3)
                    if i % 2 == 0: number = (data_prom_NOP[j][k])
                    if i % 2 == 1: number = (data_prom_JZ[j][k])
                    data_out = 0
                    if prom_id == 1: data_out = hex_to_binary_bufferer(number, 24)[:8]
                    if prom_id == 2: data_out = hex_to_binary_bufferer(number, 24)[8:16]
                    if prom_id == 3: data_out = hex_to_binary_bufferer(number, 24)[16:]
                
                    print(address)
                    print(data_out)
                    write_data(address, data_out)
                    G.output(we, G.HIGH)
                    disable_prom()
                    disable_prom_output()

#clear_prom(9, 0x0)
disp_prom(9, 0.001)


G.output(we, G.HIGH)
#clear_prom(11, 0x1)

time.sleep(1)
G.output(we, G.HIGH)
G.output(prom_oe, G.HIGH)
G.output(ce, G.HIGH)
