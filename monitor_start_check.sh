#!/bin/sh
#
#  check monitor_start.py is exist,if not ,run it

step=30
for((i = 0; i < 60; i=i+step));
do
ret=`ps aux | grep monitor_start.py | grep -v grep`
if [ -z "$ret" ]
then
python /path/monitor_start.py &
fi
sleep $step
done
exit 0
