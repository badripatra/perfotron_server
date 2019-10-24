cd "$(dirname "$(realpath "$0")")";
file="/var/lib/jenkins/secrets/initialAdminPassword"
if [ -f "$file" ]
then
    wget http://ftp.mozilla.org/pub/mozilla.org/firefox/releases/30.0/linux-x86_64/en-US/firefox-30.0.tar.bz2
    tar -xjvf firefox-30.0.tar.bz2
    sudo rm -rf /opt/firefox*
    sudo mv firefox /opt/firefox30.0
    sudo ln -sf /opt/firefox30.0/firefox /usr/bin/firefox
    sudo pip install pyvirtualdisplay
    sudo pip install selenium
    sudo python selenium_jenkins.py
else
    echo "Skipping Step : Unlock Jenkins as as installer identified a existing Jenkins Setup. "
fi