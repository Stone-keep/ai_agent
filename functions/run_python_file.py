import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    try:
        
        working_directory_abspath = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_directory_abspath, file_path))
        target_file_valid = os.path.commonpath([working_directory_abspath, target_file]) == working_directory_abspath
    
        if not target_file_valid:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
        if os.path.isfile(target_file) is False:
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if target_file.endswith(".py") is False:
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", target_file]
        
        if args:
            command.extend(args)
        
        process = subprocess.run(command, capture_output=True, text=True, timeout=30)

        process_output_string = ""

        if process.returncode != 0:
            process_output_string += f"Process exited with code {process.returncode}\n"
        
        if process.stdout == "":
            process_output_string += "No stdout output produced\n"
        else:
            process_output_string += f"STDOUT:\n{process.stdout}\n"

        if process.stderr == "":
            process_output_string += "No stderr output produced\n"
        else:
            process_output_string += f"STDERR: \n{process.stderr}\n"

        return process_output_string

    except Exception as e:
        return f"Error: executing Python file: {e}"