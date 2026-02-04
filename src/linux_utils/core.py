import argparse
from linux_utils.harvester import run_harvest


def main():
    parser = argparse.ArgumentParser(
        description="Linux Utils - Personal Productivity Suite"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available utilities")

    # Harvest Command
    harvester_parser = subparsers.add_parser(
        "harvest", help="Summarize directory structure and contents"
    )
    harvester_parser.add_argument(
        "path", nargs="?", default=".", help="Target directory"
    )
    harvester_parser.add_argument(
        "-o", "--output", default="harvest_result.txt", help="Output filename"
    )

    args = parser.parse_args()

    if args.command == "harvest":
        run_harvest(args.path, args.output)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
