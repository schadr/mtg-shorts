import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description="MTG Shorts CLI")
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    parser.add_argument('--file', type=str, help='Path to the video file that needs to be edited')
    parser.add_argument('--folder', type=str, help='Folder containing video files to be processed')
    args = parser.parse_args()

    print(f"Welcome to MTG Shorts CLI! Filename: {args.file}")


if __name__ == "__main__":
    main()