
# Home Security System

Home security systems provide families with security by alerting them by SMS in the event of an intruder or other suspicious occurrence. They are implemented using software, but in order to operate in real time, they must be connected to sensors.

## Features

- OTP verification for verified numbers using Twilio
- Token Authentication for Secure Acess
- Real-time analysis graph for dynamic data visualization
- Event Notifications through SMS
- User Activity Log
- Face Recognition Model



## Run Locally

Clone the project

```bash
  git clone https://github.com/AkshayaPujitha/HomeSecuritySystem.git
```

Create Virtual Environment

```bash
  virtualenv demoenv -p python3
```

Activate Environment

```bash
  source demoenv/bin/activate
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Go to the project directory

```bash
  cd security
```

Make migrations

```bash
  python manage.py migrate
```

Start the server

```bash
  python manage.py runserver
```
## Run Using Shell Script
You can use shell script instead doing above steps

```bash
  chmod +x run_project.sh
```

Execute the script by running:
```bash
  ./run_project.sh
```

# User Authentication API Endpoints

## Register a User
- Method: POST
- URL: `/register/`
- Headers: Content-Type: application/json

```json
{
  "phone_number":123456789,
  "password": "secretpassword"
}

```

## Login a User

- Method: POST
- URL: `/login/`
- Headers: Content-Type: application/json

```json
{
  "phone_number":123456789,
  "password": "secretpassword"
}
```




