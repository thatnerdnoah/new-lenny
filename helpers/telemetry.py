import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import config
import datetime

db = firestore.client()

class Telemetry:
    def __init__(self, path="telemetry.json"):
        self.path = path
        self.date = str(datetime.date.today())
        self.generated: int = 0
        self.success: int = 0
        self.fail: int = 0

    def pull_numbers(self):
        doc_ref = db.collection(u'telemetry').document(u'count_track')

        doc = doc_ref.get()
        if doc.exists:
            self.generated = doc.to_dict()['generated']
            self.success = doc.to_dict()['success']
            self.fail = doc.to_dict()['fail']

    def update(self, num, field: str = "generated"):
        doc_ref = db.collection(u'telemetry').document(u'count_track')

        doc_ref.update({
            field: num
        })

        if field == "success":
            self.success += 1
        elif field == "fail":
            self.fail += 1
        else:
            self.generated += 1
            