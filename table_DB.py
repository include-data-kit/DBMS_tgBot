class auth_users(db.Model):
    __tablename__ = 'tbl_user'
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(45))
    user_email = db.Column(db.String(45))
    user_passwd = db.Column(db.String(45))
#DB users
class colorsTB(db.Model):
    __bind_key__ = 'db2'
    __tablename__ = 'color'

    color_id = db.Column(db.Integer, primary_key=True)
    color = db.Column(db.String(50))