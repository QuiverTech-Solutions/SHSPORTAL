"""Base Repository."""

# Third party imports


from databases import Database


class BaseRepository:
    """Base class for Postgres repositories."""

    def __init__(self, db: Database) -> None:
        """Initialize with Postgres database instance.

        Args:
            db (Database): An instance of the Database database.
        """
        self.db = db
