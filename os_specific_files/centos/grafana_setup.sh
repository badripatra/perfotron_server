cd "$(dirname "$(realpath "$0")")";
service=`ps -ef|grep grafana-server |grep -v grep`
if [ -z "$service" ]
then
    sudo yum -y install https://dl.grafana.com/oss/release/grafana-6.0.1-1.x86_64.rpm
    sudo yum -y install grafana
    sudo service grafana-server start
    sudo /sbin/chkconfig --add grafana-server
    systemctl daemon-reload
    systemctl start grafana-server
    systemctl status grafana-server
    sudo systemctl enable grafana-server.service
    sudo yum -y install fontconfig
    sudo yum -y install freetype*
    sudo yum -y install urw-fonts
    sudo grafana-cli plugins install grafana-clock-panel
    sudo service grafana-server restart
else
    echo "Skipping Step : Grafana Server setup as installer identified a existing Grafana-Server Setup. "
fi