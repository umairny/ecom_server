# This file contains the WSGI configuration required to serve up your
# web application at http://umairahmad.pythonanywhere.com/
# It works by setting the variable 'application' to a WSGI handler of some
# description.
#
# The below has been auto-generated for your Django project

import os
import sys

# add your project directory to the sys.path
project_home = "/home/umairahmad/ecom_server"
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# set environment variable to tell django where your settings.py is
os.environ["DJANGO_SETTINGS_MODULE"] = "server.settings"


# serve django via WSGI
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
