from json import dumps
from random import randint, shuffle

from flask import Flask, render_template, request, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Tutor(db.Model):
    __tablename__ = "tutors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    about = db.Column(db.String, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    picture = db.Column(db.String, nullable=False)
    goal = db.Column(db.String, nullable=False)
    free = db.Column(db.String, nullable=False)
    relations = db.relationship("Booking", back_populates="get_rel")


class Booking(db.Model):
    __tablename__ = "bookings"
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String, nullable=False)
    time = db.Column(db.String, nullable=False)
    get_rel = db.relationship("Tutor", back_populates='relations')
    with_teach = db.Column(db.String, db.ForeignKey("tutors.id"))


class Request(db.Model):
    __tablename__ = 'requests'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    goal = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)
    teacher = db.Column(db.Integer, db.ForeignKey("tutors.id"))

#
# date = {"teachers": db.session.query(Tutor).all(), "goals": db.session(Goal).all()}
#
# redays = {"mon": "Понедельник",
#           "tue": "Вторник",
#           "wed": "Среда",
#           "thu": "Четверг",
#           "fri": "Пятница",
#           "sat": "Суббота",
#           "sun": "Воскресение"
#           }
#
#
# @app.route("/")
# def main():
#     gls = date["goals"]
#     ml = []
#     smr = []
#     for i in range(7):
#         x = randint(1, 12)
#         if x not in ml:
#             ml.append(x)
#     for te in date["teachers"]:
#         if te["id"] in ml:
#             smr.append(te)
#     return render_template("index.html", goals=gls, list=smr)
#
#
# @app.route("/all")
# def teachers():
#     return render_template("all.html", list=date["teachers"])
#
#
# @app.route("/all/sort/", methods=["POST"])
# def sort_all():
#     dct = {
#         "1": ["price", True],
#         "2": ["price", False],
#         "3": ["rating", True],
#         "4": "random"
#     }
#     atrs = dct[str(request.form.get("choose"))]
#     shuffle(date["teachers"])
#     return render_template("all_sort.html", atrs=atrs, teachers=date["teachers"], dct=dct, goals=date["goals"])
#
#
# @app.route("/goals/<goal>/")
# def goals(goal):
#     if date["goals"].get(goal) is not None:
#         my_list = []
#         for teach in date["teachers"]:
#             if goal in teach["goals"]:
#                 my_list.append(teach)
#         return render_template("goal.html", smr=my_list, goal=date["goals"][goal])
#     else:
#         abort(404)
#
#
# @app.route("/profiles/<int:id>/")
# def get_prof(id):
#     if smr.get(id) is not None:
#         table = smr[id]["free"]
#         return render_template("profile.html", te=smr[id], goals=date["goals"], days=table, redays=redays)
#     else:
#         abort(404)
#
#
# @app.route("/request/")
# def get_req():
#     return render_template("request.html", goals=date["goals"])
#
#
# @app.route("/request_done/", methods=["POST"])
# def post_req():
#     name = request.form.get("clientName")
#     phone = request.form.get("clientPhone")
#     time = request.form.get("time")
#     goal = date["goals"][request.form.get("goal")]
#     requests[6] = {"id": 6, "username": name, "phone": phone, "time": time, "goal": goal}
#     # 2+ 1
#     with open("request.json", "w") as f:
#         f.write(dumps(requests))
#     return render_template("request_done.html", name=name, phone=phone, time=time, goal=goal)
#
#
# @app.route("/booking/<int:id>/<day>/<time>/")
# def get_book(id, day, time):
#     if smr.get(id) is not None:
#         te = smr[id]
#         return render_template("booking.html", te=te, day=day, time=time, rus=redays, id=id)
#     else:
#         abort(404)
#
#
# @app.route("/booking_done/", methods=["POST"])
# def post_book():
#     name = request.form.get("clientName")
#     phone = request.form.get("clientPhone")
#     day = request.form.get("clientWeekday")
#     time = request.form.get("clientTime")
#     rendez_vous = str(redays[day] + ", " + time)
#     books[3] = {"id": 3,
#                 "teacher": smr[int(request.form.get("clientTeacher"))],
#                 "time": time,
#                 "username": name,
#                 "phone": phone,
#                 "date": rendez_vous
#                 }
#     smr[int(request.form.get("clientTeacher"))]["free"][day][time] = False
#     # 3 + 1
#     with open("booking.json", "w") as f:
#         f.write(dumps(books))
#     return render_template("booking_done.html", name=name, phone=phone, date=rendez_vous)
#
#
# @app.errorhandler(404)
# def not_found(error):
#     return "Не найдено", 404
#
#
# if __name__ == '__main__':
#     app.run()
