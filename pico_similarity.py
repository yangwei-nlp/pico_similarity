"""
Description :   
     Author :   Yang
       Date :   2019/11/26
"""
import re
input_sentence = ''
with open('pico_sentence.txt', 'r', encoding='utf-8-sig') as file:
    lines = file.readlines()
    for line in lines:
        # print(line.strip())
        if line.strip() == '':
            continue
        input_sentence = input_sentence + line.strip() + ' '
    # print(input_sentence)


file_dir = 'pubmed_result Straube_et_al-2014.txt'
# 规律：txt内容是以三个换行符为分割的，
# 不过好几个例外：PMID: 14286205  [Indexed for MEDLINE]，这种需要过滤掉
with open(file_dir, 'r', encoding='utf-8-sig') as file:
    all_the_text = file.read()
    # print(all_the_text)
    corpus = all_the_text.split('\n\n\n')

corpus = [text for text in corpus if not text.startswith('PMID')]  # index和title序号相等
print(corpus)


