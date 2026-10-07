import os
import subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:

  working_dir_abs = os.path.abspath(working_directory)
  target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))

  # Will be True or False
  valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
  if not valid_target_dir:
    return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
  if not os.path.isfile(target_dir):
    return f'Error: "{file_path}" does not exist or is not a regular file'
  if not target_dir.endswith('.py'):
    return f'Error: "{file_path}" is not a Python file'
  command = ["python", target_dir]
  if args:
    command.extend(args)
  try:
    program_process = subprocess.run(command,
    cwd = working_dir_abs,
    capture_output = True,
    text = True,
    timeout = 30,
    )
    program_output = ''
  
    if program_process.returncode != 0:
      program_output += f'Process exited with code {program_process.returncode}\n'
    if (program_process.stdout == '') and (program_process.stderr == ''):
      program_output += f'No output produced\n'
    else:
      if(program_process.stdout):
        program_output += f'STDOUT: {program_process.stdout}\n'
      if(program_process.stderr):
        program_output +=  f'STDERR: {program_process.stderr}'
    return program_output
  except Exception as e:
    return f'Error: executing Python file: {e}'