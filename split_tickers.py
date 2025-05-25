import json
import sys


def chunk_list(data, size):
    return [data[i:i + size] for i in range(0, len(data), size)]


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "tickers.json"
    chunk_size = int(sys.argv[2]) if len(sys.argv) > 2 else 3

    with open(input_file) as f:
        tickers = json.load(f)

    chunks = chunk_list(tickers, chunk_size)
    matrix = {"include": [{"chunk": chunk} for chunk in chunks]}
    print(json.dumps(matrix))
