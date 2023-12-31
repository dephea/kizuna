from flask import Flask, render_template, url_for, request, redirect, Response
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from flask import session
from flask_migrate import Migrate
from uuid import uuid4
import logging

logging.basicConfig(level=logging.DEBUG)


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///eyes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.secret_key = 'asdfPOMPOas718399qw980_'

app.permanent_session_lifetime = timedelta(days=30)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255), nullable=True)  # Image URL should be public access

    def __repr__(self):
        return '<Event %r>' % self.id


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(255), nullable=True)  # Image URL should be public access

    def __repr__(self):
        return '<Item %r>' % self.id




@app.before_request
def ensure_session():
    if 'user_session' not in session:
        session['user_session'] = str(uuid4())
        session.permanent = True
        logging.debug(f"New session created: {session['user_session']}")
    else:
        logging.debug(f"Existing session: {session['user_session']}")


@app.route('/')
@app.route('/home')
def index():

    events = Event.query.all()
    return render_template("kizuna_home.html", events=events)


@app.route('/store')
def store():
    items = Item.query.all()
    return render_template("store.html", items=items, session=session)


@app.route('/add_to_cart/<int:item_id>')
def add_to_cart(item_id):
    item = Item.query.get(item_id)

    if 'cart' not in session:
        session['cart'] = {}

    try:
        # Преобразуем ключ к строке, потому что ключи в словаре session['cart'] всегда сохраняются как строки
        item_id_str = str(item_id)

        if item_id_str in session['cart']:
            session['cart'][item_id_str] = int(session['cart'][item_id_str]) + 1
            logging.debug(f"Increased quantity for {item.name}.")
        else:
            session['cart'][item_id_str] = 1
            logging.debug(f"Added {item.name} to cart.")

        session.modified = True

        # Для логирования создаем словарь с именами вместо ID
        cart_for_logging = {Item.query.get(int(key)).name: value for key, value in session['cart'].items()}
        logging.debug(f"Cart updated: {cart_for_logging}")

    except Exception as e:
        logging.error(f"Error adding item to cart: {e}")
        raise

    return redirect(url_for('store'))



@app.route('/create_item', methods=['POST', 'GET'])
def create_item():
    items = Item.query.all()
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        image_url = request.form['image_url']


        item = Item(name=name, description=description, price=price, image_url=image_url)

        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/store')
        except:
            return "ERROR WHILE ADDING A NEW PRODUCT"
    else:
        return render_template("create_item.html", items=items)


@app.route('/create_event', methods=['POST', 'GET'])
def create_event():
    events = Event.query.all()
    if request.method == "POST":
        title = request.form['title']
        description = request.form['description']
        image_url = request.form['image_url']


        event = Event(title=title, description=description, image_url=image_url)

        try:
            db.session.add(event)
            db.session.commit()
            return redirect('/')
        except:
            return "ERROR WHILE ADDING A NEW EVENT"
    else:
        return render_template("create_event.html", events=events)

@app.route('/delete_event/<int:id>', methods=['GET', 'POST'])
def delete_event(id):
    event_to_delete = Event.query.get_or_404(id)
    try:
        db.session.delete(event_to_delete)
        db.session.commit()
        return redirect('/create_event')
    except:
        return "ERROR WHILE DELETING THE EVENT"

@app.route('/about')
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)
