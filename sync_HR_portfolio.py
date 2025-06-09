# sync_HR_portfolio.py - This script downloads Python/PyPy3 solutions from HackerRank.
# It uses config.py for login and API interaction.

import os
import json
import time
import requests
import re 
from dotenv import load_dotenv
from config import login_hackerrank # Import the login function

# --- Configuration ---
load_dotenv()
HR_USERNAME = os.getenv("HR_USERNAME")
HR_PASSWORD = os.getenv("HR_PASSWORD")
OUTPUT_BASE_DIR = "submissions" # This is where the raw data (code + metadata.json) will go

# --- NEW: Consolidated folder name ---
CONSOLIDATED_LANG_FOLDER = "python3_pypy3" 
# Filter languages to download (still used by fetch_all_submissions_metadata)
LANGUAGES_TO_DOWNLOAD = ["python3", "pypy3"] 

# Base URL for fetching submission content
# This URL structure is specific to HackerRank's submission API
SUBMISSION_CONTENT_URL_TEMPLATE = "https://www.hackerrank.com/rest/submissions/{submission_id}/code"
SUBMISSIONS_METADATA_URL = "https://www.hackerrank.com/rest/contests/master/submissions"

# Ensure the main output directory exists
os.makedirs(OUTPUT_BASE_DIR, exist_ok=True)

# --- Helper function to sanitize names for file/folder paths ---
def sanitize_filename(name):
    """Sanitizes a string to be suitable for use in filenames/paths."""
    if not isinstance(name, str):
        name = str(name)
    s = re.sub(r'[<>:"/\\|?*]', '', name) # Remove invalid characters
    s = s.replace(' ', '-')              # Replace spaces with hyphens
    s = re.sub(r'-+', '-', s)            # Replace multiple hyphens with single
    s = s.strip('-')                     # Remove leading/trailing hyphens
    if not s: # Fallback for empty or invalid names
        return "untitled"
    return s.lower() # Consistent lowercase for problem slugs/folder names

# --- Modified Directory Creation (to create submissions/python3_pypy3/submission_id/) ---
def create_submission_directory_structure(base_dir, consolidated_lang_folder_name, submission_id):
    """
    Creates the necessary directory structure for saving code and metadata:
    base_dir/consolidated_lang_folder_name/submission_id/
    """
    path = os.path.join(base_dir, consolidated_lang_folder_name, str(submission_id))
    os.makedirs(path, exist_ok=True)
    return path

