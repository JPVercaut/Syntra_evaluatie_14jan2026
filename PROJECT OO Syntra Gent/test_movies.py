"""
Part of the module02 test

Deze tests controleren of de implementatie van de gevraagde klassen en objecten goed werkt.
Voer deze test uit ter controle
"""
import datetime
import unittest

from module02.movie.movie import Movie, create_movie, Comedy, Horror, Romance
from module02.movie.rating import MovieRating, get_rating
from module02.person.person import Person, get_person

EXISTING_RATINGS = ["G", "PG", "PG-13", "R", "NR", "NC17"]
NAME = "Claassen Arvid"

GENRES = (
    "ACTION & ADVENTURE",
    "COMEDY",
    "DRAMA",
    "HORROR",
    "ROMANCE",
    "SCIENCE FICTION & FANTASY",
    "WESTERN",
)

PERSON = Person(NAME)

MOVIE_INFO = {
    "rotten_tomatoes_link": "m/1000640-all_of_me",
    "movie_title": "All of Me",
    "content_rating": "PG",
    "genre": "COMEDY",
    "directors": "Carl Reiner",
    "original_release_date": "1984-09-21",
    "streaming_release_date": "2016-10-30",
    "runtime": "93",
    "production_company": "HBO Video",
    "audience_rating": "67",
    "audience_count": "14346"
}


class MyTestCase(unittest.TestCase):
    def test_movie_creation(self):
        # for movie_type in Movie.__subclasses__():
        #     movie = movie_type()
        #     self.assertEqual(movie.genre_name(), movie_type.genre_name())

        # self.assertEqual(True, False)  # add assertion here
        pass

    def test_movie_attributes(self):
        # test of na creatie de attributen van het juiste type zijn
        m = create_movie(MOVIE_INFO)
        self.assertIsInstance(m, Movie)
        self.assertIsInstance(m, Comedy)
        self.assertIsInstance(m.rt_link, str)
        self.assertIsInstance(m.title, str)
        self.assertIsInstance(m.rating, MovieRating),
        self.assertIsInstance(m.directors, list),
        self.assertIsInstance(m.directors[0], Person),
        self.assertIsInstance(m.release_date, datetime.date),
        self.assertIsInstance(m.streaming_date, datetime.date)
        self.assertIsInstance(m.length, int)
        self.assertIsInstance(m.company, str)
        self.assertIsInstance(m.score, int)
        self.assertIsInstance(m.count, int)

    def test_empty(self):
        # test of na er voldoende gecontroleerd wordt dat specifieke attributen niet leeg mogen zijn
        for key in MOVIE_INFO:
            info_copy = MOVIE_INFO.copy()
            info_copy[key] = ""
            if key in ["rotten_tomatoes_link", "movie_title", "content_rating", "genre"]:
                with self.assertRaises(ValueError):
                    create_movie(info_copy)
            else:
                create_movie(info_copy)

        m = create_movie(MOVIE_INFO)
        self.assertIsInstance(m, Movie)
        self.assertIsInstance(m, Comedy)
        self.assertIsInstance(m.rt_link, str)
        self.assertIsInstance(m.title, str)
        self.assertIsInstance(m.rating, MovieRating),
        self.assertIsInstance(m.directors, list),
        self.assertIsInstance(m.directors[0], Person),
        self.assertIsInstance(m.release_date, datetime.date),
        self.assertIsInstance(m.streaming_date, datetime.date)
        self.assertIsInstance(m.length, int)
        self.assertIsInstance(m.company, str)
        self.assertIsInstance(m.score, int)
        self.assertIsInstance(m.count, int)

    def test_subclass_methods(self):
        checks = ((Comedy, "is_slapstick"),
                  (Romance, "is_cosy"),
                  (Horror, "is_scary"))

        info_copy = MOVIE_INFO.copy()
        for genre in GENRES:
            info_copy["genre"] = genre
            m = create_movie(info_copy)
            for check in checks:
                class_, f_name = check
                if isinstance(m, class_):
                    self.assertTrue(hasattr(m, f_name) and callable(getattr(m, f_name)),
                                    f"class {class_} mist methode {f_name}")
                else:
                    self.assertFalse(hasattr(m, f_name),
                                     f"class {class_} mag methode {f_name} niet hebben.")


