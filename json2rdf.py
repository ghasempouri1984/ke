import json
import os
import subprocess
import rdflib


# ... (process_json function)
def process_json(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"Error: {input_file} does not exist.")
        return
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if 'lyrics' not in data:
            print(f"Error: 'lyrics' key not found in {input_file}.")
            return
        
        for section in data['lyrics']:
            if 'lyrics' not in section:
                print("Error: Inner 'lyrics' key not found in section.")
                continue
            
            section['lyrics'] = ' '.join(section['lyrics'])
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    
    except json.JSONDecodeError:
        print(f"Error: {input_file} is not a valid JSON file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# ... (generate_sparql_query function)
def generate_sparql_query(json_data):
    query_prefixes = """
    PREFIX ex: <http://example.org/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    """
    
    construct_clauses = []
    where_clauses = []
    
    for i, section in enumerate(json_data['lyrics']):
        section_type = section['header'].replace(" ", "").capitalize()
        section['annotation'] = section['annotation'].replace('\n', '\\n').replace('"', '\\"')
        construct_clauses.append(f"""
        ?song ex:has{section_type}{i} ?{section_type.lower()}{i} .
        ?{section_type.lower()}{i} rdf:type ex:{section_type} ;
                                ex:header "{section['header']}" ;
                                ex:annotation "{section['annotation']}" ;
                                ex:lyrics "{section['lyrics']}" .
        """)
        where_clauses.append(f"""
        BIND (IRI(concat("http://example.org/{section_type.lower()}{i}/", STRUUID())) AS ?{section_type.lower()}{i})
        """)
    
    query_construct = "\n".join(construct_clauses)
    query_where = "\n".join(where_clauses)
    
    query = f"""
    {query_prefixes}
    CONSTRUCT {{
        ?song a ex:Song ;
              ex:title "{json_data['song_title']}" ;
              ex:hasArtist ?artist ;
              ex:isPartOfAlbum ?album .
        ?artist a ex:Artist ;
                ex:name "{json_data['artist_name']}" .
        ?album a ex:Album ;
               ex:title "{json_data['album_title']}" .
        {query_construct}
    }}
    WHERE {{
        BIND (IRI(concat("http://example.org/song/", STRUUID())) AS ?song)
        BIND (IRI(concat("http://example.org/artist/", STRUUID())) AS ?artist)
        BIND (IRI(concat("http://example.org/album/", STRUUID())) AS ?album)
        {query_where}
    }}
    """
    return query

# ... 
def generate_sparql_files(folder_path):
    query_folder_path = os.path.join(folder_path, 'queries')
    if not os.path.exists(query_folder_path):
        os.mkdir(query_folder_path)
        
    for filename in os.listdir(folder_path):
        if filename.startswith('processed_') and filename.endswith('.json'):
            input_file_path = os.path.join(folder_path, filename)
            
            try:
                with open(input_file_path, 'r') as f:
                    processed_json = json.load(f)
                
                sparql_query = generate_sparql_query(processed_json)
                output_file_path = os.path.join(query_folder_path, f'{filename.replace(".json", ".sparql")}')
                
                with open(output_file_path, 'w') as f:
                    f.write(sparql_query)
            except Exception as e:
                print(f"An error occurred while generating SPARQL query for {filename}: {e}")


def run_sparql_commands(folder_path):
    query_folder_path = os.path.join(folder_path, 'queries')
    ttl_folder_path = os.path.join(folder_path, 'ttl')
    
    if not os.path.exists(query_folder_path):
        print("Error: Query folder does not exist.")
        return
    
    if not os.path.exists(ttl_folder_path):
        os.mkdir(ttl_folder_path)
    
    for filename in os.listdir(query_folder_path):
        if filename.endswith('.sparql'):
            try:
                query_file_path = os.path.join(query_folder_path, filename)
                output_file_path = os.path.join(ttl_folder_path, f"{filename.replace('.sparql', '.ttl')}")

                print(f"Running SPARQL command for query: {filename}")  # Print the name of the query
                
                command = [
                    'java',
                    '-jar',
                    'sparql-anything-0.8.2.jar',
                    '-q',
                    query_file_path,
                    '-o',
                    output_file_path
                ]
                
                subprocess.run(command, check=True)
                
            except subprocess.CalledProcessError as e:
                print(f"An error occurred while running the SPARQL command for {filename}: {e}")


# ... 
def align_ttl_to_ontology(input_file, output_file):
    # ... (Your align_ttl_to_ontology function remains unchanged)
    graph = rdflib.Graph()
    graph.parse(input_file, format='turtle')

    aligned_graph = rdflib.Graph()
    aligned_graph.bind("ex", "http://www.semanticweb.org/ash-lab/ontologies/2023/7/untitled-ontology-18/")
    aligned_graph.bind("mm", "http://www.semanticweb.org/ash-lab/ontologies/2023/7/untitled-ontology-18#mm:")
    aligned_graph.bind("core", "http://www.semanticweb.org/ash-lab/ontologies/2023/7/untitled-ontology-18#core:")

    for s, p, o in graph:
        
        # Updating predicate URIs
        updated_predicate_uris = {
            rdflib.URIRef('http://example.org/annotation'): rdflib.URIRef('http://www.semanticweb.org/ash-lab/ontologies/2023/7/untitled-ontology-18#mm:hasAnnotation'),
            rdflib.URIRef('http://example.org/header'): rdflib.URIRef('http://www.semanticweb.org/ash-lab/ontologies/2023/7/untitled-ontology-18/fragmentName'),
            rdflib.URIRef('http://example.org/lyrics'): rdflib.URIRef('http://www.semanticweb.org/ash-lab/ontologies/2023/7/untitled-ontology-18#mm:hasText'),
            rdflib.URIRef('http://example.org/name'): rdflib.URIRef('http://www.semanticweb.org/ash-lab/ontologies/2023/7/untitled-ontology-18#core:name'),
            rdflib.URIRef('http://example.org/title'): rdflib.URIRef('http://www.semanticweb.org/ash-lab/ontologies/2023/7/untitled-ontology-18#core:title'),
        }
        p = updated_predicate_uris.get(p, p)  # replace p if a mapping is found, otherwise keep it unchanged
        
        # Dynamic mapping of object class URIs based on input
        if o.startswith(rdflib.URIRef('http://example.org/Verse')):
            o = rdflib.URIRef(f'http://www.semanticweb.org/ash-lab/ontologies/2023/7/untitled-ontology-18#mm:Verse')

        # Dynamic mapping of object property URIs based on input
        if p.startswith(rdflib.URIRef('http://example.org/hasVerse')) or \
           p.startswith(rdflib.URIRef('http://example.org/hasBridge')) or \
           p.startswith(rdflib.URIRef('http://example.org/hasOutro')):
            p = rdflib.URIRef('http://www.semanticweb.org/ash-lab/ontologies/2023/7/untitled-ontology-18#core:hasPart')
        elif p == rdflib.URIRef('http://example.org/hasArtist'):
            p = rdflib.URIRef('http://www.semanticweb.org/ash-lab/ontologies/2023/7/untitled-ontology-18#mm:isInvolvedIn')
        elif p == rdflib.URIRef('http://example.org/isPartOfAlbum'):
            p = rdflib.URIRef('http://www.semanticweb.org/ash-lab/ontologies/2023/7/untitled-ontology-18#mm:isPartOfRelease')

        aligned_graph.add((s, p, o))


    aligned_graph.serialize(destination=output_file, format='turtle')


def align_ttl_files(folder_path):
    ttl_folder_path = os.path.join(folder_path, 'ttl')
    aligned_ttl_folder_path = os.path.join(folder_path, 'aligned_ttl')
    
    if not os.path.exists(ttl_folder_path):
        print("Error: TTL folder does not exist.")
        return
    
    if not os.path.exists(aligned_ttl_folder_path):
        os.mkdir(aligned_ttl_folder_path)
    
    for filename in os.listdir(ttl_folder_path):
        if filename.endswith('.ttl'):
            try:
                print(f"Aligning TTL file: {filename}")
                input_file_path = os.path.join(ttl_folder_path, filename)
                output_file_path = os.path.join(aligned_ttl_folder_path, f"aligned_{filename}")
                align_ttl_to_ontology(input_file_path, output_file_path)
            except Exception as e:
                print(f"An error occurred while aligning TTL file {filename}: {e}")


def main(folder_path):
    if not os.path.exists(folder_path):
        print(f"Error: Folder {folder_path} does not exist.")
        return
    
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            input_file_path = os.path.join(folder_path, filename)
            output_file_path = os.path.join(folder_path, f'processed_{filename}')
            process_json(input_file_path, output_file_path)
    generate_sparql_files(folder_path)
    run_sparql_commands(folder_path)
    align_ttl_files(folder_path)

# Usage
main('jsons')

