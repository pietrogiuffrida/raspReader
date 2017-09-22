#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import datetime
from flask import Flask, request
import json
import os
import RPi.GPIO as gpio
from time import sleep
from pymongo import MongoClient
import logging
import threading

from pypid.pid import *
from jdserializer.jdserializer import jdserializer

from lib import *
from config import *
import private

env = Environment(
    loader=FileSystemLoader(root + 'jtemplate'),
    autoescape=select_autoescape(['html', 'xml'])
)
template = env.get_template('jtemplate.txt')


logging.basicConfig(
#  format='%(asctime)s\t%(levelname)s\t%(pathname)s\t%(message)s',
  format='%(asctime)s\t%(levelname)s\t%(message)s',
  filename=logfilename,
  level=logging.INFO
#  level=logging.DEBUG
  )
logging.getLogger("flask").setLevel(logging.WARNING)
logging.getLogger("werkzeug").setLevel(logging.WARNING)


def continuosly(channels, delay):

  for pin in channels:

    # fisso il quando
    now = datetime.now()

    # leggo lo status
    status = gpio.input(pin)

    # leggo la configurazione del channel
    channel = channels[pin]

    # reagisco ad eventuali cambiamenti di stato
    if status != channel['status']:

      # ----> commuto lo status e fisso il now
      channel["status_explicit"] = stati[status]
      channel['status'] = status
      channel['timestamp'] = now

      # 1. local log file
      logmsg = 'GPIO {0}, CHANNEL {1}, NAME {2}, STATUS {3}, {4}'
      logging.info(logmsg.format(pin, channel['channel'], channel['name'], channel['status_explicit'], channel['timestamp']))

      # 2. aggiorna mongolog
      mongoUpdate(pin, channel, private)

      # 3. aggiorna log remoto

      # 4. invia email, se previsto
      if channel['events'][status]['send'] == True:
        sendmail(private.senderConfig, private.recipients,
                 channel['events'][status]['message'],
                 channel['events'][status]['message']
                )

  sleep(delay)


app = Flask(__name__)
#app.logger.setLevel(logging.ERROR)


@app.route('/mail', methods=['GET'])
def mail():
  try:
    logging.info('mail')

    msg = ''
    for pin in channels:
      channel = channels[pin]
      if channel.get('timestamp'):
        dt = channel["timestamp"].strftime('%Y/%m/%d %H:%M:%S')
      else:
        dt = '00'
      msg += ' '.join(['<p>', channel['name'], channel.get('status_explicit', 'OFF'), 'dal', dt, '</p>'])
    
    sendmail(private.senderConfig, private.recipients, msg, 'Sintesi')
    return 'Send'
  except:
    logging.error('check mail error')
    logging.exception('')
    return 'Nope!'


@app.route('/check', methods=['GET'])
def one_shot():
  try:
    logging.info('one shot')
#    return json.dumps(channels, default=jdserializer)
    return template.render(out=channels)
  except:
    logging.error('check one shot error')
    logging.exception('')
    return 'Nope!'


@app.before_first_request
def timpano():
  logging.info('STARTING CONTINUOS CHEK')

  def run_job():
    while True:
      continuosly(channels, delay)

  continuo = threading.Thread(target=run_job, name="continuo")
  continuo.setDaemon(True)
  continuo.start()


if __name__ == '__main__':


  logging.info('*'*20 + ' NUOVA ESECUZIONE ' + '*'*20)


  # * ** * ** ** * *** ** * ** ** * *** ** * ** ** * *** ** * ** ** * *** ** * ** ** * **
  # PID LOCK
  # * ** * ** ** * *** ** * ** ** * *** ** * ** ** * *** ** * ** ** * *** ** * ** ** * **

  pid_status = checkpid(pidfile)
  if pid_status == 3:
    logging.error('ESCO IMMEDIATAMENTE --> PID')

    sleep(2)
    sendmail(private.senderConfig, private.error_recipients,
            'TENTATO NUOVO RUN, PID CONFLICT',
            'TENTATO NUOVO RUN, PID CONFLICT', 'log/reader.log')

    os._exit(1)

  elif pid_status in [1, 3]:
    logging.info('IL PROCESSO RISULTA CESSATO, SOVRASCRIVO IL PID')

  writeLockfile(pidfile)


  # * ** * ** ** * *** ** * ** ** * *** ** * ** ** * *** ** * ** ** * *** ** * ** ** * **
  # CONFIGURAZIONE DEI PIN
  # * ** * ** ** * *** ** * ** ** * *** ** * ** ** * *** ** * ** ** * *** ** * ** ** * **

  gpio.setmode(gpio.BOARD)
  mode = gpio.IN
  resistenza = gpio.PUD_UP

  for pin in channels:
    channel = channels[pin]
    try:
      logging.debug('loading {0}'.format(channel))
      gpio.setup(pin, mode, resistenza)
    except:
      logging.error('ERROR LOADING {0}, MODE {1}'.format(channel, mode))
      logging.exception('')

      sleep(2)
      sendmail(private.senderConfig, private.error_recipients,
              'IMPOSSIBILE CONFIGURARE GPIO {}'.format(pin),
              'IMPOSSIBILE CONFIGURARE GPIO {}'.format(pin), 'log/reader.log')

      deleteLockfile(pidfile)
      os._exit(1)


  # * ** * ** ** * *** ** * ** ** * *** ** * ** ** * *** ** * ** ** * *** ** * ** ** * **
  # Running Flask
  # * ** * ** ** * *** ** * ** ** * *** ** * ** ** * *** ** * ** ** * *** ** * ** ** * **

  host = "0.0.0.0"
  port = 5000
  app.run(host=host, port=port, debug=False)


  # * ** * ** ** * *** ** * ** ** * *** ** * ** ** * *** ** * ** ** * *** ** * ** ** * **
  # LETTURA DELLO STATUS E REAZIONI VARIE
  # * ** * ** ** * *** ** * ** ** * *** ** * ** ** * *** ** * ** ** * *** ** * ** ** * **

#  while True:
#    pinStatus(channels, delay)


gpio.cleanup()

logging.info('*'*20 + ' ESCO NORMALMENTE ' + '*'*20)
