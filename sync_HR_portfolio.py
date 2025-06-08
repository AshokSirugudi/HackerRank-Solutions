import requests
import json
import time
import os

# --- Placeholder for your existing login_hackerrank function ---
# You should have a function here (e.g., in config.py or imported)
# that performs the login and returns an authenticated requests.Session object.
# Example:
# from config import login_hackerrank # Assuming login_hackerrank is in config.py

# This is a dummy/mock session for demonstration and testing purposes.
# YOU MUST REPLACE 'session = MockSession()' with your actual authenticated session
# obtained from your login function when running against HackerRank.
class MockResponse:
    def __init__(self, content, status_code=200):
        self._content = json.dumps(content).encode('utf-8')
        self.status_code = status_code

    def json(self):
        return json.loads(self._content.decode('utf-8'))

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.exceptions.HTTPError(f"HTTP error: {self.status_code}")

class MockSession:
    def get(self, url):
        # Simulate pagination with a sample set of submissions
        offset_param = int(url.split('offset=')[1].split('&')[0])
        limit_param = int(url.split('limit=')[1])

        all_mock_submissions = [
            {"id": 432406583, "challenge_id": 56964, "contest_id": 1, "hacker_id": 28608756, "status": "Accepted", "kind": "code", "created_at": 1746927842, "language": "c", "hacker_username": None, "time_ago": "28 days", "in_contest_bounds": True, "status_code": 2, "score": "5.0", "is_preliminary_score": None, "challenge": {"name": "Sum and Difference of Two Numbers", "slug": "sum-numbers-c"}, "inserttime": 1746927842},
            {"id": 432406262, "challenge_id": 57386, "contest_id": 1, "hacker_id": 28608756, "status": "Accepted", "kind": "code", "created_at": 1746927177, "language": "c", "hacker_username": None, "time_ago": "28 days", "in_contest_bounds": True, "status_code": 2, "score": "5.0", "is_preliminary_score": None, "challenge": {"name": "Playing With Characters", "slug": "playing-with-characters"}, "inserttime": 1746927177},
            {"id": 426780351, "challenge_id": 672, "contest_id": 1, "hacker_id": 28608756, "status": "Accepted", "kind": "code", "created_at": 1742623741, "language": "python3", "hacker_username": None, "time_ago": "3 months", "in_contest_bounds": True, "status_code": 2, "score": "30.0", "is_preliminary_score": None, "challenge": {"name": "Smart IDE: Language Detection", "slug": "programming-language-detection"}, "inserttime": 1742623741},
            {"id": 426780162, "challenge_id": 670, "contest_id": 1, "hacker_id": 28608756, "status": "Accepted", "kind": "code", "created_at": 1742623647, "language": "python3", "hacker_username": None, "time_ago": "3 months", "in_contest_bounds": True, "status_code": 1, "score": "20.0", "is_preliminary_score": None, "challenge": {"name": "Smart IDE: Identifying comments", "slug": "ide-identifying-comments"}, "inserttime": 1742623647},
            {"id": 426779952, "challenge_id": 670, "contest_id": 1, "hacker_id": 28608756, "status": "Accepted", "kind": "code", "created_at": 1742623540, "language": "pypy3", "hacker_username": None, "time_ago": "3 months", "in_contest_bounds": True, "status_code": 2, "score": "20.0", "is_preliminary_score": None, "challenge": {"name": "Smart IDE: Identifying comments (PyPy)", "slug": "ide-identifying-comments-pypy"}, "inserttime": 1742623540},
            {"id": 426776804, "challenge_id": 895, "contest_id": 1, "hacker_id": 28608756, "status": "Accepted", "kind": "code", "created_at": 1742621682, "language": "python3", "hacker_username": None, "time_ago": "3 months", "in_contest_bounds": True, "status_code": 2, "score": "15.0", "is_preliminary_score": None, "challenge": {"name": "Detect Email Addresses", "slug": "detect-the-email-addresses"}, "inserttime": 1742621682},
            {"id": 426776672, "challenge_id": 733, "contest_id": 1, "hacker_id": 28608756, "status": "Accepted", "kind": "code", "created_at": 1742621586, "language": "pypy3", "hacker_username": None, "time_ago": "3 months", "in_contest_bounds": True, "status_code": 2, "score": "15.0", "is_preliminary_score": None, "challenge": {"name": "Find a Word (PyPy)", "slug": "find-a-word-pypy"}, "inserttime": 1742621587},
        ]
        
        total_mock_submissions = 78

        start_index = offset_param
        end_index = offset_param + limit_param
        
        paginated_models = all_mock_submissions[start_index:min(end_index, len(all_mock_submissions))]
        
        mock_response_content = {
            "models": paginated_models,
            "total": total_mock_submissions
        }
        
        return MockResponse(mock_response_content)

    def get_submission_code(self, submission_id):
        # Simulate fetching code content for a given submission ID
        # In a real scenario, this would be an API call like:
        # self.get(f"https://www.hackerrank.com/rest/contests/master/submissions/{submission_id}/code")
        
        mock_code_content = {
            426780351: "# Sample Python 3 code for Language Detection\nprint('Hello World - Python')",
            426780162: "# Sample Python 3 code for Identifying comments\ndef main():\n    # This is a comment\n    print('Code with comments')",
            426779952: "# Sample PyPy 3 code for Identifying comments (PyPy)\n# Another comment\nprint('PyPy code')",
            426776804: "# Sample Python 3 code for Detect Email Addresses\nimport re\nemail_regex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}'",
            426776672: "# Sample PyPy 3 code for Find a Word (PyPy)\n# Simple search algorithm\nword = 'example'",
            # Add more mock code for other submission IDs if needed for testing
        }.get(submission_id, f"# No mock code available for submission ID: {submission_id}")
        
        return MockResponse({"code": mock_code_content})


