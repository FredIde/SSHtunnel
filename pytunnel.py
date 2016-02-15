from sshtunnel import SSHTunnelForwarder
import argparse
from time import sleep

'''
Python SSH Tunnel Utility
Wrapper around **sshtunnel** - see https://github.com/pahaz/sshtunnel/
pip install sshtunnel
E. Bullen Feb 2016

sshtunnel has dependancies on
    paramiko
    ecdsa
    pycrypto
    
General useage:
    pytunnel -c config.file | -u <ssh user> -s <remote server host-name/IP-addr> -l <localport>  -r <remoteport> [ -k <sshkey> ]
    
    sshkey defaults to SSHKEY
    user defaults to ORACLE
      
# Windows command-line example for calling the sshtunnel module directly:
#PS D:\sugarsync\git\python\SSHtunnel> python -m sshtunnel -U oracle -K D:/Oracle/Cloud/testkey/rsa.priv -L :1521 -R 127.0.0.1:1521 -p 22 129.152.150.7
'''


def fileexists(fname):
    pass

def defaultconfig():
    global SSHPORT
    SSHPORT = 22
    global SSHUSER
    SSHUSER = "oracle"
    global SSHKEY
    SSHKEY = "./rsa.priv"
    global CNAME
    CNAME = "./pytunnel.conf"

def configfile(cname):
    # Todo
    #return exist, config
    pass

def parseargs():
    parser = argparse.ArgumentParser(description='SSH tunnel utility')
    parser.add_argument('-s', '--server', help='remote Server host-name or IP address', required=True)
    parser.add_argument('-l', '--localport', help='local TCP port', required=True)
    parser.add_argument('-r', '--remoteport', help='remote TCP port', required=True)
    parser.add_argument('-k', '--sshkey', help='path to private key file', required=False)
    parser.add_argument('-u', '--sshuser', help='SSH user', required=False)
    parser.add_argument('-p', '--sshport', help='SSH port', required=False)
        
    args = parser.parse_args()

    # Set vars:
    if args.sshuser:
        sshuser = args.sshuser  #or use default
    else:
        sshuser = SSHUSER
    localport = int(args.localport)
    remotehost = args.server
    remoteport = int(args.remoteport)
    if args.sshkey:
        privatekey = args.sshkey #(or use default)
    else:
        privatekey = SSHKEY
    if args.sshuser:
        sshuser = args.sshuser
    else:
        sshuser = SSHUSER
    if args.sshport:
        sshport = args.sshport
    else:    
        sshport = SSHPORT
    
    return sshuser, localport, remotehost, remoteport, privatekey, sshuser, sshport

def validate():
    pass


if __name__ == '__main__':
    
    defaultconfig()
    sshuser, localport, remotehost, remoteport, privatekey, sshuser, sshport = parseargs()
     
    #fileexists(privatekey)    
    #validate()
    
    try:
        server = SSHTunnelForwarder(
            (remotehost, sshport), 
    		    ssh_username = sshuser,
    			#ssh_password="",
    			ssh_private_key = privatekey,
    	        local_bind_address=('127.0.0.1', localport),
    			remote_bind_address=('127.0.0.1', remoteport))
        
        server.start()
        print("Server Bound to Local Port:", server.local_bind_port)
        print("Control-C to stop local-host tunnel on port {0} to {1}:{2}".format(localport,remotehost,remoteport))
        while True:
            # press Ctrl-C for stopping
            sleep(1)
    		
        #server.stop()
    
    except KeyboardInterrupt:
        pass
    	
    except Exception as err:	
        print("General Exception " , err )
    finally:
        server.close()
        print('Tunnel Session Closed')
