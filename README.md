First Time?
--------------

Setting up an EV3 with Linux opens up many new features on the ev3 but you'll probably find that many of the terminal commands, 
libraries, and packages you want have to be installed. This makes sense as it's the way Linux likes to work but that doesn't mean 
it's quick or simple to find the right terminal commands. So here is a walkthrough.

1. **Gather the following supplies/materials:** 
  - an EV3 kit with an EV3 brick and sensors
  - a microSD chip with at least 8(?)GB space (16GB+ ensures you shouldn't run out of space quickly when you update your Linux system 
  and install new library packages)
  - a WIFI dongle (Canakit's WIFI dongle is supposed to work wonderfully with Linux systems - 
  https://www.amazon.com/CanaKit-Raspberry-Wireless-Adapter-Dongle/dp/B00GFAN498); 
  
2. **Next, download the ev3dev ev3 linux system.** It is Debian-based and has language bindings for Node.js, C++ and Python so you can 
program in all three or in any of those of your choice. For this walkthrough, I will be using Python. Here is the github 
link: https://github.com/ev3dev/ev3dev/releases . Find the most current ev3dev Jessie Linux version (at the time of this writing, 
the most current released version is ev3dev-jessie-2015-12-30). Download the first ZIP file, open and transfer the contents onto 
the microSD card. 

3. **Have your EV3 turned off. Now plug the microSD card into the SD card slot** on the side of your ev3. Try turning on your ev3. When
your ev3 boots, it should now be running Jessie (linux) and Monobrick. Note that the interface will look different from the default 
LEGO interface. As well, the battery in the corner will not tell you a percentage. Rather it is a general range. You should keep an 
eye out for when the battery reaches 6.##. This means it will die soon (when it reaches 5 and it does so fairly quickly). A full 
battery should be around 8.##.

4. **Plug in your WIFI dongle into the USB slot** on the side of the brick to add WIFI searching and connecting capabilities to your brick. This can be removed and plugged in with your ev3 on.

  Now for a few notes about the interface:
  
    1. The first line should say 'File Browser.' This will allow you to click through the files stored on your ev3. Note: This is not 
    ALL files (not from root). It's all files and folders in your 'home' directory and beyond. As of now you can't run a program from 
    clicking on it on the brick. You have to give a terminal command. That's one feature I was going to look at implementing for ease.
    
    2. 'Device Browser' is your second option. This lets you choose to see ports, sensors, and motors by category and look at all 
    objects of those kinds currently active (as in plugged in) on the brick. If you select a specific sensor or motor, you can track 
    its current value from the EV3 brick window, as well as its port/address and its name.
    
    3. 'Wireless and Networks' is self-explanatory. You can click the category of connection you want (Bluetooth, Wi-Fi) and select 
    another device or network. You can have both a WIFI and a Bluetooth connection at the same time but Bluetooth supposedly drains
    battery faster than WIFI so be careful to watch the battery if you do. You can also turn your brick 'Offline' if you want, though
    that isn't helpful until I figure out how to run installed programs by clicking on the brick.
    
    4. You probably won't end up using Roberta Lab. That was a new feature added as of the most recent major update on the os system 
    and I haven't looked into its abilities. If you do, let me know and we can update this point.

5. **Update, Upgrade**
    Once you've installed the system you'll want to update and upgrade all packages on your os system that have newer versions. You 
  should do this every time you want to install a library or other package to make sure that you can use all newer packages. To 
  download anything or update/upgrade anything your brick must be connected to a WIFI network.
  
  Update finds the newest version of all packages while upgrade installs these new versions so it's simple to do update first, then 
  upgrade.
  
  To update type in the following line in your terminal:
    sudo apt-get update
  
  Now type this line to upgrade:
    sudo apt-get upgrade
  
  This usually takes at least two hours for the first upgrade and will take longer the older your system is compared to the newest 
  version. You may have to run this upgrade command multiple times (and it's a good idea to) until there is nothing left to update. 
  This is because some packages can only be set up if other packages are upgraded and set up first so running the command multiple 
  times should catch that.
  
  Now that your brick's system is up-to-date, you can install some new libraries. The following are the terminal commands for some 
  very helpful libraries you will likely need. It's a good idea to install them now as then you'll have them when you need them. 
  Please type these in order as some downloads depend on the earlier ones. (sudo gives you 'super-user' access to download which you 
  can't always do as a regular user)
  
    sudo apt-get install apt-utils
    sudo apt-get install curl
    sudo curl https://bootstrap.pypa.io/get-pip.py | python

Some other potentially helpful packages are below:
  sudo apt-get install locate (Allows you to 'find' any package you have installed or know if one is not installed)

A recent, thorough list of functions for this system can be found here:
  https://media.readthedocs.org/pdf/python-ev3dev/latest/python-ev3dev.pdf

If you use vim to edit you are all set but if you use emacs you will have to install it. Use the following command to install emacs:
  sudo apt-get install emacs
  
  Emacs is a pretty big download (289 mB) so it will take a while.
  From: http://www.thegeekstuff.com/2010/07/install-emacs-editor-on-linux/?utm_source=feedburner&utm_medium=feed&utm_campaign=Feed%3A+TheGeekStuff+(The+Geek+Stuff)
