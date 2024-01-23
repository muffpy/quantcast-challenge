"""
most-active-cookie.py: read cookie log (*.csv) and print most seen cookie on specific date to stdout
"""

from datetime import datetime
import argparse
import os

## Cookie log files contain the following header format
delimeter = ','
log_header_format = f'cookie{delimeter}timestamp'
datetime_format = "%Y-%m-%dT%H:%M:%S%z"

# Get indexes for each column header
timestamp_col_idx = log_header_format.split(delimeter).index('timestamp')
cookie_row_idx = log_header_format.split(delimeter).index('cookie')

class CookieLogAnalyzer():

    def __init__(self, file):
        """
        """
        
        self._logs = file.readlines()[1:]
        self._ck_daily_log = []
        self._newest_cookie_date = None

        # Helper to get date from timestamp
        def get_date(row):
            timestamp = row.split(delimeter)[timestamp_col_idx]
            return datetime.strptime(timestamp.strip(), datetime_format).date()
        
        # Create cookie:frequency maps for each date
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

            ck = row.split(delimeter)[cookie_row_idx]
            ck_freq = c_f_map.setdefault(ck, 0)
            c_f_map[ck] = ck_freq + 1

            if (row == rows[-1]): ## last iteration; collect final map
                self._ck_daily_log.append(c_f_map)

        # We now have batches of cookies (mapped to their frequencies) sorted by day 
        # from newest to oldest.
        # We can reverse this once so that new cookies can be appended to end of list
        # making the operation O(1) instead of O(n) if we append to the front.
        # self._ck_daily_log.reverse()
        # 
        # We will skip doing that for now

        # Save the newest date for future accesses on daily log
        self._newest_cookie_date = get_date(rows[0])


    def get_ckie_activity(self, date_str):
        """
        """
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        ckie_idx = (self._newest_cookie_date - date).days
        if (ckie_idx < 0 or ckie_idx >= len(self._ck_daily_log)):
            raise ValueError(f"Invalid date: {date_str}")
        return self._ck_daily_log[ckie_idx]


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

# Ensure the file has the .csv extension
if not args.f.endswith('.csv'):
    raise NameError("File must be a '.csv' extension")
# Ensure file exists
if not os.path.isfile(args.f):
    raise NameError(f"{args.f} does not exist")

with open(args.f, 'r') as cookie_file:
    # Ensure correct header format
    header_bytes = len(log_header_format)
    cookie_file_header = cookie_file.read(header_bytes)
    if cookie_file_header != log_header_format:
        raise ValueError(f"Wrong header format: {cookie_file_header}")

    # Analyze cookies and get activity for input date
    analyzer = CookieLogAnalyzer(cookie_file)
    ckie_activity = analyzer.get_ckie_activity(args.d)
    
    # Find most active cookie
    max_freq = max(ckie_activity.values())
    most_active_cookies = [ck for ck, f in ckie_activity.items() if f == max_freq]

    # Print cookies to stdout
    print(*most_active_cookies, sep=", ")

