#!/bin/bash

# Desired time to run the script (24-hour format, e.g., 12:00 for noon)
target_time="14:19"

while true; do
    current_time=$(date +%H:%M)
    
    if [ "$current_time" == "$target_time" ]; then
        python ~/storage/downloads/theater.py "مع" 7
        break
    fi
    
    sleep 30  # Wait for 30 seconds before checking again
done
