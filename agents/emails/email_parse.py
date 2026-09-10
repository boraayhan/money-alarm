# Name: Email Parser
# Function: Gets an email from a .mbox file and extracts the subject, sender, and recipient. It also decodes the email content if it is in quoted-printable format.

# Input: Path to .mbox file containing emails
# Output: .txt file containing the extracted information from the email(s) in 

from pathlib import Path
import mailbox
from email.header import decode_header
import quopri

EMAILS_DIR = Path(__file__).resolve().parent
MBOX_PATH = EMAILS_DIR / "Test.mbox"
OUTPUT_PATH = EMAILS_DIR / "extracted_emails.txt"

def get_subject(subject):
    subject_parts = []
    subjects = decode_header(subject)
    for content, encoding in subjects:
        try: 
            subject_parts.append(content.decode(encoding or "utf8"))
        except:
            subject_parts.append(content)

    return "".join(subject_parts)

inbox = mailbox.mbox(MBOX_PATH)

# exports to a txt file
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
with OUTPUT_PATH.open('w') as f:
    for message in inbox:
        f.write(f"To: {message['to']}\n")
        f.write(f"From: {message['from']}\n")
        f.write(f"Subject: {get_subject(message['subject'])}\n")
        parts = { part.get_content_type(): part for part in message.get_payload() }
        plain_content = parts["text/plain"]
        f.write(f"Content: {quopri.decodestring(plain_content.get_payload()).decode('utf-8')}\n\n")
