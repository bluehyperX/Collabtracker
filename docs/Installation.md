# Steps to install -

## Setup Django Backend

1. Clone the repo in home directory and open a new terminal inside it.
1. Install python virtual environment to keep the modules seperate using - 
`sudo apt update && sudo apt upgrade && sudo apt install -y python3-venv`
1. Create a virtual environment -
`python -m venv venv`
1. Activate the environment -
`source venv/bin/activate`
1. Install the required modules in the environment -
`cd backend && pip install -r requirements.txt`
1. Create migration for the database -
`python manage.py makemigration employees repositories`
1. Create the Sqlite database using the migrations -
`python manage.py migrate`
1. Create admin for Django server to add repositories -
`python manage.py createsuperuser`
1. Enter username, skip email, and enter password, reenter password to create an admin
1. Start the Django server -
`python manage.py runserver`
1. Go to `http://127.0.0.1:8000/admin/` and login with the admin credentials to add repositories.

    **_NOTE:_** Add only SSH links for the repositories. HTTPS links interfere with the automation script.
1. Close the django server `Ctrl+C` after adding the repositories
1. Run the utils.py script to populate the database for the first time. (We only need to do this once as we are going to setup a cronjob for that) -
`python utils.py`
1. Start the django server again

## Setup React Frontend

1. Now, create a new terminal in the `frontend` folder.
1. Install Node Version Manager to install nodejs and npm -
`curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash`
1. Do `source ~/.bashrc` to update the refresh the terminal
1. Install Node v16.17.0 -
`nvm install 16.17.0`
1. Install the required packages -
`npm install`
1. Start the React Frontend -
`npm start`

## Setup Cronjob

To setup cronjob for database updates, run the below command - 

`echo "0 0 * * * ~/Collabtracker/venv/bin/python ~/Collabtracker/backend/utils.py" | crontab -`

This command will setup a cronjob which will run every midnight and update the database with the latest repository data. 

## Running the web server

To run the webserver again after installation, run the following commands -

For Backend - `cd backend && source ../venv/bin/activate && python manage.py runserver`
For Frontend - `cd frontend && npm start`

To quit/stop - `Ctrl+C` (for both)