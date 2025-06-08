# sync_HR_portfolio.py - This script downloads Python/PyPy3 solutions from HackerRank.
# It uses config.py for login and API interaction.

import os
import json
import time
import requests
from dotenv import load_dotenv
from config import login_hackerrank # Import the login function

# --- Configuration ---
load_dotenv()
HR_USERNAME = os.getenv("HR_USERNAME")
HR_PASSWORD = os.getenv("HR_PASSWORD")
OUTPUT_BASE_DIR = "submissions"
LANGUAGES_TO_DOWNLOAD = ["python3", "pypy3"] # Specify the languages you want to download

# Base URL for fetching submission content
# This URL structure is specific to HackerRank's submission API
SUBMISSION_CONTENT_URL_TEMPLATE = "https://www.hackerrank.com/rest/submissions/{submission_id}/code"
SUBMISSIONS_METADATA_URL = "https://www.hackerrank.com/rest/contests/master/submissions"

def create_directory_structure(base_dir, lang_dir, problem_slug):
    """Creates the necessary directory structure for saving code."""
    path = os.path.join(base_dir, lang_dir, problem_slug)
    os.makedirs(path, exist_ok=True)
    return path

def fetch_all_submissions_metadata(session, language_filters=None):
    """
    Fetches all submission metadata by leveraging the 'total' count for pagination,
    as 'has_next' is not provided by the API.
    """
    print("Fetching all submission metadata...")
    all_submissions = []
    total_expected_submissions = -1 # Initialize, will be set from the first response
    page = 1

    while True: # Loop indefinitely, will break when all submissions are fetched
        params = {"offset": (page - 1) * 10, "limit": 10} # Fetch 10 submissions per page

        try:
            response = session.get(SUBMISSIONS_METADATA_URL, params=params, timeout=30)
            response.raise_for_status() # Raise an exception for bad status codes
            
            data = response.json()
            
            # --- DEBUG: Raw Metadata for Page X - REMOVED FOR CLEAN OUTPUT ---
            # print(f"\n--- DEBUG: Raw Metadata for Page {page} ---")
            # print(json.dumps(data, indent=2))
            # print("-------------------------------------------\n")

            submissions_on_page = data.get('models', [])
            current_page_total_count = data.get('total', 0)

            # Set total_expected_submissions on the very first page fetch
            if total_expected_submissions == -1:
                total_expected_submissions = current_page_total_count
                print(f"API reported total submissions available: {total_expected_submissions}")


            if not submissions_on_page:
                # If no submissions were returned on this page and we haven't reached the expected total,
                # it suggests an issue or end of submissions.
                if len(all_submissions) < total_expected_submissions:
                    print(f"Warning: Fetched page {page} but received no new submissions, and haven't reached total expected ({total_expected_submissions}). Breaking pagination loop prematurely.")
                break # No more submissions from this point, break the loop

            all_submissions.extend(submissions_on_page)
            
            # Per-page info (optional, can be removed if not needed)
            # print(f"Fetched page {page} with {len(submissions_on_page)} submissions. Total fetched so far: {len(all_submissions)}")
            
            # Check if we have fetched all expected submissions
            # This is the most reliable way to determine when to stop given the 'total' field.
            if len(all_submissions) >= total_expected_submissions:
                print(f"All {total_expected_submissions} submissions fetched according to API total. Breaking pagination loop.")
                break

            page += 1
            time.sleep(1) # Be polite and avoid hitting rate limits

        except requests.exceptions.RequestException as e:
            print(f"HTTP Error fetching metadata: {response.status_code if 'response' in locals() else 'N/A'} - {response.text if 'response' in locals() else e}")
            print(f"Failed to fetch submissions metadata for page {page}. Stopping pagination due to error.")
            break
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error fetching metadata: {e}. Response was: {response.text}")
            print(f"Failed to decode JSON for page {page}. Stopping pagination due to error.")
            break

    # Filter by language after fetching all available submissions
    if language_filters:
        initial_total_fetched = len(all_submissions)
        filtered_submissions = [
            sub for sub in all_submissions 
            if sub.get('language') in language_filters
        ]
        print(f"Found {len(filtered_submissions)} {', '.join(language_filters)} submissions after filtering from {initial_total_fetched} total fetched.")
        return filtered_submissions
    
    return all_submissions

def download_code_file(session, submission_id, language_dir, problem_slug, problem_name, status):
    """Downloads a single code file and saves it."""
    url = SUBMISSION_CONTENT_URL_TEMPLATE.format(submission_id=submission_id)
    
    try:
        response = session.get(url, timeout=30)
        response.raise_for_status()
        
        code_content = response.text

        if code_content:
            # Clean problem_name for filename (remove invalid characters)
            cleaned_problem_name = "".join([c for c in problem_name if c.isalnum() or c in (' ', '-', '_')]).strip()
            cleaned_problem_name = cleaned_problem_name.replace(' ', '_')
            if not cleaned_problem_name: # Fallback if cleaning results in empty string
                cleaned_problem_name = f"submission_{submission_id}"

            # Create path
            save_dir = create_directory_structure(OUTPUT_BASE_DIR, language_dir, cleaned_problem_name)
            
            # Use submission ID and status in filename to avoid overwrites and provide context
            filename = os.path.join(save_dir, f"{cleaned_problem_name}_{submission_id}_{status}.{language_dir.replace('python3', 'py').replace('pypy3', 'py')}")
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(code_content)
            # print(f"Downloaded: {filename}") # Keep this print for confirmation of individual downloads
            return True # Indicate successful download
        else:
            print(f"No code content found for submission {submission_id}.")
            return False
    except requests.exceptions.RequestException as e:
        print(f"HTTP Error downloading {submission_id}: {e}")
        # print(f"Response status code: {response.status_code if 'response' in locals() else 'N/A'}") # Optional debug
        # print(f"Response content (on error): {response.text if 'response' in locals() else 'N/A'}") # Optional debug
        return False
    except Exception as e:
        print(f"An unexpected error occurred downloading submission {submission_id}: {e}")
        return False

