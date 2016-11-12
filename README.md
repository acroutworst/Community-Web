[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/acroutworst/Community-Web)

Community
=======================

Community is a social platform to connect with like-minded community members and to bring together a community of individuals.


## Web App
Repository for the Community web application.

### Dependencies
* Python 3
* Django
* Django Rest Framework


### Local Environment Setup
1. Install Python 3.x
2. Navigate to project directory
3. Execute command: `python bootstrap_venv.py`

NOTE: For mac users, ignore the command `python bootstrap_venv.py` and run the setup.sh script:
  ```bash setup.sh```

### Running the server locally
1. Activate .venv virtual environment
2. Execute in project root: `python manage.py migrate`
3. Execute in project root: `python manage.py runserver`
4. Navigate to localhost:8000

