#!/bin/bash

stop_blog() {
	pid=`ps -ef | grep "manage.py" | awk "{ print $2 }"`
	echo $pid
	kill -9 $pid
}

start_blog() {
	python manage.py runserver 0.0.0.0:8000 > 2 &
}

if [ x$1 != x or $1 == 'run' ]; then
	start_blog
elif [ $1 == 'stop' ]; then
	stop_blog
elif [ $1 == 'restart' ]; then
	stop_blog
	start_blog
fi
