#!/usr/bin/env python

def read_api_key(file_path):
    """
    Args: file path for api key
    Outputs: text for api_key
    """
    with open(file_path, 'r') as file:
        return file.read().strip()