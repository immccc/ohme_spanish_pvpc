import argparse
import asyncio

from charger.tariffs import create_tariff

def _parse_args():
    parser = argparse.ArgumentParser(description="Create a tariff using Ohme API.")
    parser.add_argument("--name", type=str, help="Name of the tariff to create", default="PVPC")
    return parser.parse_args()
    
def main(args):
    asyncio.run(create_tariff(args.name))


if __name__ == "__main__":
    args = _parse_args()
    main(args)
