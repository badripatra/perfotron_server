cd "$(dirname "$(realpath "$0")")";
sudo fuser -k 3000/tcp
sudo fuser -k 9003/tcp
sudo fuser -k 8086/tcp
sudo ufw --force enable
sudo ufw allow OpenSSH
sudo ufw allow 3000
sudo ufw allow 9003
sudo ufw allow 8086
