# REPLACE THIS WITH YOUR CODE
import os
import yaml


def get_apikey():
    """
    Reads API key from a configuration file.

    This function opens a configuration file named "apikeys.yml", reads the API key for OpenAI

    Returns:
    api_key (str): The OpenAI API key.
    """

    # Construct the full path to the configuration file
    script_dir = os.getcwd()
    file_path = os.path.join(script_dir, "apikeys.yaml")

    with open(file_path, 'r') as yamlfile:
        # REPLACE THIS WITH YOUR CODE
        openai_svc = yaml.safe_load(yamlfile)

    return openai_svc['openai']['api_key']


if __name__ == "__main__":
    print("API_KEY", get_apikey())