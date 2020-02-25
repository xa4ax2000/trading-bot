import argparse

def run(args):
    #client = BrokerClient.__init__(**args)
    try:
        from IPython import embed
        embed()
    except ImportError:
        import code
        code.interact(local=locals())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--broker', help='The Broker to connect to. Currently only supports Alpaca!', required=True)
    parser.add_argument('--key-id', help='API_KEY_ID (if supported)')
    parser.add_argument('--secret-key', help='API_SECRET_KEY (if supported)')
    parser.add_argument('--username', help='Username (if supported)')
    parser.add_argument('--password', help='API_SECRET_KEY (if supported)')
    args = parser.parse_args()

    run({k: v for k, v in vars(args).items() if v is not None})


if __name__ == '__main__':
    main()