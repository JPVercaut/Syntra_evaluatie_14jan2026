"""
Main module for the Rotten Tomatoes movie data analysis.
This module loads movie data from a CSV file and presents a menu-driven
interface for analyzing the data in various ways.
"""

# Python standard library imports
import csv
import os
from typing import Dict, List

# Custom module imports
from module02.movie.movie import Movie, create_movie, Horror
from module02.person.person import get_person_count

# File paths - CHANGE THESE to match the present environment
# Using relative paths -> the program works on any computer
# MOVIE_FILE = "reviews.csv"
# EXPORT_FILE = "export.csv"
BASE_DIR = os.path.dirname(__file__)
MOVIE_FILE = os.path.join(BASE_DIR, "reviews.csv")
EXPORT_FILE = os.path.join(BASE_DIR, "export.csv")


def load_movies(file_location: str) -> List[Movie] | None:
    """
    Load all movies from a CSV file into a list of Movie objects.
    This function reads the CSV file line by line and creates the
    appropriate Movie subclass (Drama, Comedy, Horror, etc.) for each row.
        
    :file_location: path to the CSV file
    :return:  list of Movie objects, or None if an error occurred
    :raises:  FileNotFoundError: file can not be found
    """
    # check if file exists
    if not os.path.exists(file_location):
        raise FileNotFoundError(f"File not found: {file_location}")
    
    try:
        errors = 0
        movies = []  # movies: List[Movie] = []
        
        # open and read the CSV file
        with open(file_location, "r", encoding="UTF-8") as file:
            reader = csv.DictReader(file, delimiter=",")
            
            # process each row
            for i, row in enumerate(reader):
                try:
                    # create the appropriate Movie subclass
                    movie = create_movie(row)
                    movies.append(movie)
                except ValueError as e:
                    # log errors but continue processing
                    errors += 1
                    print(f"Problem with line {i} : '{e}' => {row}")
        
        # report total errors if any
        if errors:
            print(f"{errors} films cannot be loaded")
            
    except Exception as e:
        # catch any other errors during file reading
        print(f"Problem reading file: {file_location} => {e}")
        return None
    
    return movies

# ============================================================================
# Menu Functions
# Each function implements one menu option
# All functions take a List[Movie] parameter as required
# ============================================================================

def menu_print_movie_count(movies: List[Movie]) -> None:
    """
    Menu option 1: print the number of films.
    :movies: list of all loaded movies
    """
    print(f"\n number of films: {len(movies)}\n")


def menu_print_genre_counts(movies: List[Movie]) -> None:
    """
    Menu option 2: print films by genre.
    Shows a list of genres and their occurrences, sorted by number
    (most common first).
    :movies: list of all loaded movies
    
    Examples output:
        ActionAdventure : 200
        Comedy : 150
        Drama : 100
    """
    # count movies by genre using class name
    counts: Dict[str, int] = {}
    
    for movie in movies:
        # get the class name (e.g., "Comedy", "Drama")
        genre_name = movie.__class__.__name__
        counts[genre_name] = counts.get(genre_name, 0) + 1
    
    # sort by count descending, then by name for ties
    sorted_items = sorted(
        counts.items(),
        key=lambda item: (-item[1], item[0])
    )
    
    # print the results
    print()
    for genre_name, count in sorted_items:
        print(f"{genre_name} : {count}")
    print()


def menu_print_person_count(movies: List[Movie]) -> None:
    """
    Menu option 3: Number of persons.
    Print how many Person objects have been created.
    Note: this function uses get_person_count() instead of
    movies parameter (kept for consistent interface)
    :movies: list of all loaded movies (not used directly)
    """
    count = get_person_count()
    print(f"\n number of Person objects created: {count}\n")


def menu_print_highest_score_movies(movies: List[Movie]) -> None:
    """
    Menu option 4: highest score.
    Print the film(s) with the highest relevant score.
    A score is relevant if the movie has at least 100 votes.
    :movies: list of all loaded movies
    """
    max_score = -1
    best_movies: List[Movie] = []
    
    # find the highest relevant score
    for movie in movies:
        is_relevant, score_value = movie.relevant_score()
        
        # skip movies without relevant scores
        if not is_relevant:
            continue
        
        # check if this is a new highest score
        if score_value > max_score:
            max_score = score_value
            best_movies = [movie]
        elif score_value == max_score:
            best_movies.append(movie)
    
    # display result
    if not best_movies:
        print("\n no movies with a relevant score were found.\n")
        return
    
    print(f"\n highest relevant score: {max_score}")
    print(" movies with this score:")
    for movie in best_movies:
        print(f"  - {movie.title}")
    print()


