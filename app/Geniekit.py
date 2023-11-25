import os
from openai import OpenAI
import argparse
from dotenv import load_dotenv
import re
load_dotenv() 

MAX_INPUT_LENGTH =32
OPENAI_API_KEY=os.getenv('OPENAI_API_KEY')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", type=str, required=True)
    args = parser.parse_args()
    user_input = args.input
    print(f"User input: {user_input}")
    if validate_length(user_input):
        generate_branding_snippet(user_input)
        generate_keywords(user_input)
    else:
        raise ValueError(f"Input length is too long. must be under {MAX_INPUT_LENGTH}. submitted input is {user_input}  ")
        

def validate_length(prompt: str) -> bool:
    return len(prompt) <= 12


def generate_keywords(prompt: str) -> list[str]:
    enriched_prompt = f"Generate upbeat branding for {prompt}"
    print(enriched_prompt)
    # Load your API key from an environment or secret management service.  
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": enriched_prompt}],
        max_tokens=28
    )

    # Extract output text
    keywords_text: str = response.choices[0].message.content

    # Strip whitespace and split using multiple delimiters
    keywords_text = keywords_text.strip()
    # Define multiple delimiters as a regular expression pattern
    delimiters = r'[,|\n|\*|-| ]'  # Adjust the delimiters as needed
    keywords_array = re.split(delimiters, keywords_text)
    keywords_array = [k.lower().strip() for k in keywords_array]
    keywords_array = [k for k in keywords_array if len(k) >0]

    print(f"keywords: {keywords_array}")
    return keywords_array

def generate_branding_snippet(prompt: str) -> str:
    enriched_prompt = f"Generate upbeat branding for {prompt}"
    print(enriched_prompt)
    # Load your API kry from an environment or secret management serices.
    client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=OPENAI_API_KEY,
    )
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
    {"role": "system", "content": enriched_prompt}], 
    max_tokens=28
    )

    # Extract output text
    branding_text: str = response.choices[0].message.content

    # Strio whitespace.
    branding_text = branding_text.strip()


    # Add ... to truncated statements.
    last_char = branding_text[-1]

    if last_char not in(".", "!", "?"):
        branding_text += "..."
    print(f"Snippet: {branding_text}")
    return branding_text

if __name__ == "__main__":
    main()
