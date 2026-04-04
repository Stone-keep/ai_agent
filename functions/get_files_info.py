import os

def get_files_info(working_directory, directory="."):
    try:


        working_directory_abspath = os.path.abspath(working_directory)
        target_directory = os.path.normpath(os.path.join(working_directory_abspath, directory))
        target_dir_valid = os.path.commonpath([working_directory_abspath, target_directory]) == working_directory_abspath
        if not target_dir_valid:
            return f"Result for '{directory}' directory:\nError: Cannot list '{directory}' as it is outside the permitted working directory\n"
        
        if os.path.isdir(target_directory) is False:
            return f"Result for '{directory}' directory:\nError: '{directory}' is not a directory\n"

        result = ""
        directory_contents = os.listdir(target_directory)

    
        for file in directory_contents:
            result += f"- {file}: file_size={os.path.getsize(os.path.join(target_directory, file))} bytes, is_dir={os.path.isdir(os.path.join(target_directory, file))}\n"
    
    except Exception as e:
        return f"Result for '{directory}' directory:\nError: {e}\n"
    
    if directory == ".":
        return f"Result for current directory:\n{result}"
    else:
        return f"Result for '{directory}' directory:\n{result}"