# LivePollView
A Portfolio Project in partial fulfilment for the requirements of the ALX Software Engineering program

Authors:
- Peter
- Ezechiel
- Japhet


## Setup Requirements
At the moment, we're using sqlite for portability. For production, we'll move to a RDBMS, like
MySQL, PostgreSQL, etc.

We need to install the spatial extension depending on your Operating System

Ubuntu: `$ sudo apt install gdal-bin`<br>
Windows: <br>
MacOS: ``<br>
### SQLite:
For SQLite database: SpatiaLite

on Debian-based GNU/Linux distributions (es: Debian, Ubuntu, …):

`$ apt install libsqlite3-mod-spatialite`

on macOS using Homebrew:

`$ brew install spatialite-tools`


# Testing
This app is built on the **[Django](htttps://www.djangoproject.com) web framework**.

- Clone the repo `git clone ...`
- `cd` into the Project folder, and
- create a virtual environment: `virtualenv -p python3 venv`
- Activate the virtual environment: `source venv/bin/activate`
- Install the project pip requirements: `pip install -r requirements.txt`
- The run the test server: `./manage.py runserver localhost:8080`
- Open your web browser and navigate to `http://localhost:8080/`
