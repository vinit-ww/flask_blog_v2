Blogapp

Blogapp is an example Flask application illustrating some of my common practices

Development Environment

At the bare minimum you'll need the following for your development environment:

Python
MySQL
ORM
It is strongly recommended to also install and use the following tools:

virtualenv
Local Setup

The following assumes you have all of the recommended tools listed above installed.

1. Clone the project:
   
   git clone https://github.com/vinit-ww/flask_blog_v2.git
  
   cd flask_blog_v2

2. Create and initialize virtualenv for the project:
  
   virtualenv {name}

3. Start virtual machine:
   
   source {name}/bin/activate
   
   pip install -r requirements.txt
 
4. Upgrade the database:
   
   Use migrate ,upgrade
  
5. Run the development server:
   
   python run.py runserver
  
Development

If all went well in the setup above you will be ready to start hacking away on the application.

Database Migrations

python run.py db {command-name(migrate,init,upgrade)}

This application uses Alembic for database migrations and schema management. Changes or additions to the application data models will require the database be updated with the new tables and fields. Additionally, ensure that any new models are imported into the consolidated models file at overholt.models. To generate a migration file based on the current set of models run the following command:

python run.py db migrate

Review the resulting version file located in the Migrations/versions folder. If the file is to your liking upgrade the database with the following command:

cat {path}/{name_of_file}.py

Management Commands

Management commands can be listed with the following command:

python run.py {runserver,shell ...etc}

These can sometimes be useful to manipulate data while debugging in the browser.
