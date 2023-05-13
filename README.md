1. Install python
2. Install pipenv:
```
python -m pip install pipenv
```
3. Install dependencies
```
python -m pipenv install --dev
```
4. Connect in settings.py your mysql database
5. Run/make migrations
```
python -m pipenv shell
python manage.py migrate
```
6. Run dev server
```
python manage.py runserver
```

In case api doesn't work repeat from Step 3
