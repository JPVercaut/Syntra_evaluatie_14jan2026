"""
zoek alle films die bunnen de 18 maanden na de original_release_date
op de streaming_release_date beschikbaar is.
:streaming_date: in de Movie classs de streaming_release_date van de cvs-file
:release_date: in de Movie class de original_release_date van de csv-file.
"""
from datetime import datetime, timedelta

def early_release_date(movies: List[Movie]) -> None:
    for movie in movies:
        a_date = fromisoformat(movie.release_date)
        b_date = fromisoformat(movie.streaming_date)
_
