import os
import glob
import argparse
from dotenv import load_dotenv
from google import genai

# Load all .env files in the current directory
for env_file in glob.glob('*.env'):
    load_dotenv(env_file)

api_key = os.environ.get("GEMINI_API_KEY")

if api_key is None:
    raise RuntimeError("API key not found. Please set up the GEMINI_API_KEY environment variable in the api_key.env file.")

client = genai.Client(api_key=api_key)

response = client.models.generate_content(model="gemini-2.5-flash", contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.")

if response.usage_metadata is None:
    raise RuntimeError("GenerateContentResponse is missing usage metadata")

print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
print(response.text)