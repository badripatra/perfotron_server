cd "$(dirname "$(realpath "$0")")";
sudo fuser -k 3000/tcp
sudo fuser -k 9003/tcp
sudo fuser -k 8086/tcp
sudo systemctl enable firewalld
sudo firewall-cmd --permanent --add-port=9003/tcp
sudo firewall-cmd --permanent --add-port=8086/tcp
sudo firewall-cmd --permanent --add-port=3000/tcp
sudo firewall-cmd --reload