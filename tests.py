import pytest
import most_active_cookie

############################################
## get_cookie_log() tests
############################################
get_cookie_log = most_active_cookie.get_cookie_log

def test_non_existent_file():
    """
    Test that non-existent files throws NameError
    """
    non_existent_file_name = "data/random_file"
    with pytest.raises(NameError, match=r".* does not exist"):
        get_cookie_log(non_existent_file_name)

def test_non_csv_file():
    """
    Test that non-csv files which exist throws NameError
    """
    non_csv_file_name = "data/random_file.pdf"
    with pytest.raises(NameError, match="File must be a '.csv' extension"):
        get_cookie_log(non_csv_file_name)

def test_csv_file_has_correct_headers():
    """
    Test that csv files with wrong headers throw ValueError
    """
    wrong_header_csv_file_name = "data/wrong-cookie-log.csv"
    with pytest.raises(ValueError, match=r"Wrong header format: .*"):
        get_cookie_log(wrong_header_csv_file_name)


############################################
## CookieLogAnalyzer() tests
############################################
CookieLogAnalyzer = most_active_cookie.CookieLogAnalyzer

############################################
## most_active_cookies() tests
############################################
most_active_cookies = most_active_cookie.most_active_cookies