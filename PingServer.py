import socket
import sys
import pickle
from allClasses.Packet import  Packet
    #toDrop = [0,1,2, 3, 4, 4, 11, 14, 21, 24, 26, packets[-1], packets[-2]]
    #00001111222233334444555555555555666666666666777777778888 result before dup
    #toDrop = [3]
finalData = ""
packets= [];
finAckSent = False;
connectionOpen = -1;
lastAcked = -1;

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 2000) # Bind the socket to the port
print "starting up", server_address[0], "on port", server_address[1]
sock.bind(server_address)

while True:
    print 'waiting to receive message'
    data, address = sock.recvfrom(4096) #data, address
    receivedPacket = pickle.loads(data);

    header = receivedPacket.getHeader()
    newData = receivedPacket.getData()
    print "\n--message recieved----------"
    print "-- header: ", header;
    print "-- data: ", newData;
    

    toSend = Packet(0, 0, 0, 0, None);
    if receivedPacket.getPacketType() == 'syn' and connectionOpen == -1:
        print "setting syn and ack";
        connectionOpen = 0;
        toSend.setSyn(1);
        toSend.setAck(1);
    elif receivedPacket.getPacketType() == 'ack':
        if connectionOpen  == 0:
            print "ack received, oppening connection"
            connectionOpen = True;
            continue;
        elif finAckSent == True:
            txt = ''
            for curPacket in packets:
                txt += curPacket.getData();
            print "final:", txt
            print "connection terminated";
            break;
    elif receivedPacket.getPacketType() == 'fin':
        print "sending fin ack back";
        finAckSent = True;
        toSend = Packet(0, 1, 1, 0, None);
    elif newData != None and connectionOpen == 1:
        print "acked new data";

        #if packets is empty or received packets is the newest packet\
        # if any(x.getPacketNumber() == receivedPacket.getPacketNumber() for x in packets):
        #     "exists!!"
        # else:
        if len(packets) == 0 or receivedPacket.getPacketNumber() > packets[-1].getPacketNumber():
            print "added first packets/biggest" 
            packets.append(receivedPacket);
        else:
            #add in order
            for segment in packets:
                if receivedPacket.getPacketNumber() < segment.getPacketNumber():
                    print "inserting:", receivedPacket.getPacketNumber(), "before" ,segment.getPacketNumber()
                    packets.insert(packets.index(segment), receivedPacket);   
                    break; 

        print "--final data:--"
        toPrint = ''
        for segment in packets:
            toPrint += segment.getData();
        print toPrint;

        toSend.setAck(1);
        if lastAcked + 1 == receivedPacket.getPacketNumber(): #if correct packet received
            for curSegment in packets:
                if lastAcked +1 == curSegment.getPacketNumber():
                    print "incrementing last acked from:", lastAcked

                    lastAcked += 1;
                    print "last acked after incrementing:", lastAcked;

            toSend.setPacketNumber(lastAcked);

        elif receivedPacket.getPacketNumber() > lastAcked:
            print "Resent ack from:", receivedPacket.getPacketNumber();
            toSend.setData("Resent ack from:" + str(receivedPacket.getPacketNumber()))
            toSend.setPacketNumber(lastAcked); #resend ack


 
    if toSend:
        print "sending:";    
        toSend.description();
        objectString = pickle.dumps(toSend);
        sock.sendto(objectString, address)
    
        