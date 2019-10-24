cd "$(dirname "$(realpath "$0")")";

file="/etc/grafana/provisioning/datasources/sample_datasource.yaml"
if [ ! -f "$file" ]
then
    sudo cp sample_datasource.yaml /etc/grafana/provisioning/datasources/
    sudo chown root:grafana /etc/grafana/provisioning/datasources/sample_datasource.yaml
    sudo service grafana-server restart
    echo "sample data source is provisioned "
else
    echo "Skipping Step : adding sample data source in grafana dashboard as datasource already exists "
fi