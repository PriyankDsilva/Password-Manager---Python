import os,configparser,pandas as pd,math,time,sys

#Encryption
def encryptMessage(key, message):
    ciphertext = [''] * key

    for col in range(key):
        pointer = col

        while pointer < len(message):
            ciphertext[col] += message[pointer]
            pointer += key

    return ''.join(ciphertext)

#Decryption
def decryptMessage(key, message):

    numOfColumns = math.ceil(len(message) / key)
    numOfRows = key
    numOfShadedBoxes = (numOfColumns * numOfRows) - len(message)
    plaintext = [''] * numOfColumns

    col = 0
    row = 0

    for symbol in message:
        plaintext[col] += symbol
        col += 1 

        if (col == numOfColumns) or (col == numOfColumns - 1 and row >= numOfRows - numOfShadedBoxes):
            col = 0
            row += 1

    return ''.join(plaintext)

#Cipher File
def Cipher(FileName,Mode):

    myKey = 10
    myMode = Mode # set to 'encrypt' or 'decrypt'

    # If the input file does not exist, then the program terminates early.
    if not os.path.exists(FileName):
        print('The file %s does not exist. Quitting...' % (FileName))
        sys.exit()

    fileObj = open(FileName)
    content = fileObj.read()
    fileObj.close()

    startTime = time.time()
    if myMode == 'encrypt':
        translated = encryptMessage(myKey, content)
    elif myMode == 'decrypt':
        translated = decryptMessage(myKey, content)
    totalTime = round(time.time() - startTime, 2)

    outputFileObj = open(FileName, 'w')
    outputFileObj.write(translated)
    outputFileObj.close()


Cipher('AccountDetails.csv','decrypt')
Cipher('PasswordDetails.csv','decrypt')

#'encrypt' or 'decrypt'