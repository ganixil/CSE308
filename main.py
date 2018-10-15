from __init__ import create_app
from flask import Flask
#from flask.ext.uploads import UploadSet, configure_uploads, IMAGES

#create flask app
app = create_app()
# photos = UploadSet('photos', IMAGE)

# app.config['UPLOADED_PHOTOS_DEST'] = 'static/image'
# configure_uploads(app, photos)

#set the server certificate and key
context = ('server.crt', 'server.key')
#run the flask app

app.run(ssl_context=context, debug=True)


#cosadfasd