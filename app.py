from flask import Flask, render_template, request, session, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost:3306/auth_web'
app.config['SQLALCHEMY_BINDS'] = {'db2': 'mysql+pymysql://username:password@localhost:3306/users'}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = 'why would I tell you my secret key?'
db = SQLAlchemy(app)

#DATABASE---------------------------------------
#DB auth_web
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
#DB material
class materialTD(db.Model):
    __bind_key__ = 'db2'
    __tablename__ = 'material'

    material_id = db.Column(db.Integer, primary_key=True)
    material = db.Column(db.String(50))
    

#DB categoriesl
class categoriesTD(db.Model):
    __bind_key__ = 'db2'
    __tablename__ = 'categories'

    categorie_id = db.Column(db.Integer, primary_key=True)
    categorie = db.Column(db.String(50))

# #DB customersTD
class customersTD(db.Model):
    __bind_key__ = 'db2'
    __tablename__ = 'customers'

    telegram_id = db.Column(db.Double, primary_key=True)
    bot = db.Column(db.Boolean)
    customer_fname = db.Column(db.String(50))
    customer_lname = db.Column(db.String(50))
    username =  db.Column(db.String(50))
    phone = db.Column(db.String(15))

# #DB productsTD
class productsTD(db.Model):
    __bind_key__ = 'db2'
    __tablename__ = 'products'

    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(255))
    categorie_id = db.Column(db.Integer, db.ForeignKey("categoriesTD.categorie_id"))
    material_id = db.Column(db.Integer, db.ForeignKey("materialTD.material_id"))
    color_id = db.Column(db.Integer, db.ForeignKey("colorsTB.color_id"))

# #DB price
class priceTD(db.Model):
    __bind_key__ = 'db2'
    __tablename__ = 'price_change'

    product_id = db.Column(db.Integer, primary_key=True)
    date_price_change = db.Column(db.TIMESTAMP, primary_key=True)
    new_price = db.Column(db.Double)

#DB purchases
# class purchasesTB(db.Model):
#     __bind_key__ = 'db2'
#     __tablename__ = 'purchases'

#     purchase_id =  db.Column(db.Integer, primary_key=True)
#     customer_id = db.Column(db.Integer, db.ForeignKey("customersTD.telegram_id"))
#     purchase_date = db.Column(db.TIMESTAMP)

# #DB purchases_item
# class purchases_itemTB(db.Model):
#     __bind_key__ = 'db2'
#     __tablename__ = 'purchases_item'

#     purchase_id = db.Column(db.Integer, primary_key=True)
#     product_id = db.Column(db.Integer, primary_key=True)
#     product_count = db.Column(db.Integer)
#     product_price = db.Column(db.Double)

#END DATABASE----------------------------------------------
@app.route('/')
def main():
    return render_template('index.html')

@app.route('/signin')
def showSignin():
    return render_template('signin.html')

@app.route('/validateLogin', methods=['POST'])
def validateLogin():
    try:
        _username = request.form['inputEmail']
        _password = request.form['inputPassword']

        #connect to mysql
        connection = db.engine.raw_connection()
        cursor = connection.cursor()
        cursor.callproc('sp_validateLogin', (_username,))
        data = cursor.fetchall()
        print(data)
        #check password in table_db
        if len(data) > 0:
            if str(data[0][3] ==_password):
                session['user'] = data[0][0]
                return redirect('/userhome')
            else:
                return render_template('error.html', error='Wrong Email address or Password 12')
        else:
            return render_template('error.html', error='Wrong Email address or Password')
    except Exception as e:
        return render_template('error.html', error=str(e))
    finally:
        connection.close() 

#access to userhome
@app.route('/userhome')
def userhome():
    if session.get('user'):
        return render_template('userhome.html')
    else:
        return render_template('error.html', error='Unauthorized Access')

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')

#PAGES-----------------------------------------
#Page Color
@app.route('/color')
def colors():
    if session.get('user'):
        data = colorsTB.query.all()
        return render_template('color.html', colors=data)
    else:
        return render_template('error.html', error='Unauthorized Access')
# Page material
@app.route('/material')
def material():
    if session.get('user'):
        data = materialTD.query.all()
        return render_template('material.html', materials=data)
    else:
        return render_template('error.html', error='Unauthorized Access')
@app.route('/categories')
def TD_categories():
    if session.get('user'):
        data = categoriesTD.query.all()
        return render_template('categories.html', categories=data)
    else:
        return render_template('error.html', error='Unauthorized Access')

