#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import RPi.GPIO as gpio
from time import sleep
from pymongo import MongoClient
import logging

from lib import *
import config
import private


logging.basicConfig(
  format='%(asctime)s\t%(levelname)s\t%(message)s',
  filename=config.logfilename,
  level=logging.INFO
#  level=logging.DEBUG
  )

logging.info('*'*20 + ' NUOVA ESECUZIONE ' + '*'*20)

gpio.setmode(gpio.BOARD)
mode = gpio.IN
resistenza = gpio.PUD_UP

for channel in config.channels:
  try:
    logging.debug('loading {0}'.format(channel))
    gpio.setup(channel['pin'], mode, resistenza)
  except:
    logging.error('ERROR LOADING {0}, MODE {1}'.format(channel, mode))
    logging.exception('')


while True:

  for channel in config.channels:

    status = gpio.input(channel['pin'])
    status_explicit = config.stati[gpio.input(channel['pin'])]
    pin = channel['pin']

    if status != channel['status']:


      # log sicuro
      logging.info('GPIO {0}, CHANNEL {1}, NAME {2}, STATUS: {3}'.format(pin, channel['channel'], channel['name'], status_explicit))


      # aggiorna mongolog
      mongoUpdate(pin, status_explicit, private, config)


      # aggiorna log remoto
      # non lo so, da vedere se chiamare una qualche interfaccia


      # invia email, se previsto
      if config.messages[pin][status]['send'] == True:
        sendmail(private.senderConfig, private.recipients,
                 config.messages[pin][status]['message'],
                 config.messages[pin][status]['message']
                )


      # commuta stato storico
      channel['status'] = status


  sleep(config.delay)


gpio.cleanup()

logging.info('*'*20 + ' ESCO NORMALMENTE ' + '*'*20)
