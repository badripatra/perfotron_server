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
sudo cp influxdb.conf /etc/influxdb/influxdb.conf
sudo service influxdb start
sleep 5
sudo curl -G "http://localhost:8086/query" --data-urlencode "q=CREATE DATABASE jmeter"
sudo curl -G "http://localhost:8086/query" --data-urlencode "q=CREATE USER lnp_automation WITH PASSWORD 'lnp_automation' WITH ALL PRIVILEGES"
sudo service influxdb restart
sudo yum -y install python-pip
else
    echo "Skipping Step : Influx Setup as as installer identified a existing Influx DB Setup. "
fi