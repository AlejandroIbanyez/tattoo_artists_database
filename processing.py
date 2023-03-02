# Data processing for the bipartite graph

import sys
import io
import csv

# Create new csv file with the artist, city and type of link (base city or visiting city)
with io.open('edges.csv', 'w') as edges_file:
    writer = csv.writer(edges_file, delimiter=';',
                        quotechar='"', lineterminator='\n')
    writer.writerow(["Artist", "City", "Type", "Style", "Followers"])
    with io.open(sys.argv[1], 'r') as confirmed_file:
        reader = csv.reader(confirmed_file, delimiter=';', quotechar='"')
        next(reader)
        for row in reader:
            artist = row[0]
            followers = int(row[1])
            base_city = row[2]
            visiting_cities = row[3]
            style = row[4]

            # Write base city
            writer.writerow([artist, base_city, "base", style, followers])
            if visiting_cities != "":
                for visiting_city in visiting_cities.split(" "):
                    writer.writerow(
                        [artist, visiting_city, "visiting", style, followers])
