from socket import *
import sys
import random
import pickle

# pack the data into a packet
# pack() take 3 integers typeint, seqnumint, lengthint, and 
#   a string datastr as input and returns a msg output as bytes
def pack(typeint, seqnumint, lengthint, datastr):
    packet = {
        "type": typeint,
        "seqnum": seqnumint,
        "length": lengthint,
        "data": datastr
    }

    msg = pickle.dumps(packet)
    return msg

# unpack data from a packet
# unpack() takes a byte message as input and returns 4 output
#   ptype, seqe, length as int and de_message as string
def unpack(message):
    data = pickle.loads(message)

    ptype = -1
    seqe = -1
    length = -1
    de_message = ""

    for key, value in data.items():
        if key == "type":
            ptype = value
        if key == "seqnum":
            seqe = value
        if key == "length":
            length = value
        if key == "data":
            de_message = value

    return ptype, seqe, length, de_message

# checkfiles() takes 3 strings of file name as input
#   and check if the first input file exists, as well
#   as making sure the rest two files are empty
def checkfiles(filename, arrival, drop):
    try:
        a = open(filename)
        a.close()
    except IOError:
        print(filename, " does not exist.")
        exit(0)
    
    arr_log = open(arrival,"w+")
    drp_log = open(drop,"w+")
    
    arr_log.close()
    drp_log.close()

# writeToLog() takes a fileName as input string, opens the file
#   and append the second input string into the file
def writeToLog(fileName, txt):
    openedFile = open(fileName, "a")
    openedFile.write(txt)
    openedFile.close()

# readFromFile() takes a filename (string) and an index (int)
#   as input, read from the file with filename at the given 
#   index, and read a random length of data.
#   The function returns sentencePart (string), start (int), 
#   randLen (int), packettype (string)
def readFromFile(filename, start):
    openedFile = open(filename)
    sentence = openedFile.read()
    sentenceLen = len(sentence)

    randLen = random.randint(10, 499)
    # randLen = 10
    sentencePart = sentence[start:start + randLen]
    
    openedFile.close()

    packettype = ""
    if (start + randLen > sentenceLen):
        packettype = "2"
    else:
        packettype = "1" 

    return sentencePart, start, randLen, packettype

def main():
    # takes commandline input
    host_addr = sys.argv[1]
    recver_port = int(sys.argv[2])
    sender_port = int(sys.argv[3])
    Set_timeout = float(sys.argv[4])  
    filename = sys.argv[5]

    # checks if the file with the given filename exists
    checkfiles(filename, "ack.log","seqnum.log")

    # for sending socket
    send_socket = socket(AF_INET, SOCK_DGRAM)

    # open recieve socket
    receive_socket = socket(AF_INET,SOCK_DGRAM)
    receive_socket.bind(('', sender_port))

    # send the port for the sender to the reciever
    # we tried to specify which port the sender should send from, but it not quite make it work
    # thus for letting the receiver know which port to send ACKs to, we decided to send this port prior to sending data
    send_socket.sendto(str(sender_port).encode(), (host_addr, recver_port))

    # bool for determine when to close
    done = False

    # the start index of read
    start = 0

    # the seqeunce of each packet
    sendSeq = 0

    while (not done):
        # read from given file
        sentencePart, start, randLen, Packettype = readFromFile(filename, start)

        # pack message and send
        msg = pack(int(Packettype), sendSeq, len(sentencePart), sentencePart)
        send_socket.sendto(msg, (host_addr, recver_port))

        # set receiver port timeout
        receive_socket.settimeout(Set_timeout)

        try:
            message, clientAddress = receive_socket.recvfrom(1024)
            ptype, seq, dataLen, de_message = unpack(message)
            
            if (ptype == 2):
                done = True
                break

            if (sendSeq + 1 != seq):
                continue
            else: 
                writeToLog("ack.log", str(seq)+"\n")
        except error: 
            continue
        
        start += randLen

        sendSeq += 1
    
    receive_socket.close()
    send_socket.close()

    print("success trans")

if __name__ == "__main__":
    main()
