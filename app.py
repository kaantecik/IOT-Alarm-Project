import uuid
from db import Database
from flask_cors import CORS
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request, flash

app = Flask(__name__)
CORS(app)
db = Database()
app.secret_key = "790119ec-487c-11eb-ba89-acde48001122"


@app.route('/')
def home_page():
    return render_template("home.html")


@app.route('/alarm/toggle/<alarm_id>')
def toggle_alarm(alarm_id):
    db.toggle_alarm(alarm_id)
    return redirect(url_for('home_page'))


@app.route('/alarm/create', methods=['GET', 'POST'])
def create_alarm():
    if request.method == 'POST':
        try:
            alarm_id = str(uuid.uuid1())
            now = str(datetime.now().utcnow())
            created_at = now
            updated_at = now
            start_hour = request.form.get('start_hour')
            status = request.form.get('status') or 'off'
            db.create_alarm(
                data={
                    "alarm_id": alarm_id,
                    "created_at": created_at,
                    "updated_at": updated_at,
                    "start_hour": start_hour,
                    "status": status}
            )
        except Exception:
            flash('An error occurred', 'warning')
        return redirect(url_for("alarms_page"))
    return render_template("create_alarm.html")


@app.route('/alarm/delete/<alarm_id>')
def delete_alarm(alarm_id):
    db.delete_alarm(alarm_id)
    return redirect(url_for("alarms_page"))


@app.route('/alarm/update/<alarm_id>', methods=['GET', 'POST'])
def update_alarm(alarm_id):
    try:
        start_hour = request.form.get("start_hour")
        db.update_alarm(alarm_id, {"start_hour": start_hour, "updated_at": str(datetime.now().utcnow())})
        flash("You have been successfully update.", "success")
    except Exception as ex:
        print(ex)
        flash("An error occurred", "warning")
    return redirect(url_for('alarms_page'))


@app.route('/alarm')
def alarms_page():
    try:
        alarms = db.get_alarms().val().values()
    except Exception:
        alarms = []
    return render_template("alarms.html", alarms=alarms)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
