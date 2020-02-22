import argparse
#from .broker import Broker

def run(args):
    #initialize API
    #broker = Broker(**args)
    try:
        from IPython import embed
        embed()
    except ImportError:
        import code
        code.interact(local=locals())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--key-id', help='API_KEY_ID')
    parser.add_argument('--secret-key', help='API_SECRET_KEY')
    parser.add_argument('--base-url', help="The broker API's base url")
    args = parser.parse_args()

    run({k: v for k, v in vars(args).items() if v is not None})


if __name__ == '__main__':
    main()