import sqlite3
import json

connection = sqlite3.connect('netflix.db', check_same_thread=False)
cursor = connection.cursor()


def movie_title(arg):
    sql_request = f'SELECT title , country , release_year, listed_in, description FROM netflix  WHERE title = "{arg}" ORDER BY release_year DESC LIMIT 1'
    cursor.execute(sql_request)

    result = cursor.fetchall()

    if len(result) > 0:
        return {
            "title": result[0][0],
            "country": result[0][1],
            "release_year": result[0][2],
            "genre": result[0][3],
            "description": result[0][4]
        }
    else:
        return "Errors"


def year_to_year(y1, y2):
    sql_request = f'SELECT title, release_year FROM netflix  WHERE release_year BETWEEN {int(y1)} AND {int(y2)} ORDER BY release_year LIMIT 100'
    cursor.execute(sql_request)

    result = cursor.fetchall()
    json_data = []
    for r in result:
        json_data.append({"title": r[0], "release_year": r[1]})

    return json_data


def age_rating(my_list):
    if len(my_list) == 1:
        sql_request = f"""SELECT title, rating, description 
                                  FROM netflix 
                                  WHERE rating = '{my_list[0]}'
                """

    elif len(my_list) == 2:
        sql_request = f"""SELECT title, rating, description 
                          FROM netflix 
                          WHERE rating IN ('{my_list[0]}', '{my_list[1]}')
                          ORDER BY rating 
                        """

    elif len(my_list) == 3:
        sql_request = f"""SELECT title, rating, description 
                          FROM netflix 
                          WHERE rating IN ('{my_list[0]}', '{my_list[1]}', '{my_list[2]}')
                          ORDER BY rating 
                        """

    cursor.execute(sql_request)
    result = cursor.fetchall()
    json_data = []

    for r in result:
        json_data.append({"title": r[0], "rating": r[1], "description": r[2]})

    return json_data


def search_listed_in(arg):
    sql_request = f'''SELECT title, description
                      FROM netflix
                      WHERE listed_in LIKE "%{arg}%"
                      ORDER BY release_year DESC
                      LIMIT 10                        
                '''

    cursor.execute(sql_request)
    result = cursor.fetchall()

    json_data = []

    for r in result:
        json_data.append({"title": r[0], "description": r[1]})

    return json_data


def new_cast(arg1, arg2):
    query = f'''
                SELECT netflix.cast
                FROM netflix
                WHERE netflix.cast LIKE "%{arg1}%"
                AND netflix.cast LIKE "%{arg2}%"
    '''

    cursor.execute(query)

    result = cursor.fetchall()

    cast_list = []

    for r in result:
        for value in r[0].split(', '):
            if value not in cast_list:
                cast_list.append(value)

    counter = 0
    new_cast = []

    for cast in cast_list:
        for r2 in result:
            if cast in r2[0]:
                counter += 1

        if counter > 2:
            new_cast.append(cast)
        counter = 0

    return new_cast


def movies(type_move, release_year, listed_in):

    query = f"""
                SELECT title, description
                FROM netflix
                WHERE netflix.type = '{type_move}'
                AND release_year = {release_year}
                AND listed_in LIKE '%{listed_in}%'
    """

    cursor.execute(query)

    result = cursor.fetchall()

    list_dict = []

    for value in result:
        list_dict.append({value[0]: value[1]})

    data_json = json.dumps(list_dict)

    return data_json
