#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <user_data.csv>"
    exit 1
fi

FILE="$1"

if [ ! -f "$FILE" ]; then
    echo "Error: File '$FILE' does not exist."
    exit 1
fi

DEFAULT_PASSWORD="zaq1@WSX"

echo "Processing user removal from $FILE"

tail -n +2 "$FILE" | tr -d '\r' | while IFS=, read -r f1 f2 f3 f4 f5 f6 f7 f8 f9 f10 f11 f12 rest; do

    LOGIN="$f12"

    if [ -z $"LOGIN" ]; then
        continue
    fi

    if id "$LOGIN" &>/dev/null; then
        userdel -r "LOGIN" 2>/dev/null
    fi

done
echo "Processing complete"
