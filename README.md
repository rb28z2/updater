# updater

### Requirements
1. Hosts running Debian-based platforms (Debian, Ubuntu)
2. SSH accessible on port 22
3. Python package `fabric` - which will be installed below
### Installation
 1. Get python and pip installed
	1. `apt update`
	2. `apt install python python-pip`
 2. Install python requirements
	 1.	`pip install -r requirements.txt`
 3. edit `fabfile.py` and modify as required
	 1. add or remove ip addresses from `env.hosts` as required
	 2. modify ip addresses for specific hosts (such as pihole and home-assistant)
 
### Running
- Running `fab doAll` will iterate over every host and update in this order:
	- kill any broken apt or dpkg instances and fix conflicts
	- run `apt-get update` on 5 hosts at a time
	- run `apt-get upgrade` on 2 hosts at a time
	- run `apt-get clean` and `apt-get autoclean` on 3 hosts at a time
	- run the singular updates for pihole and home-assistant
- You can also run `fab [fix|update|upgrade|clean|singleUpdates]` to run any one of those functions manually
