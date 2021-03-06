from flask import render_template, send_file, request, send_from_directory
from app.modules.unthread import *
import logging, os, io

from app import app

logging.basicConfig(filename='bot.log', filemode='w', level=logging.WARNING)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        return render_template('index.html', files=[])
    else:
        url = request.form['tweetUrl'] if 'tweetUrl' in request.values else None
        out = unthread(url)
        filename = os.path.splitext(os.path.basename(out))
        return render_template('index.html', files=[filename[0]])


@app.route('/download', methods=['POST'])
def download():
    file_base = [x for x in request.form][0]
    fn = '{}.txt'.format(file_base)
    fp = os.path.abspath('files/{}'.format(fn))

    # read in txt file
    # store bytes
    # remove file 
    # return bytes as attachment
    try:
        download_bytes = io.BytesIO()
        with open(fp, 'rb') as f:
            download_bytes.write(f.read())
        download_bytes.seek(0)
        os.remove(fp)
        return send_file(download_bytes, as_attachment=True, attachment_filename=fn)
    except Exception as e:
        print(e)
        logging.error(e)