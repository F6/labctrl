# AeroTech Ensemble

To adjust parameters for the controller, the Ensemble software needs to be installed.

The official ensemble software only supports windows7, so install it in a virtual machine.

Refer to the official document on how to set up ethernet connection, you probably need to assign static IP address to the controller for the stability of the server. Other parameters like limit switches and total length also need to be set up in the Ensemble software. The .prme file in ControllerParameters folder can be used as a reference but some of the parameters are wrong so probably need some correction (these parameters are copied as is, from our old lab computers at Rice University. the experiment settings changed alot since then)

After parameters are committed to the controller, the server does not require the Ensemble software be installed because it is now pure Ethernet connection. However you can keep it on for monitoring and it will not conflict with the server. (The server communicates with the controller via TCP socket while the Ensemble software uses UDP)

The ensemble software is proprietary so i cannot put it here, you can probably find one copy of the installer and product key on the computer near the FTIR at A304, or simply ask prof. yu. Labview drivers and example files can also be found beside it (named THz.zip, likely) 