def menu_print_most_active_director(movies: List[Movie]) -> None:
    """
    Menu option 5: most active director.
    Print the director(s) who directed the most films.
    :movies: list of all loaded movies
    """
    from module02.person.person import Person
    
    # count films per director
    director_counts: Dict[Person, int] = {}
    
    for movie in movies:
        for director in movie.directors:
            director_counts[director] = director_counts.get(director, 0) + 1
    
    # handle case where no directors exist
    if not director_counts:
        print("\n no directors found in the dataset.\n")
        return
    
    # find the maximum count
    max_count = max(director_counts.values())
    
    # get all directors with the maximum count
    most_active = [
        person for person, count in director_counts.items()
        if count == max_count ]
    
    # display result
    print(f"\n most active director(s) with {max_count} film(s):")
    for director in most_active:
        print(f"  - {director.fullname}")
    print()


def menu_print_shortest_and_longest(movies: List[Movie]) -> None:
    """
    Menu option 6: shortest and longest film.
    Print the shortest and longest film(s) by runtime.
    :movies: list of all loaded movies
    """
    if not movies:
        print("\n no movies loaded.\n")
        return
    
    # find minimum and maximum length
    min_length = min(movie.length for movie in movies)
    max_length = max(movie.length for movie in movies)
    
    # get all movies with these lengths
    shortest = [movie for movie in movies if movie.length == min_length]
    longest = [movie for movie in movies if movie.length == max_length]
    
    # display result
    print(f"\n films with shortest length: {min_length} minutes")
    for movie in shortest:
        print(f"  - {movie.title}")
    
    print(f"\n films with longest length: {max_length} minutes")
    for movie in longest:
        print(f"  - {movie.title}")
    print()


def menu_print_scary_horror(movies: List[Movie]) -> None:
    """
    Menu option 7: scary horror.
    Print all horror movies where is_scary() returns True.
    A horror movie is scary if its rating is higher than PG.
    :movies: list of all loaded movies
    """
    # filter for scary horror movies
    scary_movies: List[Movie] = []
    
    for movie in movies:
        if isinstance(movie, Horror) and movie.is_scary():
            scary_movies.append(movie)
    
    # display result
    if not scary_movies:
        print("\n no scary horror movies found.\n")
        return
    
    print("\n scary horror movies:")
    for movie in scary_movies:
        print(f"  - {movie.title} (Rating: {movie.rating.code})")
    print()


def menu_print_score_list(movies: List[Movie]) -> None:
    """
    Menu option 8: score list.
    Print all scores from 0 to 100 and how many movies have each score.
    :movies: list of all loaded movies
    
    Example output:
        0%: 2
        1%: 0
        2%: 3
        ...
    """
    # initialize counts for all possible scores
    score_counts: Dict[int, int] = {i: 0 for i in range(0, 101)}
    
    # count movies for each score
    for movie in movies:
        if movie.score is not None and 0 <= movie.score <= 100:
            score_counts[movie.score] += 1
    
    # print all scores
    print()
    for score_value in range(0, 101):
        count = score_counts[score_value]
        print(f"{score_value}%: {count}")
    print()

# ---------------------------------------------------------------------

