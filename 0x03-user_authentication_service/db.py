from user import User

class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database
        
        Args:
            email (str): Email of the user
            hashed_password (str): Hashed password of the user
        
        Returns:
            User: The newly created user object
        """
        # Create a new User object
        new_user = User(email=email, hashed_password=hashed_password)
        
        # Add the new user to the session
        self._session.add(new_user)
        
        # Commit the session to save the changes to the database
        self._session.commit()
        
        return new_user
