from rdflib import Namespace
from rdflib import Graph
from rdflib.namespace import RDF
from rdflib.namespace import Namespace
from rdflib import URIRef, BNode, Literal
from rdflib import Graph, Literal, Namespace, RDF, RDFS, XSD, OWL
from rdflib.namespace import FOAF
import itertools
import pandas as pd   
import time
import csv
import ast
import time
from datetime import datetime
import re
fho = Namespace("http://purl.org/ontology/fho/")
mpo = Namespace('http://purl.org/ontology/mpo/')
g = Graph()
g.bind("mpo", mpo)
g.bind("fho", fho)
g.bind("owl", OWL)
# List of properties to define as ObjectProperty
object_properties = [
    mpo.isFirstTrackChordof,
    mpo.isLastTrackChordof,
    mpo.hasNextPart,
    mpo.hasFirstPartChord,
    mpo.hasLastPartChord,
    mpo.hasPartChord,
    mpo.hasPart,
    mpo.hasReleaseDate,
    mpo.hasChordProgression,
    mpo.hasFirstProgChord,
    mpo.hasLastProgChord,
    mpo.hasProgChord,
    mpo.hasNextChordProgression,
    mpo.hasGenre,
    fho.hasNext,
    fho.hasPrevious
]



# Add declarations
for prop in object_properties:
    g.add((prop, RDF.type, OWL.ObjectProperty))

nx = fho.hasNext
pr = fho.hasPrevious

is_first_track_chord = mpo.isFirstTrackChordof
is_last_track_chord = mpo.isLastTrackChordof
nx_part = mpo.hasNextPart
has_first_part_chord = mpo.hasFirstPartChord
has_last_part_chord = mpo.hasLastPartChord
has_part_chord = mpo.hasPartChord
has_part = mpo.hasPart
has_release = mpo.hasReleaseDate

has_chord_progression = mpo.hasChordProgression
has_first_prog_chord = mpo.hasFirstProgChord
has_last_prog_chord = mpo.hasLastProgChord
has_chord_count = mpo.hasChordCount
has_prog_chord = mpo.hasProgChord

has_next_progression = mpo.hasNextChordProgression
has_genre = mpo.hasGenre

class_track = mpo.Track
class_chord = mpo.Chord
class_part = mpo.Part
class_progression = mpo.ChordProgression



# reading a csv file
tracks = pd.read_csv('your csv')

ids = tracks['id'].tolist()
progressions = tracks['chord_progression'].tolist()
genres = tracks['genre'].tolist()

def is_rotational_equivalent_with_shared_position(pos1, ngram1, pos2, ngram2):
    words1 = ngram1.split()
    words2 = ngram2.split()
    
    # Check if ngram2 is a rotation of ngram1 using doubled string trick
    doubled = (ngram1 + ' ' + ngram1)
    if not re.search(re.escape(ngram2), doubled):
        return False
    
    # Check if they share a word at the same absolute position
    for i, word1 in enumerate(words1):
        abs_pos1 = pos1 + i
        for j, word2 in enumerate(words2):
            abs_pos2 = pos2 + j
            if abs_pos1 == abs_pos2 and word1 == word2:
                return True
    
    return False

def generate_ngrams_by_size(text, min_n=3, max_n=8):
    words = text.split()
    ngrams_dict = {}
    
    for n in range(min_n, max_n + 1):
        ngrams_with_positions = []
        
        # First pass: generate valid ngrams with their positions
        for i in range(len(words) - n + 1):
            ngram = ' '.join(words[i:i + n])
            if is_valid_ngram(ngram) and is_valid_ngram_heuristic2(ngram):
                ngrams_with_positions.append((i, ngram))

        # Second pass: filter rotational equivalents
        filtered_ngrams = []
        for pos1, ngram1 in ngrams_with_positions:
            should_keep = True
            for pos2, ngram2 in filtered_ngrams:
                if is_rotational_equivalent_with_shared_position(pos1, ngram1, pos2, ngram2):
                    should_keep = False
                    break
            if should_keep:
                filtered_ngrams.append((pos1, ngram1))
        # Extract just the ngrams (without positions) for final result
        ngrams_dict[n] = [ngram for pos, ngram in filtered_ngrams]
    
    return ngrams_dict

