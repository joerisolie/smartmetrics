#!/bin/bash
cd /root/smartmetrics
source venv/bin/activate
python get_smart_values.py /dev/sda 
python get_smart_values.py /dev/sdb
