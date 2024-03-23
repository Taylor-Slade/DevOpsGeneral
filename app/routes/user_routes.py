from flask import Blueprint, request, render_template, redirect, url_for, abort, jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from app import db
from app.models.models import User
from app.schemas.user_schema import UserSchema

user_schema = UserSchema()
users_schema = UserSchema(many=True)
bp = Blueprint('user', __name__, url_prefix='/users')


@bp.route('/', methods=['GET'])
def index():
    try:
        users = User.query.all()
        return render_template('user_index.html', users=users)
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        return user_schema.dump(user)
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@bp.route('/create', methods=['POST'])
def create_user():
    try:
        user_data = user_schema.load(request.form)

        password = user_data.pop('password', None)

        new_user = User(**user_data)

        if password:
            new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('user.index'))
    except ValidationError as e:
        return jsonify({"error": "Invalid db", "messages": e.messages}), 400
    except IntegrityError as e:
        db.session.rollback()
        error_message = "An error occurred. Please try again."
        if 'user.email' in str(e.__cause__):
            error_message = "This email is already in use. Please choose a different email."
        elif 'user.username' in str(e.__cause__):
            error_message = "This username is already taken. Please choose a different username."
        return jsonify({"error": error_message}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@bp.route('/<int:id>/update', methods=['POST'])
def update_user(id):
    try:
        user = User.query.get_or_404(id)
        user_data = user_schema.load(request.form, partial=True)

        for key, value in user_data.items():
            setattr(user, key, value)

        db.session.commit()
        return redirect(url_for('user.index'))
    except ValidationError as e:
        return jsonify({"error": "Invalid db", "messages": e.messages}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@bp.route('/<int:id>/delete', methods=['POST'])
def delete_user(id):
    try:
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('user.index'))
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500
