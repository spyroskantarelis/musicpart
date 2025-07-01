from owlready2 import *
from owlready2 import sync_reasoner
import itertools
from datetime import date, datetime


onto = get_ontology("http://purl.org/ontology/mpo/")

fho = onto.get_namespace('http://purl.org/ontology/fho/')

genres = ['blues','folk','hip_hop','house','indie','jazz','metal','pop',
         'punk','rap','reggae','rock','soul','pop_rock','alternative','country','electronic']

parts = ['Intro','Verse','Chorus','Outro','Bridge','Instrumental','Interlude','Solo']

with onto:


    # class definition
    class Track(Thing):
        pass
    class Genre(Thing):
        pass
    class Part(Thing):
        pass
    class TrackPart(Part):
        pass
    
    # create genre instances
    for genre in genres:
        genre_instance = Genre(genre)
    
    # define part classes
    # for part in parts:
    #     subpart = types.new_class(part, (Part,))

    class Intro(Part):
        pass
    class Verse(Part):
        pass
    class Chorus(Part):
        pass
    class Outro(Part):
        pass
    class Bridge(Part):
        pass
    class Instrumental(Part):
        pass
    class Interlude(Part):
        pass
    class Solo(Part):
        pass
    class ChordProgression(Thing):
        pass
    class TrackChordProgression(ChordProgression):
        pass
    class Chord(Thing):
        namespace = fho
        pass
    class Chord(Thing):
        equivalent_to = [Chord]

    class isChordProgressionof(ObjectProperty):
        domain = [ChordProgression]
        range = [Part]
        pass
    class hasChordProgression(ObjectProperty):
        domain = [Part]
        range = [ChordProgression]
        inverse_property = isChordProgressionof
        pass


    # properties definition

    # release date

    class hasReleaseDate(DataProperty, FunctionalProperty):
        domain = [Track]
        range = [datetime]
        pass
    
    # genres

    class isGenreof(ObjectProperty):
        domain = [Genre]
        range = [Track]
        pass
    class hasGenre(ObjectProperty):
        domain = [Track]
        reange = [Genre]
        inverse_property = isGenreof
        pass

    # parts


    class isPartof(ObjectProperty):
        domain = [Part]
        range = [Track]
        pass
    class hasPart(ObjectProperty):
        domain = [Track]
        range = [Part]
        inverse_property = isPartof
        pass

    class isIntroof(ObjectProperty, isPartof):
        domain = [Intro]
        range = [Track]
        pass
    class hasIntro(ObjectProperty, hasPart):
        domain = [Track]
        range = [Intro]
        inverse_property = isIntroof
        pass

    class isVerseof(ObjectProperty, isPartof):
        domain = [Verse]
        range = [Track]
        pass
    class hasVerse(ObjectProperty, hasPart):
        domain = [Track]
        range = [Verse]
        inverse_property = isVerseof
        pass


    class isChorusof(ObjectProperty, isPartof):
        domain = [Chorus]
        range = [Track]
        pass
    class hasChorus(ObjectProperty, hasPart):
        domain = [Track]
        range = [Chorus]
        inverse_property = isChorusof
        pass


    class isOutroof(ObjectProperty, isPartof):
        domain = [Outro]
        range = [Track]
        pass
    class hasOutro(ObjectProperty, hasPart):
        domain = [Track]
        range = [Outro]
        inverse_property = isOutroof
        pass


    class isBridgeof(ObjectProperty, isPartof):
        domain = [Bridge]
        range = [Track]
        pass
    class hasBridge(ObjectProperty, hasPart):
        domain = [Track]
        range = [Bridge]
        inverse_property = isBridgeof
        pass

    class isInstrumentalof(ObjectProperty, isPartof):
        domain = [Instrumental]
        range = [Track]
        pass
    class hasInstrumental(ObjectProperty, hasPart):
        domain = [Track]
        range = [Instrumental]
        inverse_property = isInstrumentalof
        pass

    class isInterludeof(ObjectProperty, isPartof):
        domain = [Interlude]
        range = [Track]
        pass
    class hasInterlude(ObjectProperty, hasPart):
        domain = [Track]
        range = [Interlude]
        inverse_property = isInterludeof
        pass

    class isSoloof(ObjectProperty, isPartof):
        domain = [Solo]
        range = [Track]
        pass
    class hasSolo(ObjectProperty, hasPart):
        domain = [Track]
        range = [Solo]
        inverse_property = isSoloof
        pass


    ## first,last and chords
    # track
    class isFirstTrackChordof(ObjectProperty, FunctionalProperty):
        domain = [Chord]
        range = [Track]
        pass
    class hasFirstTrackChord(ObjectProperty, FunctionalProperty):
        domain = [Track]
        range = [Chord]
        inverse_property = isFirstTrackChordof
        pass
    class isLastTrackChordof(ObjectProperty, FunctionalProperty):
        domain = [Chord]
        range = [Track]
        pass
    class hasLastTrackChord(ObjectProperty, FunctionalProperty):
        domain = [Track]
        range = [Chord]
        inverse_property = isLastTrackChordof
        pass
    # part
    class isFirstPartChordof(ObjectProperty, FunctionalProperty):
        domain = [Chord]
        range = [Part]
        pass
    class hasFirstPartChord(ObjectProperty, FunctionalProperty):
        domain = [Part]
        range = [Chord]
        inverse_property = isFirstPartChordof
        pass
    class isLastPartChordof(ObjectProperty, FunctionalProperty):
        domain = [Chord]
        range = [Part]
        pass
    class hasLastPartChord(ObjectProperty, FunctionalProperty):
        domain = [Part]
        range = [Chord]
        inverse_property = isLastPartChordof
        pass
    # prog
    class isFirstProgChordof(ObjectProperty):
        domain = [Chord]
        range = [ChordProgression]
        pass
    class hasFirstProgChord(ObjectProperty, FunctionalProperty):
        domain = [ChordProgression]
        range = [Chord]
        inverse_property = isFirstProgChordof
        pass
    class isLastProgChordof(ObjectProperty):
        domain = [Chord]
        range = [ChordProgression]
        pass
    class hasLastProgChord(ObjectProperty, FunctionalProperty):
        domain = [ChordProgression]
        range = [Chord]
        inverse_property = isLastProgChordof
        pass
    
    
    # content chords
    class isProgChordof(ObjectProperty):
        domain = [Chord]
        range = [ChordProgression]
        pass
    class hasProgChord(ObjectProperty):
        domain = [ChordProgression]
        range = [Chord]
        inverse_property = isProgChordof
        pass
    class isPartChordof(ObjectProperty):
        domain = [Chord]
        range = [Part]
        pass
    class hasPartChord(ObjectProperty):
        domain = [Part]
        range = [Chord]
        inverse_property = isPartChordof
        pass
    # dummy data property
    class hasChordCount(DataProperty, FunctionalProperty):
        domain = [ChordProgression]
        range = [int]
        pass

    ## chain properties
    # parts
    class isFollowedByPart(ObjectProperty, TransitiveProperty):
        domain = [Part]
        range = [Part]
        pass
    class isFollowingPart(ObjectProperty, TransitiveProperty):
        domain = [Part]
        range = [Part]
        inverse_property = isFollowedByPart
        pass
    class hasNextPart(ObjectProperty, FunctionalProperty, isFollowedByPart):
        domain = [Part]
        range = [Part]
        pass
    class hasPreviousPart(ObjectProperty, FunctionalProperty, isFollowingPart):
        domain = [Part]
        range = [Part]
        inverse_property = hasNextPart
        pass
    
    # chords
    class hasNext(ObjectProperty, FunctionalProperty):
        namespace = fho
        pass
    class hasPrevious(ObjectProperty, FunctionalProperty):
        namespace = fho
        pass

    class isFollowedByChord(ObjectProperty, TransitiveProperty):
        domain = [Chord]
        range = [Chord]
        pass
    class isFollowingChord(ObjectProperty, TransitiveProperty):
        domain = [Chord]
        range = [Chord]
        inverse_property = isFollowedByChord
        pass
    class hasNextChord(ObjectProperty, FunctionalProperty, isFollowedByChord):
        domain = [Chord]
        range = [Chord]
        equivalent_to = [hasNext]
        pass
    class hasPreviousChord(ObjectProperty, FunctionalProperty, isFollowingChord):
        domain = [Chord]
        range = [Chord]
        inverse_property = hasNextChord
        equivalent_to = [hasPrevious]
        pass
    
    # chord progressions
    class isFollowedByChordProgression(ObjectProperty, TransitiveProperty):
        domain = [ChordProgression]
        range = [ChordProgression]
        pass
    class isFollowingChordProgression(ObjectProperty, TransitiveProperty):
        domain = [ChordProgression]
        range = [ChordProgression]
        inverse_property = isFollowedByChordProgression
        pass
    class hasNextChordProgression(ObjectProperty, TransitiveProperty, isFollowedByChordProgression):
        domain = [ChordProgression]
        range = [ChordProgression]
        pass
    class hasPreviousChordProgression(ObjectProperty, TransitiveProperty, isFollowingChordProgression):
        domain = [ChordProgression]
        range = [ChordProgression]
        inverse_property = hasNextChordProgression
        pass

    rule = Imp()
    rule.set_as_rule(""" ChordProgression(?x), hasLastProgChord(?x, ?y),hasNextChord(?y, ?z), isFirstProgChordof(?z, ?w) -> hasNextChordProgression(?x, ?w)""")



sync_reasoner(infer_property_values = True)
onto.save(file = "mpo.owl")
