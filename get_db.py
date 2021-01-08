import json

from app import db, Teacher
from data import teachers


def load_db():
    for teach in teachers:
        goals = json.dumps(teach["goals"])
        free = json.dumps(teach["free"])
        te = Teacher(
            name=teach["name"],
            about=teach["about"],
            rating=teach["rating"],
            picture=teach["picture"],
            price=teach["price"],
            goals=goals,
            free=free
        )
        db.session.add(te)
    db.session.commit()


if __name__ == '__main__':
    load_db()
