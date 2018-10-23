import spacy

text_all = "\"Yes, of course, sir!\" Larkin said. \"Follow Domor’s team out into the field. Feygor? Form up a five-man intruder team around Larkin. Get another sniper in there if you can. Move out down the swept corridor and give the sweeper boys cover. Use the reduced range to do some real damage. I want officers and commanders picked out and killed.\" \"Don’t we all, major,\" replied Feygor as he leapt up to obey. The voice of Rawne’s adjutant had always been deep and gravelly, but ever since the final fight for Veyveyr Gate, he’d spoken through a voicebox deformed and twisted with las-burn scar tissue. He was permanently monotone and deadpan. The captain said, \"Bring me the treasure.\" And the sailor did so. \"Here you go.\" \"What’s going on?\" Bragg asked. No one heard. \"My squad returned not half an hour ago,\" Rawne said smoothly. \"The Bluebloods.\""


# open("./output.txt", mode='w', encoding='utf-8').write(text_input)

properly_encoded_text = open(u"./output.txt", encoding="utf8", errors='ignore').read()

text_input = properly_encoded_text.replace(u"\u201C", "\"")
text_input = text_input.replace(u"\u201D", "\"")


nlp = spacy.load('en_core_web_sm')
doc = nlp(text_input)

remove_these = ["said"
               ,"asked"
               ,"replied"
               ,]


def remove_said(text):
    for word in remove_these:
        while text.find(word) >= 0:
            start_index = text.find(word)
            # print("start_index is ", start_index)
            for i, char in enumerate(text[start_index + len(word) : len(text)]):
                if char == "." or char == "!" or char == "?":
                    # print("i is ", i)
                    # print("char is ", char)
                    end_index = i + start_index + len(word)
                    # print("end_index is ", end_index)
                    text = text[0 : start_index-1] + text[end_index : len(text)]
                    # print("text is ", text)
                    break
    return text

def preprocess(text):
    print("Preprocessing text. This may take a few minutes...")
    # for char in text:
    #     print(char)
    _quotes = False

    for sent in doc.sents:
        print("Original text: ", sent.text)
        sent.text,_quotes = remove_quotes(sent.text, _quotes)
        print("Processed text: ", )
        print("Quotes will continue from this text?", _quotes)
        o2 = remove_said(doc.sents[sent])
        print("Final processed text: ", o2)






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


processing_doc = doc
temp_doc_holder = ""
_quotes = False

for sent in doc.sents:
    processed_sent, _quotes = has_quotes(sent.text, _quotes)
    if processed_sent == "":
        continue
    else:
        # temp_doc_holder = processed_sent
        processing_doc = nlp(temp_doc_holder + " " + processed_sent)
        temp_doc_holder = processing_doc.text
        print("processing_doc is ", processing_doc)


# doc.ents = [Span(doc, 0, 1, label=doc.vocab.strings[u'ORG'])]
