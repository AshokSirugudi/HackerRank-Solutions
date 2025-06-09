#!/bin/bash

echo "Starting HackerRank Portfolio Sync and Generation..."

# Ensure you are in the correct directory (optional, but good practice)
# cd "/c/Users/vinil/OneDrive/Desktop/learn/Projects/Python/HackerRank_Downloader"

echo "--- Step 1: Running sync_HR_portfolio.py (Downloading submissions) ---"
python sync_HR_portfolio.py

if [ $? -eq 0 ]; then
    echo "--- Step 1 Completed. Running generate_portfolio.py (Generating portfolio) ---"
    python generate_portfolio.py
    if [ $? -eq 0 ]; then
        echo "--- Portfolio Generation Completed Successfully ---"
    else
        echo "Error: generate_portfolio.py failed. Check its output for details."
    fi
else
    echo "Error: sync_HR_portfolio.py failed. Portfolio generation skipped."
fi

echo "Process Finished."