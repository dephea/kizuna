from flask import Flask, render_template, url_for, request, redirect, Response
from flask_sqlalchemy import SQLAlchemy
#from datetime import datetime
from flask_migrate import Migrate




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///eyes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


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


@app.route('/')
@app.route('/home')
def index():
    events = Event.query.all()
    return render_template("kizuna_home.html", events=events)


@app.route('/store')
def store():
    items = Item.query.all()
    return render_template("store.html", items=items)


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
