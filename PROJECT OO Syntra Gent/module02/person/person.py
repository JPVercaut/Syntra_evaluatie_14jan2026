"""
Person module for the Rotten Tomatoes data analysis.
This module contains the Person class which represents directors and
implements a cache/Flyweight pattern to implement one instance of the
Person object per unique name (case-insensitive).
"""

from dataclasses import dataclass
from typing import ClassVar, Dict


@dataclass(frozen=True, slots=True)
class Person:
    """
    Represents a person; typically a movie director.
    Uses the Flyweight pattern: only one Person object exists  per unique name.
    Person objects are immutable (frozen=True) and names are case-insensitive.
    attributes:
        fullname:  Person's full name 
    class variables:
        _instances: cache of all created Person objects (Flyweight pattern)
                   keys are lowercase names, values are Person objects
    
    Examples: - director = get_person("Matt Groening")
                    - print(director)  # Person(Matt Groening)
                    - director.fullname  # "Matt Groening"
    """
    
    fullname: str
    
    # class-level cache for the Flyweight pattern
    # key: lowercase name, value: Person object
    _instances: ClassVar[Dict[str, "Person"]] = {}

    
    def __post_init__(self) -> None:
        """
        Validate the Person after creation.
        This method runs automatically after __init__.
        It checks that fullname is not empty and
        no duplicate Persons are created (case-insensitive).
        raises:  ValueError: if fullname is empty or if a person with this
                       name already exists (case-insensitive)
        """
        # validate that fullname is not empty
        if not self.fullname:
            raise ValueError("fullname can not be empty")
        
        # create a normalized key (lowercase, trimmed)
        key = self.fullname.strip().lower()
        
        # prevent duplicate creation (Flyweight pattern enforcement)
        if key in Person._instances:
            raise ValueError(
                f"Person '{self.fullname}' already exists. "
                f"Use get_person() instead."
            )
        # add this instance to the cache
        Person._instances[key] = self
    
    def __repr__(self) -> str:
        """
        Returns the string representation.
        return:  string in format "Person(fullname)"
        Example:  representation[(get_person("Matt Groening"))] > 
                                                                        'Person(Matt Groening)'
        """
        return f"Person({self.fullname})"
    
    def __eq__(self, other: object) -> bool:
        """
        Check if two persons are equal (same name, case-insensitive).
        other:  other Person object
        return:  True if both persons have the same name (ignoring case)
        
        Example:    - p1 = get_person("John Doe")
                            - p2 = get_person("john doe")  # Same person!
                            - p1 == p2   > True
        """
        if not isinstance(other, Person):
            return NotImplemented
        return self.fullname.lower() == other.fullname.lower()

# ----------------------------------------------------------------------
    def __hash__(self) -> int:
        """
        Returns hash value for use in sets and dictionaries.
        Uses lowercase name for consistent hashing regardless of case.
        return:  hash of the lowercase fullname
        """
        return hash(self.fullname.lower())


def get_person(fullname: str) -> Person:
    """
    Gets an existing person or create a new one.
    Is the main function when using a Person object.
    It implements the Flyweight pattern: returns existing persons instead
    of creating duplicates. Name matching is case-insensitive.
    
    :fullname:  Person's full name (e.g., "Matt Groening")
                  case-insensitive >  will be normalized
    :return:  Person object for this name (existing or newly created)
    :raises:  ValueError: if fullname is None or empty (after stripping)
    
    Example:    - director1 = get_person("Matt Groening")
                        - director2 = get_person("MATT GROENING")  # Same person!
                        - director1 is director2  # True (same object in memory) 
    """
   
    # validate input
    if fullname is None:
        raise ValueError("fullname can not be None")
    
    # clean the input: remove leading/trailing whitespace
    cleaned = fullname.strip()
    
    # validate that cleaned name is not empty
    if not cleaned:
        raise ValueError("fullname can not be empty")
    
    # create a normalized key for lookup (lowercase)
    key = cleaned.lower()
    
    # check if this person already exists (Flyweight pattern)
    if key in Person._instances:
        return Person._instances[key]
    
    # Person doesn't exist yet, then create a new one
    # Person.__post_init__ will add it to _instances
    
    return Person(fullname=cleaned)


def get_person_count() -> int:
    """
    Gets the total number of created Person objects.
    :return:  count of unique Person objects in the cache
    
    Example:    - get_person("Director A")
                        - get_person("Director B")
                        - get_person("Director A")  # Same as first, no new object
                        - get_person_count()   >>> 2
    """
    return len(Person._instances)

