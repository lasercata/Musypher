#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#--------------------------------
#
# Author            : Lasercata
# Last modification : 2024.07.26
# Version           : v1.0.0
#
#--------------------------------

'''Defining useful functions for graphs'''

#---Util
def try_to_convert_to_int_or_float(s: str|None) -> int|float|str|None:
    '''
    Try to convert `s` to an int, then to a float, and if all fail, return the string.
    Otherwise it returns the converted value.

    - s : the string to try to convert.
    '''

    if s == None:
        return s

    try:
        tmp = int(s)

        if tmp == float(s):
            ret = tmp
        else:
            raise ValueError

    except ValueError:
        try:
            ret = float(s)
        except ValueError:
            ret = s

    return ret

def format_data(data: dict) -> str:
    '''
    Formats the dict `data` in a string similar to json for the cypher dump

    - data : the dict to format.
    '''

    data_arr = []
    for k in data:
        if type(data[k]) not in (int, float, str): # Ignore attributes that are None and used internally (lists, ...)
            continue

        if k in ('id', 'id_'): # Do not try to convert id to a string
            d = data[k]
        else:
            d = try_to_convert_to_int_or_float(data[k])

        if k[-1] == '_': # changing id_ to id, class_ to class, type_ to type, ...
            k = k[:-1]

        if type(d) in (int, float):
            data_arr.append(f"{k}: {d}")
        # elif d == None:
        #     data_arr.append(f"{k}: 'null'")
        elif type(d) == str and "'" in d:
            data_arr.append(f'{k}: "{d}"')
        else:
            data_arr.append(f"{k}: '{d}'")

    data_str = '{' + ', '.join(data_arr) + '}'

    return data_str

#---Make create string
def make_create_string(cypher_id: str, type_: str, data: dict) -> str:
    '''
    Makes the CREATE clause for the cypher dump.

    - cypher_id  : the cypher id (mei id + '_' + inputfile) ;
    - type_      : the node type ('Fact', 'Event', ...) ;
    - data       : a dict with the data to write.
    '''

    data_str = format_data(data)

    return f'CREATE ({cypher_id}:{type_} {data_str})'

def make_create_link_string(id1: str, id2: str, type_: str, data: dict|None = None) -> str:
    '''
    Makes a CREATE clause that creates a link between `id1` and `id2`.

    - id1   : the cypher id of the first element to link ;
    - id2   : the cypher id of the second element to link.
    - type_ : the type of the link (e.g 'IS', 'HAS', 'NEXT', ...) ;
    - data  : the data to add on the link.
    '''

    if data == None:
        return f'CREATE (({id1})-[:{type_}]->({id2}))'

    data_str = format_data(data)
    return f'CREATE (({id1})-[:{type_} {data_str}]->({id2}))'
