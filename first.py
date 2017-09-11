#!/usr/bin/env python3

import RPi.GPIO as GPIO
from time import sleep
from config import *

import logging
logging.basicConfig(
  format='%(asctime)s\t%(levelname)s\t%(message)s',
#  filename=logfile,
#  level=logging.INFO
  level=logging.DEBUG
  )

GPIO.setmode(GPIO.BOARD)
mode = GPIO.IN
# di default legge 1, commuta 0 se eccitato
resistenza = GPIO.PUD_UP

for channel in channels:
  try:
    logging.debug('loading {0}'.format(channel))
    GPIO.setup(channel['pin'], mode, resistenza)
  except:
    logging.error('ERROR LOADING {0}, MODE {1}'.format(channel, mode))
    logging.exception('')


while True:
  for channel in channels:

    if GPIO.input(channel['pin']) != channel['status']:
      logging.warning('GPIO {0} INPUT MODE, STATUS: {1}'.format(channel['pin'], GPIO.input(channel['pin'])))
      channel['status'] = GPIO.input(channel['pin'])

  sleep(1)


GPIO.cleanup()



