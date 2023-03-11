# Kismet Web RSSI Bar

Taking the same idea as the previous tkinter based Kismet RSSI Bar, the web bar is intended to be a Kismet
add on to find Access Points or client devices based on Received Signal Strength Indicator (RSSI) provided
by Kismet. 

## Installation Requirements

````
cd kismet_web_rssi-bar
$ pip3 install -r requirements.txt
````

## Launching
After Kismet is running, run the following:
````
$ cd kismet_web_rssi-bar
$ python3 main.py
````
After launching, navigate to the provided link, which should be the local machines IP at port 5001

## Manual 
![image](https://user-images.githubusercontent.com/96986202/224188916-2d3dd191-5296-4cfd-94f2-4f3d8310014d.png)

Rssi bar can be started without Kismet being started, but will not DF without an active Kismet server at the targeted IP address. 
Once a MAC is entered, hit 'Set MAC' and 'Start DF'. Once set, the Enter MAC label will change to the current MAC address and the Current Channel label
will reflect current channel in Kismet. Lock Channel button will set the channel of all active Kismet interfaces to the Current Channel label.

## Kismet Server Login

Currently, there is no way to modify Kismet username, password, or IP from the server's GUI and must be modified within
main.py prior to running. By default, username and password are both set to 'kismet' and IP is set to localhost.

## Roadmap

The following is the intended features to be added to this project:

* Default channel hopping combinations (similar to those in offline version of rssi bar)
* Options menu (For ui preferences and Kismet Server changes)
* Active Direction Finding
* Mapping UI
