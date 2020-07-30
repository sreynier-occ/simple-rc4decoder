#!/usr/bin/python
# -*- coding: utf8 -*-
from base64 import b64decode, b32decode
import sys

#======================================================================================================
#											HELPERS FUNCTIONS
#======================================================================================================

#------------------------------------------------------------------------
# Class providing RC4 encryption/decryption functions
#------------------------------------------------------------------------
class RC4:
	def __init__(self, key = None):
		self.state = range(256) # initialisation de la table de permutation
		self.x = self.y = 0 # les index x et y, au lieu de i et j

		if key is not None:
			self.key = key
			self.init(key)

	# Key schedule
	def init(self, key):
		for i in range(256):
			self.x = (ord(key[i % len(key)]) + self.state[i] + self.x) & 0xFF
			self.state[i], self.state[self.x] = self.state[self.x], self.state[i]
		self.x = 0

	# Decrypt binary input data
	def binaryDecrypt(self, data):
		output = [None]*len(data)
		for i in xrange(len(data)):
			self.x = (self.x + 1) & 0xFF
			self.y = (self.state[self.x] + self.y) & 0xFF
			self.state[self.x], self.state[self.y] = self.state[self.y], self.state[self.x]
			output[i] = (data[i] ^ self.state[(self.state[self.x] + self.state[self.y]) & 0xFF])
		return bytearray(output)
		
#------------------------------------------------------------------------
def fromBase64URL(msg):
	msg = msg.replace('_','/').replace('-','+')
	if len(msg)%4 == 3:
		return b64decode(msg + '=')
	elif len(msg)%4 == 2:
		return b64decode(msg + '==')
	else:
		return b64decode(msg)

if __name__ == '__main__':
			
    key = 'ix2h668oCQlscJDzzdJv'
    fileData = ''        
    fileData += 'bkUoq-i0CUwVGTzyh-C0AZ7L_-9scX6YMcVFJE5s9IdTdIOY-HyW5GEtV7xs4wV.ejDQVIe068oXR23G-TdgYdyaMcXIoMIJtyh48uRk6of4Sgr-RMTjPLZUmQb2i6r.3VcZv0TnR4ISDSaMZm7I-139UIaoMeTz8iFb-t2CFcnMFTimM2KYOieqGAETz2Y.q-dy1XyHiitSUoTgn3DGnNQBDULzigr'.replace('.','')
    fileData += 'C1MWUJ-6nTmGnBeBziCeQI1Xw0rFFp05ATKoBbTb1VhN6-vd59AYLWuLlBki4nX.Q0wDa'.replace('.','')

    rc4Decryptor = RC4(key)

    outputFileName = "output.zip"
    useBase32 = False
    with open(outputFileName, 'wb+') as fileHandle:
        fileHandle.write(rc4Decryptor.binaryDecrypt(bytearray(fromBase64URL(fileData))))
        fileHandle.close()

				

