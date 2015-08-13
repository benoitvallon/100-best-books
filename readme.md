# bokklubben-world-library
==========================

An website to play with the Bokklubben World Library which is a series of the 100 best classical books

# Configuration

In order to launch the project you must define a config file. To do so, export an `env` variable called `BOKKLUBBEN_SETTINGS` which define the path to your config file.

```shell
export BOKKLUBBEN_SETTINGS=settings.cfg
```

An example of your config file could be:

```shell
# configuration
DEBUG = True
ISBNDB_KEY = 'MY_FAKE_KEY'
SECRET_KEY = 'your session key'
USERNAME = 'username'
PASSWORD = 'password'
```
