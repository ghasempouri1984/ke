# ke

## Class-Attribute Schema Pattern:

The ontology defines classes like `Song`, `Album`, `Artist`, `Bridge`, `Outro`, and `Verse`, and associates attributes to instances of these classes using properties like `core:title`, `core:name`, `mm:hasAnnotation`, `mm:hasText`, and `ex:fragmentName`.  
For example, the `Album` class has a `core:title` attribute, the `Artist` class has a `core:name` attribute, and the `Verse` class has `mm:hasText` and `mm:hasAnnotation` attributes.

## Part-Whole Schema Pattern:

The ontology employs a part-whole relationship: any object in a collection is a part of the whole composition and composition as a whole is a collection of parts, where a `Song` is divided into parts like `Bridge`, `Outro`, and `Verse`, represented by the `core:hasPart` property.  
For instance, the song "Yesterday" has parts like `Bridge`, `Outro`, and `Verse`, as seen in the triples with the `core:hasPart` predicate.

## Participation Schema Pattern:

The ontology also depicts participation relationships where a `Song` is associated with an `Artist` and an `Album` through the properties `mm:isInvolvedIn` and `mm:isPartOfRelease` respectively.  
For instance, the song "Yesterday" is associated with the artist "The Beatles" and the album "Help!" through the `mm:isInvolvedIn` and `mm:isPartOfRelease` properties respectively.

# json2rdf.py Workflow:

### `main(folder_path):` 
- **Role:** This is the entry point.
- **Actions:**
  1. Verifies if the folder exists.
  2. Calls other functions in sequence: `process_json`, `generate_sparql_files`, `run_sparql_commands`, and `align_ttl_files`.

### `process_json(input_file, output_file):`
- **Role:** Processes JSON files.
- **Actions:**
  1. Transforms the lyrics from a list of lines to a single string.
  2. Saves the changes in a new JSON file.

### `generate_sparql_files(folder_path):`
- **Role:** Reads the processed JSON files.
- **Actions:**
  1. Uses `generate_sparql_query` to convert each JSON to a SPARQL query.
  2. Saves these queries in `.sparql` files.

### `generate_sparql_query(json_data):`
- **Role:** Takes JSON data as input.
- **Actions:**
  1. Generates a SPARQL query that represents the data in RDF triples.

### `run_sparql_commands(folder_path):`
- **Role:** Executes SPARQL queries.
- **Actions:**
  1. Executes SPARQL queries saved in `.sparql` files.
  2. Outputs the results in Turtle format (`.ttl`).

### `align_ttl_to_ontology(input_file, output_file):`
- **Role:** Alters the URIs in the Turtle files.
- **Actions:**
  1. Alters the URIs in the Turtle files to align them with a specific ontology.

### `align_ttl_files(folder_path):`
- **Role:** Applies `align_ttl_to_ontology` to all `.ttl` files in the folder.

