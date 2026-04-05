import os
import glob
import argparse
import sys
from urllib import response
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

def main():

    for env_file in glob.glob('*.env'): #Loads all .env files in the current directory.
        load_dotenv(env_file)

    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key is None:
        raise RuntimeError("API key not found. Please set up the GEMINI_API_KEY environment variable in the api_key.env file.")

    parser = argparse.ArgumentParser(description="Gemini 2.5 Flash")
    parser.add_argument("user_prompt", type=str, help="User prompt goes here.")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output.")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    client = genai.Client(api_key=api_key)

    for iteration in range(20):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(system_instruction=system_prompt, tools=[available_functions])
        )

        if args.verbose:
            if response.usage_metadata is None:
                raise RuntimeError("GenerateContentResponse is missing usage metadata")
            if iteration == 0:  # Only print this once at the start
                print(f"User prompt: {args.user_prompt}")
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
            else:
                print(f"Iteration {iteration + 1}: {response.usage_metadata.prompt_token_count} prompt tokens, {response.usage_metadata.candidates_token_count} response tokens")

        if response.function_calls:
            # Execute function calls and add results to messages
            function_call_results = []
            
            for function_call in response.function_calls:
                function_call_result = call_function(function_call, verbose=args.verbose)
                
                if not function_call_result.parts:
                    raise Exception("Function call result is missing parts")
                
                if function_call_result.parts[0].function_response is None:
                    raise Exception("Function call result part is missing function response")
                    
                if function_call_result.parts[0].function_response.response is None:
                    raise Exception("Function call result part is missing function response content")
                    
                function_call_results.append(function_call_result.parts[0])

            # Add the function results as a tool message to continue the conversation
            messages.append(types.Content(role="user", parts=function_call_results))
        else:
            # No more function calls, print the final response
            print(response.text)
            return
    
    # If we reach here, we exceeded max iterations
    print("Error: Maximum number of iterations (20) reached without completing the response.")
    sys.exit(1)  

if __name__ == "__main__":
    main()