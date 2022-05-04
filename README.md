# Draftshare
An API that allows you to get your ability draft match build visualized.

## Installation:
- ```git clone https://github.com/ArtemShishkin0```
- ```EXPORT STEAMAPI_DEV_KEY=Your_DEV_API_Key``` on Linux **or**
- ```SET STEAMAPI_DEV_KEY=Your_DEV_API_Key``` on Windows
- in directory with requirements.txt run  ```pip install requirements.txt ```
- in the same directory run  ```python3 manage.py runserver```

## Update constant data:
- run ```python3 get_(abilities, heroes or items).py``` from draftshare/data/scripts directory
- wait it to finish and start server

## Use:
- http://127.0.0.1:8000/api/match/{match_id}/{user_id}

E.g: 
- http://127.0.0.1:8000/api/match/6538553844/101013989 

## Example images:
 ![example1](https://github.com/ArtemShishkin0/draftshare/blob/main/ex1.png?raw=true)
 ![example2](https://github.com/ArtemShishkin0/draftshare/blob/main/ex2.png?raw=true)
