from flask import render_template, request, redirect
from app import app
import sqlite3

@app.route('/')
def index():
    conn = sqlite3.connect('vocabulary.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM words')
    words = cursor.fetchall()
    conn.close()
    return render_template('index.html', words=words)

@app.route('/add', methods=['POST'])
def add_word():
    word = request.form['word']
    translation = request.form['translation']
    example = request.form.get('example', '')
    
    conn = sqlite3.connect('vocabulary.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO words (word, translation, example) VALUES (?, ?, ?)',
                  (word, translation, example))
    conn.commit()
    conn.close()
    return redirect('/')