import argparse
import os
import sys

from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env file before importing any other modules

from rich.console import Console
from brain import ingest_rules


console = Console()

WFDF_RULES = {
    'es': 'https://topultimatepa.files.wordpress.com/2021/06/wfdf-rules-of-ultimate-2021-2024-esp-universal-1.pdf',
    'en': 'https://rules.wfdf.org/documents/wfdf-rules-of-ultimate-2021-2024/download',
}

def main() -> int:
    lang = os.getenv('UI_LANGUAGE', 'en')
    parser = argparse.ArgumentParser(description='Ingest rules')
    parser.add_argument('--url', type=str, default=WFDF_RULES[lang], help='URL to the rules PDF document')
    args = parser.parse_args()
    docs = ingest_rules(args.url)
    console.print(f'Ingested {len(docs)} documents')

    return 0


if __name__ == '__main__':
    sys.exit(main())