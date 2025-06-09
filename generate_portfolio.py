import os
import json
import re
from datetime import datetime

# --- Global Configuration (for Portfolio Generation) ---
# Input directory where downloaded submissions are stored
PORTFOLIO_SUBMISSIONS_INPUT_DIR = os.path.join("submissions", "python3_pypy3")

# Output directory for the generated Markdown portfolio
PORTFOLIO_OUTPUT_DIR = os.path.join("HackerRank-Solutions", "Python")

# --- Helper function to sanitize names for file/folder paths ---
def sanitize_filename(name):
    """Sanitizes a string to be suitable for use in filenames/paths."""
    if not isinstance(name, str):
        name = str(name)
    s = re.sub(r'[<>:"/\\|?*]', '', name)
    s = s.replace(' ', '-')
    s = re.sub(r'-+', '-', s)
    s = s.strip('-')
    if not s:
        return "untitled"
    return s.lower()

# --- Portfolio Generation Functions ---
def load_submission_data(submission_id_path):
    """
    Loads metadata.json and the corresponding Python code from a submission directory.
    Returns a tuple (metadata, code_content) or (None, None) if files are missing/invalid.
    """
    metadata_file_path = os.path.join(submission_id_path, "metadata.json")

    if not os.path.exists(metadata_file_path):
        print(f"Warning: metadata.json not found in {submission_id_path}. Skipping.")
        return None, None

    try:
        with open(metadata_file_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {metadata_file_path}: {e}. Skipping.")
        return None, None
    except Exception as e:
        print(f"Error reading {metadata_file_path}: {e}. Skipping.")
        return None, None

    code_filename = metadata.get("code_filename")
    if not code_filename:
        print(f"Warning: 'code_filename' missing in metadata for {submission_id_path}. Skipping code.")
        return metadata, "Code content could not be found due to missing filename in metadata."

    code_file_path = os.path.join(submission_id_path, code_filename)
    if not os.path.exists(code_file_path):
        print(f"Warning: Code file '{code_filename}' not found in {submission_id_path}. Skipping code.")
        return metadata, "Code file not found at expected path."

    try:
        with open(code_file_path, 'r', encoding='utf-8') as f:
            code_content = f.read()
    except Exception as e:
        print(f"Error reading code file {code_file_path}: {e}. Skipping.")
        return metadata, "Error reading code content."

    return metadata, code_content

def generate_problem_markdown(metadata, code_content, output_base_dir):
    """
    Generates a Markdown file for a single problem.
    Output: output_base_dir/[problem_slug]/README.md
    """
    problem_title = metadata.get("problem_title", "Untitled Problem")
    problem_slug = metadata.get("problem_slug", "untitled-problem")
    problem_url = metadata.get("problem_url", "#")
    submission_status = metadata.get("submission_status", "N/A")
    score = metadata.get("score", "N/A")
    submission_timestamp_raw = metadata.get("submission_timestamp")
    language = metadata.get("language", "python")

    formatted_timestamp = "N/A"
    try:
        if submission_timestamp_raw and submission_timestamp_raw != 'N/A':
            dt_object = datetime.fromisoformat(submission_timestamp_raw.replace('Z', '+00:00'))
            formatted_timestamp = dt_object.strftime("%Y-%m-%d %H:%M:%S UTC")
    except ValueError:
        formatted_timestamp = f"Invalid timestamp: {submission_timestamp_raw}"

    problem_output_dir = os.path.join(output_base_dir, problem_slug)
    os.makedirs(problem_output_dir, exist_ok=True)

    output_filepath = os.path.join(problem_output_dir, "README.md")

    # Use a consistent language for markdown code block (e.g., python)
    # The 'language' metadata field might be 'pypy3' but 'python' is standard for markdown.
    markdown_lang = "python" if language in ["python3", "pypy3"] else language

    markdown_content = f"""# [{problem_title}]({problem_url})

**Status:** {submission_status}
**Score:** {score}
**Submitted At:** {formatted_timestamp}
**Language:** {language}

---

## Solution Code

```{markdown_lang}
{code_content}
"""
    try:
        with open(output_filepath, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        print(f"Generated: {output_filepath}")
        return True
    except Exception as e:
        print(f"Error writing Markdown for {problem_title} to {output_filepath}: {e}")
        return False

def generate_main_readme(all_problems_data, output_base_dir):
    """
    Generates the main README.md for the entire portfolio, listing all problems.
    Output: output_base_dir/README.md
    """
    output_filepath = os.path.join(output_base_dir, "README.md")

    markdown_content = "# HackerRank Solutions Portfolio\n\n"
    markdown_content += "This repository contains my solutions to various HackerRank problems, categorized by language.\n\n"
    markdown_content += "## Python / PyPy3 Solutions\n\n"

    all_problems_data.sort(key=lambda x: x['problem_title'].lower())

    for problem in all_problems_data:
        problem_title = problem.get("problem_title", "Untitled Problem")
        problem_slug = problem.get("problem_slug", "untitled-problem")
        submission_status = problem.get("submission_status", "N/A")
        score = problem.get("score", "N/A")

        # Create a relative path for the link in the main README
        link_path = os.path.join(".", problem_slug, "README.md").replace("\\", "/")

        markdown_content += f"- [{problem_title}]({link_path}) - Status: {submission_status}, Score: {score}\n"

    try:
        with open(output_filepath, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        print(f"\nGenerated main portfolio README: {output_filepath}")
    except Exception as e:
        print(f"Error writing main README to {output_filepath}: {e}")

def main_portfolio_generation():
    """
    Main logic for portfolio generation. This script assumes submissions are already downloaded.
    """
    os.makedirs(PORTFOLIO_OUTPUT_DIR, exist_ok=True)

    all_problems_for_main_readme = []
    processed_submissions_count = 0
    generated_markdown_count = 0
    errors_count = 0

    print(f"\n--- Starting Portfolio Generation ---")
    print(f"Scanning for submissions in: {PORTFOLIO_SUBMISSIONS_INPUT_DIR}")

    if not os.path.exists(PORTFOLIO_SUBMISSIONS_INPUT_DIR):
        print(f"Error: Submission input directory '{PORTFOLIO_SUBMISSIONS_INPUT_DIR}' not found. Please ensure sync_HR_portfolio.py ran successfully and created this directory.")
        return

    for submission_id_folder in os.listdir(PORTFOLIO_SUBMISSIONS_INPUT_DIR):
        submission_id_path = os.path.join(PORTFOLIO_SUBMISSIONS_INPUT_DIR, submission_id_folder)

        if os.path.isdir(submission_id_path):
            processed_submissions_count += 1
            metadata, code_content = load_submission_data(submission_id_path)

            if metadata and code_content:
                # Add problem data for the main README
                all_problems_for_main_readme.append({
                    "problem_title": metadata.get("problem_title"),
                    "problem_slug": metadata.get("problem_slug"),
                    "submission_status": metadata.get("submission_status"),
                    "score": metadata.get("score")
                })

                if generate_problem_markdown(metadata, code_content, PORTFOLIO_OUTPUT_DIR):
                    generated_markdown_count += 1
                else:
                    errors_count += 1
            else:
                errors_count += 1 # Count cases where metadata/code couldn't be loaded

    if all_problems_for_main_readme:
        generate_main_readme(all_problems_for_main_readme, PORTFOLIO_OUTPUT_DIR)
    else:
        print("No valid submissions found to generate the main portfolio README.")

    print("\n--- Portfolio Generation Summary ---")
    print(f"Total submission folders scanned: {processed_submissions_count}")
    print(f"Individual problem Markdown files generated: {generated_markdown_count}")
    print(f"Errors/Skipped submissions: {errors_count}")
    print(f"Portfolio output directory: {os.path.abspath(PORTFOLIO_OUTPUT_DIR)}")
    print("------------------------------------")
    print("Portfolio generation finished.")

if __name__ == "__main__":
    main_portfolio_generation()