import argparse
from broker_api.client import Client

def run(args):
    client = Client(**args)
    try:
        from IPython import embed
        embed()
    except ImportError:
        import code
        code.interact(local=locals())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--broker', help='The Broker to connect to. Currently only supports Alpaca!')
    parser.add_argument('--key-id', help='API_KEY_ID')
    parser.add_argument('--secret-key', help='API_SECRET_KEY')
    args = parser.parse_args()

    run({k: v for k, v in vars(args).items() if v is not None})


if __name__ == '__main__':
    main()