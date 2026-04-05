import os
from config import FILE_READ_MAX_CHARACTERS

def get_file_content(working_directory, file_path):

    try:
        working_directory_abspath = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_directory_abspath, file_path))
        target_file_valid = os.path.commonpath([working_directory_abspath, target_file]) == working_directory_abspath
    
        if not target_file_valid:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
        if os.path.isfile(target_file) is False:
            return f'Error: File not found or is not a regular file: "{file_path}"'
    
        with open(target_file, "r") as f:

            file_content = f.read(FILE_READ_MAX_CHARACTERS) # Read up to FILE_READ_MAX_CHARACTERS to prevent issues with large files.
        
            if f.read(1):
                file_content += f'\n[...File "{file_path}" truncated at {FILE_READ_MAX_CHARACTERS} characters]'
            
        return file_content

    except Exception as e:
        return f"Error: {e}"