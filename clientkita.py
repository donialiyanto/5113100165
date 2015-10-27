import sys,socket,select,time,string
 
def clientkita():

	
    # Membuat TCP/IP socket
	create = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     	server = ('localhost',9090)
	create.connect(server)

	print 'Tersambung,Silahkan Login untuk Melakukan chat'
	print '\n------------------------------------------------------------------'	
	sys.stdout.write('--> '); 
	sys.stdout.flush()
     
	while 1:
		sock_list = [sys.stdin, create]
		 
		# Mendapatkan List Sicket yang sudah ada dengan Array
		read,write,in_error = select.select(sock_list , [], [])
		 
		for sock in read:      
		
			if sock == create:
				# pesan yang masuk ke remote server
				get_data = sock.recv(4096)
				if not get_data:
					print '\n Maaf,jaringan terputus'
					sys.exit()
				else :
					#print data
					sys.stdout.write(get_data)
					sys.stdout.write('>> '); sys.stdout.flush()     
			
			else :
				# user Mengetik pesan
				create_message = []
				message = sys.stdin.readline()
				messages = message.split()
				
				d=len(messages)
				if messages[0]=="login" :
						create.send(message)
						
				elif messages[0]=="sendto" :
						create.send(message)

				elif messages[0]=="sendall" :
						create.send(message)
		
				elif messages[0]=="list" :
						create.send(message)		
				else:
					print ('Invalid syntax')
				
				#s.send(message)
				sys.stdout.write('-->'); sys.stdout.flush() 


clientkita()

