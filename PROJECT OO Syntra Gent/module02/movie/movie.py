
"""
Movie module for the Rotten Tomatoes data analysis.
Contains:
- Abstract Base Class Movie with common attributes and methods.
- Subclasses for each genre.
- Factory function create_movie() to instantiate the correct subclass.
"""

from abc import ABC
from dataclasses import dataclass, field
from datetime import date
from typing import Dict, List, Optional, Tuple, Type

from module02.movie.rating import MovieRating, get_rating
from module02.person.person import Person, get_person


@dataclass(slots=True)
class Movie(ABC):
    """
    Abstract base class for all movie types.
    This class contains attributes and methods common to all movies,
    regardless of genre. Each genre has its own subclass.
    
    attributes:
        rt_link: unique part of Rotten Tomatoes URL (required)
        title: full movie title (required)
        rating: content rating object (G, PG, R, etc.) (required)
        directors: list of Person objects who directed the film
        release_date: date of theatrical release (YYYY-MM-DD)
        streaming_date: date of streaming release (YYYY-MM-DD)
        length: runtime in minutes
        company: production company name
        score: audience rating (0-100)
        count: number of audience votes
    
    Examples:
            # movies are created via create_movie(), not directly
            movie = create_movie(csv_row_dict)
            print(movie.title)
            print(movie.url())
    """
    # required attributes (must not be empty)
    rt_link: str
    title: str
    rating: MovieRating
    # Optional attributes with defaults
    directors: List[Person] = field(default_factory=list)
    release_date: Optional[date] = None
    streaming_date: Optional[date] = None
    length: int = 0
    company: Optional[str] = None
    score: Optional[int] = None
    count: Optional[int] = None


    def __post_init__(self) -> None:
        """
        Validate the movie data after creation.
        Checks that required fields are not empty and that length is valid.
        raises:  ValueError: if rt_link, title, or rating is empty|None
        """
        if not self.rt_link:
            raise ValueError("rt_link must not be empty")
        if not self.title:
            raise ValueError("title must not be empty")
        if self.rating is None:
            raise ValueError("rating must not be None")
        if self.length is None or self.length < 0:
            self.length = 0


    def __str__(self) -> str:
        """
        Returns a readable string representation.
        return:  string with title, genre class name, and length
        
        Examples:  __str__.(movie)  >  Inception (Drama, 148 min)
        """
        return f"{self.title} ({self.__class__.__name__}, {self.length} min)"


    def relevant_score(self) -> Tuple[bool, int]:
        """
        Check if the movie has a relevant audience score.
        A score is relevant when:
        1.  score has been assigned (not None)
        2. At least 100 people voted
        return:  Tuple of (is_relevant, score_value)
            - if not relevant: (False, 0)
            - if relevant: (True, actual_score)
        
        Examples: - is_relevant, score = movie.relevant_score()
                           - if is_relevant:
                                  print(f"score: {score}%")
        """
        # Check if score and count exist
        if self.score is None or self.count is None:
            return False, 0
        # Check if enough people voted (at least 100)
        if self.count < 100:
            return False, 0
        
        return True, self.score


    def is_classic(self) -> bool:
        """
        Check if the movie is considered a classic.
        A movie is a classic when:
            1. It is at least 20 years old
            2. It has a relevant score of 80 or higher
        Returns:  True if the movie is a classic, False otherwise
        
        Examples:  if movie.is_classic():
                                 ...
                                 print("This is a classic film")
        """
        # Check if we have a release date
        if self.release_date is None:
            return False
        # Calculate age in years
        age = date.today().year - self.release_date.year
        # Must be at least 20 years old
        if age < 20:
            return False
        # Must have a relevant score of 80 or higher
        is_relevant, score = self.relevant_score()
        return is_relevant and score >= 80
        

    def is_short(self) -> bool:
        """
        Check if the movie is a short film.
        A movie is a short if it is shorter than 30 minutes.
        return:  True if length < 30 minutes, False otherwise
        
        Examples: - if movie.is_short():
                                   ...
                                   print("This is a short film")
        """
        return self.length < 30


    def url(self) -> str:
        """
        Get the full Rotten Tomatoes URL for this movie.
        return:   complete URL string
        
        Examples: -  movie.url()  >  'https://www.rottentomatoes.com/m/inception'
        """
        return "https://www.rottentomatoes.com/" + self.rt_link

# ==============================================
# Genre-specific subclasses
# Each genre is a subclass of Movie with potential additional methods
# ==============================================

@dataclass(slots=True)
class ActionAdventure(Movie):
    """Action & Adventure genre movies"""
    pass


@dataclass(slots=True)
class Comedy(Movie):
    """
    Comedy genrereturn movies.
    Additional methods:  is_slapstick(): check if this is slapstick comedy (low score)
    """
    def is_slapstick(self) -> bool:
        """
        Check if this comedy is slapstick style.
        A comedy is considered slapstick if it has a relevant score
        below 40 (indicating broad, physical humor that critics
        don't appreciate but audiences might enjoy).
        return:  True if relevant score < 40, False otherwise
        """
        is_relevant, score = self.relevant_score()
        return is_relevant and score < 40


@dataclass(slots=True)
class Drama(Movie):
    """Drama genre movies."""
    pass


