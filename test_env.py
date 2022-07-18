import os

# Set environment variables
os.environ['min_val'] = 'minimum_value'
os.environ['max_val'] = 'maximum_value'

# Get environment variables
MINIMUM = os.getenv('min_val')
MAXIMUM = os.environ.get('max_val')

print(os.environ)