def fetch_all_target_language_submissions_metadata(session, limit_per_page=50):
    """
    Fetches metadata for all Python 3 and PyPy 3 submissions from HackerRank, handling pagination.
    
    Args:
        session (requests.Session): An authenticated requests session object.
        limit_per_page (int): The number of submissions to fetch per API call.
        
    Returns:
        list: A list of dictionaries, where each dictionary is the metadata for a submission.
    """
    all_target_language_submissions = []
    total_submissions = -1 
    offset = 0
    
    # Define the languages of interest based on your requirement
    languages_of_interest = ["python3", "pypy3"] 

    print("Starting to fetch all HackerRank submissions metadata...")

    while total_submissions == -1 or offset < total_submissions:
        submissions_url = f"https://www.hackerrank.com/rest/contests/master/submissions?offset={offset}&limit={limit_per_page}"
        
        print(f"Fetching page: offset={offset}, limit={limit_per_page}")
        
        try:
            response = session.get(submissions_url)
            response.raise_for_status()
            
            data = response.json()
            
            if "models" not in data or not isinstance(data["models"], list):
                print("Error: 'models' key not found or not a list in response.")
                break 

            if total_submissions == -1:
                total_submissions = data.get("total", 0)
                print(f"Discovered total submissions: {total_submissions}")
                if total_submissions == 0:
                    print("No submissions found. Exiting.")
                    break

            # Filter for the target languages and add to our list
            for submission in data["models"]:
                if submission.get("language") in languages_of_interest:
                    all_target_language_submissions.append(submission)
            
            # Move to the next page
            offset += limit_per_page
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching submissions page at offset {offset}: {e}")
            break 
        except json.JSONDecodeError:
            print(f"Error decoding JSON response at offset {offset}. Response: {response.text[:200]}...")
            break
        
    print(f"\nFinished fetching. Total Python3/PyPy3 submissions found: {len(all_target_language_submissions)}")
    return all_target_language_submissions

