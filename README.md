Introduction 
-
This is imdb like project used to search movies and get details about the movies. It contains backend RestApis in flask using sqlite database.
-
Authenticated CRUD Apis for admin

http://flask-imdb-apis.herokuapp.com/login

http://flask-imdb-apis.herokuapp.com/api/v1/add/movie

http://flask-imdb-apis.herokuapp.com/api/v1/update/movie

http://flask-imdb-apis.herokuapp.com/api/v1/delete/movie


-
Public Apis to get list of movies or to search any movie

http://flask-imdb-apis.herokuapp.com/api/v1/movies

http://flask-imdb-apis.herokuapp.com/api/v1/search/movie?name=Kong

-
Login to below api Using the username and password provided
A jwt token will be provied 

Url
http://flask-imdb-apis.herokuapp.com/login


Raw Json Body
{
	"username": "admin",
	“password": "admin"
}


return 
Success Response
Code : 200 - OK

Response :  

{    "token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImZ5bmQiLCJleHAiOjE2MjIzNTkxMjF9.lgOEcmTp5328UsAjo1csZmwB5JSvB2hCQZYKkteLzJM"
  }
  
return 
Failure Response 

400 : Bad Request

500 : Internal Server Error


-
Authenticated add movie api for admin to use any new movie using below details

Url
http://flask-imdb-apis.herokuapp.com/api/v1/add/movie

Headers

{
"Content-Type": "application/json",
   "x-access-token" : "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImZ5bmQiLCJleHAiOjE2MjIzNTkxMjF9.lgOEcmTp5328UsAjo1csZmwB5JSvB2hCQZYKkteLzJM"
}


Raw Json Body
{
    "99popularity": 88.0,
    "director": "George Lucas",
     "movies_id": "NU8Y4DNJMD",
    "genre": [
      "Action",
      " Adventure"
    ],
    "imdb_score": 8.8,
    "name": "Star "
  }
  
  
Success Response
Code : 200 - OK

Response :  
{
    "message": "Movie Added Successfully."
  }
  
Failure Response

Code : 400 Bad Request

500: Internal Server Error

-


This Api is used by Admin to update any movie 

Url
http://flask-imdb-apis.herokuapp.com/api/v1/update/movie


Headers
{
"Content-Type": "application/json",
   "x-access-token" : "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImZ5bmQiLCJleHAiOjE2MjIzNTkxMjF9.lgOEcmTp5328UsAjo1csZmwB5JSvB2hCQZYKkteLzJM"
}


Raw Json Body
{
    "99popularity": 88.0,
    "director": "George Lucas",
     "movies_id": "NU8Y4DNJMD",
    "genre": [
      "Action",
      " Adventure"
    ],
    "imdb_score": 8.8,
    "name": "Star Wars "
  }
  
Success Response
Code : 200 - OK
Response :  
  {
    "message":"Movie Updated Successfully."
  }


Failure Response
Code : 400 Bad Request
500: Internal Server Error


-
This api is used by admin to delete any movie from the Database

Url
http://flask-imdb-apis.herokuapp.com/api/v1/delete/movie


Headers
{
"Content-Type": "application/json",
   "x-access-token" : "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImZ5bmQiLCJleHAiOjE2MjIzNTkxMjF9.lgOEcmTp5328UsAjo1csZmwB5JSvB2hCQZYKkteLzJM"
}


Raw Json Body
	{  
    "movies_id": "NU8Y4DNMD"
}


Success Response
Code : 200
Response :  
{
    "message": "Movie Deleted Successfully."
  }


-
Public Api to get all the movies from the database 


Url
http://flask-imdb-apis.herokuapp.com/api/v1/movies

params

offset=0

return

Success Response
Code : 200
Response :  
[
    {
      "99popularity": 66.0,
      "director": "Giovanni Pastrone",
      "genre": [
        "ADVENTURE",
        "DRAMA",
        "WAR"
      ],
      "imdb_score": 6.6,
      "movies_id": "728SCC8KDT",
      "name": "Cabiria"
    },
    {
      "99popularity": 87.0,
      "director": "Alfred Hitchcock",
      "genre": [
        "HORROR",
        "MYSTERY",
        "THRILLER"
      ],
      "imdb_score": 8.7,
      "movies_id": "N6Y68DX744",
      "name": "Psycho"
    },
]
return 500 Internal Server Error

-
Public Api to search any movie from Database based its name, popularity, imdb_score, director name, genre
to search by name

Url
http://flask-imdb-apis.herokuapp.com/api/v1/search/movie?name=Kong

return
Code : 200
Response :  
   	[
  {
    "99popularity": 80.0,
    "director": "Merian C. Cooper",
    "genre": [
      "ADVENTURE",
      "FANTASY",
      "HORROR"
    ],
    "imdb_score": 8.0,
    "movies_id": "5NLY9Y96BX",
    "name": "King Kong"
  }
]

return 400 Bad request

return 500 Internal sever error


similarly to search by imdb_score
Url 
http://flask-imdb-apis.herokuapp.com/api/v1/search/movie?imdb_score=9


return 
200-OK

[{
    "99popularity": 92.0,
    "director": "Francis Ford Coppola",
    "genre": [
      "CRIME",
      "DRAMA"
    ],
    "imdb_score": 9.2,
    "movies_id": "HI4GRF7QTQ",
    "name": "The Godfather"
  },
  {
    "99popularity": 90.0,
    "director": "Sergio Leone",
    "genre": [
      "ADVENTURE",
      "WESTERN"
    ],
    "imdb_score": 9.0,
    "movies_id": "79G61YEQA8",
    "name": "Il buono, il brutto, il cattivo."
  }]
  

400- Bad Request

500-Internal Server Error


likewise for other search
