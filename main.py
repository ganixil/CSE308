from __init__ import create_app
from flask import Flask

#create flask app
app = create_app()
#set the server certificate and key
context = ('server.crt', 'server.key')
#run the flask app
app.run(ssl_context=context)

#cosadfasd