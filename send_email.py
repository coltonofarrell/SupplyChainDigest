import smtplib
import os
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ✅ Load credentials securely from GitHub Actions secrets
sender = os.environ.get("GMAIL_ADDRESS")
receiver = os.environ.get("GMAIL_RECIPIENT")
app_password = os.environ.get("GMAIL_PASSWORD")

# === Load today's digest file ===
today = datetime.now().strftime("%Y-%m-%d")
filename = f"supply_chain_digest_{today}.md"

if not os.path.exists(filename):
    print(f"❌ File '{filename}' not found.")
    exit()

with open(filename, "r", encoding="utf-8") as f:
    digest_content = f.read()

# === Create the email ===
msg = MIMEMultipart("alternative")
msg["Subject"] = f"📬 Supply Chain Digest – {today}"
msg["From"] = sender
msg["To"] = receiver
msg.attach(MIMEText(digest_content, "plain"))

# === Send the email ===
try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, app_password)
        server.sendmail(sender, receiver, msg.as_string())
    print("✅ Email sent successfully!")
except Exception as e:
    print(f"❌ Email failed: {e}")
