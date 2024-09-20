import os
import pyperclip

def get_file_structure(root_dir):
    structure = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        level = dirpath.replace(root_dir, '').count(os.sep)
        indent = '  ' * level
        structure.append(f"{indent}- {os.path.basename(dirpath)}/")
        for file in filenames:
            if file.endswith('.py'):
                structure.append(f"{indent}  - {file}")
    return '\n'.join(structure)

def collect_source_code(root_dir, output_file):
    content = []

    # Add title
    content.append("# Project Overview\n")

    # Add file structure
    content.append("## Project File Structure\n")
    content.append(get_file_structure(root_dir))
    content.append("\n")

    # Add source code
    content.append("## Source Code\n")
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.py'):
                filepath = os.path.join(dirpath, filename)
                relative_path = os.path.relpath(filepath, root_dir)
                
                content.append(f"### File: {relative_path}\n")
                content.append("```python\n")
                
                with open(filepath, 'r', encoding='utf-8') as infile:
                    content.append(infile.read())
                
                content.append("\n```\n")

    # Combine all content into a single string
    all_content = '\n'.join(content)

    # Write to file
    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write(all_content)

    # Copy to clipboard
    pyperclip.copy(all_content)

# Usage
root_directory = '.'  # Current directory, change this if needed
output_file = 'util/collected_sourcecode/project_overview.md'

# ensure directory exists
os.makedirs(os.path.dirname(output_file), exist_ok=True)

collect_source_code(root_directory, output_file)
print(f"Source code and file structure collected in {output_file} and copied to clipboard 🚀")
