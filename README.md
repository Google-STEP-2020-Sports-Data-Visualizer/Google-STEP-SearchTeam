# Sports Data Visualization - Google STEP Interns 2020

## Overview


## Set up

### Prerequisites

- Python3 and Pip3 must be installed

### Setting up the project locally

- On cloning the repository, run `pip3 install requirements.txt`
- To install RabbitMQ:
    - On Ubuntu

      `sudo apt-get install -y erlang`
      `apt-get install rabbitmq-server`
    - On MacOS

      `brew install rabbitmq`

      The RabbitMQ scripts are installed into `/usr/local/sbin`. You can add it to your `.bash_profile` or `.profile`.

      `vim ~/.bash_profile`
      
      `export PATH=$PATH:/usr/local/sbin`

For more details, refer [here](https://simpleisbetterthancomplex.com/tutorial/2017/08/20/how-to-use-celery-with-django.html)


### Running the project locally

- `cd [your-project-folder-name]`
- In one terminal: `python3 manage.py runserver`
- In another terminal: To run `RabbitMQ`:
    - On Ubuntu

    `systemctl enable rabbitmq-server`
    `systemctl start rabbitmq-server`

    Check status:

    `systemctl status rabbitmq-server`

    To stop RabbitMQ:

    `sudo -u rabbitmq rabbitmqctl stop`

   - On MacOS:

     `rabbitmq-server`

- In another terminal: to run `Celery`: `celery worker -A howsThat --concurrency=5`

The webapp now runs on `http://localhost:8000/cricVis/`