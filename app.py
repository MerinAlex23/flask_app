from flask import Flask,render_template,flash,redirect,request,url_for,session,logging
from data import Articles
# from flask_mysqldb import MySQL

from flaskext.mysql import MySQL
from flaskext.mysql import MySQL


from wtforms import Form,StringField,TextAreaField,validators,PasswordField
from passlib.hash import sha256_crypt

app=Flask(__name__)
#config MySQL

app.config['MYSQL_HOST']='%'
app.config['MYSQL_USER']='Merin'
app.config['MYSQL_PASSWORD']='mamp@23'
app.config['MYSQL_DB']='myflaskapp'
app.config['MYSQL_CURSORCLASS']='DictCursor'

#init MySQLmysqk

mysql = MySQL()
mysql.init_app(app)

# mysql=MySQL(app)

# mysql = MySQL()
# mysql.init_app(app)



Articles=Articles()
@app.route('/')
def index():
    return render_template('home.html')
@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/articles')
def articles():
    return render_template('articles.html',articles=Articles)

@app.route('/article/<string:id>/')
def article(id):
    return render_template('article.html',id=id)

class RegisterForm(Form):
    name = StringField('name', [validators.Length(min=4, max=25)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm=PasswordField('Confirm password')




@app.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name=form.name.data
        email=form.email.data
        username=form.username.data
        password=sha256_crypt.encrypt(str(form.password.data))


        #create Cursor
        # cur =mysql.connection.cursor()
        cur = mysql.get_db().cursor()


        cur.execute("INSERT INTO users(name,email,username,password) VALUES(%s, %s, %s, %s)",(name,email,username,password))
        mysql.connection.commit()
        cur.close()
        flash('you are now registered and log in','success')
        return redirect(url_for('index'))
        # return render_template('register.html')
    return render_template('register.html',form=form)

if __name__=='__main__':
    app.secret_key='secret123'
    app.run(debug=True)
