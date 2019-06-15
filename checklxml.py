#!/usr/bin/env python3
# -*- encoding: utf-8-unix -*-


def main():
    """Check if lxml module is available."""
    try:
        import lxml
        exit(0)
    except ModuleNotFoundError:
        exit(1)


if __name__ == '__main__':
    main()
