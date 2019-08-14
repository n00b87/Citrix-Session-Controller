from stupid_sockets import *

import os
import time

#setup server on the given port. You can change the port to whatever you want.
setup_server(8089)

ctrx_cmd = """ "C:\Program Files (x86)\Citrix\ICA Client\SelfServicePlugin\SelfService.exe" -qlaunch MiDesktop"""

mode = 0
ctrx_file = ""
ctrx_f_path = "ctrx.rc" #Should be absolute path of file where IP Address for the Server Session is stored

mode = 0

if len(host) > 0:
    #writes the server IP address to the ctrx.rc file. The client opens this file to get the IP address to connect to.
    ctrx_file = open(ctrx_f_path,"w")
    ctrx_file.write(host+'\n')
    ctrx_file.close()
else:
    mode = 1


if mode == 0:
    print ("master process")

    #launch a new citrix session
    os.system(ctrx_cmd)
    
    while True:
        #this line connects to a client
        get_client_connection()

        #communicate with client
        #This is where you can send commands to client
        talk_to_client("test from master process") #Each word is a argument to the client
        buf = listen_to_client()
        if len(buf) > 0:
            print("slave process sent: " + buf)
            break


#close server socket
close_server()
