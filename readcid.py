#! /usr/bin/env python
# -*- coding: utf-8 -*-
# 2013-11-08 (Y-m-d)
# apt-get install pcscd python-pyscard

from smartcard.System import readers
from smartcard.CardRequest import CardRequest
from smartcard.Exceptions import SmartcardException,NoCardException, CardRequestTimeoutException,CardConnectionException
from smartcard.System import readers
import binascii
import webbrowser
import md5
import sys
import time
import base64
from base64 import decodestring
import pygame
import RPi.GPIO as GPIO

import sys
import requests

reload(sys)  
sys.setdefaultencoding('utf8')
# Thailand ID Smartcard
# define the APDUs used in this script

# Reset
SELECT = [0x00, 0xA4, 0x04, 0x00, 0x08, 0xA0, 0x00, 0x00, 0x00, 0x54, 0x48, 0x00, 0x01]

# CID
COMMAND1 = [0x80, 0xb0, 0x00, 0x04, 0x02, 0x00, 0x0d]
COMMAND2 = [0x00, 0xc0, 0x00, 0x00, 0x0d]

# Fullname Thai + Eng + BirthDate + Sex
COMMAND3 = [0x80, 0xb0, 0x00, 0x11, 0x02, 0x00, 0xd1]
COMMAND4 = [0x00, 0xc0, 0x00, 0x00, 0xd1]

# Address
COMMAND5 = [0x80, 0xb0, 0x15, 0x79, 0x02, 0x00, 0x64]
COMMAND6 = [0x00, 0xc0, 0x00, 0x00, 0x64]

# issue/expire
COMMAND7 = [0x80, 0xb0, 0x01, 0x67, 0x02, 0x00, 0x12]
COMMAND8 = [0x00, 0xc0, 0x00, 0x00, 0x12]

# readimage
COMMANDi01 = [ 0x80, 0xb0, 0x01, 0x01, 0x02, 0x00, 0x64]
COMMANDi02   = [0x00, 0xc0, 0x00, 0x00, 0x64 ]

COMMAND9 = [ 0x80, 0xb0, 0x01, 0x01, 0x02, 0x00, 0x64]
COMMAND10   = [0x00, 0xc0, 0x00, 0x00, 0x64 ]

ICOMMAND1 = [0x80,0xB0	,0x01,0x7B,0x02,0x00,0xFF]
IRCOMMAND = [0x00, 0xc0, 0x00, 0x00, 0xFF]

ICOMMAND2 = [0x80,0xB0,0x02,0x7A,0x02,0x00,0xFF]


ICOMMAND3 = [0x80,0xB0,0x03,0x79,0x02,0x00,0xFF]


ICOMMAND4 = [0x80,0xB0,0x04,0x78,0x02,0x00,0xFF]


ICOMMAND5 = [0x80,0xB0,0x05,0x77,0x02,0x00,0xFF]



ICOMMAND6 = [0x80,0xB0,0x06,0x76,0x02,0x00,0xFF]


ICOMMAND7 = [0x80,0xB0,0x07,0x75,0x02,0x00,0xFF]


ICOMMAND8 = [0x80,0xB0,0x08,0x74,0x02,0x00,0xFF]

ICOMMAND9 = [0x80,0xB0,0x09,0x73,0x02,0x00,0xFF]
ICOMMAND10 = [0x80,0xB0,0x0A,0x72,0x02,0x00,0xFF]
ICOMMAND11 = [	0x80	,0xB0	,0x0B	,0x71	,0x02	,0x00	,0xFF]
ICOMMAND12 = [	0x80	,0xB0	,0x0C	,0x70	,0x02	,0x00	,0xFF]
ICOMMAND13 = [0x80	,0xB0	,0x0D	,0x6F	,0x02	,0x00	,0xFF]
ICOMMAND14 = [	0x80	,0xB0	,0x0E	,0x6E	,0x02	,0x00	,0xFF]
ICOMMAND15 = [0x80	,0xB0	,0x0F	,0x6D	,0x02	,0x00	,0xFF]
ICOMMAND16 = [	0x80	,0xB0	,0x10	,0x6C	,0x02	,0x00	,0xFF]
ICOMMAND17 = [0x80	,0xB0	,0x11	,0x6B	,0x02	,0x00	,0xFF]
ICOMMAND18 = [	0x80	,0xB0	,0x12	,0x6A	,0x02	,0x00	,0xFF]
ICOMMAND19 = [0x80	,0xB0	,0x13	,0x69	,0x02	,0x00	,0xFF]
ICOMMAND20 = [0x80	,0xB0	,0x14	,0x68	,0x02	,0x00	,0xFF]


