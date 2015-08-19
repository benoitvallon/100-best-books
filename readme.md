# bokklubben-world-library
==========================

An website to play with the Bokklubben World Library which is a series of the 100 best classical books

# Configuration

In order to launch the project you must define a config file. To do so, export an `env` variable called `BOKKLUBBEN_SETTINGS` which define the path to your config file.

```shell
export BOKKLUBBEN_SETTINGS=settings.py
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
