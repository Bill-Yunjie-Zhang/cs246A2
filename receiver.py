from copyreg import pickle
import sys
from socket import *
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
#   and make sure they are empty
def checkfiles(file, arrival, drop):
    file_open = open(file,"w+")
    arr_log = open(arrival,"w+")
    drp_log = open(drop,"w+")
    
    file_open.close()
    arr_log.close()
    drp_log.close()

# writeToLog() takes a fileName as input string, opens the file
#   and append the second input string into the file
def writeToLog(fileName, txt):
    openedFile = open(fileName, "a")
    openedFile.write(txt)
    openedFile.close()

def main():
    # takes commandline input
    recver_port = int(sys.argv[1])
    drop_prob = float(sys.argv[2])
    filename = sys.argv[3]

    # checks if the file with the given filename exists
    checkfiles(filename, "arrival.log","drop.log")

    # open recieve socket
    receive_socket = socket(AF_INET, SOCK_DGRAM)
    receive_socket.bind(('', recver_port))
    print("The receiver is ready to receive")

    # receives the port from sender
    message, clientAddress = receive_socket.recvfrom(2048)
    UDPport_seq = int(message.decode())

    recevieSeq = -1

    while True:
        # receives message from the sender and unpack
        message, clientAddress = receive_socket.recvfrom(1024)
        ptype, seqe, length, de_message = unpack(message)

        # set drop probability
        haveDropped = random.randint(0, 100) >= drop_prob * 100

        if (not haveDropped):
            writeToLog("drop.log", str(seqe) + "\n")
        else:
            # check if we have recieved the packet with given sequence
            if recevieSeq == seqe:
                continue
            else:
                recevieSeq = seqe
            
            # write to logs
            writeToLog("arrival.log", str(seqe) + "\n")
            writeToLog(filename, de_message)

            # new a socket
            seq_trans_socket = socket(AF_INET, SOCK_DGRAM)

            # if it's the last packet return EOT
            prtype = 0
            if ptype == 2:
                prtype = 2

            # pack message and send back
            msg = pack(prtype, seqe + 1, 0, "")
            seq_trans_socket.sendto(msg, (clientAddress[0], UDPport_seq))

            # close the socket
            seq_trans_socket.close()

            # if it's the last one close connection
            if prtype == 2:
                receive_socket.close()
                break

if __name__ == "__main__":
    main()
