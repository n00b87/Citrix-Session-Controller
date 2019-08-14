#scroll down for example

import socket
from threading import Thread, Lock
import sys

lock = Lock()

host = socket.gethostbyname(socket.gethostname())
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

clients = {}
addresses = {}

client_messages = {}

client_threads = []

server_message_to_client = {}

###############################################################
BUFSIZ = 1024

server_run_flag = False

def accept_incoming_connections(callback_func):
    """Sets up handling for incoming clients."""
    global serversocket
    global clients
    global addresses

    while True:
        #print ("connecting")
        if server_run_flag == False:
            print("----quitting server here------")
            break
        try:
            client, client_address = serversocket.accept()
            addresses[client] = client_address
            clients[client] = client_address
            ct = Thread(target=callback_func, args=(client,client_address,))#.start()
            client_threads.append(ct)
            ct.start()
        except:
            try:
                print("----EXIT THREAD----")
                for x in client_threads:
                    x.join()
                sys.exit()
                return 0
            except:
                return 0

    


###########################################
server_run_flag = False
server_is_running = False
main_thread = None

def setup_server( port, main_thread, callback_func, num_connections=9):
    global serversocket
    global host
    global server_run_flag
    server_run_flag = True
    serversocket.bind( (host, port))
    serversocket.listen(num_connections)
    ACCEPT_THREAD = Thread(target=accept_incoming_connections, args=(callback_func,))
    ACCEPT_THREAD.start()
    if main_thread != None:
        MAIN_THREAD = Thread(target=main_thread)
        MAIN_THREAD.start()
        MAIN_THREAD.join()
    ACCEPT_THREAD.join()

def listen_to_client(client=0):
    msg = ""
    if client==0:
        return ""
    try:
        msg = client.recv(1024).decode("utf8")
    except:
        msg = ""
    return msg


def talk_to_client(client, data_to_send):
    if len(data_to_send) > 0:
        client.send(bytes(data_to_send, "utf8"))
        print("sent: " + data_to_send)

def server_process_running():
    return server_run_flag

def close_server():
    global server_run_flag
    global serversocket
    lock.acquire()
    server_run_flag = False
    serversocket.close()
    lock.release()



####

msg_list = []
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_run_flag = False
client_thread_isRunning = False

########CLIENT STUFF############################

def client_thread_receive():
    """Handles receiving of messages."""
    global clientsocket
    global client_run_flag
    global client_thread_isRunning
    client_thread_isRunning = True

    while client_run_flag:
        try:
            msg = clientsocket.recv(1024).decode("utf8")
            if msg != "":
                #print ("server sent: " + msg)
                msg_list.append(msg)
        except OSError:  # Possibly client has left the chat.
            break
    
    client_thread_isRunning = False
    sys.exit()


####################################################


def connect_to_server( ip, port):
    global clientsocket
    global receive_thread
    global client_run_flag
    global client_thread_isRunning
    client_run_flag = True
    clientsocket.connect( (ip, port) )
    receive_thread = Thread(target=client_thread_receive)
    receive_thread.start()

def listen_to_server():
    global msg_list
    s = ""
    if len(msg_list) > 0:
        s = msg_list.pop(0)
    return s

def talk_to_server(data_to_send):
    global clientsocket
    clientsocket.send(bytes(data_to_send, 'utf8'))

def close_client():
    global clientsocket
    global client_run_flag
    client_run_flag = False