def menu_export_movies_without_relevant_score(movies: List[Movie]) -> None:
    """
    Menu option 9: Export.
    Create a CSV file containing film information for films without
    a relevant score, sorted alphabetically by title.
    A score is not relevant if:
    - the movie has no score, or
    - the movie has fewer than 100 votes
    :movies: list of all loaded movies
    """
    # filter movies without relevant scores
    movies_without_relevant = [
        movie for movie in movies
        if not movie.relevant_score()[0]   ]
        # not relevant_score() > tuple(False, 0)
        
    # check if there's anything to export
    if not movies_without_relevant:
        print("\n all movies have a relevant score; nothing to export.\n")
        return
    
    # sort alphabetically by title
    movies_without_relevant.sort(key=lambda m: m.title)
    
    # define CSV field names (same as input file column headers)
    fieldnames = [
        "rotten_tomatoes_link",
        "movie_title",
        "content_rating",
        "genre",
        "directors",
        "original_release_date",
        "streaming_release_date",
        "runtime",
        "production_company",
        "audience_rating",
        "audience_count",
    ]
    
    try:
        # write to csv-file
        with open(EXPORT_FILE, "w", newline="", encoding="UTF-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            
            # write each movie as a row
            for movie in movies_without_relevant:
                # reconstruct directors as comma-separated string
                directors_text = ", ".join(
                    director.fullname for director in movie.directors
                )
                
                # build the row dictionary
                row = {
                    "rotten_tomatoes_link": movie.rt_link,
                    "movie_title": movie.title,
                    "content_rating": movie.rating.code,
                    "genre": movie.__class__.__name__,
                    "directors": directors_text,
                    "original_release_date": (
                        movie.release_date.isoformat()
                        if movie.release_date is not None
                        else ""
                    ),
                    "streaming_release_date": (
                        movie.streaming_date.isoformat()
                        if movie.streaming_date is not None
                        else ""
                    ),
                    "runtime": movie.length,
                    "production_company": movie.company or "",
                    "audience_rating": (
                        movie.score if movie.score is not None else ""
                    ),
                    "audience_count": (
                        movie.count if movie.count is not None else ""
                    ),
                }
                writer.writerow(row)
        
        print(f"\n exported {len(movies_without_relevant)} movies to {EXPORT_FILE}\n")
        
    except Exception as exc:
        print(f"\n errors while exporting to {EXPORT_FILE}: {exc}\n")


# ============================================================================
# Menu Display and User Input
# ============================================================================


def print_menu() -> None:
    """
    Display the menu options to the user.
    """
    # print("\n " + "="*49)
    print()
    print('=' * 50)
    print("ROTTEN TOMATOES MOVIE DATA ANALYSIS TOOL")
    print("="*50)
    print("1) Print the number of films")
    print("2) Print films by genre")
    print("3) Number of persons (Person objects)")
    print("4) Highest score")
    print("5) Most active directors")
    print("6) Shortest and longest films")
    print("7) All Scary Horror fims")
    print("8) Score list (0-100) & their numbers")
    print("9) Export films without a relevant score")
    print("10) Stop")
    print("="*50)


def get_menu_choice() -> int:
    """
    Get a valid menu choice from the user.
    Keeps asking until a valid number (1-10) is entered.
    Handles invalid input.
    :return:  integer between 1 and 10
    """
    while True:
        choice_text = input("\n choose an option (1-10): ").strip()
                
        # try to convert to integer
        try:
            choice = int(choice_text)
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 10.")
            continue
        
        # check if in valid range
        if 1 <= choice <= 10:
            print(f" input: {choice} \n")
            return choice
        
        print("Invalid choice. Please enter a number between 1 and 10.")


# ==============================================
# Main Program
# ==============================================


def main() -> None:
    """
    Main function: Load movies and present menu until user chooses to stop.
    This function:
    1. Loads movies from the CSV file
    2. Displays a menu
    3. Executes the chosen menu option
    4. Repeats until the user chooses to stop (option 10)
    """

    print("\n" + "="*50)
    print("loading movies from", MOVIE_FILE)
    print("="*50)
    
    # Load the movie data
    try:
        movies = load_movies(MOVIE_FILE)
    except FileNotFoundError as exc:
        print(f"\n Error: {exc}")
        print("please make sure the reviews.csv file is in the same folder")
        print("as this program, or update the MOVIE_FILE constant.\n")
        return
    
    # Check if loading was successful
    if movies is None:
        print("\n could not load movies. Exiting.\n")
        return
    
    print(f"successfully loaded {len(movies)} movies.")
    
    # Main menu loop
    while True:
        print_menu()
        choice = get_menu_choice()
        
        # Execute the chosen menu option
        if choice == 1:
            menu_print_movie_count(movies)
        elif choice == 2:
            menu_print_genre_counts(movies)
        elif choice == 3:
            menu_print_person_count(movies)
        elif choice == 4:
            menu_print_highest_score_movies(movies)
        elif choice == 5:
            menu_print_most_active_director(movies)
        elif choice == 6:
            menu_print_shortest_and_longest(movies)
        elif choice == 7:
            menu_print_scary_horror(movies)
        elif choice == 8:
            menu_print_score_list(movies)
        elif choice == 9:
            menu_export_movies_without_relevant_score(movies)
        elif choice == 10:
            print("\n" + "="*50)
            print("you are ending the Movie Data Analysis ")
            print("see you soon next time")
            print("="*50 + "\n")
            break


# Program entry point
if __name__ == "__main__":
    main()