def is_valid_ngram(ngram):
    words = ngram.split()
    n = len(words)
    
    if n < 3:
        return True
    
    # Create pattern for first bigram
    first_bigram = f"{re.escape(words[0])} {re.escape(words[1])}"
    
    # Check if first bigram appears again at forbidden positions
    for k in range(2, n - 1):
        start_pos = n - k  # position of cn-k+1 (0-indexed)
        if start_pos + 1 < n:  # ensure we have cn-k+2
            candidate_bigram = f"{re.escape(words[start_pos])} {re.escape(words[start_pos + 1])}"
            if first_bigram == candidate_bigram:
                return False
    
    return True

def is_valid_ngram_heuristic2(ngram):
    words = ngram.split()
    n = len(words)
    
    if n <= 3:  # No need to check if n-gram is too small
        return True
    
    target_length = n - 1  # Check only subsequences of length n-1
    
    # Check all possible contiguous subsequences of length n-1
    for i in range(n - target_length + 1):  # This gives us n-(n-1)+1 = 2 positions
        subsequence_words = words[i:i + target_length]
        subsequence = ' '.join(subsequence_words)
        # Check if this (n-1)-gram is valid AND its first word appears again in the subsequence
        if is_valid_ngram(subsequence) and (words[-1] == words[0]):
            return False
    
    return True

def hasNext_function(track,track_chord_progression, OntoProperty, OntoFirst, OntoLast, g):
    chord_count = {}
    prev_chord = None
    for i, chord in enumerate(track_chord_progression):
        if chord not in chord_count:
            chord_count[chord] = 1
        else:
            chord_count[chord] += 1
        if (i == 0) and (OntoFirst is not None):
            # setattr(chord, OntoFirst, track)
            g.add((chord, OntoFirst, track))
        if (i == len(track_chord_progression) - 1) and (OntoLast is not None):
            # setattr(chord, OntoLast, track)
            g.add((chord, OntoLast, track))

        if prev_chord is not None:
            # setattr(prev_chord, OntoProperty, chord)
            g.add((prev_chord, OntoProperty, chord))
        
        prev_chord = chord

def hasFirstandLast_function(track_dict, OntoFirst, OntoLast, OntoChord,g):
    for key in track_dict:
        value_list = track_dict[key]
        if len(value_list) > 1:
            first_element = value_list[0]
            last_element = value_list[1]
        else:
            first_element = value_list[0]
            last_element = value_list[0]
        # setattr(key, OntoFirst, first_element)
        # setattr(key, OntoLast, last_element)
        g.add((key, OntoFirst, first_element))
        g.add((key, OntoLast, last_element))
        for j in value_list:
            # getattr(key, OntoChord).append(j)
            g.add((key,OntoChord,j))

# MODIFIED: Apply n-gram heuristics to chord progression generation
def findChordProgressions_with_ngrams(part_instance, elements, part_name, OntoPart, OntoFirst, OntoLast, OntoCounting, OntoChord, min_length, max_length, g, id, counter):
    # Convert chord instances to chord names for n-gram processing
    chord_names = []
    chord_instance_map = {}
    
    for i, chord_instance in enumerate(elements):
        # Extract chord name from the instance URI
        chord_name = str(chord_instance).split('_')[-2]  # Get the chord part before the counter
        # print(chord_name)
        chord_names.append(chord_name)
        chord_instance_map[i] = chord_instance
    
    # Generate n-grams using our heuristics
    chord_sequence = ' '.join(chord_names)
    # print(f"Processing chord sequence: {chord_sequence}")
    
    valid_ngrams = generate_ngrams_by_size(chord_sequence, min_length, max_length)
    # print("DEBUG valid_ngrams:", type(valid_ngrams), valid_ngrams)
    chord_progression_instances = []
    c = 1
    
    # Process each valid n-gram
    for n, ngrams in valid_ngrams.items():
        for ngram in ngrams:
            ngram_chords = ngram.split()
            
            # Find the starting position of this n-gram in the original sequence
            for start_pos in range(len(chord_names) - len(ngram_chords) + 1):
                if chord_names[start_pos:start_pos + len(ngram_chords)] == ngram_chords:
                    # Get the corresponding chord instances
                    current_combination = [chord_instance_map[start_pos + i] for i in range(len(ngram_chords))]
                    
                    # Create progression instance
                    progression_instance = mpo[f"{str(genres[id]) + '_'+ str(ids[id])}_{part_name}_{'ChordProgression'}_{c}"]
                    g.add((progression_instance, RDF.type, class_progression))
                    chord_progression_instances.append(progression_instance)
                    c += 1
                    
                    # Add relationships
                    g.add((part_instance, OntoPart, progression_instance))
                    first_element = current_combination[0]
                    last_element = current_combination[-1]
                    g.add((progression_instance, OntoFirst, first_element))
                    g.add((progression_instance, OntoLast, last_element))
                    
                    for j in current_combination:
                        g.add((progression_instance, OntoChord, j))
                        
                    chord_count_literal = Literal(len(current_combination))
                    g.add((progression_instance, OntoCounting, chord_count_literal))
                    counter += 1
                    break  # Only use the first occurrence of this n-gram
    
    return [(prog, len(chord_names)) for prog in chord_progression_instances], counter
