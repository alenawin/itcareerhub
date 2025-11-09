
from formatter import (
    input_prompt,
    print_films_table,
    print_genres_table,
    GoToMenu,
    print_last_queries,
    print_popular_queries
)
from mongo_connector import (
    write_keyword,
    write_genre,
    get_last_queries,
    popular_keywords,
    popular_genres
)
from mysql_connector import (
    get_films_by_keyword,
    get_films_by_genre_year,
    get_categories,
    get_year_range,
    close_connection
)


def range_year():
    while True:
        try:
            min_year = int(input_prompt("Type min year: "))
            break
        except ValueError:
            print(f"Please, enter valid number")
    while True:
        try:
            max_year = int(input_prompt("Type max year: "))
            if max_year >= min_year:
                break
            else:
                print(f"Year must be >= {min_year}")
        except ValueError:
            print(f"Please, enter valid number")
    return min_year, max_year


def exact_year():
    while True:
        try:
            release_year = int(input_prompt("Type release year: "))
            break
        except ValueError:
            print(f"Please, enter valid number")
    return release_year


# keyword
def keyword_search():
    keyword = input_prompt("Type a keyword: ")
    result = get_films_by_keyword(keyword)
    write_keyword(keyword, len(result))
    if not result:
        print("No films found.")
        return
    print_films_table(result)


# genre and years
def genre_search():
    all_genres = get_categories()
    print_genres_table(all_genres)
    while True:
        genre = input_prompt("Type a genre: ")
        if genre.lower() in all_genres:
            break
        else:
            print(f"Unknown genre <{genre}>")
            print_genres_table(all_genres)
    years = get_year_range(genre)
    print(f"Years range: from {years[0]} to {years[1]}")

    while True:
        mode = input_prompt("Choose mode (1 - exact year / 2 - range of years / 3 - all time): ")
        if mode == "1":
            release = exact_year()
            min_year = release
            max_year = release
            break
        elif mode == "2":
            two_years = range_year()
            min_year = two_years[0]
            max_year = two_years[1]
            break
        elif mode == "3":
            min_year = None
            max_year = None
            break
        else:
            print(f'Unknown command {mode}. Type 1, 2 or 3.')

    result = get_films_by_genre_year(genre, min_year, max_year)
    write_genre(genre, min_year, max_year, len(result))
    if not result:
        print("No films found.")
        return
    print_films_table(result)


# Print last queries
def last_queries():
    while True:
        try:
            count = int(input_prompt("Type number of last queries (max = 10): "))
            if count > 10 or count <= 0:
                raise ValueError
            break
        except ValueError:
            print("Please enter valid number from 1 to 10")
    print_last_queries(get_last_queries(count))


def popular_queries():
    popular = popular_keywords() + popular_genres()
    popular.sort(key=lambda item: item['count'], reverse=True)
    print("Popular queries:")
    print_popular_queries(popular[:5])


def print_help():
    print("""
Available commands:
  • keyword   — Search films by keyword
  • genre     — Search films by genre and release year
  • popular   — Show most popular queries
  • last      — Show last queries
  • help      — Show available commands
  • exit      — Quit the program
  • /menu     — Go back to the main menu
""")


print("""
=========================================
=  Welcome to the Film Search Console   =
=========================================""")
print_help()


# Main loop
def main_menu():
    while True:
        try:
            command = input("Main menu. Type a command to continue: ")
            if command == "keyword":
                keyword_search()
                print()
            elif command == "genre":
                genre_search()
                print()
            elif command == "last":
                last_queries()
                print()
            elif command == "popular":
                popular_queries()
                print()
            elif command == "exit":
                print("Bye-Bye!")
                break
            elif command == "help":
                print_help()
            elif command == "/menu" or command == "":
                pass
            else:
                print(f"Unknown command <{command}>. Print 'help' for help")
        except GoToMenu:  # return to the main loop
            print()


try:
    main_menu()
except KeyboardInterrupt:
    print()
    print("bye-bye!")
finally:
    close_connection()

