import re


# unfortunately this is not part of the default re package of micropython
# https://docs.micropython.org/en/latest/library/re.html but stackoverflow to the rescue
# @source https://stackoverflow.com/questions/52603287/return-multiple-matches-using-re-match-or-re-search
def regex_findall(pattern, string):
    while True:
        match = re.search(pattern, string)
        if not match:
            break
        yield match.group(0)
        string = string[match.end():]
