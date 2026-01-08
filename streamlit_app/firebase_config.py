import pyrebase

firebase_config = {
    "apiKey": "AIzaSyBmI-Wj16ri5XpsZLiK5RPLB0qLPip4bZg",
    "authDomain": "lexiscan-142819.firebaseapp.com",
    "projectId": "lexiscan-142819",
    "storageBucket": "lexiscan-142819.appspot.com",
    "messagingSenderId": "445688272307",
    "appId": "1:445688272307:web:21900cbed132ff325527c6",
    "measurementId": "G-FRSVTGVVW1",
    "databaseURL": ""
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
