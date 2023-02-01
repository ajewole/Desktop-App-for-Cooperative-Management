import datetime

class Utils():
    def __init__(self):
        pass

    def generate_years(self):
        x = datetime.datetime.now()
        year = x.year
        years = []
        years.append(str(year))
        for i in range(50):
            year = year + 1
            years.append(str(year))
            i += 1
        return years

# results = generate_years()
# print(results)