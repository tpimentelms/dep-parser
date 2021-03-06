import numpy as np
import torch
import torch.nn as nn


class WordEmbedding(nn.Module):
    # pylint: disable=arguments-differ
    def __init__(self, vocab, embedding_size, pretrained=None):
        super().__init__()
        self.vocab = vocab
        self.vocab_size = vocab.size
        self.embedding_size = embedding_size

        if pretrained is not None:
            pretrained_tensor = self.dict2tensor(self.vocab_size, embedding_size, pretrained)
        else:
            pretrained_tensor = None

        self.embedding = nn.Embedding(self.vocab_size, self.embedding_size,
                                      _weight=pretrained_tensor, padding_idx=0)
        self.embedding.weight.requires_grad = False

    def dict2tensor(self, vocab_size, embedding_size, pretrained_dict):
        scale = np.sqrt(3.0 / embedding_size)
        pretrained = np.empty([vocab_size, embedding_size], dtype=np.float32)
        pretrained[:3, :] = np.random.uniform(
            - scale, scale, [3, embedding_size]).astype(np.float32) # Special symbols

        oov = 0
        for word, index in self.vocab.items():
            if word in pretrained_dict:
                embedding = pretrained_dict[word]
            elif word.lower() in pretrained_dict:
                embedding = pretrained_dict[word.lower()]
            else:
                embedding = np.random.uniform(-scale, scale, [1, embedding_size]).astype(np.float32)
                oov += 1
            pretrained[index, :] = embedding

        print('# OOV words: %d' % oov)
        return torch.from_numpy(pretrained)

    def forward(self, x):
        return self.embedding(x)
