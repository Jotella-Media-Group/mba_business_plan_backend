# MBA-BUSINESS-PLAN

> Django Backend api for MBA-BUSINESS-PLAN APP.
> ![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg) > ![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)

## Requirements (Prerequisites)

Tools and packages required to successfully install this project.
For example:

- Python 3.7 and up [Install](https://python.org)
- Postgres 14.0 and up [Install](https://postgres.com/)

## Installation (DEVELOPMENT SETUP)

- Create a .env file in root directory to override all environmental variables

- You can also set the variable as system variables

A step by step list of commands.

`$ git clone project-ul`

`$ python3 -m venv env`

`$ source env/bin/activate`

`$ pip install -r requirements.txt`

`$ python manage.py migrate`

`$ bash scripts/load_data.sh`

`$ python manage.py runserver_plus 8000`

## Installation (DOCKER SETUP)

- Remane the .env.example file in root directory to .env

- Ask the PM for valid cedentials and use it the update the .env file

- Install Docker Desktop [Install](https://python.org)

A step by step list of commands.

`$ git clone project-ul`

`$ cd mba_business_plan`

`$ docker-compose up --build -d`

- Visit localhost:8000 in your browser

## How View the Swagger documentation

- Visit localhost:8000/admin

- Login with admin@demo.com:323f'@2#$

- Visit localhost:7000/swagger

## Features

- Account registration

## Running the tests

Give code examples as:

- `$ python manage.py test`

## Test account

    admin admin@demo.com:323f'@2#$

    clent client@demo.com:323f$@2*&

## Tech Stack / Built With

1. [Django](https://django.com/) - The Python framework
1. [Postgres](https://postgres.com/) - The Database

## Authors

Emmanuel Nartey – aggrey.en@gmail.com

You can find me here at:
[Github](https://github.com/Emmanuel-Aggrey)
[LinkedIn](https://www.linkedin.com/in/emmanuel-teye-nartey/)

## License

This project is licensed under the MIT License - see the LICENSE.md file for details

MIT © BPOHOMES
# mba_business_plan_backend
