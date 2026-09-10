# Name: Parser
# Function: Splits job listing(s) (.txt form) to a JobListing object using LLM, outputs in JSON form to new file in /parser/out/

# Input: Path to .txt file containing job listings
# Output: JSON to new .json in /jobs/

import time
from ollama import chat
from ollama import ChatResponse

response: ChatResponse = chat(model='gemma3', messages=[
  {
    'role': 'user',
    'content': 'Why is the sky blue?',
  },
])
print(response.message.content)