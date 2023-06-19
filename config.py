app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost:3306/auth_web'
app.config['SQLALCHEMY_BINDS'] = {'db2': 'mysql+pymysql://username:password@localhost:3306/users'}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = 'why would I tell you my secret key?'