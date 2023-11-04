from flask import Flask, render_template, url_for, request, redirect, Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///eyes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id

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
    return render_template("index.html")

@app.route('/kizuna')
def kizuna():
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
            return redirect('/kizuna')
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










@app.route('/member')
def member():
    members = Article.query.order_by(Article.date).all()
    return render_template("member.html", members=members)

@app.route('/member/<int:id>')
def member_about(id):
    member = Article.query.get(id)
    return render_template("member_about.html", member=member)

@app.route('/member/<int:id>/del')
def member_delete(id):
    member = Article.query.get_or_404(id)

    try:
        db.session.delete(member)
        db.session.commit()
        return redirect('/member')
    except:
        return "ERROR WHILE DELETING A MEMBER"


@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == "POST":
        title = request.form['title']
        text = request.form['text']

        article = Article(title=title, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/member')
        except:
            return "ERROR WHILE ADDING A NEW MEMBER"
    else:
        return render_template("create-article.html")


@app.route('/member/<int:id>/update', methods=['POST', 'GET'])
def member_update(id):
    member = Article.query.get(id)
    if request.method == "POST":
        member.title = request.form['title']
        member.text = request.form['text']

        try:
            db.session.commit()
            return redirect("/member")
        except:
            return "ERROR WHILE ADDING A NEW MEMBER"
    else:
        return render_template("member_update.html", member=member)



if __name__ == "__main__":
    app.run(debug=True)
