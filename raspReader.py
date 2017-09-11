#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import RPi.GPIO as gpio
from time import sleep
from pymongo import MongoClient
import logging

from lib import *
from config import *
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


for pin in channels:
  channel = channels[pin]
  try:
    logging.debug('loading {0}'.format(channel))
    gpio.setup(channel['pin'], mode, resistenza)
  except:
    logging.error('ERROR LOADING {0}, MODE {1}'.format(channel, mode))
    logging.exception('')



while True:

  for pin in channels:

    channel = channels[pin]
    status = gpio.input(pin)

    # posso commutare lo status_explicit fin d'ora, ma non lo status, che è semanticamente rilevante!
    channel["status_explicit"] = stati[status]


    if status != channel['status']:


      # log sicuro
      logmsg = 'GPIO {0}, CHANNEL {1}, NAME {2}, STATUS {3}'
      logging.info(logmsg.format(pin, channel['channel'], channel['name'], channel['status_explicit']))


      # aggiorna mongolog
      mongoUpdate(pin, status_explicit, private)


      # aggiorna log remoto
      # non lo so, da vedere se chiamare una qualche interfaccia


      # invia email, se previsto
      if channel['events'][status]['send'] == True:

        sendmail(private.senderConfig, private.recipients,
                 channel['events'][status]['message'],
                 channel['events'][status]['message']
                )


      # commuto solo ora status storico
      channel['status'] = status


  sleep(delay)


gpio.cleanup()

logging.info('*'*20 + ' ESCO NORMALMENTE ' + '*'*20)
