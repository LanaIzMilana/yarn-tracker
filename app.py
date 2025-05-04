
from flask import Flask, render_template, request, redirect, url_for
import os, json, uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/photos'

DATA_FILE = 'data.json'

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def index():
    yarns = load_data()
    return render_template('index.html', yarns=yarns)

@app.route('/add', methods=['POST'])
def add_yarn():
    data = load_data()
    photo = request.files['photo']
    photo_filename = ''
    if photo:
        photo_filename = f"{uuid.uuid4().hex}_{photo.filename}"
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_filename))

    new_yarn = {
        "id": uuid.uuid4().hex,
        "name": request.form['name'],
        "weight": request.form['weight'],
        "length": request.form['length'],
        "color": request.form['color'],
        "color_code": request.form['color_code'],
        "quantity": request.form['quantity'],
        "price": request.form['price'],
        "photo": photo_filename
    }
    data.append(new_yarn)
    save_data(data)
    return redirect(url_for('index'))

@app.route('/yarn/<yarn_id>')
def yarn_card(yarn_id):
    data = load_data()
    yarn = next((y for y in data if y['id'] == yarn_id), None)
    return render_template('yarn_card.html', yarn=yarn)

if __name__ == '__main__':
    app.run(debug=True)
