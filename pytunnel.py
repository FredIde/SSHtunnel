from sshtunnel import SSHTunnelForwarder
import argparse
import sys
import os.path
from time import sleep
import configparser

"""
Python SSH Tunnel Utility 1.1 - E. Bullen Feb 2016
Wrapper around **sshtunnel** - see https://github.com/pahaz/sshtunnel/

Written for Python 3.3

sshtunnel has dependancies on
    paramiko
    ecdsa
    pycrypto
    
General usage:
    
    EITHER 
    pytunnel cmd -s <remote server host-name/IP-addr> -l <localport>  -r <remoteport> [ -k <sshkey> ] [ -u <ssh user> ] [-p <ssh port>] 
    OR
    pytunnel config -c <config file name>
    
    sshkey defaults to "./key.priv" if not specified
    user defaults to "oracle"
    
** Example ** - tunnel port 1521 from local host to 1521 at 129.152.150.7 over SSH with oracle user:
$> python pytunnel.py cmd -s 129.152.150.7 -l 1521 -r 1521 -k D:\Oracle\Cloud\testkey\rsa.priv
> CommandInput : binding local port 1521 to 129.152.150.7 and remote port 1521
> -> Server Bound to Local Port: 1521
> Control-C to stop SSH Tunneling

** Example ** - set up multiple SSH tunnels in one go, referencing a configuration file
$> python pytunnel.py config -c ./mycloud.conf
> Loading configuration from ./mycloud.conf
> MyCloud_DbListener_1521 : binding local port 1521 to 141.145.26.60 and remote port 1521
> MyCloud_DbConsole_5500 : binding local port 5500 to 141.145.26.60 and remote port 5500
> -> Server Bound to Local Port: 1521
> -> Server Bound to Local Port: 5500
> Control-C to stop SSH Tunneling

** Config File FMT Example ** (Uses standard Python ConfigParser)
[MyCloud_DbListener_1521]
server: 141.145.26.60 
sshport: 22
sshuser: oracle
sshpwd: 
sshkey: D:/TEMP/key.prv
localport: 1521
remoteport: 1521

[MyCloud_DbConsole_5500]
server: 141.145.26.60 
sshport: 22
sshuser: oracle
sshpwd: 
sshkey: D:/TEMP/key.prv
localport: 5500
remoteport: 5500

      
Windows command-line example for calling the sshtunnel module directly >> Without using this wrapper <<
python -m sshtunnel -U oracle -K D:/Oracle/Cloud/testkey/rsa.priv -L :1521 -R 127.0.0.1:1521 -p 22 129.152.150.7

"""

class ArgParseError(Exception):
    pass
class ConfigFileAccessError(Exception):
    pass
class KeyFileAccessError(Exception):
    pass

def fileexists(fname):
    return(os.path.isfile(fname) )

def defaultconfig():
    global SSHPORT
    SSHPORT = 22
    global SSHUSER
    SSHUSER = "oracle"
    global SSHKEY
    SSHKEY = "./key.priv"
    global CNAME
    CNAME = "./pytunnel.conf"

def getconfig(cname):
    """Read the config file and populate a list of bindings with values.
    
    """
    Config = configparser.ConfigParser()
    bindings = []
    
    if fileexists(cname):
        Config.read(cname)
        for section in Config.sections():
            binding = {}
            binding["tag"] = section
            options = Config.options(section)
            for option in options:
                try:
                    binding[option] = Config.get(section,option)
                except:
                    print("Error parsing config file: section {0}, option {1}".format(section, option))
            bindings.append(binding) # add the binding dict to the bindings list

    else:
        raise ConfigFileAccessError(cname)
    
    return bindings
    
def parseargs():
    
    parser = argparse.ArgumentParser(description='SSH tunnel utility', formatter_class=argparse.RawTextHelpFormatter)
    subparsers = parser.add_subparsers(help='run in Command (cmd) or Config (config) modes')
    
    if len(sys.argv) < 2:
        parser.error("<cmd> or <config> Mode must be specified")
    
    parser_a = subparsers.add_parser('cmd', help='specify command-line options (cmd -h for more help)')
    parser_a.add_argument('-s', '--server', help='remote Server host-name or IP address', required=True)
    parser_a.add_argument('-l', '--localport', help='local TCP port', required=True)
    parser_a.add_argument('-r', '--remoteport', help='remote TCP port', required=True)
    parser_a.add_argument('-k', '--sshkey', help='path to private key file - default='+ SSHKEY, default = SSHKEY)
    parser_a.add_argument('-u', '--sshuser', help='SSH user - default=' + SSHUSER, default = SSHUSER)
    parser_a.add_argument('-p', '--sshport', help='SSH port - default='+ str(SSHPORT), default = SSHPORT)
    
    parser_b = subparsers.add_parser('config', help='sepecfy config file')
    parser_b.add_argument('-c', '--configfile', help='config. file location', default = CNAME)

    args = parser.parse_args()
    return args


def init_binding(server, sshport, sshuser, sshpwd, sshkey,localport , remoteport):
    """Create a dictionary of binding vars for a single server connection.
    
    """
    binding = {  "tag":"CommandInput" 
               , "server":server
               ,"sshport":int(sshport)
               , "sshuser":sshuser
               , "sshpwd":sshpwd
               , "sshkey":sshkey
               , "localport":int(localport)
               , "remoteport":int(remoteport)}
    return binding

# MAIN #
if __name__ == '__main__':
    
    defaultconfig()
    bindings = []  # list of dicts - each binding dict created by init_binding
    args = vars(parseargs())  # parse args and convert to dict

    if "server" in args:
        #get the binding args from the command-line parsed options
        binding = init_binding(args["server"], args["sshport"], args["sshuser"], "dummy", args["sshkey"], args["localport"], args["remoteport"])
        bindings.append(binding)
    elif "configfile" in args:
        #go to the config file and get back a list of bindings to set up
        print("Loading configuration from",args["configfile"] )
        bindings = getconfig(args["configfile"])
    else:
        raise ArgParseError("Can't find server or configfile option")
        
    try:
        #loop setting up multiple SSHTunnel Servers in a list; loop through list of dicts - "bindings[]".
        servers = []
        for binding in bindings:
            print(binding["tag"],": binding local port", binding["localport"], "to", binding["server"], "and remote port", binding["remoteport"])
        
            if not fileexists(binding["sshkey"]):
                raise KeyFileAccessError(binding["sshkey"])
            
            #create a list of "servers" containing SSHTunnelForwarder servers
            servers.append(SSHTunnelForwarder(
                (binding["server"], int(binding["sshport"])), 
                    ssh_username = binding["sshuser"],
                    #ssh_password="",
                    ssh_private_key = binding["sshkey"],
                    local_bind_address=('127.0.0.1', int(binding["localport"])),
                    remote_bind_address=('127.0.0.1', int(binding["remoteport"]) )
                                             )
                          )
        #start the SSHTunnel Servers configured in the servers[] list
        for server in servers:
            server.start()
            print("-> Server Bound to Local Port:", server.local_bind_port)
        
        print("Control-C to stop SSH Tunneling")    
        while True:
            # press Ctrl-C for stopping
            sleep(1)
           
    except KeyboardInterrupt:
        pass
    	
    except KeyFileAccessError as err:    
        print("Key File Access Error:" , err )
    except Exception as err:	
        print("General Exception " , err )
    finally:
        for server in servers:
            server.close()
        print('Tunnel Session Closed')