class PersonTestCase(unittest.TestCase):
    def test_person_creation(self):
        # Controleer dat de de naam correct wordt overgenomen bij creatie
        self.assertEqual(PERSON.fullname, NAME)

    def test_get_person_existing(self):
        # We hebben al een Person aangemaakt met de naam NAME
        # We controleren of get_person geen nieuw object aanmaakt,
        # maar de bestaande teruggeeft
        person = get_person(NAME)
        self.assertEqual(person.fullname, NAME)
        self.assertEqual(person, PERSON)
        self.assertEqual(id(person), id(PERSON))

        # We maken een Person aan met een bestaande naam, maar dan in hoofdletters
        # We controleren of get_person geen nieuw object aanmaakt,
        # maar de bestaande teruggeeft
        person = get_person(NAME.upper())
        self.assertEqual(person, PERSON)
        self.assertEqual(id(person), id(PERSON))

        # We maken een Person aan met een bestaande naam, maar dan in kleine letters
        # We controleren of get_person geen nieuw object aanmaakt,
        # maar de bestaande teruggeeft
        person = get_person(NAME.lower())
        self.assertEqual(person, PERSON)
        self.assertEqual(id(person), id(PERSON))

        with self.assertRaises(ValueError):
            Person(NAME)

    def test_get_person_non_existing(self):
        # Maak een nog niet bestaande Person aan
        p2 = Person("Arvid Claassen")
        self.assertNotEqual(PERSON, p2)
        self.assertNotEqual(id(PERSON), id(p2))

    def test_person(self):
        # Controleer dat de class persoon bijhoudt hoeveel personen er reeds gemaakt zijn.
        p1 = get_person("Arvid Claassen")
        p2 = get_person(NAME)
        self.assertGreaterEqual(Person.get_person_count(), 2)


class RatingTestCase(unittest.TestCase):
    def test_ratings_constant(self):
        expected = {"G", "PG", "PG-13", "R", "NR", "NC17"}
        self.assertEqual(expected, set(EXISTING_RATINGS))

    def test_create_wrong_attributes(self):
        # Test dat er geen rating wordt aangemaakt met een lege code of beschrijving
        with self.assertRaises(ValueError):
            MovieRating(code="", description="Some description")
        with self.assertRaises(ValueError):
            MovieRating(code="A", description="")
        with self.assertRaises(ValueError):
            MovieRating(code="", description="")

    def test_create_existing(self):
        # Controleer dat de voorgeschreven ratings reeds bestaan
        for rating in EXISTING_RATINGS:
            with self.assertRaises(Exception):
                MovieRating(code=rating, description="Some description")
        self.assertNotEqual(get_rating("G"), get_rating("PG"))
        self.assertNotEqual(get_rating("G").description, get_rating("PG").description)

    def test_rating_comparison(self):
        # controleer daar NR de laagste rating is en NC17 de hoogste
        ratings = [get_rating(rating) for rating in EXISTING_RATINGS]
        max_rating = get_rating("NC17")
        min_rating = get_rating("NR")
        for rating in ratings:
            if rating != max_rating:
                self.assertLess(rating, max_rating, f"{rating} moet kleiner zijn dan {max_rating}")
            if rating != min_rating:
                self.assertGreater(rating, min_rating, f"{rating} moet groter zijn dan {min_rating}")

    def test_create_non_existing(self):
        # Test dat er geen twee ratings met dezelfde code kunnen worden aangemaakt
        new_code = "PG28"
        rating = MovieRating(new_code, "Nieuwe code")
        self.assertEqual(rating.code, new_code)
        self.assertEqual(rating.description, "Nieuwe code")
        with self.assertRaises(Exception):
            MovieRating(code=new_code, description="Some description")

    def test_repr(self):
        # Test dat de representatie goed is.
        for rating in EXISTING_RATINGS:
            expected = f"Rating({rating})"
            rep = repr(get_rating(rating))
            self.assertEqual(rep, expected)


if __name__ == '__main__':
    unittest.main()
