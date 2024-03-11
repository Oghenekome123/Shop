from flask import Flask, render_template,request,redirect,session,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import LoginManager,login_user,logout_user,current_user,login_required,UserMixin

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///users.db'
app.config['SECRET_KEY']="fe6b9674fb32ec6f592fbd6cb76c"
db=SQLAlchemy(app)
login_manager=LoginManager(app)
login_manager.login_view='login'


class Users(UserMixin,db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    username=db.Column(db.String(80),nullable=False,unique=True)
    password=db.Column(db.String(120),nullable=False)
    email=db.Column(db.String(15),unique=True,nullable=False)

# class Users(UserMixin):
#      def __init__(self,id):
#          self.id=id

products={
    'item1':{'id':1,'name':"Butter",'price':200,'quantity':1, 'img':'https://alfaixvillagestore.eu/wp-content/uploads/2020/04/37.jpg'},
    'item2':{'id':2,'name':"Chocolate",'price':300,'quantity':1, 'img':'https://t3.ftcdn.net/jpg/03/01/55/40/360_F_301554091_eK9O1O6WtMlDnwkGM3mswMlcGC9ZoXrI.jpg'},   
    'item3':{'id':3,'name':"Cheese",'price':50,'quantity':1, 'img':'https://www.bigbasket.com/media/uploads/p/xxl/40005021-2_3-amul-processed-cheese-block.jpg'},
    'item4':{'id':4,'name':"Yoghurt",'price':150,'quantity':1, 'img':'https://www.supermart.ng/cdn/shop/files/spar9598.jpg?v=1691144977'},
    'item5':{'id':5,'name':"Milkshake",'price':100,'quantity':1, 'img':'https://th.bing.com/th/id/OIP.Lv4cFTo4Dh-9jaYMAZi-kQHaLH?w=115&h=180&c=7&r=0&o=5&dpr=1.8&pid=1.7'},
    'item6':{'id':6,'name':"Bread",'price':400,'quantity':1, 'img':'https://th.bing.com/th?id=OIP.1UPelh2Hoxx9ImQgFaySVgHaHa&w=250&h=250&c=8&rs=1&qlt=90&o=6&dpr=1.8&pid=3.1&rm=2'}
}


cart=[]
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


# def index():
#     if current_user.is_authenticated:
#         return redirect(url_for('dashboard'))
#     else:
#         return redirect(url_for('signup'))

@app.route('/')
@app.route('/home')
def home_page():
   flash('Welcome to the Homepage')
   return render_template('home.html')

@app.route('/signup', methods=['GET','POST'])
def signup_page():
    # if current_user.is_authenticated:
    #     return redirect;{{url_for('dashboard')}}
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        hashed_password = generate_password_hash(password, method='scrypt')

        new_user = Users(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login_page'))
    return render_template('signup.html')
 
@app.route('/login', methods=['GET','POST'])
def login_page():
    # if current_user.is_authenticated:
    #     return redirect;{{url_for('dashboard')}}
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = user.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('home_page',user=user))
        else:
            flash('Invalid username or password', 'error')
    return render_template('login.html')
# @app.route('/dashboard')
# @login_required
# def dashboard():
#     return render_template('dashboard.html')

@app.route('/logout')
@login_required
def logout():
    logout_user() 
    return redirect(url_for('login'))

@app.route('/shop')
def shop_page():
    return render_template('shop.html', products = products)

# @app.route('/checkout',methods=['POST'])
# def add_to_cart():
#     product_id= int(request.form['product_id'])
#     if product_id in cart:
#       cart[product_id]['quantity']+=1
#     else:
#       cart[product_id]={'quantity':1}
   
#     return render_template('checkout.html', cart = cart)

@app.route('/checkout',methods=['POST','GET'])
def checkout():
    if request.method =='POST':
       item_id=request.form.get('item_id')
       quantity=int(request.form.get('quantity'))
       if item_id in products:
         for _ in range(quantity):
          product=products[item_id].copy()
          product[quantity]=quantity
          cart.append(products[item_id])
         return redirect('/checkout')
       else:
            return redirect('/shop')
    else:
          total_price=sum(product.get('price',0) * product.get('quantity',1) for product in cart) 
          return render_template('checkout.html',cart=cart,total_price=total_price)
    
# @app.route('/remove_item',methods=['POST'])
# def remove_item():
#     index_str=request.form.get('index','')
#     if index_str.isdigit():
#         index=int(index_str)
#         if 0 <= index < len(cart):
#            del cart[index]
#     return redirect('/shop')