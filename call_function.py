import json
from collections.abc import Callable
from functions.write_file import *
from functions.run_python_file import *
from functions.get_file_content import *
from functions.get_files_info import *

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Lists content in a specified file relative to the working directory, providing file content - limiting 10000 characters",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The file path of the requested document, this is a required property. Do not attempt to run without being provided a file path",
                },
            },
            "required": ['file_path'],
        },
    },
}

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Lists content in a specified file relative to the working directory, providing file content - limiting 10000 characters",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The file path of the requested document, this is a required property. Do not attempt to run without being provided a file path",
                },
            },
            "required": ['file_path'],
        },
    },
}

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "runs a the requested python program.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The file path of the requested python file",
                },
                "args":{
                  'type':'array',
                  'items': {
                    'type':'string'
                  },
                  'description': 'The possible agruments that may be provided'
                }
            },
            "required": ['file_path'],
        },
    },
}

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "writes to a specific file.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The file path of the requested file",
                },
                "content":{
                  'type':'string',
                  'description': 'The content that must written to the file',
                }
            },
            "required": ['file_path', 'content'],
        },
    },
}

AVAILABLE_FUNCTIONS = [
    schema_get_files_info,
    schema_get_file_content,
    schema_run_python_file,
    schema_write_file
]

def call_function(tool_call, verbose: bool = False) -> dict:
  function_name = tool_call.function.name
  function_args = json.loads(tool_call.function.arguments or "{}")
  if verbose:
    print(f" - Calling function: {function_name}({function_args})")
  else:
    print(f" - Calling function: {function_name}")
  

  function_map: dict[str, Callable[..., str]] = {
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file,
    "get_files_info": get_files_info
  }
  if function_name not in function_map:
    return {
      "role": "tool",
      "tool_call_id": tool_call.id,
      "content": f"Error: Unknown function: {function_name}",
    }
  selected_function = function_map[function_name]
  function_args["working_directory"] = "./calculator"
  result = selected_function(**function_args)
  return {
    "role": "tool",
    "tool_call_id": tool_call.id,
    "content": result,
  }