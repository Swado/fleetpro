#!/bin/bash

# Check if nc (netcat) is available
if command -v nc > /dev/null; then
  # Get the absolute path of the landing.html file
  LANDING_FILE="$(pwd)/landing.html"
  
  # Start a simple HTTP server using netcat
  while true; do
    echo "Starting server on port 5000..."
    { echo -ne "HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\n"; cat "$LANDING_FILE"; } | nc -l -p 5000
  done
else
  echo "Error: netcat (nc) is not available. Please install it or use another method to serve the file."
  exit 1
fi