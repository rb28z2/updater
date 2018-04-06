from fabric.api import *
import getpass

env.hosts = [
	'192.168.1.2',
	'192.168.1.30',
	'192.168.1.134',
	'192.168.1.133',
	'192.168.1.21',
	'192.168.1.6',
	'192.168.1.142',
	'192.168.5.158',
	'192.168.1.242',
	'192.168.5.70',
	'192.168.5.73',
	'192.168.3.2',
	'192.168.5.140',
	'192.168.5.163',
	]
	
#going to assume root user. unsafe, but it works for a local dev environment
env.user = "root"
env.password = getpass.getpass()
env.colorize_errors=True

@parallel(pool_size=5)
def update():
	""" Update apt """
	
	run("apt-get -qq update")

@parallel(pool_size=2)	
def upgrade():
	run("yes | DEBIAN_FRONTEND=noninteractive apt-get -qq -y -o Dpkg::Options::=\"--force-confdef\" -o Dpkg::Options::=\"--force-confold\" upgrade")

@parallel(pool_size=2)
def fix():
	with settings(warn_only=True):
		run("pkill apt-get")
		run("pkill dpkg")
	run("dpkg --force-confdef --force-confold --configure -a")
	
@parallel(pool_size=3)
def clean():
	run("apt-get -qq -y clean")
	run("apt-get -qq -y autoclean")

#change ip to pihole server's ip	
@hosts('192.168.1.2')
def pihole():
	run("pihole -up")

#change ip to home-assistant's ip. currently restarting in screen doesn't work. will have to restart manually
@hosts('192.168.1.30')
def hass():
	run("pkill hass")
	run("pip3 install --upgrade homeassistant")
	run("screen -dmS hass hass --open-ui")
	
@parallel
def singleUpdates():
	execute(pihole)
	execute(hass)
	
def doAll():
	execute(fix)
	execute(update)
	execute(upgrade)
	execute(clean)
	execute(singleUpdates)
