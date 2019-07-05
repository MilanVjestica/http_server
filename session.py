
class Session:

    """
    Class for handling sessions.
    """

    sessions = {}  # Dictionary for storing all sessions.
    session = {}  # Dictionary for storing current session data.

    def init(self, cookie):
        """
        Create current session by cookie value.

        :param cookie: Session id from cookie.
        """
        self.cookie = cookie
        if self.cookie not in self.sessions:
            self.sessions[self.cookie] = {}
        self.session = self.sessions[self.cookie]

    def put(self, key, value):
        """
        Put data to current session dictionary.

        :param key: Data key. ex. 'username'
        :param value: Data value. ex. 'user1'
        """
        self.session[key] = value
        self.sessions[self.cookie] = self.session

    def get(self, key):
        """
        Get data from current session.

        :param key:
        :return: Requested data for success. Exception(KeyError) if data doesn't exist.
        """
        try:
            return self.session[key]
        except KeyError:
            return None

    def clear(self):
        """
        Clear current session.
        """
        self.session.clear()
        self.sessions[self.cookie].clear()
