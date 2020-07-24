cd "$(dirname "$(realpath "$0")")";
service=`ps -ef|grep grafana-server |grep -v grep`
if [ -z "$service" ]
then
	wget https://dl.grafana.com/oss/release/grafana_6.5.2_amd64.deb
	sudo apt-get install -y adduser libfontconfig1
	sudo dpkg -i grafana_6.5.2_amd64.deb
	sudo add-apt-repository "deb https://packages.grafana.com/oss/deb stable main"
	curl -s https://packages.grafana.com/gpg.key | sudo apt-key add -
	sudo apt-get update
	sudo apt-get install -y grafana
	sudo apt-get install -y apt-transport-https
	sudo service grafana-server start
	sudo update-rc.d grafana-server defaults
	sudo systemctl enable grafana-server.service
	sudo systemctl daemon-reload
	sudo systemctl start grafana-server
	sudo systemctl enable grafana-server.service
	sudo grafana-cli plugins install grafana-clock-panel
	sudo chown -R grafana:grafana  /etc/grafana/
	sudo service grafana-server restart
	sudo systemctl enable grafana-server.service
else
    echo "Skipping Step : Grafana Server setup as installer identified a existing Grafana-Server Setup. "
fi