@dataclass(slots=True)
class Horror(Movie):
    """
    Horror genre movies.
    Additional methods:  is_scary(): check if this horror movie is considered scary
    """
    def is_scary(self) -> bool:
        """
        Check if this horror movie is scary.
        A horror movie is considered scary if its content rating
        is higher than PG (i.e., PG-13, R, or NC17).
        return:  True if rating > PG, False otherwise
        """
        pg = get_rating("PG")  # gives MovieRating object
        return self.rating > pg


@dataclass(slots=True)
class Romance(Movie):
    """
    Romance genre movies.
    Additional methods:  is_cosy(): check if this is a cosy romance (comfortable length)
    """
    def is_cosy(self) -> bool:
        """
        Check if this romance is cosy.
        A romance is considered cosy if it has a comfortable length
        between 70 and 100 minutes (not too short, not too long).
        return:  True if 70 <= length <= 100, False otherwise
        """
        return 70 <= self.length <= 100


@dataclass(slots=True)
class ScienceFictionFantasy(Movie):
    """Science Fiction & Fantasy genre movies."""
    pass


@dataclass(slots=True)
class Western(Movie):
    """Western genre movies."""
    pass

# ========================================
# Factory function and helper functions
# ========================================

# Mapping from CSV genre text to Movie subclass
_GENRE_TO_CLASS: Dict[str, Type[Movie]] = {
    "ACTION & ADVENTURE": ActionAdventure,
    "COMEDY": Comedy,
    "DRAMA": Drama,
    "HORROR": Horror,
    "ROMANCE": Romance,
    "SCIENCE FICTION & FANTASY": ScienceFictionFantasy,
    "WESTERN": Western,
}


def _parse_int(value: str) -> Optional[int]:
    """
    Parse a string to an integer, returning None if invalid or empty.
    value:  string to parse
    return:  integer value or None if parsing fails
    
    Example:    >   _parse_int("123")  >  123
                        >   _parse_int("")  >  None
                        >   _parse_int("abc")  >  None
    """
    if value is None:
        return None
    value = value.strip()
    if not value:
        return None
    try:
        return int(value)
    except ValueError:
        return None


def _parse_date(value: str) -> Optional[date]:
    """
    Parse a string to a date object, returning None if invalid or empty.
    Expected format: YYYY-MM-DD (ISO format)
    value:   string to parse
    return:   date object or None if parsing fails
    
    Examples:  >  _parse_date("2020-01-15")  >  datetime.date(2020, 1, 15)
                        >  _parse_date("")  >   None
    """
    if value is None:
        return None
    value = value.strip()
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def _parse_directors(value: str) -> List[Person]:
    """
    Parse a comma-separated string of director names into Person objects.
    Handles both simple cases and cases with multiple directors.
    Uses get_person() to ensure the Flyweight pattern is maintained.
    value:   comma-separated director names
    return:  List of Person objects (empty list if no directors)
    
    Examples:   >   directors = _parse_directors("Matt Groening, Hugo Claus")
                         >   len(directors)   >   2
    """
    if value is None:
        return []
    text = value.strip()
    if not text:
        return []
    # Split by comma and clean each name
    parts = [p.strip() for p in text.split(",")]
    # Create Person objects for non-empty names
    return [get_person(name) for name in parts if name]


def create_movie(info: Dict[str, str]) -> Movie:
    """
    Factory function to create a Movie object from CSV data.
    This function reads a dictionary (from csv.DictReader) and creates
    the appropriate Movie subclass based on the genre field.
    info:  dictionary with keys matching CSV column names
    return:  a Movie subclass instance (Comedy, Drama, Horror, etc.)
    raises:  ValueError:  if required fields are missing or genre is unknown
    
    Examples:  >  row = {'movie_title': 'Inception', 'genre': 'DRAMA', ...}
                        >  movie = create_movie(row)
                        >  isinstance(movie, Drama)  >  True
    """
    # extract and validate required fields
    rt_link = (info.get("rotten_tomatoes_link") or "").strip()
    title = (info.get("movie_title") or "").strip()
    rating_code = (info.get("content_rating") or "").strip()
    genre_text = (info.get("genre") or "").strip()

    # check that required fields are present 
    if not rt_link:
        raise ValueError("missing rotten_tomatoes_link")
    if not title:
        raise ValueError("missing movie_title")
    if not rating_code:
        raise ValueError("missing content_rating")
    if not genre_text:
        raise ValueError("missing genre")

    # convert rating code to MovieRating object
    rating = get_rating(rating_code)

    # parse directors into Person objects
    directors = _parse_directors(info.get("directors", ""))

    # parse optional date fields
    release_date = _parse_date(info.get("original_release_date", ""))
    streaming_date = _parse_date(info.get("streaming_release_date", ""))

    # parse optional numeric and text fields
    length = _parse_int(info.get("runtime", "")) or 0
    company = (info.get("production_company") or "").strip() or None
    score = _parse_int(info.get("audience_rating", ""))
    count = _parse_int(info.get("audience_count", ""))

    # determine the correct Movie subclass based on genre
    genre_upper = genre_text.upper()
    cls = _GENRE_TO_CLASS.get(genre_upper)
    
    if cls is None:
        raise ValueError(f"unknown genre: {genre_text}")

    # create and return the appropriate Movie subclass instance
    return cls(
        rt_link=rt_link,
        title=title,
        rating=rating,
        directors=directors,
        release_date=release_date,
        streaming_date=streaming_date,
        length=length,
        company=company,
        score=score,
        count=count,
    )

