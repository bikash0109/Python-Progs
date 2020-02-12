from __future__ import division
import os,sys,re,math

fname2content = {}
print("Number of documents loaded: ", len(fname2content))
print(fname2content["17_9.txt"][:500])

total_token_num=0
print("Total Number of tokens: ", total_token_num)

examples = ["Hello, we are good.",  "OK... I'll go here, ok?"]

print("Naive tokenizations")
for example in examples:
    print(example.split())


def better_tokenizer(text):
    return []

print("Better tokenizations")
for example in examples:
    print(better_tokenizer(example))

word_counts = {}