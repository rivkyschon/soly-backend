import re

import re


def extract_number_of_stress_level(user_input: str) -> float | None:
    """
    Extracts a floating-point number that follows the word 'FINISH' in the given input string.

    Args:
    user_input (str): The input string to search for the pattern.

    Returns:
    float | None: The extracted number as a float if the pattern is found, otherwise None.
    """
    # Regular expression to find the pattern "FINISH" followed by a number
    match = re.search(r'FINISH(\d+(\.\d+)?)', user_input)

    # Check if a match is found
    if match:
        # Extract the number and convert it to float
        stress_level = float(match.group(1))
    else:
        stress_level = None

    return stress_level


def contains_finish(s):
    """
    Check if the string 's' contains the word 'FINISH', case-insensitive.

    :param s: String to be checked
    :return: True if 'FINISH' is in the string, False otherwise
    """
    return 'FINISH' in s.upper()


def remove_finish(s):
    """
    Remove the word 'FINISH' from the string 's', case-insensitive.

    :param s: String from which to remove the word 'FINISH'
    :return: String with 'FINISH' removed
    """
    return ' '.join(word for word in s.split() if word.upper() != 'FINISH')

def is_finished(expression: str, output: str) -> bool:
    """
    Checks if the given input string contains the word 'FINISH'.

    Args:
    expression (str): The expression to search for in the input string.
    output (str): The input string to search for the pattern.\


    Returns:
    bool: True if the pattern is found, otherwise False.
    """
    match = re.search(rf'{expression}', output)

    # Check if a match is found
    if match:
        return True
    else:
        return False
