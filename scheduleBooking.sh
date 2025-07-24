#!/bin/bash

# Step 1: Set the target time (when to run your script)
target_time="16:00:00"

# Step 2: Get today’s date in YYYY-MM-DD format
today=$(date +%F)

# Step 3: Combine today’s date with the target time
target_datetime="$today $target_time"

# Step 4: Get current time and target time as epoch (seconds since 1970)
now_epoch=$(date +%s)
target_epoch=$(date -d "$target_datetime" +%s)

# Step 5: If target time is already passed today, add 1 day (86400 seconds)
if [ "$target_epoch" -le "$now_epoch" ]; then
    target_epoch=$(( target_epoch + 86400 ))
fi

# Step 6: Calculate how many seconds to sleep until target time
sleep_seconds=$(( target_epoch - now_epoch ))

# Step 7: Inform user (optional)
echo "Sleeping for $sleep_seconds seconds until $target_time..."
termux-wake-lock

# Step 8: Wait and then execute the command
sleep "$sleep_seconds"

echo "started executing at  $(date)"

python ~/storage/downloads/theater.py "عايش,انا,اليد,حكايات" 3

termux-wake-unlock

echo " done termux-wake-unlocked at $(date)"