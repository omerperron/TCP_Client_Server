
import sys
import time
import random
from socket import *


#get server name and port name from arguments
receiver_host_ip = str(sys.argv[1]);
receiver_port = int(sys.argv[2]);
file = sys.argv[3];
MWS = int(sys.argv[4])
MSS = int(sys.argv[5]);
PDrop = float(sys.argv[6]);
#timeout = int(sys.argv[7])

headerLen = 7;
def getHeader(packet):
   return packet[0:headerLen];

def getData(packet):
   return packet[headerLen:len(packet)];

def setHeader(syn, ack, fin, sequenceNum):
    seqPadding = ''
    ackPadding = ''
    if (sequenceNum - 10) < 0:
        seqPadding = '000'
    elif sequenceNum - 100 < 0:
        seqPadding = '00';
    elif sequenceNum - 1000 < 0:
        seqPadding = '0';
    elif sequenceNum - 10000 < 0:
        seqPadding = '';

    if ackNum - 10 < 0:
        ackPadding = '000';
    elif ackNum - 100 < 0:
        ackPadding = '00';
    elif ackNum - 1000 < 0:
        ackPadding = '0';
    elif ackNum - 10000 < 0:
        ackPadding = '';
    return str(syn) + str(ack) + str(fin) + seqPadding + str(sequenceNum); 

def PLD():
    x = random.random()
    if x < float(PDrop):
        return 1;
    else:
        return 0;


segments = '';
with open(file, 'r') as my_file:
	data = my_file.read()

count = 0;
frame = [];
while count < len(data):
    frame.append(data[count: count + MSS]);
    count += MSS;
print "frame: ", frame
for segment in frame:
    head = setHeader(0, 0, 0, )
    segments.append()



sentCount = 0;
lastSeq = 0;
syn = 1;
ack = 0;
fin = 0;
sequenceNum = 0;
ackNum = 0;

finAckRec = False;
connectionOpen = False;
synAckComplete = False;
finSent = False;
window = '';
sentList = ''
print "sending syn"

while True:
#for sequencee in range(10): 

   
    #send finish
    if sentCount >= len(frame) and finSent == False :
        #do fin stuff
        window = '';
        syn = 0;
        ack = 0;
        fin = 1;
        print "sending fin";
        finSent = True;
    

    if connectionOpen == True and sentCount < len(frame):
        toSend = MWS;
        if sentCount + MWS > len(frame):
            toSend = len(frame) - sentCount;
        window = frame[sentCount: sentCount + toSend];

        print "\nwindow:", window;

    sock = socket(AF_INET, SOCK_DGRAM) #set up socket
    #sock.settimeout(1) 
    start = time.time() #start time when packet sent

    if(PLD() == 1 and connectionOpen == True and fin != 0):
        print "packet dropped!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    else:
        if(connectionOpen == True and fin == 0):
            lastSeq = sequenceNum;
            for segment in window:
                headerStr = setHeader(syn, ack, fin, sequenceNum);
                sequenceNum += 1;
                print "sending segment:", segment
                sock.sendto(headerStr + segment, (receiver_host_ip, receiver_port)) #send packet to server name
        else:
            headerStr = setHeader(syn, ack, fin, sequenceNum);
            print "Sending: ", headerStr
            sock.sendto(headerStr, (receiver_host_ip, receiver_port)) #send packet to server name
            if syn == True:
                sequenceNum += 1;
    if(connectionOpen == False and synAckComplete == 1):
        connectionOpen = True;
        print "connection Open!"
        continue;
    if finAckRec and ack == 1:
        connectionOpen == False;
        print "connection closed!!!";
        break;

    try:

        serverData = sock.recvfrom(1024) #recieve data from socket
        packet = serverData[0]
        header = getHeader(packet)
        newData = getData(packet)
        print "\n--packet recieved----------"
        print "-- header:", header
        print "-- data:", newData
        print "-- size:", len(newData)
        print "-- ackNumber: ", header[3:8];

        if int(header[3:8]) == lastSeq and connectionOpen == True:
            sentCount += 1;
            print "ack return for", lastSeq;




        if int(header[0]) == int(header[1]) == 1: # syn ack
            syn = 0
            ack = 1
            fin = 0
            print "-- syn ack recieved. prepare to send0 ack"
            synAckComplete = True;
        elif int(header[1]) == int(header[2]) == 1: # fin and ack
            print "-- sending ack in response to fin"
            finAckRec = True;
            syn = 0;
            ack = 1;
            fin = 0;
        elif int(header[1]) == 1: #ack
           # if synAckComplete == True and connectionOpen == False:
           #    connectionOpen = True;
           #    print "-- connection open!"
            print "-- ack recieved!";
        print "----------------------------\n"
        finish = time.time()
    except timeout:
        "time out y'all"
