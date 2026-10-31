import argparse
import sys

from . import scan


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="todoscan", description="List TODO-style comments.")
    parser.add_argument("path", nargs="?", default=".")
    parser.add_argument("--tags", nargs="+", default=["TODO", "FIXME", "HACK"])
    parser.add_argument("--strict", action="store_true", help="exit 1 when anything is found")
    args = parser.parse_args(argv)
    count = 0
    for finding in scan(args.path, args.tags):
        print(finding)
        count += 1
    print(f"{count} found", file=sys.stderr)
    return 1 if args.strict and count else 0


if __name__ == "__main__":
    sys.exit(main())
