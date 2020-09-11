import os


def main():
    worldpay_api_key = input(
        "Please enter your WorldPay Service Key (https://online.worldpay.com/settings/keys):\n")
    endpoint = input(
        "Enter a webhook URL for payment confirmations (optional)\n")
    secret_key = os.urandom(24)
    with open('.env', 'w') as env:
        env.write(
            "# Your WorldPay Service Key (https://online.worldpay.com/settings/keys)\n")
        env.write(f"WORLDPAY_API_KEY={worldpay_api_key}\n")
        env.write("# Your URL for receiving payment confirmations\n")
        env.write(f"END_OF_INTERACTION_URL={endpoint}\n")
        env.write("# Secret Key for session storage\n")
        env.write(f"SECRET_KEY={secret_key}\n")


if __name__ == '__main__':
    main()
