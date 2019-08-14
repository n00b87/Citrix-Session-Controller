from stupid_sockets import *
import os
import time
import win32com.client

ctrx_cmd = """ "C:\Program Files (x86)\Citrix\ICA Client\SelfServicePlugin\SelfService.exe" -qlaunch MiDesktop"""

logoff_cmd = "logoff"

ctrx_file = ""
ctrx_f_path = "ctrx.rc" #Should be absolute path of file where IP Address for the Server Session is stored

server_host = 0

#gets the server IP address from the ctrx.rc file.
if os.path.isfile(ctrx_f_path):
    ctrx_file = open(ctrx_f_path,"r")
    server_host = ctrx_file.readline().strip()
    ctrx_file.close()
else:
    print("no master process detected")



print("slave process")


print (host)
print("connecting to " + server_host)
#connects to the server on the given port. The port must be the same as the server.
connect_to_server(server_host, 8089)

arg_count = 0

arg1 = 0
arg2 = 0 
arg3 = 0 
arg4 = 0

xl = None

#This loop is where you can get commands from the server and execute whatever process you need to run
while True:
    
    data = listen_to_server()

    if data == "{quit}":
        print("exiting client")
        break

    #if server sent nothing then exit loop
    if len(data)>0:
        args = data.split(" ")
        arg1 = int(args[0])
        arg2 = int(args[1])
        arg3 = int(args[2])
        arg4 = int(args[3])
        
        arg_count = 4
    
    if arg_count == 4:
        print("launching macro")
        print("arg1 = " + str(arg1))
        print("arg2 = " + str(arg2))
        print("arg3 = "+str(arg3))
        print("arg4 = "+str(arg4))
        
        xl=win32com.client.Dispatch("Excel.Application")
        
        xl_counter = 0

        xl_flg = False

        while xl_counter < 10:
            try:
                xl.Application.DisplayAlerts = False
                wb = xl.Workbooks.Open(os.path.abspath("test.xlsb"), ReadOnly=1)
                xl_flg = True
                break
            except:
                print("Excel Error")
                xl_counter = xl_counter + 1
        xl_counter = 0

        if not xl_flg:
            talk_to_server("fail")
            break

        xl_flg = False

        while xl_counter < 10:
            try:
                xl.Application.Run("test.xlsb!Test_Macro", arg1, arg2, arg3, arg4) #Execute Macro from test.xlsb:  Sub Test_Macro( arg1$, arg2$, arg3$, arg4$ )
                talk_to_server('complete')
                print ("sent complete")
                xl_flg = True
                break
            except:
                print("App Run Error")
                xl_counter = xl_counter + 1
        
        if not xl_flg:
            talk_to_server("fail")
            break
        
        arg_count = 0

        cg = 0
        tg = 0 
        m = 0 
        tus = 0

        xl = None


try:
    wb.Close(SaveChanges=False)
    xl.Application.Quit()
except:
    print("could not close")

#close client socket
close_client()
while client_thread_isRunning:
    pass

print ("logging off....")
os.system(logoff_cmd)
