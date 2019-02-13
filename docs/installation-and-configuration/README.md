# Nauta Installation, Configuration, and Administration Guide

This Nauta Installation, Configuration, and Administration guide provides step-by-step instructions for installing and configuring Nauta. This guide also provides an overview of Nauta requirements and configuration options.

**Note:** For instructions on configuring the Nauta client, refer to the [Nauta User Guide](../user-guide/).

Nauta is a software suite that provides a multi-user, distributed computing environment for running deep learning model training experiments. Results of experiments can be viewed and monitored using a command line interface (CLI), Web UI and/or TensorBoard*. You can use existing data sets, your own data, or downloaded data from online sources, as well as create public or private folders to make collaboration among teams easier. 

Nauta runs on Kubernetes* and Docker* for scalability and ease of management. Nauta uses customizable templates to remove the complexities of creating and running single and multi-node deep learning training experiments without all the system's complexity and scripting needed with standard container environments.

# Hardware Requirement Overview

Nauta is intended to run on a multi-server Kubernetes cluster. To run Nauta, you will need at least one Master node, and one or more Worker nodes. Nauta is a platform for performing Deep Learning training, and requires robust hardware specifications to run with optimal performance. 

# Installation Overview

To install Nauta in a 'bare metal' (for example, non-cloud) server environment, you will need to:

1. Execute the following commands from the command line: 

 - `git clone --recursive https://github.com/IntelAI/nauta.git` 
 
 - `cd nauta`

2. Build the base package (a makefile will automate the bulk of the process, but there are some minimum packages needed to get going).

3. Populate Nauta's inventory file to tell it where your master and worker nodes are, and how to access them.

4. Configure Nauta's configuration file to tell it about proxies, network quirks and filesystem preferences.

5. Run the installation script.

This process does the following:

- Creates a Kubernetes cluster, all the Docker files you need to run Tensorflow*, Jupyter*, Tensorboard, and Horovod*.

- Installs the Nauta server-side application on your new Kubernetes cluster, and starts the system running.

Completing all of the above takes some time. We are working on streamling the process. 

# Document Flow

This guide consists of the following main topics, in order:

* [System Software Components Requisites](System_Software_Components_Requisites/SSCR.md)
* [Building Nauta](How_to_Build_Nauta/HBN.md)
    * [Installer System Requirements](Installer_System_Requirements/ISR.md)
    * [Target Host Requirements](Target_Host_Requirements/THR.md)
* [Inventory Configuration](Inventory_Tasks/IT.md)
* [Nauta Configuration (Variables)](Configuration_Tasks_Variables/CTV.md)
    * [Installation Package Requirements](Installation_Package_Requirements/IPR.md)
* [Installating and Starting Nauta](Installation_Process/IP.md)
* [User Management](User_Management/UM.md)
* [Troubleshooting](Troubleshooting/T.md)
