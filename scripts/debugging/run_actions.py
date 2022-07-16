"""Simple yaml debugger"""
import subprocess
import sys

import yaml

LOCAL_TESTS = ["Run license checks", "Run Black", "Python Pylint", "Test with pytest"]


def run_command(command) -> None:
    """Run a command kill actions if it fails

    Args:
        command (str): command to run
    """
    ret_code = subprocess.call(command, shell=True)
    if ret_code != 0:
        print(f"\033[31mError: `{command}` failed. Exiting...\033[0m")
        sys.exit(1)


if __name__ == "__main__":
    with open(".github/workflows/code_checks.yml", "rb") as f:
        my_dict = yaml.safe_load(f)
    steps = my_dict["jobs"]["build"]["steps"]

    print_green = lambda x: print(f"\033[32m{x}\033[0m")

    for step in steps:
        if "name" in step and step["name"] in LOCAL_TESTS:
            compressed = step["run"].replace("\n", ";").replace("\\", "")
            compressed = compressed.replace("--check", "")
            curr_command = f"{compressed}"

            print("*" * 100)
            print_green(f"Running: {curr_command}")
            run_command(curr_command)
        else:
            print("*" * 100)
            print(f"Skipping {step}")

    # Add checks for building documentation
    print_green("Building Documentation")
    run_command("cd docs/; make html SPHINXOPTS='-W;'")

    print("\n")
    print_green("=" * 100)
    print_green("ALL CHECKS PASSED")
    print_green("=" * 100)
