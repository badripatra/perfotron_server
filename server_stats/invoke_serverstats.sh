cd "$(dirname "$(realpath "$0")")";
kill -9 `ps -ef|grep -v grep|grep 'system_monitor.py'|awk '{print $2}'` > /dev/null 2>&1
nohup python  system_monitor.py > server_stats.log &