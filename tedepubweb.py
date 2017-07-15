# -*- coding: utf-8 -*-
"""
    tedepubweb

"""

from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, send_file
import os


from tedepub import convert
app = Flask(__name__)

@app.route('/')
def show_epubs():
    epubs = os.listdir('./epub')
    return render_template('show_epubs.html', epubs=epubs)
    #return render_template('show_epubs.html')
    

@app.route('/convert_epub', methods=['POST'])
def convert_epub():
    convert(request.form['url'])
    return redirect(url_for('show_epubs'))


@app.route("/download/<file_name>")
def download_epub(file_name):
    return send_file('./epub/' + file_name, as_attachment=True)

if __name__ == "__main__":
    app.run(host='192.168.219.104', port=8888, debug=True)




