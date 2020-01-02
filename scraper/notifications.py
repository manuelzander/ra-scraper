import smtplib
import ssl
from socket import gaierror
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from datetime import date

from config import Config
from scraper.utils.file_io import get_data
from scraper.utils.logger import get_logger

log = get_logger(__name__)
config = Config()

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
EMAIL = config.ACCOUNT
EMAIL_SUBJECT = "Notifications from ra-scraper"
DATE_FORMAT = "%d/%m/%Y"


def main():
    # Get data and filter for London events
    data = get_data("EventItem.jsonl").sort_values(by=["artist"])
    data = data[data["city"] == "London"]

    # Setup email message
    msg = MIMEMultipart()
    msg["Subject"] = f"{EMAIL_SUBJECT} - {(date.today().strftime(DATE_FORMAT))}"
    msg["To"] = EMAIL
    msg["From"] = EMAIL

    html = """\
    <html>
      <head></head>
      <body>
        {0}
      </body>
    </html>
    """.format(
        data.to_html()
    )

    msg_html = MIMEText(html, "html")
    msg.attach(msg_html)

    # Send email message
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
            server.login(EMAIL, config.SECRET)
            server.sendmail(EMAIL, EMAIL, msg.as_string())
    except (gaierror, ConnectionRefusedError):
        log.error("Failed to connect to the server. Bad connection settings?")
    except smtplib.SMTPServerDisconnected:
        log.error("Failed to connect to the server. Wrong user/password?")
    except smtplib.SMTPException as e:
        log.error("SMTP error occurred: " + str(e))
    else:
        log.info("Email sent")


if __name__ == "__main__":
    main()
