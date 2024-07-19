import os
import smtplib
from datetime import datetime, timedelta
from github import Github

def send_email(to_email, subject, body):
    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = os.getenv('SMTP_PORT')
    smtp_username = os.getenv('SMTP_USERNAME')
    smtp_password = os.getenv('SMTP_PASSWORD')

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        message = f"Subject: {subject}\n\n{body}"
        server.sendmail(smtp_username, to_email, message)

def main():
    token = os.getenv('GITHUB_TOKEN')
    g = Github(token)
    org = g.get_organization("AssistAILabs")

    now = datetime.utcnow()
    soon = now + timedelta(days=2)

    for project in org.get_projects():
        for column in project.get_columns():
            for card in column.get_cards():
                issue = card.get_content()
                if issue and isinstance(issue, github.Issue.Issue):
                    deadline_str = issue.raw_data.get('Deadline')
                    if deadline_str:
                        deadline = datetime.strptime(deadline_str, "%Y-%m-%d")
                        if now <= deadline <= soon:
                            assignees = ['harshit0414@gmail.com','kunalbaghel995@gmail.com','guarika513@gmail.com']
                            for assignee in assignees:
                                send_email(
                                    to_email=assignee,
                                    subject=f"Reminder: Issue #{issue.number} is due soon",
                                    body=f"The issue #{issue.number} ({issue.title}) is due on {deadline_str}."
                                )

if __name__ == "__main__":
    main()
