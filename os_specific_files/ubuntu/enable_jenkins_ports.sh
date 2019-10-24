cd "$(dirname "$(realpath "$0")")";
sudo ufw --force enable
sudo ufw allow OpenSSH
sudo ufw allow 8080
sudo dpkg --configure -a