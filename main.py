from __init__ import create_app
from flask import Flask
import logging
import logging.handlers
#from flask.ext.uploads import UploadSet, configure_uploads, IMAGES

#logging module implementation

logging.basicConfig(filename='supercanvasser.log',filemode='w',level = logging.DEBUG)

#create flask app
logging.debug('Starting Super Canvasser')
app = create_app()

logging.info('app created successfully')

# photos = UploadSet('photos', IMAGE)

# app.config['UPLOADED_PHOTOS_DEST'] = 'static/image'
# configure_uploads(app, photos)

#set the server certificate and key
context = ('server.crt', 'server.key')

logging.info('server cert and key set successfully')
#run the flask app

logging.info("run app")
app.run(ssl_context=context, debug=True)


#cosadfasd