# steganography
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from math import ceil
from codec import Codec, CaesarCypher, HuffmanCodes

class Steganography():
    
    def __init__(self):
        self.text = ''
        self.binary = ''
        self.delimiter = '#'
        self.codec = None

    def encode(self, filein, fileout, message, codec):
        image = cv2.imread(filein)
        #print(image) # for debugging
        
        # calculate available bytes
        max_bytes = image.shape[0] * image.shape[1] * 3 // 8
        print("Maximum bytes available:", max_bytes)

        # convert into binary
        if codec == 'binary':
            self.codec = Codec() 
        elif codec == 'caesar':
            self.codec = CaesarCypher()
        elif codec == 'huffman':
            self.codec = HuffmanCodes()
        binary = self.codec.encode(message+self.delimiter)
        
        # check if possible to encode the message
        num_bytes = ceil(len(binary)//8) + 1 
        if  num_bytes > max_bytes:
            print("Error: Insufficient bytes!")
        else:
            print("Bytes to encode:", num_bytes) 
            self.text = message + self.delimiter
            self.binary = binary

            remaining_binary = self.binary
            for i in range(0,len(image)): #image height
                for j in range (0,len(image[0])): #image width
                    for k in range (0,3): # RGB values
                        bit = 0
                        if len(remaining_binary) != 0: #iterate through all the binary we want to insert into the image data, and change RGB values to odd or even
                            bit = remaining_binary[0]
                            if image[i,j,k] != 255:
                                image[i,j,k] += (image [i,j,k] + int(bit)) %2
                            else:
                                image[i,j,k] -= (image [i,j,k] + int(bit)) %2
                        remaining_binary = remaining_binary[1:]
            cv2.imwrite(fileout, image)
                   
    def decode(self, filein, codec):
        image = cv2.imread(filein)
        #print(image) # for debugging
        flag = True
        
        # convert into text
        if codec == 'binary':
            self.codec = Codec() 
        elif codec == 'caesar':
            self.codec = CaesarCypher()
        elif codec == 'huffman':
            if self.codec == None or self.codec.name != 'huffman':
                print("A Huffman tree is not set!")
                flag = False
        if flag:
            binary_data = ''
            for i in range(0,len(image)): #image height
                for j in range (0,len(image[0])): #image width
                    for k in range (0,3): #RGB
                        binary_data += str(image [i,j,k] % 2) #extract the binary data using modulus
            # update the data attributes:
            self.text = self.codec.decode(binary_data) # decode the binary data from image
            self.binary = self.codec.encode(self.text+self.delimiter)             
        
    def print(self):
        if self.text == '':
            print("The message is not set.")
        else:
            print("Text message:", self.text)
            print("Binary message:", self.binary)          

    def show(self, filename):
        plt.imshow(mpimg.imread(filename))
        plt.show()

if __name__ == '__main__': #tester
    codec = Codec()
    print(codec.encode("hi#"), 'hi#')
    remaining_binary = codec.encode("hi#")
    image = cv2.imread('a.png')
    encoded_image = image

    for i in range(0,len(image)): #image height
        for j in range (0,len(image[0])): #image width
            for k in range (0,3):
                bit = 0
                if len(remaining_binary) != 0:
                    bit = remaining_binary[0]
                print(bit,end='')
                remaining_binary = remaining_binary[1:]
    print('hi# bits')

    remaining_binary = codec.encode("hi#")
    for i in range(0,len(image)): #image height
        for j in range (0,len(image[0])): #image width
            for k in range (0,3):
                bit = 0
                if len(remaining_binary) != 0:
                    bit = remaining_binary[0]
                    #print ((image [i,j,k] + int(bit)) %2, end = '')
                    image[i,j,k] += (image [i,j,k] + int(bit)) %2
                remaining_binary = remaining_binary[1:]
    print('')

    binary = ''
    for i in range(0,len(image)): #image height
        for j in range (0,len(image[0])): #image width
            for k in range (0,3):
                binary += str(image [i,j,k] % 2)
    print (binary)
    print("-----")
   # print(image)
    codec = Codec()
