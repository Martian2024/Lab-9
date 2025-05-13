from flask import Flask, request, render_template
from database import db, Steps
import json

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def main():
    array = db.session.query(Steps).all()
    if request.method == 'POST':
        date = request.form.get('date')
        steps = request.form.get('amount')
        all_dates = map(lambda x: x.date, array)
        if date in all_dates:
            old_data = Steps.query.filter_by(date=date).first()
            old_data.amount = old_data.amount + int(steps)
        else:
            steps = Steps(date=date, amount=steps)
            db.session.add(steps)
        db.session.commit()
        array = db.session.query(Steps).all()
    return render_template('index.html', array=array)

@app.route('/handle_clear', methods=['POST'])
def handle_clear():
    db.session.query(Steps).delete()
    db.session.commit()
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 


if __name__ == '__main__':
    app.run(host='127.0.0.1', port='1080', debug=True)

