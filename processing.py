# Data processing for the bipartite graph

import sys
import io
import csv

# Create new csv file with the artist, city and type of link (base city or visiting city)

with io.open(sys.argv[1], 'r') as confirmed_file:
    reader = csv.reader(confirmed_file, delimiter=';', quotechar='"')
    next(reader)
    for row in reader:
        pass

########################
## UNDER CONSTRUCTION ##
########################
