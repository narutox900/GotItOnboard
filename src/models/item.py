import logging

from db import db


class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')

    def __init__(self, _id, name, price, store_id):
        self.id = _id
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'id': self.id, 'name': self.name, 'price': self.price, 'store_id': self.store_id}

    @classmethod
    def find_by_name(cls, name):
        # SELECT * FROM items WHERE name=name LIMIT 1
        return cls.query.filter_by(name=name).all()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            logging.exception(e)

    def delete_from_db(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            logging.exception(e)

    @staticmethod
    def get_all():
        return {'items': [item.json() for item in ItemModel.query.all()]}
