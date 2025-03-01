#!/usr/bin/env python3
"""
Bitwarden Subset Extractor

This script processes a Bitwarden JSON export file to extract entries 
containing specific keywords and saves them to a new JSON file.

Usage:
    python bitwarden_subset.py input.json output.json "keyword1,keyword2,keyword3"

Example:
    python bitwarden_subset.py bitwarden_export.json child_vault.json "school,game,club"
"""

import json
import sys
import os
from datetime import datetime

def extract_bitwarden_subset(input_file, output_file, keywords):
    """
    Process a Bitwarden JSON export to extract entries containing specific keywords.
    
    Args:
        input_file (str): Path to the Bitwarden JSON export file
        output_file (str): Path to save the filtered JSON file
        keywords (list): List of keywords to search for in each entry
    
    Returns:
        int: Number of entries extracted
    """
    # Load the Bitwarden export
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found")
        return 0
    except json.JSONDecodeError:
        print(f"Error: Input file '{input_file}' is not valid JSON")
        return 0
    
    # Check if this is a Bitwarden export
    if not isinstance(data, dict) or 'items' not in data or not isinstance(data['items'], list):
        print("Error: File doesn't appear to be a valid Bitwarden export")
        return 0
    
    # Extract items matching any of the keywords
    extracted_items = []
    
    for item in data['items']:
        # Fields to search in
        search_fields = []
        
        # Add name and notes fields if they exist
        if 'name' in item and item['name']:
            search_fields.append(item['name'].lower())
        if 'notes' in item and item['notes']:
            search_fields.append(item['notes'].lower())
        
        # Add login fields if they exist
        if 'login' in item and item['login']:
            if 'username' in item['login'] and item['login']['username']:
                search_fields.append(item['login']['username'].lower())
            if 'uris' in item['login'] and item['login']['uris']:
                for uri in item['login']['uris']:
                    if 'uri' in uri and uri['uri']:
                        search_fields.append(uri['uri'].lower())
        
        # Check custom fields if they exist
        if 'fields' in item and item['fields']:
            for field in item['fields']:
                if 'name' in field and field['name'] and 'value' in field and field['value']:
                    search_fields.append(field['name'].lower())
                    search_fields.append(field['value'].lower())
        
        # Check if any keyword matches any field
        if any(keyword.lower() in field for field in search_fields for keyword in keywords):
            extracted_items.append(item)
    
    # Create a new export with only the matched items
    output_data = {
        'encrypted': False,
        'items': extracted_items,
        'folders': data.get('folders', []),  # Include all folders
        'collections': [],  # Empty collections as they might not be relevant
        'extractedDate': datetime.now().isoformat()
    }
    
    # Save the filtered data
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2)
        print(f"Successfully extracted {len(extracted_items)} entries to '{output_file}'")
        return len(extracted_items)
    except Exception as e:
        print(f"Error saving output file: {str(e)}")
        return 0

def main():
    # Check arguments
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} input.json output.json \"keyword1,keyword2,keyword3\"")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    keywords = [k.strip() for k in sys.argv[3].split(',')]
    
    print(f"Searching for keywords: {', '.join(keywords)}")
    
    # Run the extraction
    num_extracted = extract_bitwarden_subset(input_file, output_file, keywords)
    
    # Exit with appropriate status code
    sys.exit(0 if num_extracted > 0 else 1)

if __name__ == "__main__":
    main()
