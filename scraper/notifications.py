import smtplib
import ssl
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from socket import gaierror

from config import Config
from scraper.utils.file_io import get_data, get_attachement
from scraper.utils.logger import get_logger

log = get_logger(__name__)
config = Config()

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
EMAIL = config.ACCOUNT
EMAIL_SUBJECT = "Notification from ra-scraper"
DATE_FORMAT = "%d/%m/%Y"
FILENAME = "EventItem.jsonl"
CITY_FILTER = "London"


def main():
    # Get data and filter with CITY_FILTER
    data = get_data(FILENAME).sort_values(by=["date"])
    data = data[data["city"] == CITY_FILTER]

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

    attachement = get_attachement(FILENAME)
    attachement.add_header('Content-Disposition', 'attachment', filename=f"{CITY_FILTER}_{FILENAME}")
    msg.attach(attachement)

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
        log.error("SMTP error occurred: %s", e)
    else:
        log.info("Email sent")


if __name__ == "__main__":
    main()
