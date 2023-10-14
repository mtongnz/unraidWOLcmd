# unraidWOLcmd

This repository has a few components to allow commands to be run on an unRaid host, triggered by sending a Wake On Lan packet.  I've also added a couple of helper scripts that I use with this.

### Docker Container

The container listens to the port specified in the config.yaml for WOL packets.  If it receives a packet with a MAC that matches one in the config, it pushes the corresponding command to the FIFO buffer.

I use the Compose.Manager plugin to allow use of DockerCompose via the GUI.  It can also be run via command line.  There are plenty of tutorials to assist with this so I won't cover it here.

Copy the config.yaml into your config dir and configure port (should be 9) and the commands you'd like to run.

**Security Note:** This process doesn't care who or where the WOL packets came from.  There is no security check on who sent them.  As such, don't place commands here that could lead to issues.  The config file should be "secure" (ie. if someone can edit your config files, it doesn't really matter if they can send WOL to execute them - they're already in).


### FIFO

A FIFO must be configured in the docker's config dir.  It allows the docker to write commands into a FIFO buffer that the User Script then reads.

Run this command from the docker's config directory (probably /mnt/users/appdata/wolReceive/).  
`mkfifo /fifo`


### User Scripts

I have supplied 2 user scripts.

#### fifoRun.sh
fifoRun is the main script needed for this to all work.  It takes the commands from the FIFO buffer and executes them on the unRaid host.

To setup...  
1. go to the *User Scripts* tab in your unRaid GUI
2. click *Add New Script* and give it a name
3. copy the script from here to there
4. edit the directory to point at your fifo (/mnt/user/appdata/wolReceive/fifo)
5. click *Save Changes*
6. set the schedule to *At Startup of Array*
7. click *Apply* at the bottom of the page
8. click *Run in Background* for the script you just created

After the script is running, click the *ShowLogs* button for the script.  It should show *Script Starting* and not have errors.

*Testing:*  
If you use the example config supplied & have the FIFO & docker setup  
- send a WOL packet with a MAC of *00:00:00:00:00:99*
- the log should show *This is a test*

#### vmControl.sh
vmControl is a script to start & stop virtual machines on unRaid.  It works well with unraidWOLcmd as it means we can wake virtual machines using WOL packets.  This is great in combination with Guacamole (an RDP in browser app - google it).

To setup...  
1. copy vmControl.sh somewhere (I chose /scripts/ but read below about reboot persistance)
2. run this command to change the owner & make it executable  
`chown nobody:users vmControl.sh && chmod +x vmControl.sh`

vmControl is now installed.  You can run it via the terminal:  
`/scripts/vmControl.sh 'vmName here' start|stop`

Within most VMs, you can set what the shutdown command does, so you can set it to sleep or hibernate.  This script will still allow it to wake from those states.

#### scriptMove.sh
unRaid seems to delete scripts from the /scripts/ folder on boot.  scriptMove copies scripts from the unRaid USB (we don't want to run too much from the USB if we can help it).

To setup...  
1. go to the *User Scripts* tab in your unRaid GUI
2. click *Add New Script* and give it a name
3. copy the script from here to there
5. click *Save Changes*
6. set the schedule to *At First Array Start Only*
7. click *Apply* at the bottom of the page
8. copy your scripts into /boot/scripts/

Any scripts you want to use will now be available in the /scripts/ directory after reboot with the correct owner & execute permissions.