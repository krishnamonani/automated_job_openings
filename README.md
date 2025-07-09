# Automated Daily Job Emailer

This project fetches the latest remote job postings from RemoteOK, summarizes them using Google Gemini AI, and sends a daily email with the results. It is designed for anyone who wants to receive a concise, AI-generated summary of relevant job openings (e.g., DevOps, Python, Intern roles) directly in their inbox.

---

## Features

- **Fetches jobs** from [RemoteOK](https://remoteok.com/)
- **Filters** jobs by keywords (`devops`, `python`, `intern`)
- **Summarizes** job listings using Google Gemini AI (Generative AI)
- **Sends** a daily email with the summary
- **Logs** all activity and errors to `job_log.txt`
- **Highly configurable** via environment variables

---

## Requirements

- Python 3.8+
- [Google Gemini AI API key](https://ai.google.dev/)
- Gmail account (for sending emails)
- [RemoteOK API](https://remoteok.com/api) (no key required)
- The following Python packages:
  - `requests`
  - `smtplib` (standard library)
  - `email` (standard library)
  - `python-dotenv`
  - `google-generativeai`
  - `black` (optional, for code formatting)
  - `pre-commit` (optional, for git hooks)

---

## Setup

1. **Clone the repository**

   ```sh
   git clone <your-repo-url>
   cd automated_job_openings
   ```

2. **Install dependencies**

   ```sh
   pip install -r requirements.txt
   ```

3. **Set up environment variables**

   Create a `.env` file in the project root with the following content:

   ```
   GEMINI_KEY=your_gemini_api_key
   YOUR_EMAIL=your_gmail_address@gmail.com
   EMAIL_PASSWORD=your_gmail_app_password
   TO_EMAIL=recipient_email_address
   ```

   > **Note:** For Gmail, you may need to create an [App Password](https://support.google.com/accounts/answer/185833) if 2FA is enabled.

4. **(Optional) Set up pre-commit hooks**

   If you want to use Black for code formatting on every commit:

   ```sh
   pip install pre-commit
   pre-commit install
   ```

---

## Usage

Run the script manually:

```sh
python daily_job_email.py
```

Or schedule it to run daily using Windows Task Scheduler, cron, or another automation tool.

---

## How it Works

1. **Fetch Jobs:**  
   The script requests the latest jobs from RemoteOK and filters them by keywords.

2. **Summarize:**  
   The filtered jobs are summarized into a short, readable email using Google Gemini AI.

3. **Send Email:**  
   The summary is sent to your chosen recipient via Gmail.

4. **Logging:**  
   All actions and errors are logged in `job_log.txt` for troubleshooting and auditing.

---

## File Structure

```
.
├── daily_job_email.py      # Main script
├── job_log.txt            # Log file (auto-generated)
├── requirements.txt       # Python dependencies
├── .env                   # Your environment variables (not committed)
├── .pre-commit-config.yaml# (Optional) Pre-commit hook config for Black
```

---

## Troubleshooting

- **Pre-commit not working?**  
  Make sure you ran `pre-commit install` and are using `git commit`.

- **Email not sending?**  
  - Check your `.env` values.
  - Make sure you are using an App Password for Gmail.
  - Check `job_log.txt` for error messages.

- **Gemini API errors?**  
  - Check your API key and quota.
  - See `job_log.txt` for details.

---

## Credits

- [RemoteOK](https://remoteok.com/)
- [Google Gemini AI](https://ai.google.dev/)
- [Black](https://github.com/psf/black)
- [pre-commit](https://pre-commit.com/)

---

*Made with ❤️ for job seekers and