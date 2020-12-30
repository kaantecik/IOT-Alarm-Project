import pyrebase
from datetime import  datetime

class Database:
    def __init__(self):
        self.config = {"apiKey": "AIzaSyAwCp-ovzcrMK_yI7kvP87IOcnQSU2qaMU",
                       "authDomain": "iot-alarm-project-213b5.firebaseapp.com",
                       "databaseURL":
                           "https://iot-alarm-project-213b5-default-rtdb.europe-west1.firebasedatabase.app",
                       "projectId": "iot-alarm-project-213b5",
                       "storageBucket": "iot-alarm-project-213b5.appspot.com",
                       "messagingSenderId": "942244618094",
                       "appId":
                           "1:942244618094:web:e1ad12bcc62feea120ab7f",
                       "measurementId": "G-376GEXM5HT"}
        try:
            firebase = pyrebase.initialize_app(self.config)
            self.db = firebase.database()
        except Exception as ex:
            print("An error occurred while  connecting firebase.", ex)

    def create_alarm(self, data):
        self.db.child("alarms").push(data)

    def update_alarm(self, alarm_id, data):
        try:
            for alarm in self.db.child('alarms').get().each():
                if alarm.val()['alarm_id'] == alarm_id:
                    self.db.child('alarms').child(alarm.key()).update(data)
        except Exception as ex:
            print(ex)

    def delete_alarm(self, alarm_id):
        try:
            for alarm in self.db.child('alarms').get().each():
                if alarm.val()['alarm_id'] == alarm_id:
                    print(alarm.key())
                    self.db.child("alarms").child(alarm.key()).remove()
        except Exception as ex:
            print(ex)

    def toggle_alarm(self, alarm_id):
        try:
            for alarm in self.db.child('alarms').get().each():
                if alarm.val()['alarm_id'] == alarm_id:
                    if alarm.val()['status'] == 'on':
                        status = 'off'
                    else:
                        status = 'on'
                    self.db.child('alarms').child(alarm.key()).update(
                        {"status": status, "updated_at": str(datetime.now().utcnow())})
        except Exception as ex:
            print(ex)

    def get_alarms(self):
        return self.db.child("alarms").get()

