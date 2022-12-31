from flask import Flask, jsonify, request
from popularMovies import output
from recommendedMovies import get_recommendations
import csv

all_movies=[]
liked_movies=[]
disliked_movies=[]
not_watched_movies=[]


with open('final.csv',encoding='utf8') as f:
    reader=csv.reader(f)
    data=list(reader)
    all_movies=data[1:] 


app=Flask(__name__)
@app.route('/')
def get_movie():

   movie_data = {
        "title": all_movies[0][19],
        "poster_link": all_movies[0][27],
        "release_date": all_movies[0][13] or "N/A",
        "duration": all_movies[0][15],
        "rating": all_movies[0][20],
        "overview": all_movies[0][9]
    }
   return jsonify({
        "data": movie_data,
        "status": "success"
    })


@app.route('/liked-movie')
def liked_movie():
    liked_movies.append(all_movies[0])
    all_movies.pop(0)
    return jsonify({'status':'success'})

@app.route('/disliked-movie')
def disliked_movie():
    disliked_movies.append(all_movies[0])
    all_movies.pop(0)
    return jsonify({'status':'success'})    

@app.route('/not-watched-movie')
def not_watched_movie():
    not_watched_movies.append(all_movies[0])
    all_movies.pop(0)
    return jsonify({'status':'success'})

@app.route('/popularMovies')
def popularMovies():
    movie_data = []
    for movie in output:
        _d = {
            "title": movie[0],
            "poster_link": movie[1],
            "release_date": movie[2] or "N/A",
            "duration": movie[3],
            "rating": movie[4],
            "overview": movie[5]
        }
        movie_data.append(_d)
    return jsonify({
        "data": movie_data,
        "status": "success"
    }), 200

@app.route('/recommendedMovies')
def recommendedMovies():
    all_recommended = []
    for liked_movie in liked_movies:
        output = get_recommendations(liked_movie[19])
        for data in output:
            all_recommended.append(data)
    # import itertools
    all_recommended.sort()
    # all_recommended = list(all_recommended for all_recommended,_ in itertools.groupby(all_recommended))
    movie_data = []
    for recommended in all_recommended:
        _d = {
            "title": recommended[0],
            "poster_link": recommended[1],
            "release_date": recommended[2] or "N/A",
            "duration": recommended[3],
            "rating": recommended[4],
            "overview": recommended[5]
        }
        movie_data.append(_d)
    return jsonify({
        "data": movie_data,
        "status": "success"
    }), 200

app.run(debug=True)    









