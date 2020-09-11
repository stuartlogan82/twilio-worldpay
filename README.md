# Twilio Worldpay Integration

A Flask Application that captures basic credit card details over the phone and interacts with WorldPay APIs to process a payment. You can optionally pass in a `caller_name` and `amount` as query parameters for dynamic payment amounts.

## Prerequisites

- **Make sure that you use a PCI Enabled project so that DTMF and logs are not collected in Twilio's systems.** Turn it on under [Programmable Voice Settings](https://www.twilio.com/console/voice/settings)
- Setup a [Worldpay Account](https://online.worldpay.com/signup)
- Go to [Settings -> Keys](https://online.worldpay.com/settings/keys) and make a note of the Service Key
- Optional: Setup and Configure the **gcloud** command line tool so that you can deploy to [Google AppEngine](https://cloud.google.com/sdk/gcloud/reference/app)

## Installation

Recommended: Create and run the following in a Python3 Virtual Environment

```bash
pip install -r requirements.txt
```

Populate your `.env` file from the `.env.example` file or using `configure-env.py`

```bash
python configure-env.py
```

Install the [Twilio CLI](https://www.twilio.com/docs/twilio-cli/quickstart)

Optional: Purchase a Twilio number (or use an existing one)

Optional: Search for available numbers in your region

```bash
twilio api:core:available-phone-numbers:local:list  --country-code=GB --voice-enabled
```

Optional: Buy a number

```bash
twilio api:core:incoming-phone-numbers:create --phone-number="+442038236401"
```

### Develop locally

Start the server locally

```bash
flask run
```

or, for an https connection

```bash
flask run --cert=cert.pem --key=key.pem
```

Wire up your Twilio number with your endpoint on incoming calls. This will automatically start an [ngrok](https://ngrok.com) tunnel to your machine.

```bash
twilio phone-numbers:update +442038236401 --voice-url=http://localhost:5000/make_payment
```

### Deploy to AppEngine

```bash
gcloud app deploy
```

Point your Incoming Webhook to your AppEngine instance.

```bash
twilio phone-numbers:update +442038236401 --voice-url=https://YOUR-APPENGINE-INSTANCE.appspot.com/make_payment
```

Alternatively, you would probably want to identify the caller and work out how much they had to pay. This might be something you use Twilio Studio for and then use a TwiML Redirect widget to pass the call to this payment flow. You can pass them in as query params `caller_name` and `amount`.

## Capture Payment Details at the end of the Interaction

If you set `END_OF_INTERACTION_URL` in your `.env` file to a Webhook that you host, you can handle events. You will receive the response from WorldPay with confirmation of the transaction which you could use to update your billing system or CRM.

## Caveats

There is no error handling currently for invalid inputs or failed payments.
