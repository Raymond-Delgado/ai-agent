import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI
from config import *
from call_function import *
import json
import sys

def main():
    load_dotenv()

    api_key = os.environ.get("OPENROUTER_API_KEY")

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    if api_key is None:
        raise RuntimeError('NO API KEY FOUND')

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    messages = [
        {'role': 'system', 'content': SYSTEM_PROMPT},
        {"role": "user", "content": args.user_prompt},
    ]
    for _ in range(20):
        response = client.chat.completions.create(
            model="openrouter/free",
            messages= messages,
            tools = AVAILABLE_FUNCTIONS,
        )
        if args.verbose:
            print(f'User prompt: {args.user_prompt}')
            print(f'Prompt tokens: {response.usage.prompt_tokens}')
            print(f'Response tokens: {response.usage.completion_tokens}')

        message = response.choices[0].message
        messages.append(message)
        
        if message.tool_calls:
            for tool_call in message.tool_calls:
                function_args = json.loads(tool_call.function.arguments or "{}")
                print(f"Calling function: {tool_call.function.name}({function_args})")
                result_message = call_function(tool_call,args.verbose)
                if result_message['content']:
                    if args.verbose:
                        print(f"-> {result_message['content']}")
                else:
                    raise Exception('ERROR')
                messages.append(result_message)
        else:
            print(message.content)
            return
    print('ERROR: The ai agent failed to provide an answer')
    sys.exit(1)



if __name__ == "__main__":
    main()
