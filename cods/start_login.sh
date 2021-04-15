#/bin/bash
ps -ef |grep longin|grep -v grep
if [ $? -gt 0 ] 
then
    python3 longin.py
else
    echo $?
    echo 'bb'
fi
