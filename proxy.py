#!usr/bin/python
             
    
                  #####################Part -1#####################

import socket, sys
from thread import *

try:
    listening_port = int(raw_input("Enter Listening Port Number:"))
except KeyboardInterrupt:
    print "\n[*] User requested an Interrupt..."
    print "[*]Application is exciting.."
    sys.exit()

max_conn = 5       #Max connection queues to hold
buffer_size = 4092 #Max socket buffer size

                  #####################Part -2#####################

def start():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #initiates the socket
	s.bind(("",listening_port)) # Bind socket for listen
	s.listen(max_conn)        #Start listening for incoming connections
	print "[*]Initializing sockets......done..!!"
	print "[*]Sockets are binded successfully"
	print("[*]Server started successfully[ %d ]\n" %(listening_port))
    except Exception, e:
        #This block gets executed if socket fails
	print "[*]Unable to initialize socket"
	sys.exit(2)
   
   
    while 1:
        try:
	    conn, addr = s.accept() #Accept Connection from Client browser
	    data = conn.recv(buffer_size) #Receives client data
	    start_new_thread(conn_string, (conn, data, addr)) #Start a thread
	    print "Hello...Print this"
	except KeyboardInterrupt:
	#This block gets executed if client socket fails
	    s.close()
	    print "\n[*]Proxy Server shutting down"
	    print "Have a cool day in this summer...Prof"
	    sys.exit(1)
    s.close()
                      #####################Part -3#####################


def conn_string(conn, data, addr):

    #Client browser address appears here
    try:
        first_line = data.split('\n')[0]
        url = first_line.split(' ')[1]
        http_pos = url.find("://") #Find the position of ://

        if (http_pos == -1):
            temp = url
        else:
            temp = url[(http_pos+3):]#get the rest of the url
        
        port_pos = temp.find(":") #Find the position of port if any
        webserver_pos = temp.find("/") #find the end of the web server

        if webserver_pos == -1:
            webserver_pos = len(temp)
        webserver = ""
        port = -1
        if (port_pos == -1 or webserver_pos < port_pos):
            port = 80
            webserver = temp[:webserver_pos]
        else:
            #specific port
            port = int((temp[(port_pos+1):])[:webserver_pos-port_pos-1])
            webserver = temp[:port_pos]

        proxy_server(webserver, port, conn,  addr, data)
    except Exception, e:
        pass



                      #####################Part -4#####################

def proxy_server(webserver, port, conn, data, addr):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((webserver, port))
	s.send(data)
	
	while 1:
	    #Read reply or data to form end web server
	    reply = s.recv(buffer_size)
		
	    if (len(reply) > 0):
		conn.send(reply)#Sends reply back to client
		#send Notification To proxy server [My application]
		
		dar = float(len(reply))
		dar = float(dar / 1024)
		dar = "%.3s" % (str(dar))
		dar = "%s KB" % (dar)
		#'Print a custom Message For Request Complete'
		print "[*]Request Done: %s => %s <=" (str(addr[0]),str(dar))
	    else:
		#Break connection if receiving data fails
		break
	    #Feel Free To Close Our Server Sockets
	    s.close()
    	    #Now close our client socket
	    conn.close()
    except socket.error, (value, message):
	    s.close()
	    conn.close()
	    sys.exit(1)

start()


















    



























    	
