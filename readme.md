# 100-best-books
==========================

An website to play with the 100 best classical books of all time.

# Configuration

In order to launch the project you must define a config file. To do so, export an `env` variable called `HUNDREDBESTBOOKS_SETTINGS` which define the path to your config file.

```shell
export HUNDREDBESTBOOKS_SETTINGS=settings.py
```

An example of your config file could be:

```shell
# configuration
DEBUG = True
ISBNDB_KEY = 'MY_FAKE_KEY'
SECRET_KEY = 'your session key'
USERNAME = 'username'
PASSWORD = 'password'
ENVIRONMENT = 'development'
```

You can switch the `ENVIRONMENT` form `development` to `production` variable depending whether you need the assets to be build or not. For example, if you run the project on Google App Engine, you will need to deactivate the assets building.

# Installation

This project project depends on some libraries, so you must install them via bower before running it.

```shell
bower install
```

# Run the app

## In the local environment

Launch the python web server with the following command and visit http://localhost:5000.

```shell
python web.py
```

## In the local Google App Engine environment

Launch the Google App Engine web server with the following command and visit http://localhost:8080.

```shell
dev_appserver.py .
```

Access the local Google App Engine console at http://localhost:8000/instances.

# Push the modifications to Google App Engine

Before pushing the code to Google App Engine you need to edit and change the configuration setting 'ENVIRONMENT' to "production".

```
appcfg.py -A hundred-best-books update .
```
