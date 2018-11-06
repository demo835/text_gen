#! python3

from textgenrnn import textgenrnn

textgen = textgenrnn(weights_path='gaunt_weights.hdf5', vocab_path='gaunt_vocab.json', config_path='gaunt_config.json')

textgen.generate_samples(max_gen_length=1000)
textgen.generate_to_file('generated.txt', max_gen_length=1000)