from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


POSTGRES = {
	'ENGINE': 'django.contrib.gis.db.backends.postgis',
	'NAME': 'live_poll_view',
	'USER': 'django',
	'PASSWORD': 'e2a78aa641d7519a96e99040aa21a2bb',
	'OPTIONS': {
	},
}

SQLITE = {
	# 'ENGINE': 'django.db.backends.sqlite3',
	"ENGINE": "django.contrib.gis.db.backends.spatialite",
	'NAME': BASE_DIR / 'db.sqlite3',
}

DB_CONFIG = {
	'default': SQLITE,
}
