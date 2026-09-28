import argparse
import json
import string


def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using keywords")
    search_parser.add_argument("query", type=str, help="Search query")

    args = parser.parse_args()

    match args.command:
        case "search":
            print(f"Searching for: {args.query}")
            try:
                with open('data/movies.json', 'r') as f:
                    data = json.load(f)
                
                # Access the list under the "movies" key
                movie_list = data.get("movies", [])
                query_lower = args.query.lower()
                # No Punct
                no_punct_table = str.maketrans("", "", string.punctuation)
 
                # Search case-insensitively
                movies = [
                    movie["title"]
                    for movie in movie_list
                    if "title" in movie and query_lower.translate(no_punct_table) in movie["title"].lower().translate(no_punct_table)
                ]

                if not movies:
                    print("No matching movies found.")
                    return

                # Display results indexed cleanly from 1
                for i, title in enumerate(movies, start=1):
                    print(f"{i}. {title}")

            except FileNotFoundError:
                print("Error: File 'data/movies.json' not found.")
            except json.JSONDecodeError:
                print("Error: Could not parse 'data/movies.json'. Check JSON formatting.")

        case _:
            parser.print_help()


if __name__ == "__main__":
    main()