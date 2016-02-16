## pytunnel SSH Tunnel utility for Windows 7 ##

Utility to simplify setting up SSH tunnels in a Windows environment.  This is an easier alternative to [using Putty to create SSH tunnels](http://howto.ccs.neu.edu/howto/windows/ssh-port-tunneling-with-putty/).

Functionality is provided by the Python modules [Paramiko](http://www.paramiko.org/) and [sshtunnel](https://github.com/pahaz/sshtunnel/) and bundled up in this utility to make it easy to use from the command-line as well a compiled binary version for Windows 7.  This means Windows users don't need to install Python to use this.

The utility requires a suitable Private SSH Key to reference and a suitable Open SSH Server needs to be configured at the remote server end with the associated Public Key.

## Install and Run the Windows EXE version ##

Download the latest zip-release of the pytunnel utility. See the **release** tab in this repository or go to this link:
https://github.com/edbullen/SSHtunnel/releases

+ Download the pytunnel.zip file
+ Extract the ZIP archive to a suitable location on the PC
+ in a Windows CMD.EXE window or Windows PowerShell window change directory to the extracted pytunnel directory / "folder"
+ To see usage instructions and defaults:  
```
pytunnel -h

usage: pytunnel.exe [-h] -s SERVER -l LOCALPORT -r REMOTEPORT [-k SSHKEY] [-u SSHUSER] [-p SSHPORT]

SSH tunnel utility
optional arguments:
  -h, --help            show this help message and exit
  -s SERVER, --server SERVER
                        remote Server host-name or IP address
  -l LOCALPORT, --localport LOCALPORT
                        local TCP port
  -r REMOTEPORT, --remoteport REMOTEPORT
                        remote TCP port
  -k SSHKEY, --sshkey SSHKEY
                        path to private key file - default=./key.priv
  -u SSHUSER, --sshuser SSHUSER
                        SSH user - default=oracle
  -p SSHPORT, --sshport SSHPORT
                        SSH port - default=22

```  

#### Example ####

Example tunnelling port 1521 from local host to 1521 at 10.10.0.1 over SSH with oracle user:

```
D:\pytunnel> pytunnel.exe -s 10.10.0.1 -l 1521 -r 1521 -k D:\Oracle\Cloud\testkey\rsa.priv

  Server Bound to Local Port: 1521
  Control-C to stop local-host tunnel on port 1521 to 10.10.0.1:1521
```

For multiple SSH tunnels just run more command-window sessions with different ports (i.e. create a tunnel for port 5500 to allow access to the Enterprise Manager web-console).

Example connecting to remote database server on Oracle Cloud instance using Windows SQL*Plus EZConnect string - assumes tunnel has been created in a separate Window, as per example above:

```
C:> sqlplus system/Welcome1@localhost:1521/mydb.metcsgse00453.oraclecloud.internal
``` 

Where ```mydb.metcsgse00453.oraclecloud.internal``` is the Service Name registered with the remote database server, with listener on Port 1521, running at the end of the tunnel set up previously.

## Source Code for the Wrapper ##

Is here:
https://github.com/edbullen/SSHtunnel/blob/master/pytunnel.py


 