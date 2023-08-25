from flask import Flask, render_template, request
from handler import Handler
import asyncio
app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
async def home():
    x = ""
    if request.method == 'POST':
        handler = Handler()
        command = request.form['command']
        x = await handler.handler(command)
        print(x)
    
    return render_template('index.html', x = x)

if __name__ == '__main__':
    app.run(debug=True)