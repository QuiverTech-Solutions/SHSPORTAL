"""Base Repository."""

# Third party imports


from datetime import datetime, timedelta

from databases import Database
from dateutil import relativedelta
from src.enums.time_filters import TimeFilter


class BaseRepository:
    """Base class for Postgres repositories."""

    def __init__(self, db: Database) -> None:
        """Initialize with Postgres database instance.

        Args:
            db (Database): An instance of the Database database.
        """
        self.db = db


def get_date_range(time_filter: TimeFilter) -> tuple[datetime.date, datetime.date]:
    """Calculates start and end dates based on the filter."""
    today = datetime.now().date()
    date_range_map = {
        TimeFilter.TODAY: (today, today + timedelta(days=1)),
        TimeFilter.TOMORROW: (today + timedelta(days=1), today + timedelta(days=2)),
        TimeFilter.WEEK_AGO: (today - timedelta(days=7), today),
        TimeFilter.TWO_WEEKS_AGO: (
            today - timedelta(days=14),
            today - timedelta(days=7),
        ),
        TimeFilter.NEXT_WEEK: (today + timedelta(days=1), today + timedelta(days=8)),
        TimeFilter.NEXT_TWO_WEEKS: (
            today + timedelta(days=8),
            today + timedelta(days=15),
        ),
        TimeFilter.NEXT_MONTH: (
            today.replace(day=1) + relativedelta(months=1),
            today.replace(day=1) + relativedelta(months=2),
        ),
    }
    print("This is the date range map", date_range_map)
    feels = date_range_map.get(time_filter, (today, today + timedelta(days=1)))
    return feels
