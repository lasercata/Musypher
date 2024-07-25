#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#--------------------------------
#
# Author            : Lasercata
# Last modification : 2024.07.25
# Version           : v1.0.0
#
#--------------------------------

'''Represent the Fact nodes in the graph (notes)'''

##-Import
from src.graph.utils_graph import make_create_string

##-Main
class Fact:
    '''Represent a `Fact` node (note)'''

    def __init__(self, source, id_, type_, class_, octave, duration, accid=None, accid_ges=None, syllable=None, instrument=None):
        '''
        Initate Fact.

        - source     : the name of the source file ;
        - id_        : the id of the fact ;
        - type_      : the type of the fact. Can be 'note', 'rest' ;
        - class_     : the class of the note (e.g 'c', 'd', ...). Set it to None for a rest ;
        - octave     : the octave of the note ;
        - duration   : the duration of the note (1 for whole, 2 for half, 4 for fourth, ...) ;
        - accid      : None if no accidental on the note, 's' for sharp, and 'f' for flat ;
        - accid_ges  : same as above, but represent an accidental on the staff, not on the note ;
        - syllable   : the potential syllable pronounced on this note (None if none) ;
        - instrument : the instrument.
        '''

        self.source = source
        self.id_ = id_
        self.type_ = type_
        self.class_ = class_
        self.octave = octave
        self.dur = duration
        self.accid = accid
        self.accid_ges = accid_ges
        self.syllable = syllable
        self.instrument = instrument

        self._check();
        self._calculate_other_values();

    def _calculate_other_values(self):
        '''Calculate the other needed values.'''

        self.input_file = self.source.replace('.mei', '_mei')
        self.cypher_id = self.id_ + '_' + self.input_file

        self.name = self.class_.upper() + str(self.octave)
        self.duration = 1 / self.dur

        #TODO: calculate frequency, half_tones_from_a4, half_tones_diatonic_from_a4, alteration_in_tones, alteration_in_half_tones.

    def _check(self):
        '''
        Ensures that the given attributes make sense.
        Raise a ValueError otherwise.
        '''
    
        if self.type_ not in ('note', 'rest'):
            raise ValueError(f'Fact: `type_` attribute has to be "note" or "rest", but not "{self.type_} !"')

        if self.type_ == 'note' and self.class_ not in 'abcdefg':
            raise ValueError(f'Fact: `class_` attribute has to be in (a, b, c, d, e, f, g), but not "{self.class_} !"')

        if type(self.octave) != int or self.octave < 0 or self.octave > 9: #TODO: I am not certain of the boundaries
            raise ValueError(f'Fact: `octave` attribute has to be an int, but not "{self.octave} !"')

        if type(self.duration) not in (int, float) or self.duration < 0:
            raise ValueError(f'Fact: `duration` attribute has to be a float, but not "{self.duration} !"')

        if type(self.accid) not in (None, 's', 'f'):
            raise ValueError(f'Fact: `accid` attribute has to be in (None, "s", "f"), but "{self.accid} was found !"')

        if type(self.accid_ges) not in (None, 's', 'f'):
            raise ValueError(f'Fact: `accid_ges` attribute has to be in (None, "s", "f"), but "{self.accid_ges} was found !"')

    def to_cypher(self) -> str:
        '''Returns the CREATE cypher clause'''
    
        return make_create_string(self.cypher_id, 'Fact', self.__dict__)

