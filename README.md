## pytunnel SSH Tunnel utility for Windows 7 ##

Utility to simplify setting up SSH tunnels in Windows environment.  This is an easier alternative to [using Putty to create SSH tunnels](http://howto.ccs.neu.edu/howto/windows/ssh-port-tunneling-with-putty/).

Functionality is provided by the Python modules [Paramiko](http://www.paramiko.org/) and [sshtunnel](https://github.com/pahaz/sshtunnel/) and bundled up in this utility to make it easy to use from the command-line as well a compiled binary version for Windows 7.  This means Windows users don't need to install Python to use this.

## Install and Run the Windows EXE version ##

Download the latest zip-release of the pytunnel utility. See the **release** tab in this repository or go to this link:
https://github.com/edbullen/SSHtunnel/releases

+ Download the pytunnel.zip file
+ Extract the ZIP archive to a suitable location on the PC
+ in a Windows CMD.EXE window or Windows PowerShell window change directory to the extracted pytunnel directory / "folder"
+ To see usage instructions and defaults:  
'''
pytunnel -h
'''  

#### Example ####

Example tunnelling port 1521 from local host to 1521 at 10.10.0.1 over SSH with oracle user:

'''
D:\pytunnel> pytunnel.exe -s 10.10.0.1 -l 1521 -r 1521 -k D:\Oracle\Cloud\testkey\rsa.priv

>  Server Bound to Local Port: 1521
>  Control-C to stop local-host tunnel on port 1521 to 10.10.0.1:1521
'''

## Source Code for the Wrapper ##

Is here:
https://github.com/edbullen/SSHtunnel/blob/master/pytunnel.py


 