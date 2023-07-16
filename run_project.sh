#Create Virtual environment
virtualenv secenv -p python3

#Activate virtual environment
source secenv/bin/activate

#Install Dependencies
pip install -r requirements.txt

# Change to your project directory
cd security

# Run Django migrations
python manage.py migrate

# Start the Django development server
python manage.py runserver