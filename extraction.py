import sys
import io
import csv
from instaloader import Instaloader

class DataBase():
    def __init__(self):
        self._tentative = {}
        self._confirmed = {}
        self._rejected  = {}
    
    def _add(self, data):
        # Add a new element to the tentative list
        self._tentative[data._name] = data

    def _confirm(self, name):
        # Add a certain element to the confirmed list and delete it from the tentative list
        self._confirmed[name] = self._tentative[name]
        del self._tentative[name]
    
    def _reject(self, name):
        # Delete a certain element from the tentative list and add it to the rejected list
        self._rejected[name] = self._tentative[name]
        del self._tentative[name]

    def _edit(self, name, ubication=None, visiting_ubications=None, style=None):
        # Edit a certain element from the tentative list
        if ubication is not None:
            self._tentative[name].update_ubication(ubication)
        if visiting_ubications is not None:
            self._tentative[name].update_visiting_ubications(visiting_ubications)
        if style is not None:
            self._tentative[name].update_style(style)
        

    def get_tentative(self):
        return self._tentative

    def get_confirmed(self):
        return self._confirmed
    
    def get_rejected(self):
        return self._rejected
    
    def load_to_csv(self):
        # Load the both dictionaries to csv files
        with io.open('tentative.csv', 'w') as tentative_file:
            writer = csv.writer(tentative_file, delimiter=';', quotechar='"', lineterminator='\n')
            writer.writerow(["Name", "Followers", "Ubication", "Visiting Ubications", "Style"])
            for key, user in self._tentative.items():
                writer.writerow([user._name, user._followers, user.ubication, user.visiting_ubications, user.style])

        with io.open('confirmed.csv', 'w') as confirmed_file:
            writer = csv.writer(confirmed_file, delimiter=';', quotechar='"', lineterminator='\n')
            writer.writerow(["Name", "Followers", "Ubication", "Visiting Ubications", "Style"])
            for key, user in self._confirmed.items():
                writer.writerow([user._name, user._followers, user.ubication, user.visiting_ubications, user.style])

        with io.open('rejected.csv', 'w') as rejected_file:
            writer = csv.writer(rejected_file, delimiter=';', quotechar='"', lineterminator='\n')
            writer.writerow(["Name", "Followers", "Ubication", "Visiting Ubications", "Style"])
            for key, user in self._rejected.items():
                writer.writerow([user._name, user._followers, user.ubication, user.visiting_ubications, user.style])

    def load_from_csv(self, tentative_filename, confirmed_filename, rejected_filename):
        # Load the both dictionaries from csv files
        with io.open(tentative_filename, 'r') as tentative_file:
            reader = csv.reader(tentative_file, delimiter=';', quotechar='"')
            next(reader)
            for row in reader:
                self._tentative[row[0]] = Artist(row[0], row[1])
                self._tentative[row[0]].update_ubication(row[2])
                self._tentative[row[0]].update_visiting_ubications(row[3])
                self._tentative[row[0]].update_style(row[4])

        with io.open(confirmed_filename, 'r') as confirmed_file:
            reader = csv.reader(confirmed_file, delimiter=';', quotechar='"')
            next(reader)
            for row in reader:
                self._confirmed[row[0]] = Artist(row[0], row[1])
                self._confirmed[row[0]].update_ubication(row[2])
                self._confirmed[row[0]].update_visiting_ubications(row[3])
                self._confirmed[row[0]].update_style(row[4])

        with io.open(rejected_filename, 'r') as rejected_file:
            reader = csv.reader(rejected_file, delimiter=';', quotechar='"')
            next(reader)
            for row in reader:
                self._rejected[row[0]] = Artist(row[0], row[1])
                self._rejected[row[0]].update_ubication(row[2])
                self._rejected[row[0]].update_visiting_ubications(row[3])
                self._rejected[row[0]].update_style(row[4])

class Artist():
    def __init__(self, name, followers):
        self._name = name
        self._followers = followers
        self.ubication = None
        self.visiting_ubications = []
        self.style = None

    def update_ubication(self, ubication):
        self.ubication = ubication

    def update_visiting_ubications(self, visiting_ubications):
        self.visiting_ubications = visiting_ubications
    
    def update_style(self, style):
        self.style = style

    def __repr__(self):
        return f"{self._name} with {self._followers} followers and {self.ubication} as ubication and {self.visiting_ubications} as visiting ubications and {self.style} as style"


def get_data(hashtag, db, STOP_AT=1000):
    counter = 0
    loader = Instaloader()
    media = loader.get_hashtag_posts(hashtag)
    for post in media:
        try:
            if counter < STOP_AT and post.owner_username not in db.get_tentative() and post.owner_username not in db.get_confirmed() and post.owner_username not in db.get_rejected() and post.owner_profile.followers > 1000:  
                db._add(Artist(post.owner_username, post.owner_profile.followers))
                counter += 1
        except:
            pass

if __name__ == "__main__":
    db = DataBase()
    if sys.argv[1] == "get_from_load":
        db.load_from_csv(sys.argv[3], sys.argv[4], sys.argv[5])
        get_data(sys.argv[2], db)
        db.load_to_csv()

    elif sys.argv[1] == "get_new":
        get_data(sys.argv[2], db)
        db.load_to_csv()

    elif sys.argv[1] == "edit":
        db.load_from_csv(sys.argv[2], sys.argv[3], sys.argv[4])
        for key, user in db.get_tentative().items():
            print(user)
            print("1. Confirm")
            print("2. Reject")
            print("3. Edit")
            print("4. Skip")
            option = input()
            if option == "1":
                db._confirm(user._name)
            elif option == "2":
                db._reject(user._name)
            elif option == "3":
                keep_editing = "y"
                while keep_editing == "y":
                    print("1. Ubication")
                    print("2. Visiting Ubications")
                    print("3. Style")
                    option = input()
                    if option == "1":
                        new_ubication = input("New ubication: ")
                        db._edit(user._name, ubication=new_ubication)
                    elif option == "2":
                        new_visiting_ubications = input("New visiting ubications: ")
                        db._edit(user._name, visiting_ubications=new_visiting_ubications)
                    elif option == "3":
                        new_style = input("New style: ")
                        db._edit(user._name, style=new_style)
                    
                    print("Keep editing? (y/n)")
                
            elif option == "4":
                pass
