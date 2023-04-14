# LivePollView
A Portfolio Project in partial fulfilment for the requirements of the ALX Software Engineering program

Authors:
- Peter
- Ezechiel
- Japhet
## Demo
A demo is available at https://peterchibunna.github.io/LivePollView/  with a CTA linking to https://peterchibunna.tech/

## Setup Requirements
At the moment, we're using sqlite for portability. For production, we might move to a RDBMS, like
MySQL, PostgreSQL, Oracle, etc.

We need to install the spatial extension (Geospatial Data Abstraction Library)(`gdal`) depending on your Operating System

Ubuntu: `$ sudo apt install gdal-bin libgdal-dev`<br>
Windows: <br>
MacOS: ``<br>
### SQLite:
For SQLite database: SpatiaLite

on Debian-based GNU/Linux distributions (es: Debian, Ubuntu, …):

`$ apt install libsqlite3-mod-spatialite`

on macOS using Homebrew:

`$ brew install spatialite-tools`


## Testing and Installation and Usage
This app is built on the **[Django](htttps://www.djangoproject.com) web framework**.

- Clone the repo `git clone https://github.com/peterchibunna/LivePollView.git`
- `cd` into the Project folder, and
- create a virtual environment: `virtualenv -p python3 venv`
- Activate the virtual environment: `source venv/bin/activate`
- Install the project pip requirements: `pip install -r requirements.txt`
- The run the test server: `./manage.py runserver localhost:8080`
- For deployment, we need gunicorn and nginx proxying the gunicorn socket.
- Open your web browser and navigate to `http://localhost:8080/` or the address with port of your choice as configured

## Troubleshooting

Make sure the required packages are installed. For example, you might encounter errors
if you didn't install the gdal libraries.
