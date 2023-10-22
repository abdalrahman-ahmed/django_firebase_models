# django_firebase_models
Simple django project with firebase plus models.


## Installation
### Clone the repository
```shell
git clone git@github.com:abdalrahman-ahmed/django_firebase_models.git
```
### Create a virtual environment
```shell
python -m venv venv
```
### Activate the virtual environment
#### Windows
```powershell
venv\Scripts\activate
```
#### Linux/Mac
```shell
source venv/bin/activate
```
###### Note: Your terminal should look like this
```shell
(venv) $
```
### Install requirements
##### Note: Make sure you are in the project directory
```shell
python -m pip install -r requirements.txt
```
### Create a firebase project
#### Go to [Firebase Console](https://console.firebase.google.com/)
#### Create a new project
#### Go to project settings
#### Go to service accounts
#### Click on generate new private key
#### Rename the downloaded file to `firebase_config.json`
#### Move the file to the project directory
### Run the server
```shell
python manage.py runserver
```
### Open the browser and Go to (http://127.0.0.1:8000/)