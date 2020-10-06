from apk import db,datetime


class Conten(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    tilte=db.Column(db.Text(),nullable = False)
    isi=db.Column(db.Text(),nullable = False)
    ket=db.Column(db.Text(),nullable = False)
    data_time=db.Column(db.DateTime,nullable = False)
    userku_id=db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)   
    kategori_id=db.Column(db.Integer, db.ForeignKey('kategori.id'),nullable=False)   
     

class Kategori(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    kat=db.Column(db.String(100),nullable = False)
    rel=db.relationship('Conten',backref='kategori',lazy=True)


class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    nama=db.Column(db.String(100),nullable = False)
    user=db.Column(db.String(100))
    pas=db.Column(db.String(20))
    gambar=db.Column(db.Text(),nullable = False) 
    rol_id=db.Column(db.Integer, db.ForeignKey('rol.id'), nullable = False, default = 2)    
    addresses = db.relationship('Conten', backref='user', lazy=True)

class Rol(db.Model):
    id=db.Column(db.Integer,primary_key=True,nullable=False)
    level=db.Column(db.String(20),nullable = False)
    relasi=db.relationship('User', backref='rol', lazy=True)
    

# class Person(db.Model): 
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), nullable=False)
#     addresses = db.relationship('Address', backref='person', lazy=True)

# class Address(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120), nullable=False)
#     person_id = db.Column(db.Integer, db.ForeignKey('person.id'),
#         nullable=False)        


