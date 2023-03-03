import sys
import io
import csv
from instaloader import Instaloader


class DataBase():
    def __init__(self, hashtag):
        self._tentative = {}
        self._confirmed = {}
        self._rejected = {}
        self._hashtag = hashtag

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
            self._tentative[name].update_visiting_ubications(
                visiting_ubications)
        if style is not None:
            self._tentative[name].update_style(style)

    def get_tentative(self):
        return self._tentative

    def get_confirmed(self):
        return self._confirmed

    def get_rejected(self):
        return self._rejected

    def load_tentative_to_csv(self, tentative_filename):
        # Load the tentative dictionary to a csv file
        with io.open(tentative_filename, 'w') as tentative_file:
            writer = csv.writer(tentative_file, delimiter=';',
                                quotechar='"', lineterminator='\n')
            writer.writerow(["Name", "Followers", "Ubication",
                            "Visiting Ubications", "Style"])
            for key, user in self._tentative.items():
                writer.writerow(
                    [user._name, user._followers, user.ubication, user.visiting_ubications, user.style])

    def load_confirmed_to_csv(self, confirmed_filename):
        # Load the confirmed dictionary to a csv file
        with io.open(confirmed_filename, 'w') as confirmed_file:
            writer = csv.writer(confirmed_file, delimiter=';',
                                quotechar='"', lineterminator='\n')
            writer.writerow(["Name", "Followers", "Ubication",
                            "Visiting Ubications", "Style"])
            for key, user in self._confirmed.items():
                writer.writerow(
                    [user._name, user._followers, user.ubication, user.visiting_ubications, user.style])

    def load_rejected_to_csv(self, rejected_filename):
        # Load the rejected dictionary to a csv file
        with io.open(rejected_filename, 'w') as rejected_file:
            writer = csv.writer(rejected_file, delimiter=';',
                                quotechar='"', lineterminator='\n')
            writer.writerow(["Name", "Followers", "Ubication",
                            "Visiting Ubications", "Style"])
            for key, user in self._rejected.items():
                writer.writerow(
                    [user._name, user._followers, user.ubication, user.visiting_ubications, user.style])

    def load_tentative_from_csv(self, tentative_filename):
        # Load the tentative dictionary from a csv file
        with io.open(tentative_filename, 'r') as tentative_file:
            reader = csv.reader(tentative_file, delimiter=';', quotechar='"')
            next(reader)
            for row in reader:
                self._tentative[row[0]] = Artist(row[0], row[1])
                self._tentative[row[0]].update_ubication(row[2])
                self._tentative[row[0]].overwrite_visiting_ubications(row[3])
                self._tentative[row[0]].update_style(row[4])

    def load_confirmed_from_csv(self, confirmed_filename):
        # Load the confirmed dictionary from a csv file
        with io.open(confirmed_filename, 'r') as confirmed_file:
            reader = csv.reader(confirmed_file, delimiter=';', quotechar='"')
            next(reader)
            for row in reader:
                self._confirmed[row[0]] = Artist(row[0], row[1])
                self._confirmed[row[0]].update_ubication(row[2])
                self._confirmed[row[0]].overwrite_visiting_ubications(row[3])
                self._confirmed[row[0]].update_style(row[4])

    def load_rejected_from_csv(self, rejected_filename):
        # Load the rejected dictionary from a csv file
        with io.open(rejected_filename, 'r') as rejected_file:
            reader = csv.reader(rejected_file, delimiter=';', quotechar='"')
            next(reader)
            for row in reader:
                self._rejected[row[0]] = Artist(row[0], row[1])
                self._rejected[row[0]].update_ubication(row[2])
                self._rejected[row[0]].overwrite_visiting_ubications(row[3])
                self._rejected[row[0]].update_style(row[4])

    def get_data(self, tentative_filename, STOP_AT=1000):
        counter = 0
        loader = Instaloader()
        media = loader.get_hashtag_posts(self._hashtag)
        # Open the tentative.csv file, if it doesn't exist, create it and add a first row with the column names, then add the data to the csv and the list; if not, just add the data to the csv and the list
        try:
            with io.open(tentative_filename, 'r') as tentative_file:
                reader = csv.reader(
                    tentative_file, delimiter=';', quotechar='"')
                next(reader)
                for row in reader:
                    self._tentative[row[0]] = Artist(row[0], row[1])
                    self._tentative[row[0]].update_ubication(row[2])
                    self._tentative[row[0]
                                    ].overwrite_visiting_ubications(row[3])
                    self._tentative[row[0]].update_style(row[4])

                for post in media:
                    if counter == STOP_AT:
                        break

                    try:
                        if post.owner_username not in db.get_tentative() and post.owner_username not in db.get_confirmed() and post.owner_username not in db.get_rejected() and post.owner_profile.followers > 1000:
                            self._tentative[post.owner_username] = Artist(
                                post.owner_username, post.owner_profile.followers)
                            writer.writerow(
                                [post.owner_username, post.owner_profile.followers, None, None, None])
                            counter += 1
                    except:
                        pass

        except FileNotFoundError:
            with io.open(tentative_filename, 'w') as tentative_file:
                writer = csv.writer(tentative_file, delimiter=';',
                                    quotechar='"', lineterminator='\n')
                writer.writerow(["Name", "Followers", "Ubication",
                                "Visiting Ubications", "Style"])
                for post in media:
                    if counter == STOP_AT:
                        break

                    try:
                        if post.owner_username not in db.get_tentative() and post.owner_username not in db.get_confirmed() and post.owner_username not in db.get_rejected() and post.owner_profile.followers > 1000:
                            self._tentative[post.owner_username] = Artist(
                                post.owner_username, post.owner_profile.followers)
                            writer.writerow(
                                [post.owner_username, post.owner_profile.followers, None, None, None])
                            counter += 1
                    except:
                        pass


