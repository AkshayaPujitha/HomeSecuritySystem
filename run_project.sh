source secenv/bin/activate

# Change to your project directory
cd security

# Run Django migrations
python manage.py migrate

# Start the Django development server
python manage.py runserver