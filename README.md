SENG422
=======

Land Surveyor Django Application

Recommended Django Installation Steps (for Linux master race)
-------------------------------------------------------------

Install pip (package manager for python)
* sudo apt-get install python-pip

Install Django
* sudo pip install Django==1.6.5

Install django-passwords (used to enforce password strength)
* sudo pip install django-passwords

Running the Server
------------------

Using python 2.7.x and django 1.6.5: 'python manage.py runserver' will start the server.

Note: The SQL database is included as 'db.sqlite3' for everyone's use. Please keep this updated by running the 'python manage.py syncdb' command(s) when changing the Model classes.

Admin Interface
---------------

The admin interface can be found at localhost:8000/admin/

Username: admin
Password: admin

Since we are using the built-in django authentication module, this provides user creation, password changing, and admin logging for free.

Home Page
---------

The login page can be found at localhost:8000/

Project Structure
-----------------

The lscs directory contains the authentication stuff (logging in, signing up new users, resetting passwords), and the surveys directory contains the surveys django app which is the main project.

Adding New Pages
----------------

To add a new page, first update the controller (urls.py) to point to your django app or directly to your view/template. 
Next create your view/template combination for the new page.

