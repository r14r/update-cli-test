#!/usr/bin/env python3
"""Dependency-free Python CLI fixture."""
import argparse
import json


def compute(a: int, b: int) -> int:
    return a + b


def main() -> None:
    parser = argparse.ArgumentParser(prog="fixture-py")
    parser.add_argument("command", choices=["health", "add"])
    parser.add_argument("numbers", type=int, nargs="*")
    args = parser.parse_args()
    if args.command == "health":
        print(json.dumps({"status": "ok", "runtime": "python"}, sort_keys=True))
    else:
        if len(args.numbers) != 2:
            parser.error("add requires exactly two integers")
        print(json.dumps({"result": compute(*args.numbers)}, sort_keys=True))


if __name__ == "__main__":
    main()
