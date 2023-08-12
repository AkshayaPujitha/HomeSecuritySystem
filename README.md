
# Home Security System

Home security systems provide families with security by alerting them by SMS in the event of an intruder or other suspicious occurrence. They are implemented using software, but in order to operate in real time, they must be connected to sensors.

## Features

- OTP verification for verified numbers using Twilio
- Token Authentication for Secure Acess
- Real-time analysis graph for dynamic data visualization
- Event Notifications through SMS
- User Activity Log
- Face Recognition Model

## Run Using Shell Script

```bash
  chmod +x run_project.sh
```

Execute the script by running:
```bash
  ./run_project.sh
```

## User Authentication API Endpoints

### Register a User
- Method: POST
- URL: `/register/`
- Headers: Content-Type: application/json

```json
{
  "phone_number":123456789,
  "password": "secretpassword"
}

```

### Login a User

- Method: POST
- URL: `/login/`
- Headers: Content-Type: application/json

```json
{
  "phone_number":123456789,
  "password": "secretpassword"
}

```
### Verify OTP

- Method: POST
- URL: `/verify_otp/`
- Headers: Content-Type: application/json

```json
{
  "otp_code":1234
  
}
```




