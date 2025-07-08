import requests, smtplib
from email.mime.text import MIMEText
from datetime import datetime
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

# Config
GEMINI_KEY = os.getenv("GEMINI_KEY")
YOUR_EMAIL = os.getenv("YOUR_EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
TO_EMAIL = os.getenv("TO_EMAIL")

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")


def get_jobs():
    try:
        response = requests.get("https://remoteok.com/api", timeout=10)
        response.raise_for_status()
        jobs = response.json()[1:]
        kws = ["devops", "python", "intern"]
        return [job for job in jobs if any(k in job["position"].lower() for k in kws)][
            :5
        ]
    except Exception as e:
        log(f"[ERROR] Failed to fetch jobs: {e}")
        return []


def summarize_jobs(jobs):
    content = "\n\n".join(
        [
            f"{job['position']} at {job['company']} ({job.get('location', 'Remote')})\nApply: {job['url']}"
            for job in jobs
        ]
    )

    prompt = f"""
Act as a job assistant.
Summarize the following jobs into a neat, email-friendly message.
Make sure each entry includes the job title, company, remote status, and apply link.

Jobs:
{content}
"""

    response = model.generate_content(prompt)
    return response.text


def send_email(body):
    msg = MIMEText(body)
    msg["Subject"] = f"Daily Jobs ({datetime.now():%d %b})"
    msg["From"], msg["To"] = YOUR_EMAIL, TO_EMAIL
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
        s.login(YOUR_EMAIL, EMAIL_PASSWORD)
        s.send_message(msg)


def log(message):
    with open("job_log.txt", "a") as f:
        f.write(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {message}\n")


def main():
    jobs = get_jobs()
    if not jobs:
        log("No jobs found today.")
        return

    log(f"Found {len(jobs)} jobs")
    try:
        body = summarize_jobs(jobs)
        send_email(body)
        log("Email sent successfully.")
    except Exception as e:
        log(f"[ERROR] {e}")


if __name__ == "__main__":
    main()