def main():
    if not HR_USERNAME or not HR_PASSWORD:
        print("Error: HR_USERNAME or HR_PASSWORD environment variables are not set.")
        print("Please set them in your .env file or environment.")
        return

    # --- Run summary variables ---
    total_submissions_api = 0
    python_pypy_submissions_found = 0
    files_downloaded = 0
    download_errors = 0
    
    start_time = time.time()

    authenticated_session = login_hackerrank(HR_USERNAME, HR_PASSWORD)

    if authenticated_session:
        print("Fetching and processing submissions...")
        
        # Fetch all submissions metadata (this function already returns filtered submissions)
        all_submissions_metadata = fetch_all_submissions_metadata(authenticated_session, LANGUAGES_TO_DOWNLOAD)
        
        # Capture total submissions from API from the first page's response for summary
        # This is for reporting purposes only, the pagination loop in fetch_all_submissions_metadata
        # already handles the total count internally.
        try:
            first_page_response = authenticated_session.get(SUBMISSIONS_METADATA_URL, params={"offset": 0, "limit": 10}, timeout=10)
            first_page_response.raise_for_status()
            first_page_data = first_page_response.json()
            total_submissions_api = first_page_data.get('total', 0)
        except Exception as e:
            print(f"Could not retrieve total submissions from API for summary: {e}")
            total_submissions_api = len(all_submissions_metadata) # Fallback to count of fetched filtered data


        # Save raw metadata for the filtered submissions to JSON for inspection
        metadata_output_dir = os.path.join(OUTPUT_BASE_DIR, "_".join(LANGUAGES_TO_DOWNLOAD))
        os.makedirs(metadata_output_dir, exist_ok=True)
        metadata_filepath = os.path.join(metadata_output_dir, "all_submissions_metadata.json")
        with open(metadata_filepath, 'w', encoding='utf-8') as f:
            json.dump(all_submissions_metadata, f, indent=4)
        print(f"Metadata for {len(all_submissions_metadata)} filtered submissions saved to {metadata_filepath}")
        
        # Update count for summary
        python_pypy_submissions_found = len(all_submissions_metadata)


        print("Starting download of Python/PyPy3 code files...")
        for submission in all_submissions_metadata:
            submission_id = submission.get('id')
            language = submission.get('language')
            status = submission.get('status', 'Unknown')
            
            challenge_info = submission.get('challenge', {})
            problem_name = challenge_info.get('name')
            problem_slug = challenge_info.get('slug')

            # This check is technically redundant here because all_submissions_metadata
            # already contains only filtered languages, but harmless.
            if submission_id and language and problem_name and problem_slug and language in LANGUAGES_TO_DOWNLOAD:
                language_dir = language
                # Removed detailed download attempt print, keeping just the confirmation below
                # print(f"Attempting to download submission {submission_id} (Problem: {problem_name}, Lang: {language})...")
                if download_code_file(authenticated_session, submission_id, language_dir, problem_slug, problem_name, status):
                    files_downloaded += 1
                    print(f"Downloaded {language_dir}\\{problem_name}\\{problem_name}_{submission_id}_{status}.{language_dir.replace('python3', 'py').replace('pypy3', 'py')}")
                else:
                    download_errors += 1
                time.sleep(0.5)
            # The 'else' block for skipping irrelevant submissions is removed as the list is already filtered
            # else:
            #     print(f"Skipping submission {submission_id} (Problem: {problem_name}, Language: {language}) - internal filter issue or missing info.")
        
        print(f"Code file download process completed. Downloaded {files_downloaded} files with {download_errors} errors.")
    else:
        print("Login failed. Cannot proceed with fetching submissions.")

    end_time = time.time()
    duration = end_time - start_time

    # --- Generate Summary ---
    summary_filename = os.path.join(OUTPUT_BASE_DIR, f"run_summary_{time.strftime('%Y%m%d-%H%M%S')}.txt")
    with open(summary_filename, 'w', encoding='utf-8') as f:
        f.write(f"--- HackerRank Submission Downloader Summary ---\n")
        f.write(f"Run Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Duration: {duration:.2f} seconds\n")
        f.write(f"--------------------------------------------------\n")
        f.write(f"API Reported Total Submissions (all languages): {total_submissions_api}\n")
        f.write(f"Python/PyPy3 Submissions Found (after filtering): {python_pypy_submissions_found}\n")
        f.write(f"Files Successfully Downloaded: {files_downloaded}\n")
        f.write(f"Download Errors/Skipped (Python/PyPy3): {download_errors}\n")
        f.write(f"Output Directory: {os.path.abspath(OUTPUT_BASE_DIR)}\n")
        f.write(f"Metadata File for Filtered Submissions: {os.path.abspath(metadata_filepath)}\n")
        f.write(f"--------------------------------------------------\n")
    print(f"\nRun summary saved to: {summary_filename}")


if __name__ == "__main__":
    main()