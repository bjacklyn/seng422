SENG422
=======

Land Surveyor Django Application

Running the Server
------------------

Using python 2.7.x and django 1.6.5: 'python manage.py runserver' will start the server.

Note: The SQL database is included as 'db.sqlite3' for everyone's use. Please keep this updated by running the 'python manage.py migrate' or 'python manage.py syncdb' command(s) when changing the Model classes.

Admin Interface
---------------

The admin interface can be found at localhost:8000/admin/
Username: admin
Password: admin

Since we are using the built-in django authentication module, this provides user creation, password changing, and admin logging for free.

Home Page
---------

Currently the (non-functional) login page can be found at localhost:8000/login/

Adding New Pages
----------------

To add a new page, first update the controller (urls.py) to point to your django app or directly to your view/template. 
Next create your view/template combination for the new page.

Note: the lscs directory contains the main django project -- the surveys directory contains the surveys django app which is included by the lscs project.

