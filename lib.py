#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from pymongo import MongoClient
import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import pandas as pd



def sendmail(senderConfig, toaddr, text, sbj, allegati=None):

  try:
    logging.debug('Invio email {0}'.format(sbj))
    msg = MIMEMultipart()
    msg['Subject'] = '{0} -> {1}'.format(sbj, datetime.today().strftime('%Y-%m-%d %H:%M'))
#    msg['Subject'] = sbj
    msg['From'] = senderConfig["fromaddr"]
#    msg['From'] = "Belice"

    text = text + '\n' + datetime.today().strftime('%Y-%m-%d %H:%M')
    testo = MIMEText(text, 'html', 'utf-8')
    msg.attach(testo)

    if allegati != None:

      if type(allegati) == str:
        allegati = [allegati]

      for filename in allegati:
        attachment = open(filename, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename.split('/')[-1])
        msg.attach(part)

    s = smtplib.SMTP_SSL(senderConfig["smtp"])
#    s.starttls()
    s.login(senderConfig['fromaddr'], senderConfig['password'])

    if type(toaddr) == str:
      toaddr = [toaddr]

    for addr in toaddr:
      msg['To'] = addr
      s.sendmail(senderConfig['fromaddr'], addr, msg.as_string())

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
#    logging.exception('')
    return 1, None, None



def recentUpdates(private):
  mongoStatus, collection, connection = mongoConnect(private.mongo_config)
  yesterday = datetime.now() - timedelta(days=1)
  recent_data = list(collection.find({'timestamp': {"$gt": yesterday}}, {'_id': 0}))
  connection.close()
  df = pd.DataFrame(recent_data)
  return df.to_html()



def mongoUpdate(pin, channel, private):

  mongoStatus, collection, connection = mongoConnect(private.mongo_config)

  if mongoStatus == 0:
    collection.insert({'gpio': pin,
                       'status': channel["status_explicit"],
                       'timestamp': channel['timestamp'],
                       'channel': channel['channel'],
                       'name': channel['name'],
                     })
    connection.close()

  else:
    sendmail(private.senderConfig, private.error_recipient,
             "IMPOSSIBILE CONNETTERSI A MONGODB", "IMPOSSIBILE CONNETTERSI A MONGODB")
