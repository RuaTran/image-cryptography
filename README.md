
# Python Stenography Tool
Created as a class assignment in order to explore the process of cryptographically concealing a message within a file, be it image, audio, video, text, et cetera. This application allows the user to compress text using Huffman coding and hide the encrypted message and Huffman tree used to decrypt it within images using the 'least-significant-bit technique'.

An uncompressed image file with no alpha channel consists of an array of RGB values (i.e. one red pixel is [255, 0, 0]), and we can take advantage of this by slightly altering these values in order to hide bits. If we wanted to store '0 1 0' in the above example, we can use evens and odds to represent it by changing it to [254, 1, 0]

(even, odd, even = 0 1 0)

Thus the message is hidden, and it's impossible for the human eye to spot the difference, and even if it could, the fact that there is a hidden message would be difficult to ascertain as it is encryped as well! Can you tell the difference between the two pizzas?

![ye](https://user-images.githubusercontent.com/110074141/214980680-126f76a7-3e53-41fa-b39c-16da50f05376.png)


## Usage
Download the python files and run **cryptography .py**. This will run a command line python interface that will list multiple options. Also, the python **source code** is available for you to inspect and modify freely. **stenography .py** contains the functions 'encode' and 'decode' an image, and if you so wish, can be easily used to create an application that can batch process images as opposed to using **cryptography .py**.
``` Flags
	'Encode a message - E',
	'Decode a message - D',
	'Print a message - P',
	'Show an image - S',
	'Quit the program - Q']
```

## Contact
Please feel free to send a message to MunfMunf#9104 if you're looking at the code in an attempt to modify it or use bits of it to make your own project. I love learning, and I'm always happy to help people learn.

##### This project was created as a class assignment at UCSC
