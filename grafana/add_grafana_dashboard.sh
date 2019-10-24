cd "$(dirname "$(realpath "$0")")";

file="/var/lib/grafana/dashboards/sample_dashboard.json"
if [ ! -f "$file" ]
then
    sudo service grafana-server stop
    sudo mkdir /var/lib/grafana/dashboards/
    sudo cp sample_dashboard.json /var/lib/grafana/dashboards/
    sudo chown root:grafana /var/lib/grafana/dashboards/sample_dashboard.json
    sudo cp sample_dashboard.yaml /etc/grafana/provisioning/dashboards/
    sudo chown root:grafana /etc/grafana/provisioning/dashboards/sample_dashboard.yaml
    sudo service grafana-server start
else
    echo "Skipping Step : adding sample dashboard in grafana dashboard as dashboard already exists "
fi