
# class Packet:
    

#     def __init__(self, name, salary, yo, sup):
#         self.name = name
#         self.salary = salary
#     def displayEmployee(self):
#         print "Name : ", self.name,  ", Salary: ", self.salary


class Packet:

    def __init__(self, syn, ack, fin, packetNum, data):
		self.syn = syn;
		self.ack = ack;
		self.fin = fin;
		self.packetNum = packetNum;
		self.data = data;
		self.timeSent = -1;

    def description(self):
        print "------------------";
        print "--header:", self.syn, self.ack, self.fin, self.packetNum;
        print "--data:", self.data;
        print "--time sent:", self.timeSent;
        print "------------------";


    def getPacketType(self):
    	packetType = '';
    	if self.syn and self.ack:
    		#print "--synack--"
    		packetType = 'synack';
    	elif self.fin and self.ack:
    		#print "--finack--"
    		packetType = 'finack';
    	elif self.ack:
    		#print "--ack--"
    		packetType = 'ack';
    	elif self.syn:
    		#print "--syn--"
    		packetType = 'syn';
    	elif self.fin:
			#print "--fin--"
			packetType = 'fin';
    	return packetType;

    def getHeader(self):
    	return str(self.syn) + str(self.ack) + str(self.fin) + str(self.packetNum);

    def getData(self):
    	return str(self.data);

    def getPacketNumber(self):
    	return int(self.packetNum);

    def getTimeSent(self):
    	return self.timeSent;

    def getSyn(self):
    	return self.syn;

    def getAck(self):
    	return self.ack;

    def getFin(self):
    	return self.fin;

    def setTimeSent(self, time):
    	print "new packet time, ", time;
    	self.timeSent = time;

    def setAck(self, ack):
    	self.ack = ack;

    def setSyn(self, syn):
    	self.syn = syn;

    def setFin(self, fin):
    	self.fin = fin;

    def setPacketNumber(self, num):
    	self.packetNum = num;

    def setData(self, data):
    	self.data = data;

    	

