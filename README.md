**Send drone sample data**
The data is sent to server in JSON format. There is mandatory parameter to run script. 

Run:
python3 sample_data.py [serverIP]

* [serverIP] is websocket server IP without port

To controll drone, firstly press **\`** character (below escape button) to enable keyboard input, then you can controll drone:
* W, A, S, D - move drone horizonvally
* Shift, Ctrl - change altitude
* Q, E - Rotate drone
* **\`** - enable/disable keyboard input
* Esc - end script
