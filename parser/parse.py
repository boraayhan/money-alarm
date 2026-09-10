# Name: Parser
# Function: Splits job listing(s) (.txt form) to a JobListing object using LLM, outputs in JSON form to new file in /parser/out/

# Input: Path to .txt file containing job listings
# Output: JSON to new .json in /jobs/

import datetime
import json
from typing import Optional

from ollama import chat, ChatResponse
from pydantic import BaseModel


class JobListing:
    def __init__(
        self,
        title: str | None,
        companyName: str | None,
        location: str | None = None,
        description: str | None = None,
        postDate: datetime.datetime | None = None,
        deadline: datetime.datetime | None = None,
    ):
        self.title = title
        self.companyName = companyName
        self.location = location
        self.description = description
        self.postDate = postDate
        self.deadline = deadline

        self.postDate = datetime.datetime.now()


class JobListingOutput(BaseModel):
    title: str | None = None
    companyName: str | None = None
    location: str | None = None
    description: str
    postDate: datetime.datetime | None = None
    deadline: datetime.datetime | None = None


f = open("emails/extracted_emails.txt", "r")
content = f.read()
f.close()

response: ChatResponse = chat(
    model="qwen3:4b-instruct-2507-q8_0",
    messages=[
        {
            "role": "system",
            "content": "You are an email parser that generates job listings given emails. Should there be insufficient information to fill out a field, leave that field blank. Do NOT generate job listings from emails that are not strictly listings for jobs. For the description, include context from the email that is relevant to the job listing, and try to copy sentences and phrases verbatim for the description, but do not add or infer any information not listed in the email content.",
        },
        {
            "role": "user",
            "content": f"Parse the following emails:\n\n{content}",
        },
    ],
    format={
        "type": "array",
        "items": JobListingOutput.model_json_schema(),
    },
)

data = [
    JobListingOutput.model_validate(job) for job in json.loads(response.message.content)
]

jobs = [
    JobListing(
        title=job.title,
        companyName=job.companyName,
        location=job.location,
        description=job.description,
        postDate=job.postDate,
        deadline=job.deadline,
    )
    for job in data
]

output = [
    {
        "title": job.title,
        "companyName": job.companyName,
        "location": job.location,
        "description": job.description,
        "postDate": job.postDate.isoformat() if job.postDate else None,
        "deadline": job.deadline.isoformat() if job.deadline else None,
    }
    for job in jobs
]


with open(f"parser/out/output{datetime.datetime.now().isoformat()}.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)
