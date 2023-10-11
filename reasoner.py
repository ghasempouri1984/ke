import rdflib
import owlrl

# Load your RDF data from the aligned-output.ttl file
g = rdflib.Graph()
g.parse("aligned_output.ttl", format='turtle')

# Perform reasoning
owlrl.DeductiveClosure(owlrl.RDFS_Semantics).expand(g)

# The graph `g` now contains the inferred triples as well
# Optionally, you can serialize and save the enriched graph to a file
g.serialize(destination='enriched_output.ttl', format='turtle')
