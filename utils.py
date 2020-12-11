#!/usr/bin/env python
import os

known_signatures = {
    '5414F5EE': 'pup',
    '534C4232': 'slb2',
    '7F464948': 'fih',
    '7F434E54': 'cnt',
    '89504E47': 'png',
    '44445320': 'dds',
    '7B0D0A20': 'json',
    '706C6778': 'plgx',
    '7F524C43': 'rlc',
    '52494646': 'riff',
    'D2560102': 'ov',
    '00000001': 'toc',
}


def _create_working_dir(filename: str) -> str:
    
    directory = filename + '_extracted'
    try:
        os.mkdir(directory)
    except OSError:
        pass
    return directory


def _get_extension_by_signature(signature: str) -> str:
    
    return known_signatures.get(signature.upper(), 'unknown')

