from io import BytesIO

from flask import Flask, jsonify, make_response, request
from requests import get
from PIL import Image
import pytesseract
from config import TESSDATA_DIR

tessdata_dir_config = f'--tessdata-dir {TESSDATA_DIR}'
available_langs = pytesseract.get_languages(config=tessdata_dir_config)


def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")


def parse_lang(lang):
    if not lang:
        return None

    # Format for lang: eng khm
    if '+' in lang:
        return lang

    langs = lang.split(' ')
    return '+'.join(langs)


def is_lang_supported(lang):
    if not lang:
        return False

    # Format for lang: eng+khm
    langs = lang.split('+')
    for l in langs:
        print("Checking lang:", l)
        if l not in available_langs:
            return False
    return True


def image_to_text(data, lang):
    image = Image.open(data)
    image = image.convert('L')  # convert image to black and white
    text = pytesseract.image_to_string(
        image, config=tessdata_dir_config, lang=lang)

    return make_response(jsonify({
        'text': text,
        'text_length': len(text),
        'text_words': len(text.split(' ')),
        'text_lines': len(text.splitlines()),
        'text_chars': len(text.replace(' ', '')),
        'lang': lang,
    }), 200)


def create_app():
    app = Flask(__name__)

    @app.route('/', methods=['GET', 'POST'])
    def index():
        # Format for lang: eng+khm
        lang = request.args.get('lang') or request.form.get('lang')
        lang = parse_lang(lang)

        if lang:
            if not is_lang_supported(lang):
                return make_response(jsonify({
                    'error': 'Language not supported',
                    'lang': lang,
                }), 400)

        if request.method == 'POST':
            file = request.files.get('file')
            if file:
                return image_to_text(file.stream, lang)

        url = request.args.get('url') or request.form.get('url')
        if url:
            downloadImageFromUrl = get(url)
            mine_type = downloadImageFromUrl.headers['Content-Type']
            data = downloadImageFromUrl.content
            if mine_type == 'image/png' or mine_type == 'image/jpeg' or mine_type == 'image/jpg':
                return image_to_text(BytesIO(data), lang)
            else:
                return make_response(jsonify({
                    'error': 'Only png image is supported',
                    'mine_type': mine_type,
                }), 400)

        return make_response(jsonify({
            'error': 'No file or url provided',
            'params': {
                'file': 'file',
                'url': 'https://example.com/image.png',
                'lang': 'eng+khm',
            },
            "langs": {
                "link": "/langs?lang=eng+khm",
            }
        }), 400)

    @app.route('/langs', methods=['GET'])
    def langs():
        global available_langs
        if not available_langs:
            available_langs = pytesseract.get_languages(
                config=tessdata_dir_config)

        lang = request.args.get('lang') or request.form.get('lang')
        lang = parse_lang(lang)

        supported = is_lang_supported(lang)

        return make_response(jsonify({
            'supported': supported,
            'lang': lang,
            'langs': available_langs,
            "tessdata": "https://github.com/tesseract-ocr/tessdata.git",
        }), 200)

    return app
