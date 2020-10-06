from apk import app,request,render_template,os,secrets,secure_filename,db,session,url_for,redirect,datetime,session,os
from apk import Flask
from apk.modul import *
from apk.model.db import User,Conten,Kategori
import calendar


@app.route('/')
def utama():
   return redirect(url_for('index'))

# def datetimeformat(value, format='%H:%M / %d-%m-%Y'):
#     return value.strftime(format)      

@app.route('/index')
def index():
   usr=User.query.all()
   cont=Conten.query.all()
   
   
   # time=environment.filters['datetimeformat'] = datetimeformat
   
   if not usr :   
      return render_template('idexlog.html',)
   print("calender saya",calendar.month(2019,1))   
   return render_template('index.html',data=cont)   

@app.route('/search',methods=['POST','GET'])
def search():
   if request.method=='POST':
      data=request.form['search']
      search='%{}%'.format(data)
      date=Conten.query.filter(Conten.tilte.like(search)).all()
      return render_template('contensearch.html',data=date,value=data)
   return render_template('contensearch.html')



#========================details conten ========================= 

@app.route('/details<int:id>')
def details(id):
   conten=Conten.query.filter_by(id=id).first()
   return render_template('detailsconten.html',data=conten)

# ===========================/===================================

#=====================admin controler================================= 

@app.route('/admin')
def admin():
   if 'user' in session:
       user=session['user'] 
       data=User.query.filter_by(user=user).first()
       if data.rol_id == 1: 
          return render_template('admin.html')
       return redirect(url_for('user'))   
   return redirect(url_for('login'))    

@app.route('/add',methods=['POST','GET'])
def add():
   if request.method =='POST':
      nama=request.form['name']
      userst=request.form['username']
      pas=request.form['password']
      gam=request.files['gambar']

      dat=User.query.filter_by(user=userst).first()

      if dat:
         return 'users al ready exist'
         
    
      if 'gambar' not in request.files:
            return '1'
      if gam.filename =='':
            return '2'
      if gam and allowed_file(gam.filename):
            namrandom= secrets.token_urlsafe(10)
            filname=secure_filename(gam.filename+namrandom)
            gam.save(os.path.join(con,filname))
            usr=User.query.all()
            if not usr:
               save= User(
               nama=nama,
               user=userst,
               pas=pas,
               gambar=filname,
               rol_id=1
              )
            else:
               save= User(
                  nama=nama,
                  user=userst,
                  pas=pas,
                  gambar=filname,
               )
            db.session.add(save)
            db.session.commit()
            return 'berhasil upload data',filname
      return "3"      
   return render_template('add.html')

@app.route('/kategori',methods=['POST','GET'])
def kategori():
   if request.method=='POST':
      kt=request.form['kategori']
      save=Kategori(
         kat=kt
      )
      if kt=="":
         return redirect(url_for('kategori'))
      db.session.add(save)
      db.session.commit()
      return redirect(url_for('kategori'))
   ktr=Kategori.query.all()   
   no=[]
   a=0
   for i in ktr:
      a+=1
      no.append(a)

   return render_template('addkt.html',data=ktr,no=no)

@app.route('/adminconten')
def adminconten():
   if 'user' in session:
      datalog=session['user']
      datalog=User.query.filter_by(user=datalog).first()
      user_id=datalog.id
      conten=Conten.query.filter_by(userku_id=user_id).all()
      no=[]
      a=0
      for i in conten:
         a+=1
         no.append(a)
      return render_template('adminconten.html',data=conten,no=no)
   return redirect(url_for('login'))   

# =============================/====================================

# ======================user controler================================

@app.route('/user')
def user():
   if 'user' in session:
       return render_template('user.html')
   return redirect(url_for('login'))    

@app.route('/usrconten')
def usrconten():
   if 'user' in session:
      datalog=session['user']
      datalog=User.query.filter_by(user=datalog).first()
      user_id=datalog.id
      conten=Conten.query.filter_by(userku_id=user_id).all()
      return render_template('userconten.html',data=conten)
   return redirect(url_for('login'))
#===========================/========================================

# =========================upload controler ================================

@app.route('/upload',methods=['POST','GET'])
def upload():
   if 'user' in session:
      if request.method=='POST':
         s=session['user']
         user=User.query.filter_by(user=s).first()
         title=request.form['title']
         isi=request.form['isi']
         kat=request.form.get('kategori')
         ket=request.form['ket']
         kteg=Kategori.query.filter_by(kat=kat).first()
         id_kateg=kteg.id
         save=Conten(tilte=title,isi=isi,data_time=datetime.now(),userku_id=user.id, ket=ket,  kategori_id=id_kateg)
         db.session.add(save)
         db.session.commit()
         return 'berhasil di upload'

      ktr= Kategori.query.all()
      ar=[]
      for i in ktr:
         ar.append(i.kat)
      ar.insert(0,'--pilih kategori--')

      log=session['user']
      datalogin=User.query.filter_by(user=log).first()
      if datalogin.rol_id==1:
         return render_template('upload.html',data=ar)
      return render_template('userupload.html',data=ar)  
   return redirect(url_for('login'))    

   # ======================================/=================================

# =============================update controler===========================

@app.route('/update<id>',methods=['POST','GET'])
def method_name(id):
    data=Conten.query.filter_by(id=id).first()
    kat=Kategori.query.all()
    kategori=data.kategori.kat
    arr=[]
    for i in kat:
       arr.append(i.kat)   
    t=data.kategori.kat
    arr.remove(t)
    arr.insert(0,t)

    if request.method == 'POST':
      title=request.form['title']
      kategori=request.form.get('kategori')
      keterangan=request.form['keterangan']
      isi=request.form['isi']
      ka=Kategori.query.filter_by(kat=kategori).first() 

      data.tilte=title
      data.isi=isi
      data.ket=keterangan
      data.data_time=datetime.now()
      data.kategori_id=ka.id
      db.session.commit()
      return 'berhasil di update'
       
    return render_template('updateconten.html',data=data, k = arr)

 # ====================================/===================================

@app.route('/delete<id>',methods=['GET'])
def delet(id):
   data=Kategori.query.filter_by(id=id).first()
   db.session.delete(data)
   db.session.commit()
   return redirect(url_for('kategori'))

# @app.route('/addadmin')
# def addadmin():
#    return render_template('newadd.html')


@app.route('/login', methods=['POST','GET'])
def login():
   if 'user' in session:
      user=session['user']   
      data=User.query.filter_by(user=user).first()
      if data.rol_id==1:
         return redirect(url_for('admin'))
      elif data.rol_id==2:
         return redirect(url_for('user'))

   if request.method=='POST':
      usr=request.form['username']
      paswords=request.form['password']
      user=User.query.filter_by(user=usr).first()
      rol=user.rol_id
      if user:
         if user.pas == paswords:
            session['user']=str(user.user)
            if rol == 1:
               return redirect(url_for('admin'))
            return redirect(url_for('user'))   
         return 'posword  and password not compatible'   
      return 'user not exist'      
   return render_template('login.html')

@app.route('/logout')
def logout():
   session.pop('user',None)
   return redirect(url_for('index'))


@app.after_request
def after_request(response):
    response.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
    return response   