import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import requests
from credentials import EMAIL_ADDRESS, EMAIL_PASSWORD

# --- Function to get today's push count from GitLab API ---
def get_push_count(git_url):
    try:
        username = git_url.strip().split('/')[-1]
        api_url = f"https://gitlab.com/api/v4/users/{username}/events?action=pushed"
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            today = datetime.now().date()
            count = 0
            for event in data:
                created_at = event.get("created_at", "")
                if created_at and datetime.strptime(created_at[:10], "%Y-%m-%d").date() == today:
                    count += 1
            return count
        else:
            return 0
    except Exception as e:
        print(f"Error fetching push count for {git_url}: {e}")
        return 0

# --- Function to send email ---
def send_email(to_address, name, push_count):
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = to_address
        msg["Subject"] = f"Git Push Summary for {datetime.now().strftime('%d-%m-%Y')}"

        if push_count > 0:
            body = f"Hi {name},\n\n✅ You pushed {push_count} time(s) today. Great job! Keep it up 💪"
        else:
            body = f"Hi {name},\n\n⚠️ You haven’t pushed today. Please make sure to push at least once a day!"

        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)

        print(f"✅ Email sent to {to_address}")
    except Exception as e:
        print(f"❌ Error sending email to {to_address}: {e}")

# --- Main function ---
def main():
    input_file = "git.xlsx"
    output_file = "gitusers_updated.xlsx"

    try:
        df = pd.read_excel(input_file)
    except Exception as e:
        print(f"❌ Failed to read input file: {e}")
        return

    today_col = datetime.now().strftime("%d-%m-%Y")
    updated_data = []

    for _, row in df.iterrows():
        try:
            name, git_url, email = row[:3]
            push_count = get_push_count(git_url)
            pushed_today = "YES" if push_count > 0 else "NO"
            push_status = f"{push_count} pushes" if push_count > 0 else "Not pushed"

            if pd.notna(email) and '@' in email:
                send_email(email, name, push_count)

            new_row = {
                "NAME": name,
                "GITLINK": git_url,
                "Pushed_Today": pushed_today,
                today_col: push_status
            }
            updated_data.append(new_row)
        except Exception as e:
            print(f"❌ Error processing row: {e}")
            continue

    result_df = pd.DataFrame(updated_data)
    result_df.to_excel(output_file, index=False)
    print(f"✅ Updated Excel file saved at {output_file}")

if __name__ == "__main__":
    main()
