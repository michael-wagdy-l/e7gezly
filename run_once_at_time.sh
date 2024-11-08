#!/bin/bash

# Desired time to run the script (24-hour format, e.g., 12:00:10 for noon)
target_time="12:00:10"

while true; do
    current_time=$(date +%H:%M:%S)
    
    # Compare current time with target time
    if [[ "$current_time" > "$target_time" ]] || [[ "$current_time" == "$target_time" ]]; then
        python ~/storage/downloads/theater.py "مع" 7
        break
    fi
    
    sleep 30  # Wait for 30 seconds before checking again
done
