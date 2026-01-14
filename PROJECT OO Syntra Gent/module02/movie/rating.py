"""
Movie rating module for the Rotten Tomatoes data analysis.
This module contains the MovieRating class which represents
content ratings (G, PG, PG-13, R, NC17, NR) and implements
a Flyweight pattern to implement one instance per rating code.
"""

from dataclasses import dataclass
from typing import ClassVar, Dict


@dataclass(frozen=True, slots=True)
class MovieRating:
    """
    Represents a content rating for a movie.
    Uses the Flyweight pattern: only one MovieRating object exists
    per code.
    Rating objects are immutable (frozen=True) and comparable.
    attributes:
        code: short rating code (G, PG, PG-13, R, NC17, NR)
        description: text description of the rating
    class variables:
        _instances: cache of all created rating objects (Flyweight pattern)
        _order: Defines the sorting order of ratings
                      (NR is lowest, NC17 is highest)
    Examples: - rating = get_rating("PG")
        - print(rating)  # Rating(PG)
        - rating.description  # "parental guidance advised"
    """ 
    
    code: str
    description: str
    
    # class-level cache for the Flyweight pattern
    _instances: ClassVar[Dict[str, "MovieRating"]] = {}
    
    # order of ratings from lowest (NR) to highest (NC17)
    _order: ClassVar[list[str]] = ["NR", "G", "PG", "PG-13", "R", "NC17"]
    
    def __post_init__(self) -> None:
        """
        Validate the rating after creation.
        This method runs automatically after __init__.
        It checks that code and description are not empty and that
        no duplicate ratings are created.
        Raises: isinstance ValueError: if code or description is empty, if code is
                        unknown, or if a rating with this code already exists
        """
        # validate that code is not empty
        if not self.code:
            raise ValueError("rating code can not be empty")
        
        # validate that description is not empty
        if not self.description:
            raise ValueError("rating description can not be empty")
        
        # normalize the code to uppercase for consistency
        normalized = self.code.upper()
        
        # check if this is a valid rating code
        if normalized not in MovieRating._order:
            raise ValueError(f"unknown rating code: {normalized}")
        
        # prevent duplicate creation (Flyweight pattern enforcement)
        if normalized in MovieRating._instances:
            raise ValueError(
                f"Rating '{normalized}' already exists. Use get_rating() instead."
            )
        # add this instance to the cache
        MovieRating._instances[normalized] = self
    
    def __repr__(self) -> str:
        """
        Returns the string representation.
        return:  string in format "Rating(CODE)"
        Example:  representation[(get_rating("PG"))] > 'rating(PG)'
        """
        return f"Rating({self.code})"
    
    def _sort_index(self) -> int:
        """
        Get the sort position of this rating.
        return:  integer index in the _order list (0 for NR, 5 for NC17)
        """
        return self._order.index(self.code.upper())
    
    def __lt__(self, other: object) -> bool:
        """
        Compare if this rating is less than another.
        other: other MovieRating object
        return:  True if self rating is lower than the other rating
        Example:  get_rating("PG") < get_rating("R")  >  True
        """
        if not isinstance(other, MovieRating):
            return NotImplemented
        return self._sort_index() < other._sort_index()
    
    def __eq__(self, other: object) -> bool:
        """
        Check if two ratings are equal (same code).
        other: other MovieRating object
        return:  True if both ratings have the same code
        """
        if not isinstance(other, MovieRating):
            return NotImplemented
        return self.code.upper() == other.code.upper()
    
    def __hash__(self) -> int:
        """
        Return hash value for use in sets and dictionaries.
        return:  hash of the uppercase code
        """
        return hash(self.code.upper())


def _create_predefined_ratings() -> None:
    """rating
    Creates the six predefined rating objects.
    This function is called when the module is loaded > see l.179.
    The ratings created are:
    - NR: Not rated
    - G: All ages
    - PG: Parental guidance advised
    - PG-13: Parental guidance strongly advised
    - R: Under 17, parental guidance advised
    - NC17: For adults only
    """
    descriptions = {
        "NR": "Not rated",
        "G": "All ages",
        "PG": "Parental guidance advised",
        "PG-13": "Parental guidance strongly advised",
        "R": "Under 17, parental guidance advised",
        "NC17": "For adults only",
    }
    
    # create each rating if it doesn't exist yet
    for code, desc in descriptions.items():
        if code not in MovieRating._instances:
            MovieRating(code=code, description=desc)


def get_rating(code: str) -> MovieRating:
    """
    Gets or create a rating object for the given code.
    Is the main function when using a MovieRating object.
    It implements the Flyweight pattern: returns existing ratings
    instead of creating duplicates.
    
    code: Rating code (e.g., "PG", "R", "NC17")
             case-insensitive > normalized to uppercase
    return:  the MovieRating object for this code
    raises:  ValueError: if code is None, empty, or not a valid rating code

    Example:   - rating = get_rating("pg")
                       - print(rating)  # Rating(PG)
                       - rating.description  # "parental guidance advised"
    """
    # validate input
    if code is None:
        raise ValueError("rating code cannot be None")
    
    # normalize the code: strip whitespace and convert to uppercase
    normalized = code.strip().upper()
    
    # handle the special case of "PG-13" (with hyphen)
    # if normalized == "PG-13":
    #    normalized = "PG13"
    
    # check if this rating exists in the cache
    if normalized not in MovieRating._instances:
        raise ValueError(f"Unknown rating code: {normalized}")
    
    # return the cached instance (Flyweight pattern)
    return MovieRating._instances[normalized]


# create all predefined ratings when the module is imported
_create_predefined_ratings()

