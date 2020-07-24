cd "$(dirname "$(realpath "$0")")";
kill -9 `ps -ef|grep -v grep|grep 'python demo_api.py'|awk '{print $2}'` > /dev/null 2>&1
nohup python  demo_api.py > RestLogs.log &
(crontab -l ; echo "@reboot nohup python `pwd`/demo_api.py > RestLogs.log &") 2>&1 | grep -v "no crontab" | sort | uniq | crontab -