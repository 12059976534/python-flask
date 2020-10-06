from apk import app

alow = ALLOWED_EXTENSION = set(['jpeg','jpg','png'])
con =app.config['UPLOAD_FOLDER'] = 'apk/static/upload'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSION


