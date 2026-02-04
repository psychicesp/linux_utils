import argparse
from linux_utils.harvester import run_harvest


def main():
    parser = argparse.ArgumentParser(
        description="Harvester - Summarize directory structure and contents"
    )
    parser.add_argument(
        "path", 
        nargs="?", 
        default=".", 
        help="Target directory to harvest"
    )
    parser.add_argument(
        "-o", 
        "--output", 
        default="harvest_result.txt", 
        help="Output filename"
    )

    args = parser.parse_args()

    run_harvest(args.path, args.output)

if __name__ == "__main__":
    main()
