# Ride Share APP

## Overview of Implementation

- Driver, User Registration
- Ride Share System
- Ride Status 
- Driver Comfirmation, Completion
- With CSS Style 

## How to run it

After activating your google api service and adding `credentials.json`, You can run it in both ways:

1. Set up postgresql according to `settings.py`:

```Bash
cd web-app
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
```

2. Set up docker and run it directly. Don't forget to change `CSRF_TRUSTED_ORIGINS` in `settings.py`: 

```Bash
sudo docker-compose up
```
