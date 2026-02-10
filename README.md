# PROYEK GKM-SUBLINE-4.0

Proyek GKM-SUBLINE 4.0 Dibuat Menggunakan Bahasa Pemrograman Python version 3.9 .

Menggunakan Framework Flask version 2.0.2 .

Terintegrasi Dengan Flask-SQLalchemy, Flask-Admin, API Internal IT, Sphinx Documentation, Pandas, Plotly.

## Flask Application Structure 
- Jika ingin melihat detail dokumentasi buka folder :
  ```
  docs/build/html/index.html
  ```
- Struktur Folder Project :
  ```
  |──────app_center/
  | |──────entry/
  | | |──────controller/
  | | |──────model/
  | | |──────view/
  | |──────process
  | | |──────controller/
  | | |──────model/
  | | |──────view/
  | |──────exit
  | | |──────controller/
  | | |──────model/
  | | |──────view/
  | |──────static/
  | |──────template/
  | |──────__init__.py
  | |────docs/
  | |────env/
  | |────migrations/
  | |────config.py
  | |────requirements.txt
  |──────run.py
  ```

## Flask Database Structure 
- GKM-SUBLINE

![GKM-SUBLINE](https://user-images.githubusercontent.com/58338837/163771356-a93b7ef4-4e8a-4cd3-9de9-44829d5b5c06.png)


### Extension:
- FLask :[Flask-Module](https://flask.palletsprojects.com/en/2.1.x/)

- SQL ORM: [Flask-SQLalchemy](http://flask-sqlalchemy.pocoo.org/2.1/)

- Admin: [Flask-Admin](https://flask-admin.readthedocs.io/en/latest/)

- Sphinx: [Sphinx-Dcoumentation](https://www.sphinx-doc.org/en/master/contents.html)

- Pandas: [Pandas](https://pandas.pydata.org/docs/getting_started/install.html)

- Plotly: [Plotly](https://plotly.com/python/getting-started/) , [Plotly-Express](https://plotly.com/python/plotly-express/) 


## Cloning Repository

Buat Folder di PC / Laptop local, Lalu Clone Repository Dengan Ketik Perintah Di Terminal :

```
git clone https://github.com/dummy/GKM-SUBLINE-4.0.git
```

## Installation

Install with pip:

```
$ pip install -r requirements.txt
```

## Migrations

Migrate with Flask:

```
$ flask db migrate -m '{{Keterangan}}'
```

## Run Flask
### Run flask for development
```
$ flask run
```
In flask, Default port is `5000`

Running on page:  `http://127.0.0.1:5000/`

### Run flask for production
```
$ flask run --host=172.20.140.98 --port=2000
```
In Project GKM-SUBLINE-4.0, Default port is `2000`

Running on page:  `http://172.20.140.98:2000/`

## Reference

Offical Website

- [Flask](http://flask.pocoo.org/)
- [Flask Extension](http://flask.pocoo.org/extensions/)
- [Flask-SQLalchemy](http://flask-sqlalchemy.pocoo.org/2.1/)
- [elasticsearch-dsl](http://elasticsearch-dsl.readthedocs.io/en/latest/index.html)

Tutorial

- [Flask Overview](https://www.slideshare.net/maxcnunes1/flask-python-16299282)
- [In Flask we trust](http://igordavydenko.com/talks/ua-pycon-2012.pdf)


## Changelog

- Version 1.0 : add Sphinx Documentation
- Version 1.0 : add Database Documentation
