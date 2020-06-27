from app.config import MEALS_PER_COMBO
from app.extensions import db
from app.auth.models import User
from app.data.util import get_current_week_number, get_day_from_id
from datetime import datetime
from psycopg2.errors import UniqueViolation
from sqlalchemy import UniqueConstraint
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import relationship

class Meals(db.Model):
    __tablename__ = 'meals'

    id         = db.Column(db.Integer, primary_key=True, autoincrement=True)
    meal_id    = db.Column(db.Integer, unique=True)
    name       = db.Column(db.String)
    calories   = db.Column(db.Integer)

    @classmethod
    def get(cls, meal_id):

        return cls.query.filter_by(meal_id=meal_id).first()

    @classmethod
    def save_or_get(cls, meal_id, name, calories):

        try:
            meal = Meals(meal_id=meal_id, name=name, calories=calories)
            db.session.add(meal)
            db.session.commit()

        except IntegrityError as e:
            db.session.rollback()
            assert isinstance(e.orig, UniqueViolation) # assert it's a Unique Violation
            meal = cls.get(meal_id)

        return meal

    def to_json(self):

        return {
            'meal_id'  : self.meal_id,
            'name'     : self.name,
            'calories' : self.calories
        }

class UserCombos(db.Model):
    __tablename__ = 'user_combos'

    id          = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id     = db.Column(db.ForeignKey("users.id"))
    day_of_week = db.Column(db.Integer)
    week_num    = db.Column(db.Integer)
    meal1_id    = db.Column(db.ForeignKey("meals.id", ondelete='CASCADE'))
    meal2_id    = db.Column(db.ForeignKey("meals.id", ondelete='CASCADE'))
    meal3_id    = db.Column(db.ForeignKey("meals.id", ondelete='CASCADE'))

    meal1       = relationship("Meals", foreign_keys=[meal1_id])
    meal2       = relationship("Meals", foreign_keys=[meal2_id])
    meal3       = relationship("Meals", foreign_keys=[meal3_id])

    __table_args__ = (UniqueConstraint('user_id', 'day_of_week', 'week_num', name='user_combo_uc'),)

    @classmethod
    def get(cls, user_id, day_of_week, week_num):

        return cls.query.filter_by(user_id=user_id, day_of_week=day_of_week, week_num=week_num).first()

    @classmethod
    def save_or_update(cls, user_id, day_of_week, meal_objects=[]):

        meals = [Meals.save_or_get(meal_id=meal_obj['meal_id'], name=meal_obj['name'], calories=meal_obj['calories']) for meal_obj in meal_objects]

        data = {'user_id': user_id, 'day_of_week': day_of_week, 'week_num': get_current_week_number()}
        meals_data = {}
        for i, meal in enumerate(meals, 1):
            meals_data[f'meal{i}_id'] = meal.id
        data.update(meals_data)

        try:
            user_combo = UserCombos(**data)
            db.session.add(user_combo)
            db.session.commit()

        except IntegrityError as e:
            db.session.rollback()
            assert isinstance(e.orig, UniqueViolation)  # assert it's a Unique Violation

            user_combo = UserCombos.get(user_id=user_id, day_of_week=day_of_week, week_num=get_current_week_number())
            for meal, meal_id in meals_data.items():
                setattr(user_combo, meal, meal_id)

            db.session.add(user_combo)
            db.session.commit()

        return user_combo

    @classmethod
    def get_weekly_plan(cls, user_id):

        weekly_plan_data = {
            'plan' : [],
            'total_calories_week' : 0
        }

        user_combos = UserCombos.query.filter_by(user_id=user_id, week_num=get_current_week_number()).all()

        total_week_calories = 0
        for combo in user_combos:
            day_calories = 0
            day_data     = {
                'day'          : get_day_from_id(combo.day_of_week),
                'meals'        : [],
                'day_calories' : 0
            }

            combo_meals = [getattr(combo, f'meal{i}') for i in range(1, MEALS_PER_COMBO+1)]
            for meal in combo_meals:
                meal_data     = meal.to_json()
                day_calories += meal_data['calories']
                day_data['meals'].append(meal_data)
            
            day_data['day_calories'] = day_calories
            total_week_calories     += day_calories

            weekly_plan_data['plan'].append(day_data)

        weekly_plan_data['total_calories_week'] = total_week_calories
        return weekly_plan_data
