import spacy

read = open(u"./input.txt", encoding="utf8", errors='ignore').read()

# Fix unicode quotation mark confusables
text_input = read.replace(u"\u201C", "\"")
text_input = text_input.replace(u"\u201D", "\"")

nlp = spacy.load('en_core_web_sm')
doc = nlp(text_input)

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
        if rest_of_text.find('\"') >= 0:
            return "", False # we found a closing quotation mark
        elif rest_of_text[0] == '\n':
            return "", False # end of a quote that started earlier
        else:
            return "", True
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
    

def preprocess(doc):
    temp_doc_holder = ""
    _quotes = False

    for sent in doc.sents:
        processed_sent, _quotes = remove_dialogue(sent.text, _quotes)
        if processed_sent == "":
            continue
        else:
            processing_doc = nlp(temp_doc_holder + " " + remove_newline(processed_sent))
            temp_doc_holder = processing_doc.text
            # temp_doc_holder = processing_doc.text # need to change into doc with nlp, just text right now
    
    open("./output.txt", mode='w', encoding='utf-8').write(processing_doc.text)

    return processing_doc

print("Processed document is:", preprocess(doc))

# doc.ents = [Span(doc, 0, 1, label=doc.vocab.strings[u'ORG'])]
