


text = "Captain Adam Bolitho stood by the quarterdeck rail and watched the land edging out in a slow and final embrace. Buildings, even a church, were taking shape, and he saw a fishing lugger on a converging tack, a man climbing into the rigging to wave as the frigate’s shadow passed over him. How many hundreds of times had he stood in this place? As many hours as he had walked the deck, or been called from his cot for some emergency or other. Like the last time in Biscay, when a seaman had been lost overboard. It was nothing new. A familiar face, a cry in the night, then oblivion. Perhaps he, too, had been thinking of going home. Or leaving the ship. It only took a second; a ship had no forgiveness for carelessness or that one treacherous lapse of attention. He shook himself and gripped the scabbard of the old sword beneath his coat, something else he did without noticing it. He glanced along his command, the neat batteries of eighteen-pounders, each muzzle exactly in line with the gangway above it. The decks clean and uncluttered, each unwanted piece of cordage flaked down, while sheets and braces were loosened in readiness. The scars of that last savage battle at Algiers, a lifetime ago or so it felt sometimes, had been carefully repaired, painted or tarred, hidden except to the eye of the true sailor. A block squeaked and without turning his head he knew that the signals party had hoisted Unrivalled’s number. Not that many people would need telling. It was only then that you remembered."

text = "The ship went out to sea. the sea went in to the beach."

maxlen = 20
step = 5
sentences = []
next_chars = []
for i in range(0, len(text) - maxlen, step):
    sentences.append(text[i: i + maxlen])
    print("sentences...")
    print(sentences)
    next_chars.append(text[i + maxlen])
    print("next_chars...")
    print(next_chars)
print('nb sequences:', len(sentences))

text = "I saw him over"
maxlen = 10
start_index = 0
sentence = text[start_index: start_index + maxlen]
    
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