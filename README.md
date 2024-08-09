Number Plate Detection using OpenCV and Python This repository contains a Python project that detects vehicle number plates using OpenCV, identifies the state to which the vehicle belongs based on the plate, and extracts the relevant details into an XML file. Introduction This project is designed to detect vehicle number plates from images or video streams using OpenCV. After detecting the number plate, the system identifies the state in India to which the vehicle is registered based on the plate's alphanumeric code. The extracted information is then saved in an XML file.

Features *Detect number plates from images or video streams. *Extract the alphanumeric code from the number plate. *Identify the Indian state based on the number plate code. *Save extracted information (number plate, state) in an XML file. *Easy to use and extendable for further improvements.

State Identification Indian number plates follow a specific format where the first two letters indicate the state or union territory. This project includes a predefined mapping of state codes, allowing it to identify the state based on the number plate.

Example:
KA for Karnataka 
MH for Maharashtra 
DL for Delhi 
TN for Tamil Nadu ... and more