url="http://localhost:1880/start"

# get all the available readers
n=0
#while True:
for x in range (0,2):
    try :
        r = readers()
        reader = r[0]
        connection = reader.createConnection()
        connection.connect()
        # Reset
        data, sw1, sw2 = connection.transmit(SELECT)
        #print data
        #print "Select Applet: %02X %02X" % (sw1, sw2)

        data, sw1, sw2 = connection.transmit(COMMAND1)
        #print "Command1: %02X %02X" % (sw1, sw2)

        # CID
        data, sw1, sw2 = connection.transmit(COMMAND2)
        #print data
        cidNew = ""
        name=""
        for d in data:
            cidNew+=chr(d)
        print ("cid : " + cidNew)
        #print cid
        data, sw1, sw2 = connection.transmit(COMMAND3)
        data, sw1, sw2 = connection.transmit(COMMAND4)
        for d in data:
                #name += unicode(d,"tis-620")
                #name += unicode(chr(d))
                name += chr(d)
       # print "test" +name
        name = name.replace("#", " ")       
        if cidNew != cid:
            m =md5.new()
            m.update(cidNew)
            ptlink = m.hexdigest()

        cid=cidNew
        address =""
        img = ""
        print ("read address")
        data, sw1, sw2 = connection.transmit(COMMAND5) 
        data, sw1, sw2 = connection.transmit(COMMAND6)
        for d in data:
                address+= chr(d)
               	#address += chr(d)
            
        print ("read image")
        data, sw1, sw2 = connection.transmit(ICOMMAND1) 
        data, sw1, sw2 = connection.transmit(IRCOMMAND)
	
        for d in data:
               	img += (chr(d))

        data, sw1, sw2 = connection.transmit(ICOMMAND2) 
        data, sw1, sw2 = connection.transmit(IRCOMMAND)
	
        for d in data:
               	img += (chr(d))
     
        data, sw1, sw2 = connection.transmit(ICOMMAND3) 
        data, sw1, sw2 = connection.transmit(IRCOMMAND)
	
        for d in data:
                #name += unicode(d,"tis-620")
                #name += unicode(chr(d))
               	img += (chr(d))

        data, sw1, sw2 = connection.transmit(ICOMMAND4) 
        data, sw1, sw2 = connection.transmit(IRCOMMAND)
	
        for d in data:
                #name += unicode(d,"tis-620")
                #name += unicode(chr(d))
               	img += (chr(d))

        data, sw1, sw2 = connection.transmit(ICOMMAND5) 
        data, sw1, sw2 = connection.transmit(IRCOMMAND)
	
        for d in data:
                #name += unicode(d,"tis-620")
                #name += unicode(chr(d))
               	img += (chr(d))

        data, sw1, sw2 = connection.transmit(ICOMMAND6) 
        data, sw1, sw2 = connection.transmit(IRCOMMAND)
	
        for d in data:
                #name += unicode(d,"tis-620")
                #name += unicode(chr(d))
               	img += (chr(d))

        data, sw1, sw2 = connection.transmit(ICOMMAND7) 
        data, sw1, sw2 = connection.transmit(IRCOMMAND)
	
        for d in data:
                #name += unicode(d,"tis-620")
                #name += unicode(chr(d))
               	img += (chr(d))

        data, sw1, sw2 = connection.transmit(ICOMMAND8) 
        data, sw1, sw2 = connection.transmit(IRCOMMAND)
	
        for d in data:
                #name += unicode(d,"tis-620")
                #name += unicode(chr(d))
               	img += (chr(d))

        data, sw1, sw2 = connection.transmit(ICOMMAND9) 
        data, sw1, sw2 = connection.transmit(IRCOMMAND)
	
        for d in data:
                #name += unicode(d,"tis-620")
                #name += unicode(chr(d))
               	img += (chr(d))


        data, sw1, sw2 = connection.transmit(ICOMMAND10) 
        data, sw1, sw2 = connection.transmit(IRCOMMAND)
	
        for d in data:
                #name += unicode(d,"tis-620")
                #name += unicode(chr(d))
               	img += (chr(d))

        data, sw1, sw2 = connection.transmit(ICOMMAND11) 
        data, sw1, sw2 = connection.transmit(IRCOMMAND)
	
        for d in data:
                #name += unicode(d,"tis-620")
                #name += unicode(chr(d))
               	img += (chr(d))

        data, sw1, sw2 = connection.transmit(ICOMMAND12) 
        data, sw1, sw2 = connection.transmit(IRCOMMAND)
	
        for d in data:
                #name += unicode(d,"tis-620")
                #name += unicode(chr(d))
               	img += (chr(d))

        data, sw1, sw2 = connection.transmit(ICOMMAND13) 
        data, sw1, sw2 = connection.transmit(IRCOMMAND)
	
        for d in data:
                #name += unicode(d,"tis-620")
                #name += unicode(chr(d))
               	img += (chr(d))



        data, sw1, sw2 = connection.transmit(ICOMMAND14) 
        data, sw1, sw2 = connection.transmit(IRCOMMAND)
	
        for d in data:
                #name += unicode(d,"tis-620")
                #name += unicode(chr(d))
               	img += (chr(d))

        data, sw1, sw2 = connection.transmit(ICOMMAND15) 
        data, sw1, sw2 = connection.transmit(IRCOMMAND)
	
        for d in data:
                #name += unicode(d,"tis-620")
                #name += unicode(chr(d))
               	img += (chr(d))

        data, sw1, sw2 = connection.transmit(ICOMMAND16) 
        data, sw1, sw2 = connection.transmit(IRCOMMAND)
	
        for d in data:
                #name += unicode(d,"tis-620")
                #name += unicode(chr(d))
               	img += (chr(d))

        data, sw1, sw2 = connection.transmit(ICOMMAND17) 
        data, sw1, sw2 = connection.transmit(IRCOMMAND)
	
        for d in data:
                #name += unicode(d,"tis-620")
                #name += unicode(chr(d))
               	img += (chr(d))

        data, sw1, sw2 = connection.transmit(ICOMMAND18) 
        data, sw1, sw2 = connection.transmit(IRCOMMAND)

        for d in data:
                #name += unicode(d,"tis-620")
                #name += unicode(chr(d))
               	img += (chr(d))

        data, sw1, sw2 = connection.transmit(ICOMMAND19) 
        data, sw1, sw2 = connection.transmit(IRCOMMAND)
	
        for d in data:
                #name += unicode(d,"tis-620")
                #name += unicode(chr(d))
               	img += (chr(d))


        data, sw1, sw2 = connection.transmit(ICOMMAND20) 
        data, sw1, sw2 = connection.transmit(IRCOMMAND)
	
        for d in data:
                #name += unicode(d,"tis-620")
                #name += unicode(chr(d))
               	img += (chr(d))

        eImg =  base64.b64encode(img)
        str = unicode(address,"tis-620")
        dname = unicode(name,"tis-620")
        pdata = "{" + "'cid' :  '" + cid+"' , 'name_th': '" +dname[0:100]+"' "+ " ,'name_en' : '" +dname[100:200]+"' "+ ",'birthdate' : '"+dname[len(dname)-9:len(dname)-1]+"' "+",'sex' : " +dname[len(dname)-1]+" ',address' : '"+str + "'}"
        fh = open(cid+".jpg","wb")
        fh.write(decodestring(eImg))
        fh.close()
        fht = open(cid+".json","wb")
        fht.write(pdata)
        fht.close()


    except (RuntimeError, TypeError, NameError,SmartcardException):
        cid = '-'
	
    time.sleep(1)

    requests.get(url);
