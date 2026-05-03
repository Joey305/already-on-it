from __future__ import annotations

import csv
import os
from datetime import datetime
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, url_for


def create_app() -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.update(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'change-me-for-production'),
        BUSINESS_PHONE=os.environ.get('BUSINESS_PHONE', '732-996-8234'),
        BUSINESS_EMAIL=os.environ.get('BUSINESS_EMAIL', 'alreadyonitllc@gmail.com'),
        BUSINESS_NAME='Already On IT LLC',
        SERVICE_AREA='Naranja and throughout South Florida',
    )

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.post('/contact')
    def contact():
        name = request.form.get('name', '').strip()
        phone = request.form.get('phone', '').strip()
        email = request.form.get('email', '').strip()
        service = request.form.get('service', '').strip()
        message = request.form.get('message', '').strip()

        if not name or not (phone or email) or not message:
            flash('Please include your name, a phone or email, and a short project message.', 'error')
            return redirect(url_for('index') + '#contact')

        csv_path = Path(app.instance_path) / 'messages.csv'
        is_new = not csv_path.exists()
        with csv_path.open('a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if is_new:
                writer.writerow(['timestamp_utc', 'name', 'phone', 'email', 'service', 'message'])
            writer.writerow([
                datetime.utcnow().isoformat(timespec='seconds') + 'Z',
                name,
                phone,
                email,
                service,
                message,
            ])

        flash("Thanks — your message was saved. You can later wire this form to email, a CRM, or a database.", 'success')
        return redirect(url_for('index') + '#contact')

    return app


app = create_app()


if __name__ == '__main__':
    app.run(debug=True, port=5055)