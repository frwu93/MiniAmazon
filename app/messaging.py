from flask import render_template
from flask_login import current_user
import datetime

from .models.cart import Cart
from .models.product import Product
from flask import render_template, redirect, url_for, flash, request



from flask import Blueprint
bp = Blueprint('messaging', __name__)

@bp.route('/messages', methods=['GET'])
def messages():
    print("go to messages")
    return render_template('messaging.html', title='Message')

@bp.route('/feedback.html', methods=['GET'])
def feedback():
    print("go to messageshtml")
    return render_template('feedback.html', title='Feedback')


@bp.route('/post_review.html', methods=['GET'])
def post_review():
    print("go to post_review")
    return render_template('post_review.html', title='Post Review')