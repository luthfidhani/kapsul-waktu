import json
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from web import cache
from web.models import db, Message
from web.utils import decrypt_message, encrypt_message, calculate_hash, expiration_date_check


urls_blueprint = Blueprint('urls', __name__)

@urls_blueprint.route('/')
def index():
    return render_template('index.html')

@urls_blueprint.route('/save_message', methods=['POST'])
def save_message():
    if request.method == 'POST':
        message_content = request.form['message']
        original_date = datetime.strptime(request.form['expiration_time'], '%Y-%m-%d')
        formatted_date_str = original_date.strftime('%d-%m-%Y')

        encrypted_message, encryption_key = encrypt_message(message_content)
        url_hash = calculate_hash(encrypted_message.encode())

        new_message = Message(
            encrypted_message=encrypted_message,
            encryption_key=encryption_key,
            url_hash=url_hash,
            expiration_time=formatted_date_str,
        )

        db.session.add(new_message)
        db.session.commit()

        message_link = url_for('urls.view_message', hash=url_hash, _external=True)
        flash(f'Pesan berhasil disimpan! Berikut adalah link pesan Anda: {message_link}', 'success')

        return render_template('message_link.html', message_link=message_link)

    return redirect(url_for('urls.index'))


@urls_blueprint.route('/<hash>')
def view_message(hash):
    caching_message = cache.hgetall(f"message:{hash}")

    if caching_message:
        caching_message = {key.decode('utf-8'): value.decode('utf-8') for key, value in caching_message.items()}
    else:
        message = Message.query.filter_by(url_hash=hash).first()
        if not message:
            return render_template('404.html')

        caching_message = {
            "id": message.id,
            "encrypted_message": message.encrypted_message,
            "encryption_key": message.encryption_key,
            "url_hash": message.url_hash,
            "expiration_time": message.expiration_time,
            "created_at": message.created_at,
        }

    cache.hset(f"message:{hash}",mapping=caching_message)
    cache.expire(
        f"message:{hash}",
        60*60*1,  # 1 day
    )

    if expiration_date_check(caching_message["expiration_time"]):
        data = {
            "status": True,
            "message": decrypt_message(caching_message["encrypted_message"], caching_message["encryption_key"]),
            "date": caching_message["expiration_time"],
        }

    else:
        data = {
            "status": False,
            "date": caching_message["expiration_time"]
        }

    return render_template('view_message.html', data=data)
