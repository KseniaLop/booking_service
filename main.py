from urllib.parse import unquote_plus
from flask import render_template, request, redirect, make_response
import json

from app import db, app
from app.models import User, Film


SITS_TEMPLATE_STRING = json.dumps([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
], separators=(',', ':'))

PLACE_STATUS_MAP = {
    1: 'Занято',
    0: 'Свободно'
}

PLACE_STATUS_REPR_MAP = {
    1: 'taken',
    0: 'free'
}


def format_sits(sits, place_price):
    formatted_sits = list(sits)
    
    rows_count = len(formatted_sits)
    places_count = len(formatted_sits[0])
    
    for i in range(rows_count):
        row = formatted_sits[i]
        for j in range(places_count):
            place = row[j]
            formatted_sits[i][j] = {
                'status': PLACE_STATUS_MAP[place],
                'status_repr': PLACE_STATUS_REPR_MAP[place],
                'status_code': place,
                'row': i,
                'column': j,
                'price': place_price,
            }
    return formatted_sits


def order_film_place(film_name, row, column):
    info = get_film_info(film_name)
    sits = json.loads(info.data)
    free_sits_count = json.loads(str(info.free_sits_count))

    if not info or sits[row][column] == 1 or free_sits_count == 0:
        return False

    sits[row][column] = 1
    free_sits_count -= 1

    sits_data = json.dumps(sits, separators=(',', ':'))
    new_free_sits_count = json.dumps(free_sits_count, separators=(',', ':'))
    
    info.data = sits_data
    info.free_sits_count = new_free_sits_count

    db.session.commit()

    return True


def get_film_info(film_name):
    film = Film.query.filter(Film.name == unquote_plus(film_name)).first()
    return film


@app.route('/')
def index():
    films_names = db.session.query(Film.name).select_from(Film).all()
    return render_template('index.html',
                           films_names=map(lambda fnt: fnt[0], films_names))


@app.route('/login')
def admin_login():
    return render_template('login.html')


@app.route('/login-callback', methods=['POST'])
def admin_login_callback():
    login = request.form['login']
    password = request.form['password']

    if not login or not password:
        return 'Не хватает данных'

    user = User.query\
        .filter(User.username == login)\
        .filter(User.password_hash == password)\
        .first()
    if not user:
        return 'Неправильные данные'

    response = make_response(redirect('/panel'))
    response.set_cookie('login', login)
    response.set_cookie('password', password)
    return response


@app.route('/panel')
def admin_panel():
    login = request.cookies.get('login')
    password = request.cookies.get('password')

    user = User.query\
        .filter(User.username == login)\
        .filter(User.password_hash == password)\
        .first()
    if not user:
        return 'Неправильные данные'

    films_names = db.session.query(Film.name).select_from(Film).all()

    return render_template('panel.html',
                           films_names=map(lambda fnt: fnt[0], films_names))


@app.route('/add-film', methods=['POST'])
def add_film():
    film_name = request.form['film_name'].strip()
    place_price = request.form['place_price'].strip()
    
    try:
        place_price = int(place_price)
    except:
        return 'Надо ввести правильные данные'

    if not film_name.strip() or int(place_price) <= 0:
        return 'Надо ввести правильные данные'

    new_film = Film(name=film_name, data=SITS_TEMPLATE_STRING,
                    free_sits_count=100, price=place_price)

    db.session.add(new_film)
    db.session.commit()

    return redirect('/panel')


@app.route('/remove-film', methods=['POST'])
def remove_film():
    film_name = request.form['film_name']

    film_to_remove = db.session\
        .query(Film)\
        .filter(Film.name == film_name)\
        .first()

    if not film_to_remove:
        return 'Невозможно найти данный фильм'

    db.session.delete(film_to_remove)
    db.session.commit()

    return redirect('/panel')


@app.route('/film/<film_name>')
def film_info(film_name):
    info = get_film_info(film_name)
    
    if not info:
        return 'Странно, такого фильма нет...'
    
    sits = json.loads(info.data)
    free_sits_count = json.loads(str(info.free_sits_count))
    place_price = json.loads(str(info.price))

    formatted_sits = format_sits(sits, place_price)
    
    return render_template('film_info.html',
                           film_name=film_name,
                           formatted_sits=formatted_sits,
                           free_sits_count=free_sits_count)


@app.route('/film/order_place/', methods=['POST'])
def order_place():
    film_name = request.json['film_id']
    row = request.json['row']
    column = request.json['column']

    has_ordered = order_film_place(film_name, row, column)

    code_status = 200
    if not has_ordered:
        code_status = 500

    return {
        'film_id': film_name,
        'row': row,
        'column': column
    }, code_status


if __name__ == '__main__':
    app.run(debug=True)
