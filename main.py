from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'THESECRETKEYTHATNOONEKNOWS'
Bootstrap5(app)

db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///top-10-movies.db"
db.init_app(app)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    ranking = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String, nullable=False)
    img_url = db.Column(db.String, nullable=False)

    def __init__(self, title, year, description, rating, ranking, review, img_url):
        self.title = title
        self.year = int(year)
        self.description = description
        self.rating = rating
        self.ranking = ranking
        self.review = review
        self.img_url = img_url

class EditForm(FlaskForm):
    edited_rating = StringField(label="Your rating out of 10 e.g. 7.5", validators=[DataRequired()])
    edited_review = StringField(label="Your review", validators=[DataRequired()])
    submit = SubmitField(label="Done")

class AddMovie(FlaskForm):
    add_movie = StringField(label="Movie Title", validators=[DataRequired()])
    add_button = SubmitField(label="Add Movie")

class MovieDetails():
    def __init__(self, title, date, description, rating, ranking, review, img_url, movie_id):
        self.title = title
        self.release_date = date
        self.year = int(date.split("-")[0])
        print(self.year)
        print(type(self.year))
        self.description = description
        self.rating = rating
        self.ranking = ranking
        self.review = review
        self.img_url = f"https://image.tmdb.org/t/p/w500{img_url}"
        self.movie_id = movie_id

@app.route("/")
def home():
    new_movie = db.session.execute(db.select(Movie)).scalar_one_or_none()
    print(new_movie)
    return render_template("index.html", movie_info=new_movie)

@app.route("/edit/<int:id_num>", methods=["GET", "POST"])
def edit(id_num):
    form = EditForm()
    if form.validate_on_submit():
        movie_info = db.session.execute(db.select(Movie).filter_by(id=id_num)).scalar_one()
        movie_info.rating = form.edited_rating.data
        movie_info.review = form.edited_review.data
        db.session.commit()
        print(form.edited_rating.data)
        print(form.edited_review.data)
        return redirect(url_for("home"))
    return render_template("edit.html", form=form)

@app.route("/add", methods=["GET", "POST"])
def add():
    add_movie_form = AddMovie()
    if add_movie_form.validate_on_submit():
        new_movie = add_movie_form.data["add_movie"]
        print(new_movie)
        headings = {
            "api_key": "THESECRETKEYTHATNOONEKNOWS",
            "query": new_movie,
        }
        SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
        response = requests.get(SEARCH_URL, params=headings).json()["results"]
        print(response)
        movie_list = []
        for movie in response:
            movie_details = MovieDetails(title=movie["title"],
                                         date=movie["release_date"],
                                         description=movie["overview"],
                                         rating=movie["vote_average"],
                                         ranking=movie["popularity"],
                                         review="None",
                                         img_url=movie["poster_path"],
                                         movie_id=movie["id"])
            movie_list.append(movie_details)
        return render_template("select.html", movie_list=movie_list)
    return render_template("add.html", form=add_movie_form)

@app.route("/delete/<int:id_num>")
def delete(id_num):
    movie_info = db.session.execute(db.select(Movie).filter_by(id=id_num)).scalar_one()
    db.session.delete(movie_info)
    db.session.commit()
    print("deleted!")
    return redirect(url_for("home"))

@app.route("/adding/<movie_object>")
def adding_movie(movie_object):
    with app.app_context():
        db.create_all()
        new_movie = Movie(
            title=movie_object.title,
            year=movie_object.year,
            description=movie_object.description,
            rating=movie_object.rating,
            ranking=movie_object.ranking,
            review="None",
            img_url=movie_object.img_url
        )
        db.session.add(new_movie)
        db.session.commit()
        print(dir(new_movie))
    return redirect(url_for("home"))

if __name__ == '__main__':
    app.run(debug=True)
