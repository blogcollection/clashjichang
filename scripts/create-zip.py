import os
import zipfile
import sys

sys.stdout.reconfigure(encoding='utf-8')

project_root = r"c:\Users\USER\Desktop\新建文件夹 (3)\blog\G BLOG\14.BLOG CLASHJICHANG.SBS"
output_zip = os.path.join(project_root, "clashjichang-sbs-project.zip")

# Directories and files to exclude
EXCLUDE_DIRS = {
    'node_modules',
    '.git',
    '.astro',
    '__pycache__',
    '.system_generated'
}

EXCLUDE_FILES = {
    'clashjichang-sbs-project.zip'
}

file_count = 0
total_size = 0

with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
    for root, dirs, files in os.walk(project_root):
        # Filter out excluded directories in-place
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith('.')]
        
        for file in files:
            if file in EXCLUDE_FILES or file.endswith('.pyc') or file.endswith('.tmp'):
                continue
            
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, project_root)
            
            # Avoid packing the zip into itself
            if os.path.abspath(full_path) == os.path.abspath(output_zip):
                continue
                
            zipf.write(full_path, rel_path)
            file_count += 1
            total_size += os.path.getsize(full_path)

zip_size_mb = os.path.getsize(output_zip) / (1024 * 1024)
raw_size_mb = total_size / (1024 * 1024)

print(f"Zip created successfully: {output_zip}")
print(f"Total files packed: {file_count}")
print(f"Uncompressed size: {raw_size_mb:.2f} MB")
print(f"Compressed zip size: {zip_size_mb:.2f} MB")
