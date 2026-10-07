import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
  working_dir_abs = os.path.abspath(working_directory)
  target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))



  # Will be True or False
  valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
  if valid_target_dir == False:
    return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
  if os.path.isdir(target_dir):
    items = os.listdir(target_dir)
    strs_list = []
    for item in items:
      item_path = os.path.join(target_dir, item)
      strs_list.append(f' - {item}: file_size={os.path.getsize(item_path)} bytes, is_dir={os.path.isdir(item_path)}')
    return '\n'.join(strs_list)
  else:
    return f'Error: "{directory}" is not a directory'