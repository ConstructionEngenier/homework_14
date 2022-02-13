from flask import Flask, request, jsonify
from utils import get_title, get_title_by_year, get_rating, get_title_by_genre

app = Flask(__name__)


@app.route('/movie/<title>')
def search_title(title):
    result = get_title(title)
    return result


@app.route('/movie/year')
def search_year():
    if request.method == 'GET':
        start_year = request.args.get('start_year')
        end_year = request.args.get('end_year')
        result = get_title_by_year(start_year, end_year)
        return result
    return "Введите запрос"


@app.route('/rating/children')
def rating_children():
    response = get_rating(['G'])
    return jsonify(response)


@app.route('/rating/family')
def rating_family():
    response = get_rating(['PG', 'PG-13'])
    return jsonify(response)


@app.route('/rating/adult')
def rating_adult():
    response = get_rating(['R', 'NC-17'])
    return jsonify(response)


@app.route('/genre/<genre>')
def top_genre(genre):
    result = get_title_by_genre(genre)
    return result


app.run(debug=True, port=5002)
