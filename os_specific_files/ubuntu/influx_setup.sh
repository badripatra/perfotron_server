cd "$(dirname "$(realpath "$0")")";
service=`ps -ef|grep influxd|grep -v grep`
if [ -z "$service" ]
then
sudo apt-key list  | grep "expired: " | sed -ne 's|pub .*/\([^ ]*\) .*|\1|gp' | xargs -n1 sudo apt-key adv --keyserver keys.gnupg.net --recv-keys
wget -qO- https://repos.influxdata.com/influxdb.key | sudo apt-key add -
source /etc/lsb-release
sudo dpkg --configure -a
echo "deb https://repos.influxdata.com/${DISTRIB_ID,,} ${DISTRIB_CODENAME} stable" | sudo tee /etc/apt/sources.list.d/influxdb.list
sudo apt-get update
sudo apt-get install -y influxdb
sudo service influxdb start
sudo apt install -y influxdb-client
sudo influxd -config /etc/influxdb/influxdb.conf
sudo sed -i -e 's/  # Determines whether HTTP endpoint is enabled.\n  # enabled = true/  # Determines whether HTTP endpoint is enabled.\n  enabled = true/g' /etc/influxdb/influxdb.conf
sudo sed -i -e 's/auth-enabled = false/auth-enabled = true/g' /etc/influxdb/influxdb.conf
sudo curl -G "http://localhost:8086/query" --data-urlencode "q=CREATE DATABASE jmeter"
sudo curl -G "http://localhost:8086/query" --data-urlencode "q=CREATE USER lnp_automation WITH PASSWORD 'lnp_automation' WITH ALL PRIVILEGES"
sudo service influxdb restart
else
    echo "Skipping Step : Influx Setup as as installer identified a existing Influx DB Setup. "
fi