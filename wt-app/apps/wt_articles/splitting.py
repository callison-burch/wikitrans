#!/usr/bin/env python


from wt_languages.models import LANGUAGE_CHOICES

import sys
import re
import nltk.data

def determine_splitter(language):
    if language == 'ur':
        return urdu_split_sentences

    for desc_pair in LANGUAGE_CHOICES:
        if desc_pair[0] == language:
            tokenizer = 'tokenizers/punkt/%s.pickle' % (desc_pair[1].lower())
            break
    try:
        tokenizer = nltk.data.load(tokenizer)
        return tokenizer.tokenize
    except:
        raise AttributeError('%s not supported by sentence splitters' % (language))

def urdu_split_sentences(text):
    DASH = u'\u06D4' # arabic full stop
    QUESTION = u'\u061F'
    ELLIPSIS = u'\u2026'
    FULL_STOP = u'\u002e'
    BULLET = u'\u2022'

    # break on multiple newline characters
    multiple_newlines = re.compile('\s*\n+\n+|\n+\s+\n+')
    text = multiple_newlines.sub('MULTIPLENEWLINESPLACEHOLDER', text)  

    initial_whitespace = re.compile('^\s+')
    text = initial_whitespace.sub('', text)    

    whitespace = re.compile('\s+')
    text = whitespace.sub(' ', text)

    split_after = u'([%s|%s|%s|%s])' % (QUESTION, ELLIPSIS, FULL_STOP, DASH)
    p = re.compile(split_after, re.VERBOSE)
    text = p.sub(r'\1\n', text)

    split_before = u'([%s])' % (BULLET)
    p = re.compile(split_before, re.VERBOSE)
    text = p.sub(r'\n\1', text)

    multiple_newlines_placeholder = re.compile('MULTIPLENEWLINESPLACEHOLDER')
    text = multiple_newlines_placeholder.sub('\n', text)
    text = multiple_newlines.sub('\n', text)    

    sentences = []
    for sentence in text.split('\n'):
       sentence = sentence.strip()
       if not sentence == '':
           sentences.append(sentence)

    return sentences 
