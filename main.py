from bitcoin import BTC, green, yellow


btc = BTC()


if __name__ == '__main__':
    btc.document()

    print(green("Bitcoin Address: "), yellow(btc.ADDRESS))
    print(green("Private Key WIF: "), yellow(btc.WIF))

    btc.answer()