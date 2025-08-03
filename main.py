import argparse
import asyncio
import sys

from charger.tariffs import create_tariff

def parse_args(args):
    parser = argparse.ArgumentParser(description="Create a tariff using Ohme API.")
    parser.add_argument("--name", type=str, help="Name of the tariff to create", default="PVPC")
    return parser.parse_args(args)

def main(args):
    asyncio.run(create_tariff(args.name))

if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    main(args)
