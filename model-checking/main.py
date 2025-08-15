import logging
import os
import re
import subprocess

def get_pages(folder: str) -> list[int]:
    """
    Scans the specified folder for files with the '.trail' extension and extracts unique page numbers from filenames
    matching the pattern '.pml<page_number>.'.
    Args:
        folder (str): The path to the folder to scan for files.
    Returns:
        list[int]: A sorted list of unique page numbers (as integers) extracted from the filenames.
    Note:
        The function expects filenames to contain the pattern '.pml<page_number>.' (e.g., 'example.pml3.trail').
        Only files ending with '.trail' are considered.
    """
    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]

    pages = []

    for file in files:
        if not file.endswith('.trail'):
            continue
        match = re.search(r'\.pml(\d+)\.', file)

        if not match:
            continue

        pages.append(match.group(1))

    return sorted(set(pages), key=int)


def verify_trail_files(folder: str, promela_file: str) -> None:
    """
    Verifies a set of trail files against a given Promela model using the Spin model checker.
    Args:
        folder (str): The path to the folder containing the trail files to be verified.
        promela_file (str): The path to the Promela (.pml) file to be used for verification.
    Returns:
        None
    Behavior:
        - Retrieves all trail files (pages) from the specified folder.
        - For each trail file, runs the Spin model checker with the specified Promela file.
        - Prints the verification status for each trail file.
        - Logs an error if the model checking output does not contain either "End_S_success" or "End_S_cancel".
    Raises:
        None directly, but logs errors if verification fails.
    """

    pages = get_pages(folder)

    for page in pages:
        print(f"Verifying the trail file {page}...")
        command = f"spin -t{page} {promela_file}"

        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        if not "valid end state" in str(result.stdout):
            logging.error(f"Model checking failed for page {page}: {command}.")

        # if "pbbLog[0] = cancel_a" in str(result.stdout) and "pbbLog[2] = cancel_b" in str(result.stdout):
        #     print(f"Trail file {page} verified: End_S_cancel")

BASE_DIR = './'
PROMELA_FILE = 'alice.pml'

verify_trail_files(BASE_DIR, os.path.join(BASE_DIR, PROMELA_FILE))