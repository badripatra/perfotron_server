cd "$(dirname "$(realpath "$0")")";
service=`ps -ef|grep influxd|grep -v grep`
if [ -z "$service" ]
then
cat <<EOF | sudo tee /etc/yum.repos.d/influxdb.repo
[influxdb]
name = InfluxDB Repository - RHEL \$releasever
baseurl = https://repos.influxdata.com/rhel/\$releasever/\$basearch/stable
enabled = 1
gpgcheck = 1
gpgkey = https://repos.influxdata.com/influxdb.key
EOF
sudo yum -y update
sudo yum -y install influxdb
sudo service influxdb start
sleep 5
sudo influxd -config /etc/influxdb/influxdb.conf
sleep 5
sudo sed -i -e 's/  # Determines whether HTTP endpoint is enabled.\n  # enabled = true/  # Determines whether HTTP endpoint is enabled.\n  enabled = true/g' /etc/influxdb/influxdb.conf
sudo sed -i -e 's/auth-enabled = false/auth-enabled = true/g' /etc/influxdb/influxdb.conf
sudo curl -G "http://localhost:8086/query" --data-urlencode "q=CREATE DATABASE jmeter"
sudo curl -G "http://localhost:8086/query" --data-urlencode "q=CREATE USER perfotron_influx WITH PASSWORD 'perfotron_influx' WITH ALL PRIVILEGES"
sudo service influxdb restart
else
    echo "Skipping Step : Influx Setup as as installer identified a existing Influx DB Setup. "
fi