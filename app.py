import json
from random import randint, shuffle

from flask import Flask, render_template, request, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Teacher(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    about = db.Column(db.String, unique=True, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    picture = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    goals = db.Column(db.String, nullable=False)
    free = db.Column(db.String)
    teacher_relations = db.relationship("Booking", back_populates="teacher_relation")


class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    teacher_relation = db.relationship("Teacher", back_populates="teacher_relations")
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"))


class Request(db.Model):
    __tablename__ = 'requests'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    goal = db.Column(db.String, nullable=False)
    time = db.Column(db.String, nullable=False)


db.create_all()

ru_days = {
    'mon': 'Понедельник',
    'tue': 'Вторник',
    'wed': 'Среда',
    'thu': 'Четверг',
    'fri': 'Пятница',
    'sat': 'Суббота',
    'sun': 'Воскресение'
}
date = {
    "teachers": db.session.query(Teacher).all(),
    "goals": json.loads(open('goals.json', 'r', encoding='utf-8').read())
}


@app.route("/")
def main():
    gls = date["goals"][0]
    random_nums = []
    random_teachers = []
    for i in range(7):
        x = randint(1, 12)
        if x not in random_nums:
            random_nums.append(x)
    for teach in date["teachers"]:
        if teach.id in random_nums:
            random_teachers.append(teach)
    return render_template("index.html", goals=gls, list=random_teachers)


@app.route("/profiles/<int:id>/")
def get_prof(id):
    table = db.session.query(Teacher).get_or_404(id).free
    return render_template("profile.html",
                           te=db.session.query(Teacher).get_or_404(id),
                           goals=date["goals"],
                           days=json.loads(table),
                           redays=ru_days)


@app.route("/all")
def teachers():
    return render_template("all.html", list=date["teachers"])


@app.route("/all/sort/", methods=["POST"])
def sort_all():
    dct = {
        "1": ["price", True],
        "2": ["price", False],
        "3": ["rating", True],
        "4": "random"
    }
    atrs = dct[str(request.form.get("choose"))]
    shuffle(date["teachers"])
    return render_template("all_sort.html", atrs=atrs, teachers=date["teachers"], dct=dct, goals=date["goals"])


@app.route("/goals/<goal>/")
def goals(goal):
    if date["goals"][0].get(goal) is not None:
        teachers_for_goal = []
        for teach in date["teachers"]:
            if goal in json.loads(teach.goals):
                teachers_for_goal.append(teach)
        return render_template("goal.html", smr=teachers_for_goal, goal=date["goals"][0][goal])
    else:
        abort(404)


@app.route("/request/")
def get_req():
    return render_template("request.html", goals=date["goals"][0])


@app.route("/request_done/", methods=["POST"])
def post_req():
    name = request.form.get("clientName")
    phone = request.form.get("clientPhone")
    time = request.form.get("time")
    goal = date["goals"][0][request.form.get("goal")]
    req = Request(name=name, phone=phone, goal=goal, time=time)
    db.session.add(req)
    db.session.commit()
    return render_template("request_done.html", name=name, phone=phone, goal=goal, time=time)


@app.route("/booking/<int:id>/<day>/<time>/")
def get_book(id, day, time):
    teach = db.session.query(Teacher).get_or_404(id)
    return render_template("booking.html", te=teach, day=day, time=time, rus=ru_days, id=id)


@app.route("/booking_done/", methods=["POST"])
def post_book():
    name = request.form.get("clientName")
    phone = request.form.get("clientPhone")
    day = request.form.get("clientWeekday")
    time = request.form.get("clientTime")
    rendez_vous = str(ru_days[day] + ", " + time)
    bkng = Booking(name=name, phone=phone, teacher_id=int(request.form.get("clientTeacher")))
    db.session.add(bkng)
    json.loads(db.session.query(Teacher).get_or_404(int(request.form.get("clientTeacher"))).free)[day][time] = False
    db.session.commit()
    return render_template("booking_done.html", name=name, phone=phone, date=rendez_vous)


@app.errorhandler(404)
def not_found(error):
    return "Не найдено", 404


if __name__ == '__main__':
    app.run()
