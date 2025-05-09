def create_json_file(data, filename):
    """
    Create a JSON file from the given data.

    Args:
        data (dict): The data to be written to the JSON file.
        filename (str): The name of the JSON file to be created.
    """
    import json

    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)
        print(f"JSON file '{filename}' created successfully.")