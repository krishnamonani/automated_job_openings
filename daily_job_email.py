import requests, smtplib  # For HTTP requests and sending emails
from email.mime.text import MIMEText  # For HTTP requests and sending emails
from datetime import datetime  # For timestamps in logs and email subjects
import google.generativeai as genai  # For using Gemini AI to summarize jobs
from dotenv import load_dotenv  # For loading environment variables from .env file
import os  # For accessing environment variables

# Load environment variables from .env file (API keys, email credentials, etc.)
load_dotenv()

# Read sensitive configuration from environment variables
GEMINI_KEY = os.getenv("GEMINI_KEY")  # Gemini API key
YOUR_EMAIL = os.getenv("YOUR_EMAIL")  # Sender's email address
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")  # Sender's email password
TO_EMAIL = os.getenv("TO_EMAIL")  # Recipient's email address

# Configure Gemini AI model with your API key
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")  # Use the Gemini 1.5 Flash model


def get_jobs():
    try:
        # Make a GET request to the RemoteOK API with a 10-second timeout
        response = requests.get("https://remoteok.com/api", timeout=10)
        response.raise_for_status()  # Raise an error if the request failed
        jobs = response.json()[1:]  # Skip the first element (API metadata)
        kws = ["devops", "python", "intern"]  # Keywords to filter jobs
        # Filter jobs by keywords in the position title
        return [job for job in jobs if any(k in job["position"].lower() for k in kws)][
            :5
        ]
    except Exception as e:
        # Log any error that occurs during fetching or filtering
        log(f"[ERROR] Failed to fetch jobs: {e}")
        return []


def summarize_jobs(jobs):
    # Prepare a compact string with job details for the AI prompt
    content = "\n".join(
        [
            f"{job['position']} | {job['company']} | {job.get('location', 'Remote')} | {job['url']}"
            for job in jobs
        ]
    )
    # Instruction for Gemini: summarize the jobs for an email
    prompt = (
        "Summarize these jobs for an email. Each entry: title, company, location, link.\n"
        f"{content}"
    )
    # Call Gemini AI to generate the summary
    response = model.generate_content(prompt)
    return response.text  # Return the AI-generated summary


def send_email(body):
    # Create a plain text email message
    msg = MIMEText(body)
    # Set the email subject with today's date
    msg["Subject"] = f"Daily Jobs ({datetime.now():%d %b})"
    # Set sender and recipient
    msg["From"], msg["To"] = YOUR_EMAIL, TO_EMAIL
    # Connect to Gmail's SMTP server using SSL
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
        s.login(YOUR_EMAIL, EMAIL_PASSWORD)  # Log in with your credentials
        s.send_message(msg)  # Send the email


def log(message):
    with open("job_log.txt", "a") as f:
        # Write the message with a timestamp
        f.write(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {message}\n")


def main():
    jobs = get_jobs()  # Step 1: Fetch and filter jobs
    if not jobs:
        log("No jobs found today.")  # Log if no jobs were found
        return

    log(f"Found {len(jobs)} jobs")  # Log the number of jobs found
    try:
        body = summarize_jobs(jobs)  # Step 2: Summarize jobs using Gemini AI
        send_email(body)  # Step 3: Send the summary via email
        log("Email sent successfully.")  # Log success
    except Exception as e:
        log(f"[ERROR] {e}")  # Log any error that occurs in summarizing or sending


if __name__ == "__main__":
    main()  # Run the main workflow if this script is executed directly
