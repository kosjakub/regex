import os
from fastai.text import *
import sentencepiece as spm
from termcolor import colored


def highlighted(
    highlight,
    whole_text,
):
    return whole_text.replace(
    highlight, colored(highlight, color="green"))

fastai_model_path = "./work/up_low50k/models/fwd_v50k_finetune_lm_enc.h5"
sp_model = "./work/up_low50k/tmp/sp-50k.model" 
sentencepiece_vocab_path = "./work/up_low50k/tmp/sp-50k.vocab"

spm_processor = spm.SentencePieceProcessor()
spm_processor.Load(sp_model)


spm_processor.SetEncodeExtraOptions("bos:eos")
spm_processor.SetDecodeExtraOptions("bos:eos")

torch.cuda.set_device(0)

# "these parameters aren't used, but this is the easiest way to get a model" !!!!!!!!!!!!!!!!!!!!!!!! 
# https://github.com/fastai/fastai/blob/master/courses/dl2/imdb_scripts/predict_with_classifier.py

bptt = 5
max_seq = 1000000
n_tok = len(spm_processor)
emb_sz = 400
n_hid = 1150
n_layers = 4
pad_token = 1
bidir = False
qrnn = False

rnn_enc = MultiBatchRNN(bptt, max_seq, n_tok, emb_sz, n_hid, n_layers, pad_token=pad_token, bidir=bidir, qrnn=qrnn)
lm = SequentialRNN(rnn_enc, LinearDecoder(n_tok, emb_sz, 0, tie_encoder=rnn_enc.encoder))
lm = to_gpu(lm)
load_model(lm[0], fastai_model_path)
lm.reset()
lm.eval()

class TextDataset(Dataset):
    def __init__(self, x):
        self.x = x

    def __getitem__(self, idx):
        sentence = self.x[idx]
        return sentence[:-1], sentence[1:]


def next_word_(sentence, model): 
    ids = [np.array(spm_processor.encode_as_ids(sentence))]

    dataset = TextDataset(ids)
    sampler = SortSampler(ids, key=lambda x: len(ids[x]))
    dl = DataLoader(dataset,
                    pad_idx=1,
                    sampler=sampler)

    tensors = None
    with no_grad_context():
        for (x, y) in dl:
            tensors, _, _ = model(x)
            
    last_tensor = tensors[-1]

    best = int(torch.argmax(last_tensor))
    word = spm_processor.decode_ids([best])
    
    while not word.isalpha():
        last_tensor[best] = -1
        best = int(torch.argmax(last_tensor))
        word = spm_processor.decode_ids([best])

    return word


def next_word(sentence, new_words, model): 
    ids = [np.array(spm_processor.encode_as_ids(sentence))]
    new_words_ids = [np.array(spm_processor.encode_as_ids(new_words), dtype=int)]
    dataset = TextDataset(ids)
    sampler = SortSampler(ids, key=lambda x: len(ids[x]))
    dl = DataLoader(dataset,
                    batch_size=100,
                    transpose=True,
                    pad_idx=1,
                    sampler=sampler,
                    pre_pad=False)

    tensors = None
    with no_grad_context():
        for (x, y) in dl:
            tensors, _, _ = model(x)
            
    last_tensor = tensors[-1]
    best = int(torch.argmax(last_tensor))

    word = spm_processor.decode_ids([best])
    last_word = spm_processor.decode_ids([int(new_words_ids[0][-2])])
    while best in new_words_ids[0] or not word.isalpha() or (len(last_word) == 1 and word in ["a", "i", "o", "w", "z"]):
        last_tensor[best] = -1
        best = int(torch.argmax(last_tensor))
        word = spm_processor.decode_ids([best])
    return word

def extend_sentence(sentence, model, n_words):
    new_sentence = sentence
    new_words = " "
    for _ in range(n_words):
        new_ = next_word(new_sentence, new_words, model)
        new_words += " " + new_
        new_sentence += " " + new_
    return new_sentence


sentences = [
    "Warszawa to największe", "Te zabawki należą do",
    "Policjant przygląda się", "Na środku skrzyżowania widać",
    "Właściciel samochodu widział złodzieja z",
    "Prezydent z premierem rozmawiali wczoraj o", "Witaj drogi",
    "Gdybym wiedział wtedy dokładnie to co wiem teraz, to bym się nie",
    "Gdybym wiedziała wtedy dokładnie to co wiem teraz, to bym się nie",
    "Polscy naukowcy odkryli w Tatrach nowy gatunek istoty żywej. Zwięrzę to przypomina małpę, lecz porusza się na dwóch nogach i potrafi posługiwać się narzędziami. Przy dłuższej obserwacji okazało się, że potrafi również posługiwać się językiem polskim, a konkretnie gwarą podhalańską. Zwierzę to zostało nazwane",
    "Pan baton jest dzbanem",
    "Szymon się nie zna"
    ]
for sentence in sentences:
    print("[" + str(extend_sentence(sentence, lm, 30)) + "]" + '\n')
     

