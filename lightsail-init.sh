#!/bin/bash

sudo amazon-linux-extras install docker
sudo service docker start
sudo usermod -a -G docker ec2-user

sudo chkconfig docker on

# install docker-compose
sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# copy the dockerfile into /srv/docker
# if you change this, change the systemd service file to match
# WorkingDirectory=[whatever you have below]
mkdir /srv/docker
curl -o /srv/docker/docker-compose.yml https://github.com/heast/evanduke/blob/master/docker-compose.yml

# copy in systemd unit file and register it so our compose file runs
# on system restart
curl -o /etc/systemd/system/docker-compose-app.service https://github.com/heast/evanduke/blob/master/docker-compose-app.service
systemctl enable docker-compose-app

# start up the application via docker-compose
docker-compose -f /srv/docker/docker-compose.yml up -d