class Artist():
    def __init__(self, name, followers):
        self._name = name
        self._followers = followers
        self.ubication = None
        self.visiting_ubications = None
        self.style = None

    def update_ubication(self, ubication):
        self.ubication = ubication

    def update_visiting_ubications(self, visiting_ubication):
        if len(self.visiting_ubications) == 0:
            self.visiting_ubications = visiting_ubication
        else:
            self.visiting_ubications += ' ' + visiting_ubication

    def overwrite_visiting_ubications(self, visiting_ubications):
        self.visiting_ubications = visiting_ubications

    def update_style(self, style):
        self.style = style

    def __repr__(self):
        return f"{self._name} with {self._followers} followers and {self.ubication} as ubication and {self.visiting_ubications} as visiting ubications and {self.style} as style"


if __name__ == "__main__":
    db = DataBase(sys.argv[2])
    if sys.argv[1] == "get_from_load":
        db.get_data(sys.argv[3])

    elif sys.argv[1] == "get_new":
        db.get_data(sys.argv[3])
        db.load_confirmed_to_csv(sys.argv[4])
        db.load_rejected_to_csv(sys.argv[5])

    elif sys.argv[1] == "edit":
        db.load_tentative_from_csv(sys.argv[2])
        db.load_confirmed_from_csv(sys.argv[3])
        db.load_rejected_from_csv(sys.argv[4])

        for key in list(db.get_tentative().keys()):
            user = db.get_tentative()[key]
            print(user)
            print("1. Confirm")
            print("2. Reject")
            print("3. Edit")
            print("4. Skip")
            print("5. Exit")
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
                        new_visiting_ubications = input(
                            "New visiting ubications: ")
                        db._edit(
                            user._name, visiting_ubications=new_visiting_ubications)
                    elif option == "3":
                        new_style = input("New style: ")
                        db._edit(user._name, style=new_style)

                    print("Keep editing? (y/n)")
                    keep_editing = input()

                print(user)
                print("1. Confirm")
                print("2. Reject")
                print("3. Skip")
                option = input()
                if option == "1":
                    db._confirm(user._name)
                elif option == "2":
                    db._reject(user._name)
                elif option == "3":
                    pass

            elif option == "4":
                pass

            elif option == "5":
                print("Exiting...")
                print("Saving...")
                print("Bye :)")
                break

        db.load_tentative_to_csv(sys.argv[2])
        db.load_confirmed_to_csv(sys.argv[3])
        db.load_rejected_to_csv(sys.argv[4])
