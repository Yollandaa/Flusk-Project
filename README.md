# Flusk-Project

## Create virtual environment
- Creates a copy of your current python
    - ```bash python -m venv myen ```
- ```.\myenv\Scripts\Activate.ps1``` -> activate -> python -> local copy of python
- ```deactivate``` -> python -> global python installed
- Create a gitignore file and insert "myenv" so that it ignores any changes in the myenv folder.

## Git
- Initialize the git repository
```sh
git init
```
- Then the normal git add, commit, and push

## Installing Flask
- Make sure your env is activated, then install flask: [ref](https://flask.palletsprojects.com/en/3.0.x/installation/)
```sh
pip install flask
```

## Why Flask?
- Building are own mock API.
- Micro-framework(lightweight) that gives you tools to do the REST API.
- Flask gives you the freedom to choose whatever library you want to use
- Django -> Has everything inbuilt.

## How to run flask
```sh
flask --app main run
```

- If my file name is app:
```sh  
flask run 
```

- For development:
```sh  
flask run  --debug
```

## Jinja 2
- What python gives you to manipulate your html
- Improves DX
    - Easy to create templates

## Installing Dependencies
```sh
pip install -r requirements.txt
```
- Sharing your project with others: If you share your project with others, you can include the requirements.txt file so that they can easily install the required packages.
- Managing dependencies: By listing the dependencies of your project in a requirements.txt file, you can easily see what packages are required and what versions they need to be.