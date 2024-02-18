import csv
import random
from pathlib import Path

# Define the edge types
edge_types = ["InstanceOf", "SubclassOf", "HasAttribute"]

# Define entities
entities = [
    "drink",
    "musical instrument",
    "food",
    "geographic region",
    "product",
    "animal",
    "creamy",
    "Indian",
    "aromatic",
    "piano",
    "grand piano",
    "baby grand",
    "upright piano",
    "digital piano",
    "acoustic piano",
    "electric piano",
    "drink",
    "alcoholic drink",
    "non-alcoholic drink",
    "carbonated drink",
    "soft drink",
    "soda",
    "cola",
    "lemon-lime soda",
    "orange soda",
    "root beer",
    "ginger ale",
    "tonic water",
    "club soda",
    "sparkling water",
    "seltzer water",
    "tonic",
    "bitter lemon",
    "ginger beer",
    "lemonade",
    "fruit punch",
    "sports drink",
    "energy drink",
    "tea",
    "black tea",
    "green tea",
    "white tea",
    "oolong tea",
    "herbal tea",
    "fruit tea",
    "flavored tea",
    "chai",
    "bubble tea",
    "coffee",
    "hot",
    "cold",
    "creamy",
    "sweet",
    "sour",
    "bitter",
    "spicy",
    "aromatic",
    "strong",
    "weak",
    "Indian",
    "Chinese",
    "Japanese",
    "Korean",
    "Thai",
    "Vietnamese",
    "Mediterranean",
    "Middle Eastern",
    "European",
    "American",
]

# Define the number of records you want
# kept low for commiting to the repo...
num_records = 10  # For example, one million records


# Define a function to generate random records
def generate_record(record_id):
    edge_type = random.choice(edge_types)
    head_entity = random.choice(entities)
    tail_entity = random.choice(entities)
    return [record_id, edge_type, head_entity, tail_entity]


# Generate the records
records = [generate_record(i) for i in range(num_records)]

# Write the records to a CSV file
file_path = Path("data/ontology-huge.csv")
with open(file_path, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["ID", "EDGE_TYPE", "HEAD_ENTITY", "TAIL_ENTITY"])
    writer.writerows(records)
