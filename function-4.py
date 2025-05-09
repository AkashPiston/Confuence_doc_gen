def create_random_list(length):
    """
    Create a list of random integers.

    Args:
        length (int): The length of the list to be created.

    Returns:
        list: A list of random integers.
    """
    import random

    return [random.randint(1, 100) for _ in range(length)]