cd "$(dirname "$(realpath "$0")")";
service=`ps -ef|grep influxd|grep -v grep`
if [ -z "$service" ]
then
    sudo rm -rf /var/lib/dpkg/lock
	sudo apt-key list  | grep "expired: " | sed -ne 's|pub .*/\([^ ]*\) .*|\1|gp' | xargs -n1 sudo apt-key adv --keyserver keys.gnupg.net --recv-keys
	wget -qO- https://repos.influxdata.com/influxdb.key | sudo apt-key add -
	source /etc/lsb-release
	sudo dpkg --configure -a
	echo "deb https://repos.influxdata.com/${DISTRIB_ID,,} ${DISTRIB_CODENAME} stable" | sudo tee /etc/apt/sources.list.d/influxdb.list
	sudo apt-get update
	sudo apt-get install -y influxdb
	sudo service influxdb start
	sudo apt install -y influxdb-client
	sudo cp influxdb.conf /etc/influxdb/influxdb.conf
	sudo service influxdb start
    sleep 5
	sudo curl -G "http://localhost:8086/query" --data-urlencode "q=CREATE DATABASE jmeter"
	sudo curl -G "http://localhost:8086/query" --data-urlencode "q=CREATE USER lnp_automation WITH PASSWORD 'lnp_automation' WITH ALL PRIVILEGES"
	sudo service influxdb restart
	sudo apt-get -y install python-pip
else
    echo "Skipping Step : Influx Setup as as installer identified a existing Influx DB Setup. "
fi