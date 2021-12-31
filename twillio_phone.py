# Download the helper library from https://www.twilio.com/docs/python/install
import os
from CONST import *
from twilio.rest import Client

account_sid = TWILIO_ACCOUNT_SID
auth_token = TWILIO_AUTH_TOKEN
client = Client(account_sid, auth_token)


def make_outbound_call(abonent):
    call = client.calls.create(
        twiml='<Response><Say>Ahoy, World!</Say></Response>',
        to=abonent.strip(),
        from_='+13342125274'
    )

    calls = client.calls.list()
    cur_call = calls[0]

    while cur_call.status != 'completed' and cur_call.status != 'busy':
        calls = client.calls.list()
        cur_call = calls[0]
        print(cur_call.status)

    return True
