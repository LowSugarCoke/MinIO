from datetime import datetime
import re

class DateCapture:
    def __init__(self):
        """
        Create a new DateCapture instance.

        Attributes:
            regex (str): The regular expression used to match the date part in a filename.
        """
        self.regex = r"^(.+)([0-9]{4}-[0-9]{2}-[0-9]{2})(.+)$"

    def extract_date(self, filename):
        """
        Extract the date from a filename and return a datetime object.

        Args:
            filename (str): The filename to extract the date from.

        Returns:
            datetime: A datetime object representing the date extracted from the filename,
                or the string 'No Date' if no date was found in the filename.
        """
        match = re.match(self.regex, filename)
        if match:
            date_str = match.group(2)
            date = datetime.strptime(date_str, '%Y-%m-%d')
            return date
        else:
            return "No Date"
