import sqlite3
from flask import Flask, jsonify
from functions import movie_title, year_to_year, age_rating, search_listed_in

app = Flask('__main__')

connection = sqlite3.connect('netflix.db', check_same_thread=False)
cursor = connection.cursor()


@app.route('/movie/<test>')
def page_1(test):
    result = movie_title(test)
    return jsonify(result)


@app.route('/movie/<year1>/to/<year2>')
def page_2(year1, year2):
    result = year_to_year(year1, year2)
    return jsonify(result)


@app.route('/rating/<arg>')
def children_rating(arg):
    rating_list = {'children': ['G'], 'family': ['G', 'PG', 'PG-13'], 'adult': ['R', 'NC-17'],}

    for key in rating_list.keys():
        if key == arg:
            result = age_rating(rating_list[arg])
            break

    return jsonify(result)


@app.route('/genre/<genre>')
def views_genre(genre):

    return jsonify(search_listed_in(genre))


if __name__ == '__main__':
    app.run()
