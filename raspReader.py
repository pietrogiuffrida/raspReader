#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import RPi.GPIO as gpio
from time import sleep
from pymongo import MongoClient
import logging
from functools import partial

import lib
import config
import private


logging.basicConfig(
  format='%(asctime)s\t%(levelname)s\t%(message)s',
  #filename=logfilename,
#  level=logging.INFO
  level=logging.DEBUG
  )

sendmail = partial(sendmail, private.senderConfig)

gpio.setmode(gpio.BOARD)
mode = gpio.IN
resistenza = gpio.PUD_UP

for channel in channels:
  try:
    logging.debug('loading {0}'.format(channel))
    gpio.setup(channel['pin'], mode, resistenza)
  except:
    logging.error('ERROR LOADING {0}, MODE {1}'.format(channel, mode))
    logging.exception('')


while True:

  for channel in channels:

    status = gpio.input(channel['pin'])

    if status != channel['status']:


      # log sicuro
      logging.info('GPIO {0}, STATUS: {1}'.format(channel['pin'], status))


      # aggiorna mongolog
      mongoUpdate(channel['pin'], status, private, config)


      # aggiorna log remoto
      # non lo so, da vedere se chiamare una qualche interfaccia


      # invia email, se previsto
      if config.messages[channel][status]['send'] != True:
        senderConfig(private.recipients,
                    config.messages[channel][status]['message'],
                    config.messages[channel][status]['message']
                    )


      # commuta stato storico
      channel['status'] = status


  sleep(delay)


gpio.cleanup()
