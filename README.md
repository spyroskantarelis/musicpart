# musicpart
Music Part Ontology updated repository

An ontology designed to formalize symbolic representations of music by focusing on the structural and sequential aspects of tracks, such as chords, chord progressions, and music parts. MPO transforms textual music data into a machine-readable format, representing it as a knowledge graph. This repository contains the tools and examples for utilizing MPO in Music Information Retrieval (MIR), demonstrating its integration with other ontologies and enabling advanced music analysis tasks. We use two subsets of the ChoCo dataset and the Chordonomicon dataset.

The ontology is created in mpo.py using owlready2. The knowledge graph is created in convert_graph.py using rdflib.

For harmonic context analysis, we facilitate the Functional Harmony Ontology: https://github.com/spyroskantarelis/FunctionalHarmony

Kantarelis Spyridon, Edmund Dervakos, and Giorgos Stamou. "The Music Part Ontology." Description Logics. 2023.
