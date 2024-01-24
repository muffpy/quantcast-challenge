"""
most-active-cookie.py: read cookie log (*.csv) and print most seen cookie(s) on specific date
"""

from datetime import datetime
import argparse
import os

## Cookie log files contain the following header format and timestamp format
delimeter = ','
log_header_format = f'cookie{delimeter}timestamp'
timestamp_format = "%Y-%m-%dT%H:%M:%S%z"

## Column header indexes in log file
timestamp_col_idx = 1
cookie_col_idx = 0

class CookieLogAnalyzer():
    """
    Represents the activity analysis of timestamped cookies from a log file.
    We store the analysis results of cookies for each day in a sorted python array 
    and we store the newest date of cookie log information. The cookie IDs are hashed
    and mapped to analysis results which are currently limited to:
        - frequency of cookie seen in an interval,
    but can be extended easily in the future.

    Each timestamp is an index into this sorted array.
    > arr
    => [newest_date analysis, (newest_date - 1) analysis, (newest_date - 2) ...]
    > f(timestamp)
    => arr[newest_date - timestamp] => {... cookie analysis data}
    ...

    This is preferred over hashing each day to avoid 0(n) worst case hash collisions
    and also because it's more readable than nested dictionaries of days -> cookies ->
    analysis data.

    Instance attributes
    ----------
    _logs : [str]
        A list of lines from the cookie log buffer stream
    _ck_daily_log : [{ str: ... }]
        A sorted list of cookie analysis data
    _newest_cookie_date : str
        The newest date index into _ck_daily_log


    Methods
    -------
    get_ckie_activity(date_str)
        Returns all cookie activity on input date

    """

    def __init__(self, logs):
        """
        Parameters
        ----------
        file : str
            The cookie log information minus the headers
        """
        
        self._logs = logs
        self._ck_daily_log = []
        self._newest_cookie_date = None

        # Helper to get date from timestamp
        def get_date(row):
            timestamp = row.split(delimeter)[timestamp_col_idx]
            return datetime.strptime(timestamp.strip(), timestamp_format).date()
        
        # Create {cookie:frequency} maps for each date
        rows = self._logs
        old_d = None # old date pointer
        c_f_map = {} # cookie:frequency maps collector
        for row in rows:
            cur_d = get_date(row) # current date pointer
            if (cur_d != old_d):
                if (c_f_map):
                    self._ck_daily_log.append(c_f_map)
                old_d = cur_d
                c_f_map = {}

            ck = row.split(delimeter)[cookie_col_idx]
            ck_freq = c_f_map.setdefault(ck, 0)
            c_f_map[ck] = ck_freq + 1

            if (row == rows[-1]): ## last iteration; collect final map
                self._ck_daily_log.append(c_f_map)

        # We now have batches of cookies (mapped to their frequencies) sorted by day 
        # from newest to oldest.
        # We can reverse this so that new cookies can be appended to end of list
        # making the operation O(1) instead of O(n) if we append to the front.
        # self._ck_daily_log.reverse()
        # 
        # We will skip doing that for now as adding new cookie logs is beyond the scope
        # of this challenge

        # Save the newest date for future accesses on daily log
        self._newest_cookie_date = get_date(rows[0])


    def get_ckie_activity(self, date_str):
        """
        Return all cookie activity as hash maps {cookie: ...} for
        user-specified date

        Parameters
        ----------
        date_str : str
            The user-specified input date
        """
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        ckie_idx = (self._newest_cookie_date - date).days
        if (ckie_idx < 0 or ckie_idx >= len(self._ck_daily_log)):
            raise ValueError(f"Invalid date: {date_str}")
        return self._ck_daily_log[ckie_idx]


def get_cookie_log(f):
    """
    Check if file is valid and return cookie log information

    Parameters
    ----------
    f : str
        User-specified input file name
    """

    # Ensure file exists
    if not os.path.isfile(f):
        raise NameError(f"{f} does not exist")
    
    # Ensure the file has the .csv extension
    if not f.endswith('.csv'):
        raise NameError("File must be a '.csv' extension")

    # Get cookie log information
    cookie_file =  None
    with open(f, 'r') as cf:
        # Ensure correct header format
        header_bytes = len(log_header_format)
        cookie_file_header = cf.read(header_bytes)
        if cookie_file_header != log_header_format:
            raise ValueError(f"Wrong header format: {cookie_file_header}")
        
        # Remove headers
        cookie_file = cf.readlines()[1:]

    return cookie_file

def most_active_cookies(cookie_activity):
    """
    Find most active cookies from 

    Parameters
    ----------
    cookie_activity : [{cookie1: .., cookie2: .., ...}]
        Cookie activity on a specific day as a hash map
    """
    max_freq = max(cookie_activity.values())
    most_active_cookies = [ck for ck, f in cookie_activity.items() if f == max_freq]

    return most_active_cookies


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Find most active cookie for a specific day")
    parser.add_argument('-f',
                        required=True, 
                        help='CSV file (*.csv) containing cookie log')
    parser.add_argument('-d',
                        required=True,
                        help='Timestamp of cookie including date and UTC(+hh:mm) time offset')

    # Parse the args (argparse automatically grabs the values from
    # sys.argv)
    args = parser.parse_args()

    # Get cookie log information from input file
    cookie_log = get_cookie_log(args.f)

    # Analyze cookies and get activity for input date
    analyzer = CookieLogAnalyzer(cookie_log)
    ckie_activity = analyzer.get_ckie_activity(args.d)
    
    # Find most active cookie(s)
    m_a_c = most_active_cookies(ckie_activity)

    # Print cookie(s) to stdout
    print(*m_a_c, sep="\n")