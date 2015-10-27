
import sys,socket,select,string

Host = 'localhost' 
Socket_list = []
Username_list = []
Recv_buffer = 4000 


def serverkita():

	print "Selamat datang di Serverkita"
	
	#Membuat TCP/IP socket
	serverkita_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serverkita_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	# Menghubungkan socket
	serverkita_socket.bind(('localhost', 9090))
	serverkita_socket.listen(10)

	# Menambahkan Socket server ke Koneksi yang ada
	Socket_list.append(serverkita_socket)
	
	# Server terhubung dengan port
	print "Selamat Server anda aktif dengan port 9090 "

	while True:
		
		#asynchronous 
		read,write,in_error = select.select(Socket_list,[],[],0)
	  
		for sock in read:
			# ketika koneksi baru masuk,client masuk
			if sock == serverkita_socket: 
				sockfd, addr = serverkita_socket.accept()
				Socket_list.append(sockfd)
				print "Clientkita (%s, %s) terhubung" % addr
				 
				broadcast(serverkita_socket, sockfd, "Selamat [%s:%s] telah bergabung\n" % addr)
			 
			
			else:
				 
				try:
					# menerima data dari socket.
					data = sock.recv(Recv_buffer)
					
					if data:  
						tmp = string.split(data[:-1]) #untuk memisahkan setiap ada spasi
				
						d=len(tmp)
						if tmp[0]=="login" : 
							login(sock, str(tmp[1])) 
								
						elif tmp[0]=="sendto" :
							
							logged = 0 # tidak ada client yang masuk
							user = "" 
							for x in range (len(Username_list)):
								if Username_list[x]==sock:
									logged=1
									user=Username_list[x+1] 
							if logged==0:
								send_message(sock, "Silahkan login terlebih dahulu\n")
							
							else:
								tmp2=""
								for x in range (len(tmp)):
									if x>1:
										if not tmp2:
											tmp2+=str(tmp[x])
											
										else:
											tmp2+=" "
											tmp2+=str(tmp[x])
											
								
								for x in range (len(Username_list)):
									if Username_list[x]==tmp[1]:
										send_message(Username_list[x-1], "["+user+"] : "+tmp2+"\n")
						
								
						elif tmp[0]=="sendall" :
							
							logged = 0
							user = ""
							for x in range (len(Username_list)):
								if Username_list[x]==sock:
									logged=1
									user=Username_list[x+1]
							
							if logged==0:
								send_message(sock, "Silahkan login dahulu\n")
							
							else:
								tmp2=""
								for x in range(len(tmp)):
									if x!=0:
										if not tmp2:
											tmp2=str(tmp[x])
										else:
											tmp2+=" "
											tmp2+=tmp[x]
								broadcast(serverkita_socket, sock, "["+user+"] : "+tmp2+"\n")	
						elif tmp[0]=="list" :
							
							logged = 0
							for x in range (len(Username_list)):
								if Username_list[x]==sock:
									logged=1
							
							if logged==0:
								send_message(sock, "Silahkan login dahulu\n")
							
							else:
								tmp2=""
								for x in range (len(Username_list)):
									if x%2==1:
										tmp2+=" "
										tmp2+=str(Username_list[x])
								send_message(sock, "List: "+tmp2+ "\n")
					else:
						# menghapus socket   
						if sock in Socket_list:
							Socket_list.remove(sock)

						# jika koneksi terputus
						broadcast(serverkita_socket, sock, "Client (%s, %s) is offline\n" % addr) 

				# exception 
				except:
					broadcast(serverkita_socket, sock, "Client (%s, %s) is offline\n" % addr)
					continue

	serverkita_socket.close()
    
# memberitahu kesemua client yang aktif 
def broadcast (serverkita_socket, sock, message):
    for x in range (len(Username_list)):
		
        # Mengirim pesan ke orang tertentu
        if Username_list[x] != serverkita_socket and Username_list[x] != sock and x%2==0 :
            try :
                Username_list[x].send(message)
            except :
                
                Username_list[x].close()
                
                if Username_list[x] in Socket_list:
                    Socket_list.remove(Username_list[x])
 
def send_message (sock, message):
	try:
		sock.send(message)
	except:
		sock.close()
		
		if sock in Socket_list:
			Socket_list.remove(sock)

def login (sock, user):
	a = 0
	b = 0
	for username in Username_list:
		if username == user:
			a = 1
		if username == sock:
			b = 1
	if a==1:
		send_message(sock, "Usernamemu sudah ada,usernamemu adalah " + user + "\n")
	elif b==1:
		send_message(sock, "Kamu sudah punya username\n")
	
	else:
		Username_list.append(sock)
		Username_list.append(user)
		send_message(sock, "Selamat ! Login success\n")
	
serverkita()
