import os
import json
import unittest
import requests
import copy

# HOST = "http://localhost:5000"
HOST = "http://flask-imdb-apis.herokuapp.com"


class TestMovies(unittest.TestCase):

    data = {
        "director": "Test Director",
        "genre": [" Fiction", " Fantasy"],
        "99popularity": 87,
        "imdb_score": 8.3,
        "name": "Test Movie 1",
    }

    movieid = None
    token = None


    def test_A(self):
        # Test Request API : /v1/user/login
        # Login user-account using credentials

        LOGIN_URL = HOST + "/login"
        login_data = {"username": "fynd", "password": "admin123"}

        response = requests.post(
            url=LOGIN_URL,
            data=json.dumps(login_data),
            headers={"Content-Type": "application/json"},
        )
        TestMovies.token = json.loads(response.content)["token"]
        self.assertEqual(response.status_code, 200)

    def test_B(self):
        # Test Request API: /api/v1/add/movies
        # Add movies to database
        data = copy.deepcopy(TestMovies.data)
        URL = HOST + "/api/v1/add/movie"
        headers = {"Content-Type": "application/json", "x-access-token": TestMovies.token}

        response = requests.post(url=URL, data=json.dumps(data), headers=headers)
        self.assertEqual(response.status_code, 200)


    def test_C(self):
        # Test Request API: /api/v1/add/movies
        # Testing parameter missing error for API
        data = copy.deepcopy(TestMovies.data)
        data.pop("imdb_score")

        URL = HOST + "/api/v1/add/movie"
        headers = {"Content-Type": "application/json", "x-access-token": TestMovies.token}

        response = requests.post(url=URL, data=json.dumps(data), headers=headers)

        self.assertEqual(response.status_code, 400)

    def test_E(self):
        # Test Request API: /api/v1/add/movies
        # Test outofbound index error of API
        data = copy.deepcopy(TestMovies.data)
        data["imdb_score"] = 19

        URL = HOST + "/api/v1/add/movie"
        headers = {"Content-Type": "application/json", "x-access-token": TestMovies.token}
        response = requests.post(url=URL, data=json.dumps(data), headers=headers)

        self.assertEqual(response.status_code, 400)