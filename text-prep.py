import time

import spacy

start_time = time.time()

def make_passes():

    print("Preprocessing the document. This may take several minutes...")

    nlp = spacy.load('en_core_web_sm')

    output_file = open("./processed.txt", mode='r+', encoding='utf-8')

    # text document cannot start halfway through a quote
    quotes = False
    incrementer = 40
    start_index = 0
    end_index = incrementer
    num_passes = 0
    while num_passes < 100:
        text = open(u"./input.txt", encoding="utf8", errors='ignore').read()[start_index:end_index]
        if text == '': # input file is empty
            break
        text = fix_unicode(text)
        # output_file.read()[end_index - 1:end_index - 1]
        text, quotes = preprocess(text, quotes, nlp)
        output_file.write(text)
        start_index += incrementer
        end_index += incrementer
        num_passes += 1

def fix_unicode(text):
    # Fix unicode quotation mark confusables
    text = text.replace(u"\u201C", "\"")
    text = text.replace(u"\u201D", "\"")
    return text

def remove_dialogue(text, quotes_continue):
    if quotes_continue == True and text.find('\"') == -1:
        return "", True # part of a quote and still continues
    elif quotes_continue == True and text[0] == '\"':
        return "", True
    elif quotes_continue == True:
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
            return text.replace('\n', ' ')
        else:
            return text.replace('\n', '')
    else:
        return text
    

def preprocess(text, quotes, nlp):
    doc = nlp(text)

    temp_doc_holder = nlp("")

    for sent in doc.sents:
        processed_sent, quotes = remove_dialogue(sent.text, quotes)
        if processed_sent == "":
            continue
        else:
            if text[len(text) - 1] == ' ':
                processed_sent = processed_sent + ' '
            processing_doc = nlp(temp_doc_holder.text + " " + remove_newline(processed_sent))
            temp_doc_holder = processing_doc
    
    if processed_sent == "":
        processing_doc = nlp("") 
        return processing_doc.text, quotes # text at beginning of read contained a quote
    elif processing_doc.text[0:2] == '  ':
        return processing_doc.text[1:], quotes # text starts with a space
    # elif processing_doc.text[0:1] == ' ':
    #     return processing_doc.text, quotes
    else:
        return processing_doc.text.lstrip(' '), quotes # no dialogue, no leading space

make_passes()
elapsed_time = time.time() - start_time
print("Elapsed Time: ", round(elapsed_time, 3), "s")

# doc.ents = [Span(doc, 0, 1, label=doc.vocab.strings[u'ORG'])]
