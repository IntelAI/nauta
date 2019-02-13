# Client Installation and Configuration

This section provides instructions for installing and configuring Nauta to run on your client system. 

For instructions to install and configure Nauta to run on the host server, refer to the _Nauta Installation and Configuration Guide_.


## Supported Operating Systems

This release of the Nauta client software has been validated on the following operating systems and versions:

* Ubuntu 16.04
* Red Hat 7.5 
* macOS High Sierra
* Windows 10


## Required Software Packages
The following software _must_ be installed on the client system before installing Nauta:

* kubectl version 1.10 or later: (https://kubernetes.io/docs/tasks/tools/install-kubectl/#install-kubectl)

* docker version 18.03.0-ce or later: (https://docs.docker.com/install/)


## Installation

To install the Nauta client software package, do the following:

1.	Download and install the two required software packages listed above, preferably in the order given.

2.	Build the Nauta client software package for your operating system ([Nauta CLI build instructions](nctl.md)). There is no installation utility. You can unpack this package and place the unpacked files in any location you prefer. Take note of the path. 

3.	Set KUBECONFIG environment variable to the Kubernetes configuration file provided by your Nauta administrator. Here, `<PATH>` is wherever your _config_ file is located.
 
    * For MacOS/Ubuntu, enter: `export KUBECONFIG=<PATH>/<USERNAME>.config`
 
    * For Windows, enter: `set KUBECONFIG=<PATH>\<USERNAME>.config`
 
4.	(OPTIONAL) Add the package `nctl` to your terminal PATH. `NCTL_HOME` should be the path to the nctl application folder:

    * For MacOS/Ubuntu, enter: `export PATH=$PATH:NCTL_HOME`
    
    * For Windows, enter: `set PATH=%PATH%;NCTL_HOME`
    
**Note**: If you want to set the variables permanently, you can add the variables to your .bashrc, .bash_profile, or Windows system PATH. Alternatively, you may want to set the PATH and KUBECONFIG variables in the “Environment Variables” window. This is accessed by opening the Control Panel > System and Security > System > Advanced system settings, and accessing Environment variables. This is an administrator function only.

 
