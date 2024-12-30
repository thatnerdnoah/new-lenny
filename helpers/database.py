import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

local_test = False

try:
    import config_local as config
    local_test = True
except ImportError:
    import config

cred = credentials.Certificate(config.path_to_credential)
firebase_admin.initialize_app(cred)
 
db = firestore.client()

def database_pull():
    expected_number : int = 0
    record : int = 0
    lives : int = 0

    if not config.local_test:
        doc_ref = db.collection(u'counting').document(u'count')
    else:
        doc_ref = db.collection(u'counting').document(u'count_test')
        

    doc = doc_ref.get()
    if doc.exists:
        expected_number = doc.to_dict()['count']
        record = doc.to_dict()['reward']
        lives = doc.to_dict()['lives']

    return expected_number, record, lives

def update_record(num: int):
    if not config.local_test:
        counter_ref = db.collection(u'counting').document(u'count')
    else:
        counter_ref = db.collection(u'counting').document(u'count_test')

    counter_ref.update({
        u'reward': num
    })

def database_push(num: int):
    if not config.local_test:
        counter_ref = db.collection(u'counting').document(u'count')
    else:
        counter_ref = db.collection(u'counting').document(u'count_test')

    counter_ref.update({
        u'count': num
    })

def update_lives(num: int):
    if not config.local_test:
        counter_ref = db.collection(u'counting').document(u'count')
    else:
        counter_ref = db.collection(u'counting').document(u'count_test')

    counter_ref.update({
        u'lives': num
    })

def database_copy(num: int):
    if not config.local_test:
        counter_ref = db.collection(u'counting').document(u'count')
    else:
        counter_ref = db.collection(u'counting').document(u'count_test')
    
    if num >= 1:
        counter_ref.update ({
            u'count_backup': num
        })

def pull_backup():
    backup_numnber: int = 0
    
    if not config.local_test:
        doc_ref = db.collection(u'counting').document(u'count')
    else:
        doc_ref = db.collection(u'counting').document(u'count_test')

    doc = doc_ref.get()
    if doc.exists:
        backup_numnber = doc.to_dict()['count_backup']

    return backup_numnber

def letter_pull():
    current_letter = 'a'
    lives = 2

    if not config.local_test:
        doc_ref = db.collection(u'letter').document(u'letter')
    else:
        doc_ref = db.collection(u'letter').document(u'letter_test')

    doc = doc_ref.get()
    if doc.exists:
        current_letter = doc.to_dict()['letter']
        lives = doc.to_dict()['lives']

    return current_letter, lives

def letter_push(letter: str):
    if not config.local_test:
        doc_ref = db.collection(u'letter').document(u'letter')
    else:
        doc_ref = db.collection(u'letter').document(u'letter_test')

    doc_ref.update({
        u'letter': f"{letter}"
    })