start_time = time.time()
counter = 0
for i in range(len(ids)):
# for i in range(2):
    if i % 100 == 0:
        c_time = time.time()
        print(f"Elapsed time: {c_time-start_time:.2f} seconds")
        print(f"Estimated time: {(c_time-start_time)/(i+1)*600:.2f} seconds")
        print(f"Processed {i} tracks so far.")
    g = Graph()
    b = 0 #chord counter
    string_with_brackets = progressions[i]
    string_without_brackets = string_with_brackets.replace("[", "").replace("]", "")  # Step 1
    string_without_quotes = string_without_brackets.replace("'", "")  # Step 2
    final_string = string_without_quotes.replace(", ", " ")  # Step 3
    track_list = final_string.split()

    track_dict = {}
    current_key = None
    current_value = []

    # define instances!!!!!
    track_instance = mpo[str(genres[i]) + '_'+ str(ids[i])]
    g.add((track_instance, RDF.type, class_track))
    genre_instance = mpo[str(genres[i]).capitalize()]
    g.add((track_instance, has_genre, genre_instance))
  

  
    chord_count = {}
    part_count = {}
    dummy_part = ''
    for part in track_list:
        # dummy_part = ''

        if part.startswith('<'):
            new_part = part.replace('<','').replace('>','')
            if part not in part_count:
                part_count[part] = 1
            else:
                part_count[part] += 1
            if current_key is not None:
                track_dict[current_key] = current_value
            part_instance = mpo[f"{str(genres[i]) + '_'+ str(ids[i])}_{new_part}"]
            part_class = mpo[new_part.split("_")[0].capitalize()]
            g.add((part_instance, RDF.type, part_class))
            g.add((track_instance, mpo['has'+new_part.split("_")[0].capitalize()], part_instance))
            current_key = part_instance
            current_value = []
            dummy_part = part
        else:
            if part != dummy_part:
                if part not in chord_count:
                    chord_count[part] = 1
                else:
                    chord_count[part] += 1
                b +=1 
                part_instance = mpo[f"{str(genres[i]) + '_'+ str(ids[i])}_{part}_{b}"]
                part_class = fho[part]
                g.add((part_instance, RDF.type, part_class))
                current_value.append(part_instance)
                dummy_part = part

    if current_key is not None:
        track_dict[current_key] = current_value
    # print(track_dict)
    track_chord_progression = []
    for value_list in track_dict.values():
        track_chord_progression.extend(value_list)

    hasNext_function(track_instance,track_chord_progression, nx, is_first_track_chord, is_last_track_chord, g )
    hasNext_function(track_instance,track_dict.keys(), nx_part, None, None,g)
    hasFirstandLast_function(track_dict, has_first_part_chord, has_last_part_chord, has_part_chord,g)
    full_chord_progression_instances = []
    
    for part in track_dict:
        chords = track_dict[part]
        part_str = str(part)
        part_str_split = part_str.split('_')
        part_name = part_str_split[-2] + '_' + part_str_split[-1]
        chord_progression_instances = findChordProgressions_with_ngrams(part, chords, part_name, has_chord_progression, has_first_prog_chord, has_last_prog_chord,has_chord_count,has_prog_chord, 3, 8, g, i, counter)
       

    counter = chord_progression_instances[1]  # Update counter with the last value from the last progression

 

    # creating the RDFs for each track
    g.serialize(destination='your directory/' + str(genres[i]) + '_'+ str(ids[i]) + '.owl', format='xml')
    

print(counter)

