from io import BytesIO

from flask import Flask, Response, jsonify, make_response, request
from requests import get
from PIL import Image
import pytesseract

def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")


def create_app():
    app = Flask(__name__)

    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            file = request.files.get('file')
            if file:
                image = Image.open(file.stream)
                image = image.convert('L')  # convert image to black and white
                text = pytesseract.image_to_string(image)
                langs = pytesseract.get_languages(config='')

                return make_response(jsonify({
                    'text': text,
                    'text_length': len(text),
                    'text_words': len(text.split(' ')),
                    'text_lines': len(text.splitlines()),
                    'text_chars': len(text.replace(' ', '')),
                    'langs': langs
                }), 200)

        url = request.args.get('url') or request.form.get('url')
        if url:
            downloadImageFromUrl = get(url)
            mine_type = downloadImageFromUrl.headers['Content-Type']
            data = downloadImageFromUrl.content
            result = remove(data=data)
            return Response(response=result, mimetype=mine_type, headers={
                'Content-Disposition': f'inline; filename=removedbg_{url.split("/")[-1]}'
            })

        return Response(response='No file or url provided', status=400)

    return app
