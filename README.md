# Stock News App

## Introduction
This application allows users to see the change in price of a specific stock, and be alerted to the top three news articles about that company via email.

## Features
- **Email Functionality**: When the application is run, the expected data will be sent to the user's email address.
- **API Functionality**: This program uses stock price data from the Alphavantage API and collects news stories from NewsAPI.

## Installation
To run the stock news application, follow these steps:

- Clone the repository:
- git clone https://github.com/evanjamesc/stock-api-app.git
- cd stock-api-app
- Run "main.py" locally on your machine

## How to Use
- Launch the application using the instructions above.
- Enter your own Twilio account SID and authorization token for text functionality.
- Enter your own email address and password for the account at which you would like to be notified of stock price changes.
- By default, this application tracks the stock of Apple Inc., change this to your desired stock.
- Run the application to recieve your price change and news summary in your inbox.

## Technologies Used
- Twilio, Alphavantage API, NewsAPI, and Python 3, including the following libraries/modules:
- Requests
- SMPT Protocol Client
- MIME (Multipurpose Internet Mail Extensions)

## Contact
For more information, please contact Evan Christianson at evanjameschristianson@gmail.com
