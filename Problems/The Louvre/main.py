class Painting:
    museum = 'Louvre'

    def __init__(self, title, painter, year):
        self.title = title
        self.painter = painter
        self.year = year

    def show(self):
        print(f'"{self.title}" by {self.painter} ({self.year}) hangs in the {Painting.museum}.')


ititle = input()
ipainter = input()
iyear = input()

artist = Painting(ititle, ipainter, iyear)
artist.show()
