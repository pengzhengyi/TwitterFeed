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

echo 'Start the server'
echo 'listening to http://localhost:8080/feed/start'
python3 swiftweet_feeder.py
