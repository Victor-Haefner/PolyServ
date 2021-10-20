#!/bin/sh

echo "\nUsers:"
tail users/* 2> /dev/null

echo "\n\nMessages:"
tail messages/* 2> /dev/null

echo "\n\nActive py processes:"
ps -ef | grep www-data | grep startConnection.py