def fetch_all_submissions_metadata(session, language_filters=None):
    """
    Fetches all submission metadata by leveraging the 'total' count for pagination,
    as 'has_next' is not provided by the API.
    """
    print("Fetching all submission metadata...")
    all_submissions = []
    total_expected_submissions = -1 
    page = 1

    while True:
        params = {"offset": (page - 1) * 10, "limit": 10}

        try:
            response = session.get(SUBMISSIONS_METADATA_URL, params=params, timeout=30)
            response.raise_for_status() 
            
            data = response.json()
            
            submissions_on_page = data.get('models', [])
            current_page_total_count = data.get('total', 0)

            if total_expected_submissions == -1:
                total_expected_submissions = current_page_total_count
                print(f"API reported total submissions available: {total_expected_submissions}")

            if not submissions_on_page:
                if len(all_submissions) < total_expected_submissions:
                    print(f"Warning: Fetched page {page} but received no new submissions, and haven't reached total expected ({total_expected_submissions}). Breaking pagination loop prematurely.")
                break 

            all_submissions.extend(submissions_on_page)
            
            if len(all_submissions) >= total_expected_submissions:
                print(f"All {total_expected_submissions} submissions fetched according to API total. Breaking pagination loop.")
                break

            page += 1
            time.sleep(1)

        except requests.exceptions.RequestException as e:
            print(f"HTTP Error fetching metadata: {response.status_code if 'response' in locals() else 'N/A'} - {response.text if 'response' in locals() else e}")
            print(f"Failed to fetch submissions metadata for page {page}. Stopping pagination due to error.")
            break
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error fetching metadata: {e}. Response was: {response.text}")
            print(f"Failed to decode JSON for page {page}. Stopping pagination due to error.")
            break

    if language_filters:
        initial_total_fetched = len(all_submissions)
        filtered_submissions = [
            sub for sub in all_submissions 
            if sub.get('language') in language_filters
        ]
        print(f"Found {len(filtered_submissions)} {', '.join(language_filters)} submissions after filtering from {initial_total_fetched} total fetched.")
        return filtered_submissions
    
    return all_submissions

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
    metadata_files_saved = 0
    
    start_time = time.time()

    authenticated_session = login_hackerrank(HR_USERNAME, HR_PASSWORD)

    if authenticated_session:
        print("Fetching and processing submissions...")
        
        all_submissions_metadata = fetch_all_submissions_metadata(authenticated_session, LANGUAGES_TO_DOWNLOAD)
        
        try:
            first_page_response = authenticated_session.get(SUBMISSIONS_METADATA_URL, params={"offset": 0, "limit": 10}, timeout=10)
            first_page_response.raise_for_status()
            first_page_data = first_page_response.json()
            total_submissions_api = first_page_data.get('total', 0)
        except Exception as e:
            print(f"Could not retrieve total submissions from API for summary: {e}")
            total_submissions_api = len(all_submissions_metadata) 

        python_pypy_submissions_found = len(all_submissions_metadata)

        print(f"Starting download of code files and saving metadata into '{CONSOLIDATED_LANG_FOLDER}' folder...")
        for submission in all_submissions_metadata:
            submission_id = submission.get('id')
            language = submission.get('language') # e.g., 'python3', 'pypy3'
            status = submission.get('status', 'Unknown')
            challenge_info = submission.get('challenge', {})
            problem_name = challenge_info.get('name')
            problem_slug = challenge_info.get('slug') 
            
            score = submission.get('score', 'N/A')
            submitted_at = submission.get('submitted_at', 'N/A') 

            if submission_id and language and problem_name and problem_slug and language in LANGUAGES_TO_DOWNLOAD:
                # --- Get Code Content ---
                code_content_url = SUBMISSION_CONTENT_URL_TEMPLATE.format(submission_id=submission_id)
                code_content = None
                try:
                    code_response = authenticated_session.get(code_content_url, timeout=30)
                    code_response.raise_for_status()
                    code_content = code_response.text
                except requests.exceptions.RequestException as e:
                    print(f"HTTP Error downloading code for submission {submission_id}: {e}")
                    download_errors += 1
                    continue
                except Exception as e:
                    print(f"An unexpected error occurred getting code for submission {submission_id}: {e}")
                    download_errors += 1
                    continue

                if not code_content:
                    print(f"No code content found for submission {submission_id}, skipping.")
                    download_errors += 1
                    continue

                # --- Modified: Create specific directory for this submission under the consolidated folder ---
                # This creates: submissions/python3_pypy3/submission_id/
                submission_save_path = create_submission_directory_structure(
                    OUTPUT_BASE_DIR, 
                    CONSOLIDATED_LANG_FOLDER, # Use the new consolidated folder name
                    submission_id
                )
                
                # Define filename for the code (e.g., problem-slug_submission_id_status.py)
                sanitized_problem_slug = sanitize_filename(problem_slug)
                # Use problem_slug directly for filename consistency, combined with submission_id and status
                code_filename = f"{sanitized_problem_slug}_{submission_id}_{sanitize_filename(status)}.py"
                code_file_path = os.path.join(submission_save_path, code_filename)
                
                # --- Save the code file ---
                if not os.path.exists(code_file_path): 
                    with open(code_file_path, "w", encoding="utf-8") as f:
                        f.write(code_content)
                    print(f"Saved code to: {code_file_path}")
                    files_downloaded += 1
                else:
                    print(f"Code already exists, skipping: {code_file_path}")

                # --- Prepare and save the metadata JSON file ---
                metadata_content = {
                    "problem_title": problem_name,
                    "problem_slug": problem_slug, 
                    "submission_id": submission_id,
                    "submission_status": status,
                    "score": score,
                    "submission_timestamp": submitted_at, 
                    "language": language, # Keep original 'python3' or 'pypy3' in metadata
                    "code_filename": code_filename,
                    "problem_url": f"https://www.hackerrank.com/challenges/{problem_slug}/problem"
                }

                metadata_file_path = os.path.join(submission_save_path, "metadata.json")
                
                with open(metadata_file_path, "w", encoding="utf-8") as f:
                    json.dump(metadata_content, f, indent=4)
                print(f"Saved metadata to: {metadata_file_path}")
                metadata_files_saved += 1
                
                time.sleep(0.5) 

            else:
                print(f"Skipping submission due to missing info or unexpected language: ID={submission_id}, Lang={language}, Problem={problem_name}")
                download_errors += 1
        
        print(f"Code file download and metadata saving process completed. Downloaded {files_downloaded} files, saved {metadata_files_saved} metadata files with {download_errors} errors.")
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
        f.write(f"Code Files Successfully Downloaded: {files_downloaded}\n")
        f.write(f"Metadata Files Successfully Saved: {metadata_files_saved}\n")
        f.write(f"Download/Processing Errors: {download_errors}\n")
        f.write(f"Output Directory: {os.path.abspath(OUTPUT_BASE_DIR)}\n")
        f.write(f"--------------------------------------------------\n")
    print(f"\nRun summary saved to: {summary_filename}")


if __name__ == "__main__":
    main()