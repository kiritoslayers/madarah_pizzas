import os
from twilio.rest import Client

account_id = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']

client = Client(account_id, auth_token)

client.messages.create(
    to = os.environ['+5511953463376'],
    from_ = os.environ['+12672140219'],
    body = 'Mensagem'
    
)