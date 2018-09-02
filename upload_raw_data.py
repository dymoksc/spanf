#!/usr/bin/env python

import argparse
import sys

from pony.orm import db_session

from spanf.entities import Data, DataFormat, Sensor

parser = argparse.ArgumentParser()
parser.add_argument('sensor_id', type=int)
parser.add_argument('data_format_id', type=int)
args = parser.parse_args()


with db_session:
    data = Data(
        dataFormat=DataFormat[args.data_format_id],
        sensor=Sensor[args.sensor_id],
        content=sys.stdin.read()
    )

print('Data was successfully imported. ID = %d' % data.id)