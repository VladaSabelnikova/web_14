import json
import logging
import os

from flask import Flask, request

from src.gets.get_cities import get_cities
from src.gets.get_coord import get_coordinates
from src.gets.get_country import get_country
from src.gets.get_distance import get_distance

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    filename='app.log',
    format='%(asctime)s %(levelname)s %(name)s %(message)s'
)


@app.route('/post', methods=['POST'])
def main():
    logging.info('Request: %r', request.json)
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(response, request.json)
    logging.info('Request: %r', response)
    return json.dumps(response)


def handle_dialog(res, req):
    user_id = req['session']['user_id']
    if req['session']['new']:
        res['response']['text'] = \
            'Привет! Я могу показать город или сказать расстояние между городами!' \
            'Если нужна страна города — пиши название города,' \
            'если нужно расстояние между городами — пиши название двух городов'
        return
    # Получаем города из нашего
    cities = get_cities(req)
    if not cities:
        res['response']['text'] = 'Ты не написал название не одного города!'
    elif len(cities) == 1:
        res['response']['text'] = f'Этот город в стране - {get_country(cities[0])}'

    elif len(cities) == 2:
        distance = get_distance(
            get_coordinates(cities[0]),
            get_coordinates(cities[1])
        )
        res['response']['text'] = f'Расстояние между этими городами: {round(distance)} км.'
    else:
        res['response']['text'] = 'Слишком много городов! Максимум 2 можно!'


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    app.run()
