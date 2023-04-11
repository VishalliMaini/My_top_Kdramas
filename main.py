from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

##CREATE DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.app_context().push()

##CREATE TABLE
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Float, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String(250), nullable=True)
    img_url = db.Column(db.String(250), nullable=False)
db.create_all()



## After adding the new_movie the code needs to be commented out/deleted.
## So you are not trying to add the same movie twice.
'''new_movie = Movie(
 title="It's okay not to be okay",
   year=2022,
 description="A story about a man employed in a psychiatric ward and a woman, with an antisocial personality disorder, who is a popular writer of children's books."
    ,  ranking=5,
    rating=7.5,

  review="A romantic and movie full of suspense.",
    img_url="https://asianwiki.com/images/d/d5/It%27s_Okay_to_Not_Be_Okay-CPsm1.jpg")
db.session.add(new_movie)
db.session.commit()
'''

@app.route("/")
def home():
    all_movies = Movie.query.all()
    return render_template("index.html", movies=all_movies)

class RateMovieForm(FlaskForm):
    rating=StringField("Your Rating Out of 10 e.g. 7.5")

    review=StringField("Your Review")
    submit=SubmitField("Done")

@app.route("/edit",methods=["GET","POST"])
def rate_movie():
    form=RateMovieForm()
    movie_id=request.args.get("id")
    movie=Movie.query.get(movie_id)
    if form.validate_on_submit():
        movie.rating=float(form.rating.data)


        movie.review=form.review.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html",movie=movie,form=form)
@app.route("/delete")
def delete_movie():
    movie_id=request.args.get("id")
    movie=Movie.query.get(movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for("home"))

class FindMovieForm(FlaskForm):
    title=StringField("Movie Title")
    submit=SubmitField("Add Movie")
@app.route("/add",methods=["GET","POST"])
def add_movie():
    form=FindMovieForm()
    return render_template("add.html",form=form)

if __name__ == '__main__':
    app.run(debug=True,use_reloader=False)
