# Najua: A Quiz Webapp
#### Video Demo:  <URL HERE>
#### Description: Najua means I know in my native swahili. A perfect name for this quiz app built with flask, vanilla JS, TriviaAPI, and Firebase Realtime database and storage.

# Installation
## Requirements
Python 3.xx
configured firebase project
running redis-server

##Instuctions
### Configure Firebase
go to https://console.firebase.google.com/
- Get started with Firebase project
- On the add an app to get started pick web
- Register app


On add firebase SDK step, copy 
apiKey:
authDomain:
projectId:
storageBucket:
messagingSenderId:
appId:
measurementId:

Add these values to the .env file

Go to Build > authentication
select sign-in provider as email/password and enable the email/password option

Go to Build > firebase database
create database
start in test mode
create
click on rules tab and ensure rules are set to allow read, write
Go to build > storage
get started, start in test mode

save the .env file in the root folder of the app

# Features


clone auth submodule
go to auth folder then:
git submodule init
git submodule update

