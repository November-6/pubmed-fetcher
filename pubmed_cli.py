

# Command-line interface: cli.py
import argparse
import sys
from pubmed_fetcher import fetch_paper_ids, fetch_xml_data, extract_pubmed_data_to_csv

def main():
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed.")
    parser.add_argument("query", type=str, help="Query to search PubMed.")
    parser.add_argument(
        "-f", "--file", type=str, default=None,
        help="Filename to save CSV results. If not provided, outputs to console."
    )
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug output.")

    args = parser.parse_args()

    if args.debug:
        print(f"Running with query: {args.query}")

    try:
        paper_ids = fetch_paper_ids(args.query)
        if not paper_ids:
            print("No papers found.")
            sys.exit(0)

        xml_data = fetch_xml_data(paper_ids)
        results = extract_pubmed_data_to_csv(xml_data, args.file)

        if args.file:
            print(f"Results saved to {args.file}")
        else:
            for row in results:
                print(row)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