@app.route('/customers')
def customers():
    if session.get('user'):
        data = customersTD.query.all()
        return render_template('customers.html', customers=data)
    else:
        return render_template('error.html', error='Unauthorized Access')

@app.route('/products')
def products ():
    if session.get('user'):
        data = productsTD.query.all()
        color = colorsTB.query.all()
        material = materialTD.query.all()
        categorie = categoriesTD.query.all()
        return render_template('products.html', products=data, 
                                                colors=color,
                                                materials=material,
                                                categories=categorie)
    else:
        return render_template('error.html', error='Unauthorized Access')

#END PAGES------
# TEMPLATE
# @app.route('/')
# def ():
#     if session.get('user'):
#         data = colorsTB.query.all()
#         return render_template('.html', colors=data)
#     else:
#         return render_template('error.html', error='Unauthorized Access')
#END PAGES----------------------------------------------
# @app.route('/TB_delete/', methods=['GET'])
@app.route('/TB_delete', methods=['POST'])
def TB_delete ():
    try:
        data = request.get_json()
        if data['page'] == 'page_Color':
            rowDel = colorsTB.query.filter_by(color_id=data['testing'][0]).one()
            db.session.delete(rowDel)
            db.session.commit()
            return jsonify({'message': 'Строка удалена!'})
        elif data['page'] == 'page_mat':
            rowDel = materialTD.query.filter_by(material_id=data['testing'][0]).one()
            db.session.delete(rowDel)
            db.session.commit()
            return jsonify({'message': 'Строка изменена!'})           
        elif data['page'] == 'page_cat':
            rowDel = categoriesTD.query.filter_by(categorie_id=data['testing'][0]).one()
            db.session.delete(rowDel)
            db.session.commit()
            return jsonify({'message': 'Строка изменена!'})
        elif data['page'] == 'page_products':
            rowDel = productsTD.query.filter_by(product_id=data['testing'][0]).one()
            db.session.delete(rowDel)
            db.session.commit()
            return jsonify({'message': 'Строка изменена!'}) 
    except Exception as e:
        return jsonify({'message': e})

@app.route('/TB_add', methods=['POST'])
def TB_add ():
    try:
        data = request.get_json()
        if data['page'] == 'page_Color':
            rowAdd = colorsTB(color=data['addQuery'])
            db.session.add(rowAdd)
            db.session.commit()
            return jsonify({'message': 'Строка добавлена!'})
        elif data['page'] == 'page_mat':
            rowAdd = materialTD(material=data['addQuery'])
            db.session.add(rowAdd)
            db.session.commit()
            return jsonify({'message': 'Строка добавлена!'})
        elif data['page'] == 'page_cat':
            rowAdd = categoriesTD(categorie=data['addQuery'])
            db.session.add(rowAdd)
            db.session.commit()
            return jsonify({'message': 'Строка добавлена!'})
        elif data['page'] == 'page_products':
            rowAdd = productsTD(product_name=data['Description'])
            # rowAdd = productsTD(product_name=data['Description'],data['Categories'], data['Material'], data['Color'])
            db.session.add(rowAdd)
            db.session.commit()
            return jsonify({'message': 'Строка добавлена!'})
    except Exception as e:
            print(e)
            return jsonify({'message': e})


@app.route('/TB_edit', methods=['POST'])
def TB_edit ():
    try:
        data = request.get_json()
        if data['page'] == 'page_Color':
            rowEdit = colorsTB.query.filter_by(color_id=data['testing'][0]).one()
            rowEdit.color = data['editQuery']
            db.session.commit()
            return jsonify({'message': 'Строка изменена!'})
        elif data['page'] == 'page_mat':
            rowEdit = materialTD.query.filter_by(material_id=data['testing'][0]).one()
            rowEdit.material = data['editQuery']
            db.session.commit()
            return jsonify({'message': 'Строка изменена!'})
        elif data['page'] == 'page_cat':
            rowEdit = categoriesTD.query.filter_by(categorie_id=data['testing'][0]).one()
            rowEdit.categorie = data['editQuery']
            db.session.commit()
            return jsonify({'message': 'Строка изменена!'})
        elif data['page'] == 'page_products':
            rowEdit = productsTD.query.filter_by(product_id=data['testing'][0]).one()
            rowEdit = productsTD(product_name=data['Description'],
                                categorie_id=data['Categories'],
                                material_id=data['Material'],
                                color_id=data['Color'],
                                )
            db.session.commit()
            return jsonify({'message': 'Строка добавлена!'})
    except Exception as e:
        print(e)
        return jsonify({'message': e})


if __name__ == '__main__':
    app.run()