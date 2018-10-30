#!/bin/bash

if [[ $(pip3 show selenium) ]];
then
				echo 'selenium has already been installed'
else
				echo 'installing selenium...'
				pip3 install selenium
fi

if [[ $(pip3 show bs4) ]];
then
				echo 'bs4 has already been installed'
else
				echo 'installing bs4...'
				pip3 install bs4
fi

unameOut="$(uname -s)"
case "${unameOut}" in
    Linux*)     machine=Linux;;
    Darwin*)    machine=Mac;;
    CYGWIN*)    machine=Cygwin;;
    MINGW*)     machine=MinGw;;
    *)          machine="UNKNOWN:${unameOut}"
esac
echo "Operating System: [${machine}]"


echo 'Start the server'
echo 'listening to http://localhost:8080/feed/start'
python3 swiftweet_feeder.py
