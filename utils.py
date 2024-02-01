# This is a template. 
# You should modify the functions below to match
# the signatures determined by the project specification

def sumvalues(values):
    """
    Calculates the sum of values in a list or array.

    Args:
        values (list or array): A list or array of numerical values.

    Returns:
        float: The sum of the values.

    Raises:
        ValueError: If non-numerical values are present in the list or array.

    Example:
        >>> sumvalues([1, 2, 3, 4, 5])
        15
        >>> sumvalues([-1, 0, 1, 2])
        2.0
    """
    total = 0
    for value in values:
        if not isinstance(value, (int, float)):
            raise ValueError("Non-numerical value found in the list")
        total += value
    return total


def maxvalue(values):
    """
    Returns the maximum value in a list or array.

    Args:
        values (list or array): A list or array of numerical values.

    Returns:
        float: The maximum value in the list or array.

    Raises:
        ValueError: If non-numerical values are present in the list or array.
        ValueError: If the list or array is empty.

    Example:
        >>> maxvalue([1, 2, 3, 4, 5])
        5
        >>> maxvalue([-1, 0, 1, 2])
        2
    """
    if not values:
        raise ValueError("Empty list")
    max_value = values[0]
    for i in range(1, len(values)):
        if not isinstance(values[i], (int, float)):
            raise ValueError("Non-numerical value found in the list")
        if values[i] > max_value:
            max_value = values[i]
    return max_value


def minvalue(values):
    """
    Returns the minimum value in a list or array.

    Args:
        values (list or array): A list or array of numerical values.

    Returns:
        float: The minimum value in the list or array.

    Raises:
        ValueError: If non-numerical values are present in the list or array.
        ValueError: If the list or array is empty.

    Example:
        >>> minvalue([1, 2, 3, 4, 5])
        1
        >>> minvalue([-1, 0, 1, 2])
        -1
    """
    if not values:
        raise ValueError("Empty list")
    min_value = values[0]
    for i in range(1, len(values)):
        if not isinstance(values[i], (int, float)):
            raise ValueError("Non-numerical value found in the list")
        if values[i] < min_value:
            min_value = values[i]
    return min_value


def meanvalue(values):
    """
    Calculates the arithmetic mean value of a list or array.

    Args:
        values (list or array): A list or array of numerical values.

    Returns:
        float: The arithmetic mean value of the list or array.

    Raises:
        ValueError: If non-numerical values are present in the list or array.
        ValueError: If the list or array is empty.

    Example:
        >>> meanvalue([1, 2, 3, 4, 5])
        3.0
        >>> meanvalue([-1, 0, 1, 2])
        0.5
    """
    if not values:
        raise ValueError("Empty list")
    total = 0
    count = 0
    for value in values:
        if not isinstance(value, (int, float)):
            raise ValueError("Non-numerical value found in the list")
        total += value
        count += 1
    return total / count


def countvalue(values, xw):
    """
    Counts the number of occurrences of a value in a list or array.

    Args:
        values (list or array): A list or array of values.
        x: The value to count.

    Returns:
        int: The number of occurrences of the value in the list or array.

    Example:
        >>> countvalue([1, 2, 2, 3, 3, 3], 2)
        2
        >>> countvalue([1, 2, 2, 3, 3, 3], 4)
        0
    """
    count = 0
    for value in values:
        if value == xw:
            count += 1
    return count
