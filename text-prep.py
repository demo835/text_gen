import time

import spacy

start_time = time.time()

def make_passes():

    print("Preprocessing the document. This may take several minutes...")

    nlp = spacy.load('en_core_web_sm')

    output_file = open("./processed.txt", mode='r+', encoding='utf-8')

    # text document cannot start halfway through a quote
    quotes_continue = False
    incrementer = 200
    start_index = 0
    end_index = incrementer
    num_passes = 0
    while num_passes < 200:
        text = open(u"./input.txt", encoding="utf8", errors='ignore').read()[start_index:end_index]
        clip_index = text.rfind(".") + 1
        start_index = start_index + clip_index
        end_index = start_index
        text = text[0:clip_index]
        if text == '':
            break # stop making passes over doc when text is empty
        text = fix_unicode(text)
        text, quotes_continue = preprocess(text, quotes_continue, nlp)
        output_file.write(text)
        # start_index += incrementer
        end_index += incrementer
        num_passes += 1
        print("We've made ", num_passes, " passes", end='\r')

def fix_unicode(text):
    # Fix unicode quotation mark confusables
    text = text.replace(u"\u201C", "\"").replace(u"\u201D", "\"")
    return text

def remove_dialogue(text, quotes_continue):
    # if quotes_continue == True and text.find('\"') == -1:
    #     return "", True # part of a quote and still continues
    # elif quotes_continue == True and text[0] == '\"':
    #     return "", True
    # elif quotes_continue == True:
    #     return "", False
    
    if quotes_continue == True:
        if text.find('\"') == -1 or text[0] == '\"':
            return "", True
        else:
            return "", False

    start_index = text.find('\"')
    if start_index >= 0:
        rest_of_text = text[start_index + 1 : len(text)]
        try:
            if rest_of_text.find('\"') >= 0:
                return "", False # we found a closing quotation mark
            elif rest_of_text[0] == '\n':
                return "", False # end of a quote that started earlier
            else:
                return "", True # quote opens but does not close
        except IndexError:
            return "", False
    else:
        return text, False

def remove_newline(text):
    start_index = text.find('\n')
    if start_index >= 0:
        if text[start_index + -1] != "." and text[start_index + -1] != "?" and text[start_index + -1] != "!":
            return text.replace('\n', ' ') # fix the rare middle-of-sentence newlines
        else:
            return text.replace('\n', '')
    else:
        return text
    

def preprocess(text, quotes_continue, nlp):
    doc = nlp(text)

    temp_doc_holder = nlp("")

    for sent in doc.sents:
        sent, quotes_continue = remove_dialogue(sent.text, quotes_continue)
        if sent == "":
            continue
        # else:
        if text[len(text) - 1] == ' ':
            sent = sent + ' '
        temp_doc_holder = nlp(temp_doc_holder.text + " " + remove_newline(sent))
        # temp_doc_holder = doc
    
    if doc.text[0:2] == '  ':
        return temp_doc_holder.text[1:], quotes_continue # text starts with a space
    else:
        # return temp_doc_holder.text.lstrip(' '), quotes_continue # no dialogue, no leading space
        return temp_doc_holder.text, quotes_continue

make_passes()
elapsed_time = time.time() - start_time
print("\nElapsed Time: ", round(elapsed_time, 3), "s")

# doc.ents = [Span(doc, 0, 1, label=doc.vocab.strings[u'ORG'])]

# KNOWN BUGS:
# Dialogue at beginning of file. Especially if text starts with an open quote
