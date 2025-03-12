#!/usr/bin/env python3

import os
from pathlib import Path

# Set
#  of directories to ignore
EXCLUDED_DIRS = {'.git', 'node_modules', '__pycache__', '.idea', '.vscode', '.venv', 'venv'}

def generate_index_html(directory: Path):
    """Generate an index.html file in the given directory, listing all other HTML files."""
    html_files = [f for f in directory.glob('*.html') if f.name != 'index.html']
    if not html_files:
        return  # No need to create index.html if no other HTML files

    index_path = directory / 'index.html'
    with index_path.open('w', encoding='utf-8') as f:
        f.write('<!DOCTYPE html>\n')
        f.write('<html><head><meta charset="UTF-8"><title>Index of {}</title></head><body>\n'.format(directory))
        f.write('<h1>Index of {}</h1>\n'.format(directory))
        f.write('<ul>\n')
        for file in sorted(html_files):
            f.write(f'<li><a href="./{file.name}">{file.name}</a></li>\n')
        f.write('</ul>\n</body></html>\n')

    print(f"Generated index.html in {directory}")

def generate_root_index(root_dir: Path, subdirs_with_index):
    """Generate a root index.html that links to subdirectories containing an index.html."""
    index_path = root_dir / 'index.html'
    with index_path.open('w', encoding='utf-8') as f:
        f.write('<!DOCTYPE html>\n')
        f.write('<html><head><meta charset="UTF-8"><title>Root Index</title></head><body>\n')
        f.write('<h1>Root Index</h1>\n')
        f.write('<ul>\n')
        for subdir in sorted(subdirs_with_index):
            relative_path = os.path.relpath(subdir, root_dir)
            f.write(f'<li><a href="./{relative_path}/index.html">{relative_path}</a></li>\n')
        f.write('</ul>\n</body></html>\n')

    print(f"Generated root index.html with links to {len(subdirs_with_index)} subdirectories.")

def generate_readme(root_dir: Path, subdirs_with_index):
    """Generate a README.md file that links to subdirectories containing an index.html."""
    readme_path = root_dir / 'README.md'
    with readme_path.open('w', encoding='utf-8') as f:
        f.write('# Project Index\n\n')
        f.write('This README automatically lists subdirectories that contain HTML content.\n\n')
        f.write('## Subdirectories\n\n')
        for subdir in sorted(subdirs_with_index):
            relative_path = os.path.relpath(subdir, root_dir)
            f.write(f'- [{relative_path}](./{relative_path}/index.html)\n')

    print(f"Updated README.md with links to {len(subdirs_with_index)} subdirectories.")

def main():
    """Main function to scan directories and generate index.html and README.md files."""
    root_dir = Path('.').resolve()
    subdirs_with_index = []

    for root, dirs, files in os.walk('.'):
        root_path = Path(root).resolve()

        # Skip hidden and excluded directories
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS and not d.startswith('.')]

        if any(f.endswith('.html') for f in files):
            generate_index_html(root_path)
            if root_path != root_dir:  # Skip adding root itself to subdirs list
                subdirs_with_index.append(root_path)

    # Now generate the root index.html and README.md
    generate_root_index(root_dir, subdirs_with_index)
    generate_readme(root_dir, subdirs_with_index)

if __name__ == '__main__':
    main()
