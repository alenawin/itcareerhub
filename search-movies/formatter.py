
# Exception to go to main menu - command /menu
class GoToMenu(BaseException):
    pass


# Raise exception if user entered /menu
def input_prompt(prompt: str):
    result = input(prompt)
    if result == '/menu':
        raise GoToMenu
    return result


def wrap_text(string: str, width: int) -> list[str]:
    """
    Splits a string into a list of substrings of the specified width.
    """
    words = string.split()
    lines = []
    line = []
    cur_length = 0
    for word in words:
        if cur_length == 0:
            line.append(word)
            cur_length += len(word)
        elif cur_length + 1 + len(word) <= width:
            line.append(word)
            cur_length += 1 + len(word)
        else:
            lines.append(" ".join(line))
            line, cur_length = [word], len(word)
    if line:
        lines.append(" ".join(line))
    return lines


def print_films_table(films: list[tuple]):
    """
    Prints a formatted table of films with their titles, release years, and descriptions.
    Shows up to 10 films per page and asks the user if they want to see more.
    Descriptions are wrapped to fit within a fixed width for better readability.
    """

    title_width = max(len(row[0]) for row in films + [("Title", "", "")])
    year_width = len("Year")
    desc_width = 50

    print(f"{'Title': <{title_width}}  {'Year': <{year_width}}  Description")
    print("-" * (title_width + year_width + desc_width + 6))

    cur_page = films[:10]
    remaining = films[10:]
    for title, description, year in cur_page:
        lines = wrap_text(description.strip(), desc_width) or [""]
        print(f"{title: <{title_width}}  {year: <{year_width}}  {lines[0]}")
        for cont in lines[1:]:
            print(f"{'': <{title_width}}  {'': <{year_width}}  {cont}")
    while remaining:
        print_next = input_prompt("Type 'y' to print next 10 films or 'n' to go to menu: ")
        if print_next == 'y':
            print()
            print_films_table(remaining)
            break
        elif print_next == 'n':
            break


def print_genres_table(genres: list[str]):
    """
    Prints a formatted table of available genres in 3 columns.
    Sets column width automatically based on the longest genre name.
    """

    columns = 3
    col_width = max(len(genre) for genre in genres) + 4

    print("Available genres:\n" + "-" * (columns * col_width))

    for i, genre in enumerate(genres, start=1):
        print(f"{genre: <{col_width}}", end="")
        if i % columns == 0:
            print()
    if len(genres) % columns != 0:
        print()
    print("-" * (columns * col_width))


def get_criteria(query: dict) -> str:
    if query['search_type'] == 'keyword':
        result = query['params']['keyword']
    else:
        if query['params']['min_year'] and query['params']['max_year']:
            result = f"{query['params']['genre']}, {query['params']['min_year']}-{query['params']['max_year']}"
        else:
            result = f"{query['params']['genre']}"
    return result


def print_last_queries(queries: list[dict]):
    criteria_width = len('Criteria')
    type_width = 10
    films_width = 5
    for q in queries:
        criteria_width = max(criteria_width, len(get_criteria(q)))
    max(len(genre) for genre in queries) + 12
    print(f"{'Type': <{type_width}}  {'Criteria': <{criteria_width}}  {'Films': <{films_width}}")
    print("-" * (criteria_width + type_width + films_width + 4))
    for q in queries:
        print(f"{q['search_type']: <{type_width}}  {get_criteria(q): <{criteria_width}}  {q['results_count']: >{films_width}}")


def print_popular_queries(rows: list[dict]):
    criteria_col_width = len('Query')
    count_col_width = len('Count')
    type_col_width = len('keyword')

    for r in rows:
        criteria = r.get("_id")
        criteria_col_width = max(criteria_col_width, len(criteria))

    print(f"{'Query': <{criteria_col_width}}  {'Type': <{type_col_width}}  Count")
    print("-" * (criteria_col_width + count_col_width + type_col_width + 4))
    for r in rows:
        criteria = r.get("_id")
        cnt = r.get("count")
        search_type = r.get("type")
        print(f"{criteria: <{criteria_col_width}}  {search_type: <{type_col_width}}  {cnt: >{count_col_width}}")
