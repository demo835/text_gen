import spacy

read = open(u"./input.txt", encoding="utf8", errors='ignore').read()

text_input = read.replace(u"\u201C", "\"")
text_input = text_input.replace(u"\u201D", "\"")

nlp = spacy.load('en_core_web_sm')
doc = nlp(text_input)

def has_quotes(text, quotes_continue):
    if quotes_continue == True and text.find('\"') == -1:
        return "", True # part of a quote and still continues
    elif quotes_continue == True:
        return "", False

    start_index = text.find('\"')
    if start_index >= 0:
        rest_of_text = text[start_index + 1 : len(text)]
        if rest_of_text.find('\"') >= 0:
            return "", False # we found a closing quotation mark
        else:
            return "", True
    else:
        return text, False

def false_newline(text):
    start_index = text.find('\n')
    if start_index >= 0:
        if text[start_index + -1] != "." and text[start_index + -1] != "?" and text[start_index + -1] != "!":
            return text.replace('\n', ' ')
    

def preprocess(doc):
    processing_doc = doc
    temp_doc_holder = ""
    _quotes = False

    for sent in doc.sents:
        processed_sent, _quotes = has_quotes(sent.text, _quotes)
        if processed_sent == "":
            continue
        else:
            # processing_doc = nlp(temp_doc_holder + " " + processed_sent)
            processing_doc = temp_doc_holder + " " + false_newline(processed_sent)
            temp_doc_holder = processing_doc
            # temp_doc_holder = processing_doc.text # need to change into doc with nlp, just text right now
    
    doc = nlp(processing_doc)

    # for sent in doc.sents:
    #     temp_doc_holder = false_newline(sent)


    open("./output.txt", mode='w', encoding='utf-8').write(processing_doc.text)

    return processing_doc

# print("Processed document is ", preprocess(doc))
print("Processed document is ", false_newline(doc.text))

# doc.ents = [Span(doc, 0, 1, label=doc.vocab.strings[u'ORG'])]
