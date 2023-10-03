#!/bin/bash
set -e

# Kill any existing servers
if [ $(sudo lsof -t -i:9090) ]; then
    sudo kill -9 $(sudo lsof -t -i:9090)
fi

if [ $(sudo lsof -t -i:8080) ]; then
    sudo kill -9 $(sudo lsof -t -i:8080)
fi

# Set environment variables
export USE_ROCKY_8=1
export LOG_FILE_LOCATION=app.log

# Activate the virtual environment
source env/bin/activate

# Start the main server in the background
(gunicorn -c guni.py --bind 0.0.0.0:8080 app:app &)

# Start the mock server in the background
(gunicorn -c guni.py --bind 0.0.0.0:9090 mock_server:app &)

# Allow some time for the servers to start (you can adjust this as needed)
sleep 3

# Deactivate the virtual environment
deactivate

# Tail the log file to see the output
tail -f "$(pwd)/app.log"
