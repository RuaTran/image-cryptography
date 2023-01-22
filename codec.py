# codecs
import numpy as np

class Codec():
    
    def __init__(self):
        self.name = 'binary'
        self.delimiter = '00100011' # a hash symbol '#' 

    # convert text or numbers into binary form    
    def encode(self, text):
        if type(text) == str:
            return ''.join([format(ord(i), "08b") for i in text])
        else:
            print('Format error')

    # convert binary data into text
    def decode(self, data):
        binary = []        
        for i in range(0,len(data),8):
            byte = data[i: i+8]
            if byte == self.delimiter:
                break
            binary.append(byte)
        text = ''
        for byte in binary:
            text += chr(int(byte,2))
            #print (byte,2)
        return text 

class CaesarCypher(Codec):

    def __init__(self, shift=3):
        self.name = 'caesar'
        self.delimiter = '#'  # set up it to a corresponding binary code
        self.shift = shift    
        self.chars = 256      # total number of characters

    # convert text into binary form, shifted
    def encode(self, text):
        data = ''
        if type(text) == str:
            data += (''.join([format((ord(i)+self.shift)%self.chars, "08b") for i in text])) #encode shifted binary data, wrapping around to only permit valid characters
        else:
            print('Format error')
        return data
    
    # convert binary data into text
    def decode(self, data):
        text = ''
        binary = []        
        for i in range(0,len(data),8):
            byte = data[i: i+8]
            decoded_char = (ord(chr(int(byte,2)))-self.shift)%self.chars #decode the encoded byte data, shifting it back to it's orignal character
            decoded_byte = format(decoded_char,"08b") #formats the character back into bytes
            if decoded_byte == format(ord(self.delimiter),"08b"): #checks if the upcoming byte is the delimiter and stops if that is the case
                break
            binary.append(decoded_byte) #put the byte data into a variable to be converted to text
        text = ''
        for byte in binary:
            text += chr(int(byte,2)) #convert to text using the binary data from function variable
        return text

# a helper class used for class HuffmanCodes that implements a Huffman tree
class Node:
    def __init__(self, freq, symbol, left=None, right=None):
        self.left = left
        self.right = right
        self.freq = freq
        self.symbol = symbol
        self.code = ''
        
class HuffmanCodes(Codec):
    
    def __init__(self):
        self.nodes = None
        self.name = 'huffman'
        self.delimiter = '#'  # set up it to a corresponding binary code
    # make a Huffman Tree    
    def make_tree(self, data):
        # make nodes
        nodes = []
        for char, freq in data.items():
            nodes.append(Node(freq, char))
        while len(nodes) > 1:
            # sort the current nodes by frequency
            nodes = sorted(nodes, key=lambda x: x.freq)
            # pick two nodes with the lowest frequencies
            left = nodes[0]
            right = nodes[1]

            # assign codes
            left.code = '0'
            right.code = '1'

            # combine the nodes into a tree
            root = Node(left.freq+right.freq, left.symbol+right.symbol,
                        left, right)

            # remove the two nodes and add their parent to the list of nodes
            nodes.remove(left)
            nodes.remove(right)
            nodes.append(root)
        return nodes

    # traverse a Huffman tree
    def traverse_tree(self, node, val):
        next_val = val + node.code
        if(node.left):
            self.traverse_tree(node.left, next_val)
        if(node.right):
            self.traverse_tree(node.right, next_val)
        if(not node.left and not node.right):
            print(f"{node.symbol}->{next_val}")

    # traverse the Huffman tree, generating and returning encoding codes
    def generate_code_dict(self, node, val = ''):
        codes = {}
        def helper(node, val = ''): #helper recursive method that allows the filling of dictionary
            next_val = val + node.code
            if(node.left):
                helper(node.left, next_val)
            if(node.right):
                helper(node.right, next_val)
            if(not node.left and not node.right):
                #print(f"{node.symbol}->{next_val}")
                codes[node.symbol] = next_val #instead of printing, put into a dictionary to be returned and used in encode
        helper(node)
        return codes
    
    # convert text into binary form
    def encode(self, text):
        data = ''

        char_dict = {i : text.count(i) for i in set(text)} #create a character frequency dictionary
        sorted_values = sorted (char_dict.values())
        sorted_dict = {}

        #generate a dictionary of characters in the message by frequency (least to greatest)
        for x in sorted_values:
            for y in char_dict.keys():
                if char_dict[y] == x:
                    sorted_dict[y] = char_dict[y]
        #create a huffman tree from the frequency dictionary and store as an object variable
        self.nodes = self.make_tree(sorted_dict)[0]
        #generate dictionary of huffman codes by recursively traversing the tree.
        code_dict = self.generate_code_dict(self.nodes)
        #generate binary encoded message based on previously generated code dictionary
        for i in text:
            data += code_dict.get(i)  
        return data

    # convert binary data into text
    def decode(self, data):
        text = ''
        target = ''
        while (len(data) != 0):
            target += data[0]
            #traverse huffman tree looking for leaf that is the same binary as target.
            current_node = self.nodes
            for i in target:
                if (i == '0' and current_node.left):
                    current_node = current_node.left
                if (i == '1' and current_node.right):
                    current_node = current_node.right
            if (not current_node.left and not current_node.right): #if at an endpoint
                if current_node.symbol == '#': #check for delimiter
                    return text #message is finished
                text+=current_node.symbol #add found character to 'text' return string
                target = ''
            data = data [1:]
        return text #message is finished

# driver program for codec classes
if __name__ == '__main__':
    text = 'hello'
    print('Original:', text)

    c = Codec()
    binary = c.encode(text)
    print('Binary:',binary)
    data = c.decode(binary)
    print('Text:',data)

    cc = CaesarCypher()
    binary = cc.encode(text)
    print('Binary:',binary)
    data = cc.decode(binary)
    print('Text:',data)

    h = HuffmanCodes()
    binary = h.encode(text)
    print('Binary:',binary)
    data = h.decode(binary)
    print('Text:',data)  

    print(h.generate_code_dict(h.nodes))
