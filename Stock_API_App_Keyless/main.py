import requests
# Text functionality
from twilio.rest import Client
# Email functionality
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Twilio for SMS functionality
VIRTUAL_TWILIO_NUMBER = "+18773602563"
# This is the number for the Twilio virtual phone for testing
VERIFIED_NUMBER = "+18777804236"
TWILIO_SID = "Your Twilio account SID goes here"
TWILIO_AUTH_TOKEN = "Your Twilio authorization token goes here"

# Email functionality
EMAIL_ADDRESS = "yourEmail@email.com"
EMAIL_PASSWORD = "Secret - use your own email and password"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Set preferred stock to track
STOCK_NAME = "AAPL"
COMPANY_NAME = "Apple Inc"

# API components
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_API_KEY = "Your Alphavantage API key goes here"
NEWS_API_KEY = "Your News API key goes here"

# Get yesterday's closing stock price
stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}

response = requests.get(STOCK_ENDPOINT, params=stock_parameters)
data = response.json()["Time Series (Daily)"]
# Get value from Time Series
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
print(yesterday_closing_price)

# Get closing stock price for day before yesterday
day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
print(day_before_yesterday_closing_price)

# Find the difference between yesterday's price and the day before yesterday's price
difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
up_down = None
# If prices are different
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

# Find percent difference between the two stock prices
diff_percent = round((difference / float(yesterday_closing_price)) * 100)
print(diff_percent)

# If stock difference is greater than 1%, draft and send messages
if abs(diff_percent) > 1:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }

    # Get articles from NewsAPI about the company we're tracking
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]

    # Python slice operator to get first 3 articles returned from NewsAPI
    three_articles = articles[:3]
    print(three_articles)

    # Format articles into a new list
    formatted_articles = [
        f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for
        article in three_articles]
    print(formatted_articles)
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    # Send each article as a separate message via Twilio.
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_=VIRTUAL_TWILIO_NUMBER,
            to=VERIFIED_NUMBER
        )

    # Send all articles in one email
    email_content = "\n\n".join(formatted_articles)
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS
    msg['Subject'] = "Apple Stock Alert"
    msg.attach(MIMEText(email_content, 'plain'))

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    server.send_message(msg)
    server.quit()
