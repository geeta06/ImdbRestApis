Authenticated RestApis in Flask

Login api for admin the user is created use the username and password provided over mail.

Host
  	127.0.0.1:5000

Url
 	{{Host}}/login

Method
POST

Raw Json Body
	{
	"username": "admin",
	“password": "admin"
}

Success Response

Code : 200
Response :  
{    "token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImZ5bmQiLCJleHAiOjE2MjIzNTkxMjF9.lgOEcmTp5328UsAjo1csZmwB5JSvB2hCQZYKkteLzJM"
  }
 
Failure Response
Code : 400
Response:
Bad Request


Error  Response
Code : 500
Response:
Internal Server Error
