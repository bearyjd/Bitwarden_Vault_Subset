# Bitwarden Vault Subset

A Python utility to extract a subset of passwords from a Bitwarden vault export based on keywords.

## Overview

This tool helps you create a filtered subset of passwords from a Bitwarden vault export by searching for specific keywords across all fields. It's particularly useful for parents who want to share only certain passwords with their children, or for anyone who needs to split a vault during account separation.

## Features

- Extract password entries containing specific keywords
- Search across multiple fields (name, username, URL, notes, custom fields)
- Preserve the complete entry structure for each matched item
- Maintain folder structure from the original export
- Generate a valid JSON file ready to be imported into another Bitwarden account

## Requirements

- Python 3.6 or higher
- A JSON export from Bitwarden

## Installation

Clone this repository:

```bash
git clone https://github.com/bearyjd/Bitwarden_Vault_Subset.git
cd Bitwarden_Vault_Subset
```

No additional dependencies are required beyond the Python standard library.

## Usage

1. **Export your Bitwarden vault**:
   - In Bitwarden, go to **Tools** > **Export Vault**
   - Select **JSON** format (recommended for preserving all data)
   - Enter your master password
   - Save the file securely

2. **Run the script**:

```bash
python bitwarden_subset.py input.json output.json "keyword1,keyword2,keyword3"
```

Where:
- `input.json` is the path to your Bitwarden export file
- `output.json` is the path where the filtered vault will be saved
- `"keyword1,keyword2,keyword3"` is a comma-separated list of keywords to search for

3. **Import the filtered export**:
   - Create or log into the target Bitwarden account
   - Go to **Tools** > **Import Data**
   - Select **Bitwarden (JSON)** as the file format
   - Upload the `output.json` file

## Example

To extract all entries related to school, games, and clubs:

```bash
python bitwarden_subset.py my_vault_export.json child_vault.json "school,game,club"
```

## How It Works

1. The script loads the Bitwarden JSON export
2. It searches for each keyword in the following fields of each entry:
   - Item name
   - Username
   - Website URLs
   - Notes
   - Custom fields (both names and values)
3. If any keyword is found in any of these fields, the entire entry is included in the output
4. The script creates a new JSON file with the same structure as a Bitwarden export, but containing only the matched entries

## Security Considerations

- Handle the export files securely - they contain sensitive information
- Delete the input and output JSON files when you're done with them
- Avoid storing these files in cloud storage unless encrypted
- If creating a vault for a child, consider changing any shared critical passwords afterward

## Use Cases

- Creating a subset of passwords for a child
- Splitting a shared vault during relationship changes
- Creating a limited vault for travel
- Sharing only work-related credentials with colleagues

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Acknowledgments

- Bitwarden for their excellent password manager
- All contributors to this project
