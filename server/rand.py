from datetime import date


def randomString():
    """Generate a random string of fixed length """
    # letters = string.ascii_lowercase
    return str(date.today().strftime("%Y%d%m"))


print("Date String is {}".format(randomString()))
