import requests
from flask import Flask, request
import logging

import json

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
sessionStorage = {}
address = 'https://api.mymemory.translated.net/get?q={0}!&langpair={1}'


@app.route('/post', methods=['POST'])
def main():
    logging.info(f'Request: {request.json!r}')
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }

    handle_dialog(request.json, response)
    logging.info(f'Response:  {response!r}')

    return json.dumps(response)


def handle_dialog(req, res):
    if req['session']['new']:
        res['response']['text'] = 'Привет! ' \
                                  'Спроси меня в формате ' \
                                  'Переведи слово [ваше слово]'
        return

    user_request = req['request']['original_utterance']
    if len(user_request.split()) != 3:
        res['response']['text'] = 'Упс, что-от пошло не так! ' \
                                  'Еще раз: ' \
                                  'Спроси меня в формате ' \
                                  'Переведи слово [ваше слово]'
        return

    result = translator(user_request.split()[-1])
    res['response']['text'] = result


def translator(text):
    addr = address.format(text, 'ru|en')
    response = requests.get(addr)

    if response.status_code == 200:
        json_response = response.json()
        result = json_response['responseData']['translatedText']
        return result
    return f'status code {response.status_code}'


if __name__ == '__main__':
    app.run()
