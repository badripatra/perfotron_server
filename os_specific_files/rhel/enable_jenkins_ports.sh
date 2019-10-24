cd "$(dirname "$(realpath "$0")")";
sudo systemctl enable firewalld
sudo firewall-cmd --permanent --add-port=8080/tcp
sudo firewall-cmd --reload