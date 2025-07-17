import argparse
from cli import CLI

if __name__ == "__main__" :
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--company", type=str, help="Company name", required=True)
    parser.add_argument("-o", "--output", type=str, help="Output file name", required=False, default="output.txt")
    parser.add_argument("-d", "--domain", type=str, help="Domain name", required=True)
    parser.add_argument("-p", "--pagenumber", type=int, help="Number of pages to be read", required=False, default=5)
    args = parser.parse_args()

    cli = CLI(args)