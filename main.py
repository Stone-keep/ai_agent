import os
import glob
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load all .env files in the current directory
for env_file in glob.glob('*.env'):
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

response = client.models.generate_content(model="gemini-2.5-flash", contents=messages)

if response.usage_metadata is None:
    raise RuntimeError("GenerateContentResponse is missing usage metadata")

def main():
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        print(response.text)
    else:
        print(response.text)


if __name__ == "__main__":
    main()