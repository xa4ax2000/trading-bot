import argparse
from broker_api.broker_client import BrokerClient
"""Interactive console broker client

This script allows the user to access the BrokerClient and interact with the Broker via supported APIs. This script
requires the `ipython` module to be installed - which could be found in the requirements.txt.
"""


def run(args):
    client = BrokerClient(**args)
    try:
        from IPython import embed
        embed()
    except ImportError:
        import code
        code.interact(local=locals())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--broker-input', help='The Broker to connect to. Currently only supports Alpaca!',
                        required=True)
    parser.add_argument('--key-id', help='API_KEY_ID (if supported)')
    parser.add_argument('--secret-key', help='API_SECRET_KEY (if supported)')
    parser.add_argument('--username', help='Username (if supported)')
    parser.add_argument('--password', help='API_SECRET_KEY (if supported)')
    args = parser.parse_args()

    run({k: v for k, v in vars(args).items() if v is not None})


if __name__ == '__main__':
    main()