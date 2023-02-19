from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

TMDB_API = "615eae181753e7f26bc0eaa07f11a92a"
suggested_movie_list = []

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
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


with app.app_context():
    db.create_all()

class EditForm(FlaskForm):
    edited_rating = StringField(label="Your rating out of 10 e.g. 7.5", validators=[DataRequired()])
    edited_review = StringField(label="Your review", validators=[DataRequired()])
    submit = SubmitField(label="Done")

class AddMovieForm(FlaskForm):
    add_movie = StringField(label="Movie Title", validators=[DataRequired()])
    add_button = SubmitField(label="Add Movie")

class MovieDetails:
    def __init__(self, title, date=None, description=None, rating=None, review=None, img_url=None, movie_id=None):
        self.error = False
        self.title = title
        try:
            self.year = int(date.split("-")[0])
            self.release_date = date
            self.description = description
            self.rating = rating
            self.ranking = "None"
            self.review = review
            self.img_url = f"https://image.tmdb.org/t/p/w500{img_url}"
            self.id = movie_id
        except:
            self.error = True

@app.route("/")
def home():
    sorted_movie = db.session.execute(db.select(Movie).order_by(Movie.rating)).scalars().all()
    print(sorted_movie)
    rank = 1
    for movie in sorted_movie[::-1]:
        movie.ranking = rank
        rank += 1
    return render_template("index.html", movie_list=sorted_movie)

@app.route("/edit/<int:id_num>", methods=["GET", "POST"])
def edit(id_num):
    suggested_movie_list.clear()
    form = EditForm()
    if form.validate_on_submit():
        movie_info = db.session.execute(db.select(Movie).filter_by(id=id_num)).scalar()
        movie_info.rating = form.edited_rating.data
        movie_info.review = form.edited_review.data
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("edit.html", form=form)

@app.route("/add", methods=["GET", "POST"])
def add():
    add_movie_form = AddMovieForm()
    if add_movie_form.validate_on_submit():
        new_movie = add_movie_form.data["add_movie"]
        headings = {
            "api_key": TMDB_API,
            "query": new_movie,
        }
        response = requests.get("https://api.themoviedb.org/3/search/movie", params=headings).json()["results"]
        for movie in response:
            movie_details = MovieDetails(title=movie["title"],
                                         date=movie["release_date"],
                                         description=movie["overview"],
                                         rating=movie["vote_average"],
                                         review="None",
                                         img_url=movie["poster_path"],
                                         movie_id=movie["id"])
            if not movie_details.error:
                suggested_movie_list.append(movie_details)
        return render_template("select.html", movie_list=suggested_movie_list)
    return render_template("add.html", form=add_movie_form)

@app.route("/delete/<int:id_num>")
def delete(id_num):
    movie_info = db.session.execute(db.select(Movie).filter_by(id=id_num)).scalar_one()
    db.session.delete(movie_info)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/adding/<int:movie_id>")
def adding_movie(movie_id):
    for movie_object in suggested_movie_list:
        if movie_id == movie_object.id:
            new_movie = Movie(
                title=movie_object.title,
                year=movie_object.year,
                description=movie_object.description,
                rating=movie_object.rating,
                ranking=movie_object.ranking,
                review="None",
                img_url=movie_object.img_url,
                movie_id=movie_object.id
            )
            db.session.add(new_movie)
            db.session.commit()
            return redirect(url_for("edit", id_num=new_movie.id))

if __name__ == '__main__':
    app.run(debug=True)