# --- Main execution block ---
if __name__ == "__main__":
    # --- IMPORTANT: Replace the MockSession with your actual login logic ---
    # Example:
    # from your_login_module import login_hackerrank # if login is in another file
    # authenticated_session = login_hackerrank(username, password) # Pass your actual credentials securely

    # For now, using the MockSession for testing the metadata fetching logic
    # Make sure to replace this with your actual authenticated session object
    authenticated_session = MockSession() 

    if authenticated_session:
        all_submissions_metadata = fetch_all_target_language_submissions_metadata(authenticated_session)
        
        if all_submissions_metadata:
            print("\n--- First 5 Python3/PyPy3 Submissions Metadata Sample (from fetched data) ---")
            for i, submission in enumerate(all_submissions_metadata[:5]):
                print(f"Submission {i+1}:")
                print(f"  ID: {submission.get('id')}")
                print(f"  Problem: {submission.get('challenge', {}).get('name')} ({submission.get('challenge', {}).get('slug')})")
                print(f"  Language: {submission.get('language')}")
                print(f"  Status: {submission.get('status')}")
                print("-" * 30)
            
            # --- LOCAL STORAGE: Saving Metadata (Commit 2) ---
            current_script_dir = os.path.dirname(os.path.abspath(__file__))
            base_submissions_dir = os.path.join(current_script_dir, "submissions", "python_pypy3")
            
            os.makedirs(base_submissions_dir, exist_ok=True)
            print(f"\nSubmissions directory ensured: {base_submissions_dir}")

            metadata_file_path = os.path.join(base_submissions_dir, "all_submissions_metadata.json")
            
            try:
                with open(metadata_file_path, 'w', encoding='utf-8') as f:
                    json.dump(all_submissions_metadata, f, indent=4)
                print(f"All Python3/PyPy3 submission metadata saved to: {metadata_file_path}")
            except IOError as e:
                print(f"Error saving metadata to file: {e}")

            # --- Start of New Code for Commit 3: Downloading Actual Code Files ---

            # Load the metadata to process.
            # This step ensures robustness if this part of the script were run independently
            # or if the 'all_submissions_metadata' variable was not directly available.
            processed_metadata = []
            try:
                with open(metadata_file_path, 'r', encoding='utf-8') as f:
                    processed_metadata = json.load(f)
                print(f"Successfully loaded {len(processed_metadata)} submissions from metadata file.")
            except FileNotFoundError:
                print(f"Error: Metadata file not found at {metadata_file_path}. Cannot proceed with code download.")
                processed_metadata = []
            except json.JSONDecodeError:
                print(f"Error: Could not decode JSON from {metadata_file_path}. File might be corrupted.")
                processed_metadata = []

            if not processed_metadata:
                print("No submissions metadata found or loaded to process for code download.")
            else:
                print("\nInitiating download of individual code files...")
                # Iterate through each submission's metadata to download its code
                for submission in processed_metadata:
                    submission_id = submission.get('id')
                    challenge_slug = submission.get('challenge', {}).get('slug')
                    language = submission.get('language')
                    
                    if not submission_id or not challenge_slug or not language:
                        print(f"Skipping malformed metadata entry: {submission}")
                        continue
                    
                    # Determine the file extension based on the submission language
                    file_extension = ".py" 
                    
                    # Construct the problem-specific directory path
                    problem_dir = os.path.join(base_submissions_dir, challenge_slug)
                    
                    # Create the problem-specific directory if it doesn't exist
                    os.makedirs(problem_dir, exist_ok=True)
                    
                    # Define the full path for the code file
                    code_file_path = os.path.join(problem_dir, f"{submission_id}{file_extension}")
                    
                    # Fetch the actual code content for the submission
                    print(f"  Downloading code for {challenge_slug} (ID: {submission_id})...")
                    try:
                        # In a real scenario, this would be:
                        # code_url = f"https://www.hackerrank.com/rest/contests/master/submissions/{submission_id}/code"
                        # code_response = authenticated_session.get(code_url)
                        # code_response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
                        # submission_code = code_response.json().get('code', '')

                        # Using MockSession's get_submission_code for demonstration
                        code_response = authenticated_session.get_submission_code(submission_id)
                        submission_code = code_response.json().get('code', '')

                        if submission_code:
                            with open(code_file_path, 'w', encoding='utf-8') as code_file:
                                code_file.write(submission_code)
                            print(f"    Saved code to {code_file_path}")
                        else:
                            print(f"    No code found for submission ID: {submission_id}")
                    except requests.exceptions.RequestException as e:
                        print(f"  Error fetching code for submission ID {submission_id}: {e}")
                    except json.JSONDecodeError:
                        print(f"  Error decoding JSON response for submission ID {submission_id}.")
                    except IOError as e:
                        print(f"  Error saving code file for submission ID {submission_id}: {e}")
                    time.sleep(1) # Be respectful: Add a small delay between requests

            print("\nFinished downloading all available code files.")
            # --- End of New Code for Commit 3: Downloading Actual Code Files ---

        else:
            print("No Python3/PyPy3 submissions metadata fetched.")
    else:
        print("Authentication failed. Cannot proceed with code download.")