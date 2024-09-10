from airtable import Airtable
from dotenv import load_dotenv
from os import path
import os
import time
from twilio.rest import Client
import json

def twilio_message(csid, bdy, recipient, content_variables):

  account_sid = TWILIO_ACCOUNT_SID
  auth_token = TWILIO_AUTH_TOKEN
  client = Client(account_sid, auth_token)

  message = client.messages.create(
    content_sid=csid,
    messaging_service_sid=MESSAGING_SERVICE_SID,
    content_variables=content_variables,
    to=f'whatsapp:{recipient}',
  )


def send_whatsapp(record):
    msg_counter = 0
    phone_number = record['fields']['phone_number']
    print(phone_number)
    id = record['id']
    twilio_dict ={ENGLISH_INVITATION_TEMPLATE: 'Hope to See you there! Please click the link to RSVP :)',
                  HEBREW_INVITATION_TEMPLATE:'נשמח לראותכם! אנא לחץ/י על הקישור כדי להגיב :)',
                  }
    # Adding the link with the dynamic id to the dictionary
    link_template_sid = LINK_TEMPLATE_SID
    link = f'RSVP Here \n {SITE_ADDRESS}/{id}'
    twilio_dict[link_template_sid] = link
    
    for content_sid in twilio_dict:
        content_variables = json.dumps({'1':id})
        body = twilio_dict[content_sid]

        if msg_counter ==2:
            time.sleep(5) # sleep so it sends the link after it sends both pictures
        twilio_message(content_sid, body, phone_number, content_variables)
        msg_counter +=1

def bus_rsvp(record):
    phone_number = record['fields']['number']
    print(phone_number)
    twilio_message(BUS_RSVP_SID,bdy=None,recipient=phone_number,content_variables=None)

def send_invitation():
  airtable = Airtable(base_id, table_name, api_key)
      
    # Fetch all records from the table
  records = airtable.get_all()

  # Print the records
  for record in records:
      # print(record['fields']['phone_number'])
      if record['fields']['invited'] == '0':
        send_whatsapp(record)
        airtable.update(record['id'], {'invited': '1'})

def send_bus_rsvp():
     airtable = Airtable(base_id, bus_table, api_key)
     records = airtable.get_all()

     for record in records:
      # print(record['fields']['phone_number'])
      if record['fields']['invited'] == '0':
        bus_rsvp(record)
        airtable.update(record['id'], {'invited': '1'})

if __name__ == "__main__":
    basedir = path.abspath(path.dirname(__file__))
    load_dotenv(path.join(basedir, ".env"))

    # Replace with your Airtable API key, Base ID, and Table Name
    api_key =       os.getenv('AIRTABLE_API_KEY')
    base_id =       os.getenv('AIRTABLE_BASE_ID')
    table_name =    os.getenv('AIRTABLE_TABLE_NAME')
    bus_table =     os.getenv('BUS_TABLE')

    # image Paths 
    english_invation_path =   os.getenv('ENGLISH_INVITATION_PATH')
    hebrew_invitation_path =  os.getenv('HEBREW_INVITATION_PATH')

    # parse twilio
    TWILIO_ACCOUNT_SID =            os.getenv('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN =             os.getenv('TWILIO_AUTH_TOKEN')
    LINK_TEMPLATE_SID =             os.getenv('LINK_TEMPLATE_SID')
    ENGLISH_INVITATION_TEMPLATE =   os.getenv('ENGLISH_INVITATION_TEMPLATE')
    HEBREW_INVITATION_TEMPLATE =    os.getenv('HEBREW_INVITATION_TEMPLATE')
    SITE_ADDRESS =                  os.getenv('SITE_ADDRESS')
    MESSAGING_SERVICE_SID =         os.getenv('MESSAGING_SERVICE_SID')
    CARD_SID =                      os.getenv('CARD_SID')
    BUS_RSVP_SID =                  os.getenv('BUS_RSVP_TEMPLATE')

    # Initialize image list
    img_list = [english_invation_path, hebrew_invitation_path]


    send_invitation()
