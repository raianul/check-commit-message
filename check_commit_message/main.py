import sys
import subprocess
import re


def get_current_branch():
    # Use Git command to get the current branch name
    result = subprocess.run(
        ['git', 'rev-parse', '--abbrev-ref', 'HEAD'], stdout=subprocess.PIPE, text=True
    )
    return result.stdout.strip()


def check_branch_name(branch_name):
    # Extract the ticket number from the branch name
    match = re.match(r'^([A-Z0-9]+-\d+)', branch_name)
    if not match:
        print(f"Debug: Full branch name: '{branch_name}'")
        print(
            f"Error: Branch name '{branch_name}' does not match the expected pattern."
        )
        sys.exit(1)

    ticket_number = match.group(1)
    return ticket_number


def check_commit_message(stage, files):
    if stage != 'commit':
        # Skip if not a commit (e.g., during pre-push)
        return

    # Get the current branch name
    branch_name = get_current_branch()
    print('BRANCH:', branch_name)
    print(f"Debug: Current branch name: '{branch_name}'")

    # Check the branch name
    ticket_number = check_branch_name(branch_name)
    print('TKT_NUM:', ticket_number)
    # Read the commit message from the file
    commit_msg_path = files[0]
    with open(commit_msg_path, 'r') as commit_file:
        commit_message = (
            commit_file.read().strip()
        )  # Remove leading and trailing whitespaces

    print(f"Debug: Commit message: '{commit_message}'")

    # Check if the commit message starts with the ticket number
    if not commit_message.startswith(ticket_number):
        print(f"Error: Commit message should start with '{ticket_number}'.")
        sys.exit(1)


if __name__ == '__main__':
    print(sys.argv)
    if len(sys.argv) < 3:
        print('Usage: python3 check_commit_message.py <stage> <file1> [<file2> ...]')
        sys.exit(1)

    stage = sys.argv[1]
    files = sys.argv[2:]
    check_commit_message(stage, files)
