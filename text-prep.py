import time

import spacy

start_time = time.time()

def make_passes():

    print("Preprocessing the document. This may take several minutes...")

    nlp = spacy.load('en_core_web_sm')

    output_file = open("./processed.txt", mode='r+', encoding='utf-8')

    start_index = 0
    end_index = 5000
    num_passes = 0
    while num_passes < 100:
        text = open(u"./source-gaunt-unprepared.txt", encoding="utf8", errors='ignore').read()[start_index:end_index]
        if text == '': # input file is empty
            break
        text = fix_unicode(text)
        # output_file.read()[end_index - 1:end_index - 1]
        output_file.write(preprocess(text, nlp))
        start_index += 5000
        end_index += 5000
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
                return "", True
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
    

def preprocess(text, nlp):
    doc = nlp(text)

    temp_doc_holder = nlp("")
    _quotes = False

    for sent in doc.sents:
        processed_sent, _quotes = remove_dialogue(sent.text, _quotes)
        if processed_sent == "":
            continue
        else:
            processing_doc = nlp(temp_doc_holder.text + " " + remove_newline(processed_sent))
            temp_doc_holder = processing_doc
    
    # open("./output.txt", mode='a', encoding='utf-8').write(processing_doc.text)
    if processed_sent == "":
        processing_doc = nlp("")
        return processing_doc.text
    elif processing_doc.text[0:2] == '  ':
        return processing_doc.text[1:]
    else:
        return processing_doc.text.lstrip(' ')

make_passes()
elapsed_time = time.time() - start_time
print("Elapsed Time: ", round(elapsed_time, 3), "s")

# doc.ents = [Span(doc, 0, 1, label=doc.vocab.strings[u'ORG'])]
