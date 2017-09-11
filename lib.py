#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from pymongo import MongoClient
import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.mime.multipart import MIMEMultipart
from datetime import datetime


def sendmail(senderConfig, toaddr, text, sbj, allegati=[]):

  try:
    logging.debug('Invio email {0}'.format(sbj))
    msg = MIMEMultipart()
    msg['Subject'] = '{0} {1}'.format(sbj, datetime.today().strftime('%Y-%m-%d %H:%M'))
    msg['From'] = senderConfig["fromaddr"]
    msg['To'] = to

    testo = MIMEText(text, 'html', 'utf-8')
    msg.attach(testo)

    if allegati != []:
      for filename in allegati:
        attachment = open(filename, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        msg.attach(part)

    s = smtplib.SMTP(senderConfig["smtp"])
    s.starttls()
    s.login(senderConfig['fromaddr'], senderConfig['password'])
    s.sendmail(senderConfig['fromaddr'], to, msg.as_string())
    s.quit()

  except:
    logging.error("IMPOSSIBILE INVIARE L'EMAIL!")
    logging.exception('')



def mongoConnect(mongo_config):

  try:
    connection = MongoClient(
      mongo_config['host'],
      mongo_config['port'],
      )
    db = connection[mongo_config['db']]
    collection = db[mongo_config['collection']]
    return 0, collection, connection

  except:
    logging.error('IMPOSSIBILE CONNETTERSI A MONGODB')
    logging.exception('')
    return 1, None, None



def mongoUpdate(pin, status, private, config):

  mongoStatus, collection, connection = lib.mongoConnect(private.mongo_config)

  if mongoStatus == 0:
    collection.insert({'GPIO': pin, 'STATUS': status})
    connection.close()

  else:
    sendmail(private.error_recipient,
              config.mongo_error_message,
              config.mongo_error_sbj)
