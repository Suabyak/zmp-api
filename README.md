1. Install python
2. Install pipenv:
```
python -m pip install pipenv
```
3. Install dependencies
```
python -m pipenv shell
pipenv install --dev
```
3. Connect in settings.py your mysql database
4. Run/make migrations
```
python manage.py makemigrations
python manage.py migrate
```
5. Run dev server
```
python manage.py runserver
```

In case api doesn't work repeat Step 3
