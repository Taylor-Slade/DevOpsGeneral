#!/bin/bash

# Run database migrations
flask db upgrade

# Start the Flask application
exec flask run --host=0.0.0.0

#test