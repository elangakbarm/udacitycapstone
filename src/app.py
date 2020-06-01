import os
import json
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Actor, Movie, db
from auth.auth import requires_auth, AuthError

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app)
    db.init_app(app)
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers','Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods','GET,PUT,POST,DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    # ROUTES

    @app.route('/actors')
    def get_actors():

        all_actors = Actor.query.order_by(Actor.id).all()

        if len(all_actors) == 0:
            abort(404)
        try:
            actors = [{"name": actor.name, "role": actor.role,
                       "gender": actor.gender}
                      for actor in all_actors]

            return jsonify({
                'success': True,
                'actors': actors,
            }), 200
        except Exception:
            abort(422)

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def createactor(self):

        body = request.get_json()
        new_name = body.get('name')
        new_role = body.get('role')
        new_gender = body.get('gender')

        if new_name is None:
            abort(400)
        try:
            actor = Actor(name=new_name, role=new_role, gender=new_gender)
            actor.insert()
            new_actor = actor.format()

            return jsonify({
                'success': True,
                'actor': new_actor,
            }), 200
        except Exception:
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(self, actor_id):

        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        if actor is None:
            abort(404)

        body = request.get_json()
        if body is None:
            abort(400)

        new_name = body.get('name')
        new_role = body.get('role')
        new_gender = body.get('gender')

        try:
            if new_name is not None:
                actor.name = new_name

            if new_gender is not None:
                actor.gender = new_gender

            actor.update()

            new_actor = [actor.format()]

            return jsonify({
                'success': True,
                'actor': new_actor,
            }), 200

        except Exception:
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(self, actor_id):

        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        if actor is None:
            abort(404)

        actor.delete()

        return jsonify({
            'success': True,
            'delete': actor_id,
        }), 200

    @app.route('/movies')
    def get_movies():
        try:
            all_movies = Movie.query.order_by(Movie.id).all()
            print(len(all_movies))
            if len(all_movies) == 0:
                abort(404)

            movies = [movie.format() for movie in all_movies]

            return jsonify({
                'success': True,
                'movies': movies,
            }), 200
        except Exception:
            abort(422)

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def createmovie(self):

        body = request.get_json()
        new_title = body.get('title')
        new_year = body.get('year')
        new_director = body.get('director')
        new_genre = body.get('genre')

        if new_title is None:
            abort(400)
        try:
            movie = Movie(title=new_title, year=new_year,
                          director=new_director,
                          genre=new_genre)
            movie.insert()
            new_movie = movie.format()

            return jsonify({
                'success': True,
                'movie': new_movie,
            }), 200
        except Exception:
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(self, movie_id):

        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if movie is None:
            abort(404)

        body = request.get_json()
        if body is None:
            abort(400)

        new_title = body.get('title')
        new_year = body.get('year')
        new_director = body.get('director')
        new_genre = body.get('genre')

        try:
            if new_title is not None:
                movie.title = new_title

            if new_year is not None:
                movie.year = new_year

            movie.update()

            new_movie = [movie.format()]

            return jsonify({
                'success': True,
                'movie': new_movie,
            }), 200

        except Exception:
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(self, movie_id):

        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if movie is None:
            abort(404)

        movie.delete()

        return jsonify({
            'success': True,
            'delete': movie_id,
        }), 200

    # Error Handling
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "message": error.error
        }), error.status_code
  
  
    return app

APP = create_app()
if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)