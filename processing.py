# Data processing for the bipartite graph

import sys
import io
import csv

# Create new csv file with the artist, city and type of link (base city or visiting city)
with io.open('edges.csv', 'w') as edges_file:
    writer = csv.writer(edges_file, delimiter=';',
                        quotechar='"', lineterminator='\n')
    writer.writerow(["Artist", "City", "Type"])

    with io.open('nodes.csv', 'w') as nodes_file:
        writer_nodes = csv.writer(nodes_file, delimiter=';',
                                  quotechar='"', lineterminator='\n')
        writer_nodes.writerow(
            ["Artist", "Followers", "Style", "City", "Country"])

        cities = []

        with io.open(sys.argv[1], 'r') as confirmed_file:
            reader = csv.reader(confirmed_file, delimiter=';', quotechar='"')
            next(reader)
            for row in reader:
                artist = row[0]
                followers = row[1]
                base_city = row[2].replace('-', ' ')
                visiting_cities = row[3]
                style = row[4]

                # Write artist node
                writer_nodes.writerow([artist, followers, style, None, None])

                # Write base city node
                if base_city not in cities:
                    writer_nodes.writerow([None, None, None, base_city, None])
                    cities.append(base_city)

                # Write base city
                writer.writerow([artist, base_city, "base"])
                if visiting_cities != "":
                    for visiting_city in visiting_cities.split(" "):
                        writer.writerow(
                            [artist, visiting_city.replace('-', ' '), "visiting"])

                        # Write visiting cities nodes
                        if visiting_city.replace('-', ' ') not in cities:
                            writer_nodes.writerow(
                                [None, None, None, visiting_city.replace('-', ' '), None])
                            cities.append(visiting_city.replace('-', ' '))
