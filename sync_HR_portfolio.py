import requests
import json
import time # For potential rate limiting or delays if needed
import os   # For creating directories in the next commit

# --- Placeholder for your existing login_hackerrank function ---
# You should have a function here (e.g., in config.py or imported)
# that performs the login and returns an authenticated requests.Session object.
# Example:
# from config import login_hackerrank # Assuming login_hackerrank is in config.py
# If login_hackerrank is in this file, ensure it's defined above its usage.

# This is a dummy/mock session for demonstration and testing purposes.
# YOU MUST REPLACE 'session = MockSession()' with your actual authenticated session
# obtained from your login function.
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

        # This mock list should ideally reflect your actual HackerRank data structure
        # I've included a mix of languages to demonstrate filtering
        all_mock_submissions = [
            {"id": 432406583, "challenge_id": 56964, "contest_id": 1, "hacker_id": 28608756, "status": "Accepted", "kind": "code", "created_at": 1746927842, "language": "c", "hacker_username": None, "time_ago": "28 days", "in_contest_bounds": True, "status_code": 2, "score": "5.0", "is_preliminary_score": None, "challenge": {"name": "Sum and Difference of Two Numbers", "slug": "sum-numbers-c"}, "inserttime": 1746927842},
            {"id": 432406262, "challenge_id": 57386, "contest_id": 1, "hacker_id": 28608756, "status": "Accepted", "kind": "code", "created_at": 1746927177, "language": "c", "hacker_username": None, "time_ago": "28 days", "in_contest_bounds": True, "status_code": 2, "score": "5.0", "is_preliminary_score": None, "challenge": {"name": "Playing With Characters", "slug": "playing-with-characters"}, "inserttime": 1746927177},
            {"id": 426780351, "challenge_id": 672, "contest_id": 1, "hacker_id": 28608756, "status": "Accepted", "kind": "code", "created_at": 1742623741, "language": "python3", "hacker_username": None, "time_ago": "3 months", "in_contest_bounds": True, "status_code": 2, "score": "30.0", "is_preliminary_score": None, "challenge": {"name": "Smart IDE: Language Detection", "slug": "programming-language-detection"}, "inserttime": 1742623741},
            {"id": 426780162, "challenge_id": 670, "contest_id": 1, "hacker_id": 28608756, "status": "Accepted", "kind": "code", "created_at": 1742623647, "language": "python3", "hacker_username": None, "time_ago": "3 months", "in_contest_bounds": True, "status_code": 1, "score": "20.0", "is_preliminary_score": None, "challenge": {"name": "Smart IDE: Identifying comments", "slug": "ide-identifying-comments"}, "inserttime": 1742623647},
            {"id": 426779952, "challenge_id": 670, "contest_id": 1, "hacker_id": 28608756, "status": "Accepted", "kind": "code", "created_at": 1742623540, "language": "pypy3", "hacker_username": None, "time_ago": "3 months", "in_contest_bounds": True, "status_code": 2, "score": "20.0", "is_preliminary_score": None, "challenge": {"name": "Smart IDE: Identifying comments (PyPy)", "slug": "ide-identifying-comments-pypy"}, "inserttime": 1742623540}, # PyPy3 sample
            {"id": 426776804, "challenge_id": 895, "contest_id": 1, "hacker_id": 28608756, "status": "Accepted", "kind": "code", "created_at": 1742621682, "language": "python3", "hacker_username": None, "time_ago": "3 months", "in_contest_bounds": True, "status_code": 2, "score": "15.0", "is_preliminary_score": None, "challenge": {"name": "Detect Email Addresses", "slug": "detect-the-email-addresses"}, "inserttime": 1742621682},
            {"id": 426776672, "challenge_id": 733, "contest_id": 1, "hacker_id": 28608756, "status": "Accepted", "kind": "code", "created_at": 1742621586, "language": "pypy3", "hacker_username": None, "time_ago": "3 months", "in_contest_bounds": True, "status_code": 2, "score": "15.0", "is_preliminary_score": None, "challenge": {"name": "Find a Word (PyPy)", "slug": "find-a-word-pypy"}, "inserttime": 1742621587}, # PyPy3 sample
            {"id": 426776244, "challenge_id": 733, "contest_id": 1, "hacker_id": 28608756, "status": "Wrong Answer", "kind": "code", "created_at": 1742621313, "language": "python3", "hacker_username": None, "time_ago": "3 months", "in_contest_bounds": True, "status_code": 1, "score": "1.5", "is_preliminary_score": None, "challenge": {"name": "Find a Word", "slug": "find-a-word"}, "inserttime": 1742621313},
            # ... add more mock submissions here if you want to simulate more pages
            # For a total of 78, you'd have 70 more entries here if using limit=10
        ]
        
        # This part simulates the 'total' field from HackerRank's API
        total_mock_submissions = 78 # Based on your earlier provided total

        start_index = offset_param
        end_index = offset_param + limit_param
        
        # Ensure we don't go out of bounds of the mock list
        paginated_models = all_mock_submissions[start_index:min(end_index, len(all_mock_submissions))]
        
        mock_response_content = {
            "models": paginated_models,
            "total": total_mock_submissions
        }
        
        return MockResponse(mock_response_content)

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
    total_submissions = -1 # Initialize to -1 to ensure loop runs at least once
    offset = 0
    
    # Define the languages of interest based on your requirement
    languages_of_interest = ["python3", "pypy3"] 

    print("Starting to fetch all HackerRank submissions metadata...")

    while total_submissions == -1 or offset < total_submissions:
        submissions_url = f"https://www.hackerrank.com/rest/contests/master/submissions?offset={offset}&limit={limit_per_page}"
        
        print(f"Fetching page: offset={offset}, limit={limit_per_page}")
        
        try:
            response = session.get(submissions_url)
            response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
            
            data = response.json()
            
            if "models" not in data or not isinstance(data["models"], list):
                print("Error: 'models' key not found or not a list in response.")
                break # Exit loop if response structure is unexpected

            # Update total_submissions from the first page's response
            if total_submissions == -1: # Only set on the first successful page fetch
                total_submissions = data.get("total", 0)
                print(f"Discovered total submissions: {total_submissions}")
                if total_submissions == 0:
                    print("No submissions found. Exiting.")
                    break

            # Filter for the target languages and add to our list
            for submission in data["models"]:
                if submission.get("language") in languages_of_interest: # Updated filter
                    all_target_language_submissions.append(submission)
                    # print(f"  Found {submission.get('language')} submission: ID={submission.get('id')}, Problem='{submission.get('challenge', {}).get('name')}'")
            
            # Move to the next page
            offset += limit_per_page
            
            # Optional: Add a small delay to avoid hitting rate limits if making many requests
            # time.sleep(0.5) 

        except requests.exceptions.RequestException as e:
            print(f"Error fetching submissions page at offset {offset}: {e}")
            break # Exit loop on error
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
            
            # --- NEXT STEP FOR COMMIT 3: LOCAL STORAGE ---
            # Define the base directory for saving submissions
            current_script_dir = os.path.dirname(os.path.abspath(__file__))
            base_submissions_dir = os.path.join(current_script_dir, "submissions", "python_pypy3")
            
            # Create the directories if they don't exist
            os.makedirs(base_submissions_dir, exist_ok=True)
            print(f"\nSubmissions directory ensured: {base_submissions_dir}")

            # Define the path for the metadata JSON file
            metadata_file_path = os.path.join(base_submissions_dir, "all_submissions_metadata.json")
            
            # Save the metadata to the JSON file
            try:
                with open(metadata_file_path, 'w', encoding='utf-8') as f:
                    json.dump(all_submissions_metadata, f, indent=4)
                print(f"All Python3/PyPy3 submission metadata saved to: {metadata_file_path}")
            except IOError as e:
                print(f"Error saving metadata to file: {e}")

        else:
            print("No Python3/PyPy3 submissions metadata fetched.")
    else:
        print("Authentication failed. Cannot fetch submission metadata.")