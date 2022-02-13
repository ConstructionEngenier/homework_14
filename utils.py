import sqlite3
from collections import Counter

from flask import jsonify


def db_connect(db, query):
    """
    Передаем название базы данных, query запрос и получаем на выходе результат запроса

    :param db:
    :param query:
    :return:
    """
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute(query)
    result = cur.fetchall()
    con.close()
    return result


def get_title(title):
    """
    Передаем название картины и получаем на выходе в JSON список картин с страной производства, годом выпуска,
    жанром и соответствующим запросу названием

    :param title:
    :return:
    """

    response = []

    if title:
        query = f"""
                    SELECT title,
                           country,
                           release_year,
                           listed_in,
                           description
                    FROM netflix
                    WHERE `title` like '%{title}%'
                    ORDER BY `release_year` DESC
                    LIMIT 10
            """
        result = db_connect('netflix.db', query)
        if len(result):

            for line in result:
                line = {
                    "title": line[0],
                    "country": line[1],
                    "release_year": line[2],
                    "listed_in": line[3],
                    "description": line[4],
                }
                response.append(line)
        return jsonify(response)
    return "Название не введено"


def get_rating(rating):
    """
    Передаем рейтинг картины и получаем на выходе в JSON список с названием, описанием картин
    и соответствующим запросу рейтингом

    :param rating:
    :return:
    """
    response = []

    if len(rating) > 1:
        str_rating = "','".join(rating)
    else:
        str_rating = "".join(rating)
    query = f"""
            SELECT title,
                   rating,
                   description
            FROM netflix
            WHERE rating IN ('{str_rating}')
            LIMIT 100
    """
    result = db_connect('netflix.db', query)
    for line in result:
        line_dict = {
            "title": line[0],
            "rating": line[1],
            "description": line[2]
        }
        response.append(line_dict)
    return response


def get_title_by_year(start_year, end_year):
    """
    Передаем диапазон для поиска в виде начального года и конечного, и получаем на выходе в JSON
    список с названием картины и годом выпуска, удовлетворяющим условиям поиска

    :param start_year:
    :param end_year:
    :return:
    """
    response = []

    if start_year and end_year:
        query = f"""
        SELECT title,
               release_year
        FROM netflix
        WHERE `release_year` BETWEEN {start_year} AND {end_year}
        ORDER BY `release_year` DESC
        """
        result = db_connect('netflix.db', query)

        for line in result:
            line_dict = {
                "title": line[0],
                "release_year": line[1],
            }
            response.append(line_dict)
    return jsonify(response)


def get_title_by_genre(genre):
    """
    Передаем жанр картины и получаем на выходе список названий картин в JSON
    с годом выпуска и соответствующим запросу жанром

    :param genre:
    :return:
    """
    response = []

    query = f"""
                    SELECT title,
                           description
                    FROM netflix
                    WHERE `listed_in` LIKE '%{genre}%'
                    ORDER BY release_year DESC
                    LIMIT 10;
                    """
    result = db_connect('netflix.db', query)

    for line in result:
        line_dict = {
            "title": line[0],
            "description": line[1],
        }
        response.append(line_dict)
    return jsonify(response)


def search_pair(actor_one, actor_two):
    """
    Передаем имена актеров  и получаем на выходе в JSON список тех, кто играет с ними в паре больше 2 раз

    :param actor_one:
    :param actor_two:
    :return:
    """
    result_list = []

    query = f"""
    select `cast`
    from netflix
    where `cast` like '%{actor_one}%'
    and `cast` like '%{actor_two}%'
    """
    result = db_connect('netflix.db', query)

    for line in result:
        line_list = line[0].split(',')
        result_list += line_list
    counter = Counter(result_list)
    actor_list = []

    for key, value in counter.items():
        if value > 2 and key.strip() not in [actor_one, actor_two]:
            actor_list.append(key)
    return actor_list


def get_list_of_films(picture_type, release_year, genre):
    """
    Передаем тип картины (фильм или сериал), год выпуска и ее жанр и получаем на выходе список названий картин
    с их описаниями в JSON

    :return:
    """
    response = []

    query = f"""
                    SELECT title,
                           description
                    FROM netflix
                    WHERE `type` like '%{picture_type}%'
                    AND `release_year` = '{release_year}'
                    AND `listed_in` LIKE '%{genre}%'
                    ORDER BY `release_year` DESC
            """
    result = db_connect('netflix.db', query)
    if len(result):
        for line in result:
            line = {
                "title": line[0],
                "description": line[1],
            }
            response.append(line)
        return response
    return "Ничего не найдено"
