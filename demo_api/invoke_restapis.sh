cd "$(dirname "$(realpath "$0")")";
kill -9 `ps -ef|grep -v grep|grep 'python demo_api.py'|awk '{print $2}'` > /dev/null 2>&1
nohup python  demo_api.py > RestLogs.log &