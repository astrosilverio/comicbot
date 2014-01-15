from flask import Flask, request, redirect, render_template, g
from comicbot import CLDBot
import unicodedata

app = Flask(__name__)
bot = CLDBot('empty.txt')

@app.route('/', methods = ['GET', 'POST'])
def main():
    if request.method == 'GET':
        return render_template('main.html')
    elif request.method == 'POST':
        # request was a POST
        user_input = request.form['user_input']
        g.message = bot.process(user_input)
        print type(g.message)
        return render_template('main.html')
        
if __name__ == '__main__':
    app.run(debug=True)
    