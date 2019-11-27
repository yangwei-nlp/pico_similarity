"""
Description :   
     Author :   Yang
       Date :   2019/11/26
"""
from sklearn.metrics.pairwise import cosine_similarity
import os
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, TfidfTransformer


def read_data(dir1, dir2):
    """
    :param dir1:
    :param dir2:
    :return:
    """
    input_sentence = ''
    with open(dir1, 'r', encoding='utf-8-sig') as file:
        lines = file.readlines()
        for line in lines:
            # print(line.strip())
            if line.strip() == '':
                continue
            input_sentence = input_sentence + line.strip() + ' '
        # print(input_sentence)

    # 规律：txt内容是以三个换行符为分割的，
    # 不过好几个例外：PMID: 14286205  [Indexed for MEDLINE]，这种需要过滤掉
    with open(dir2, 'r', encoding='utf-8-sig') as file:
        all_the_text = file.read()
        # print(all_the_text)
        corpus = all_the_text.split('\n\n\n')
    corpus = [text for text in corpus if not text.startswith('PMID')]  # index和title序号相等
    return input_sentence, corpus


def compute_func(input_name, input_sentence, corpus, top_k=10):
    """利用 bert 词向量计算文本相似度"""
    from bert_serving.client import BertClient

    bc = BertClient(ip='172.29.231.5', output_fmt='list', check_version=False)
    # bc.encode(['First do it', 'then do it right', 'then do it better'])

    corpus_deal = [text.replace('\n', '') for text in corpus]
    embed_vecs = bc.encode(corpus_deal)
    input_vec = bc.encode([input_sentence])

    similarities = cosine_similarity(input_vec, embed_vecs)[0]
    top_k_idx = similarities.argsort()[::-1][0: top_k]

    prefix = input_name.split('/')[0] + '/' + input_name.split('/')[1] + '/'
    file_name = prefix + 'predict ' + input_name.split('/')[-1].split('input-')[1]
    with open(file_name, 'w', encoding='utf-8-sig') as file:
        for rank, idx in enumerate(top_k_idx):
            file.write('------------- Rank: {},  Paper Title: {} ----------------\n'.format(rank + 1, idx + 1))
            file.write(corpus[idx])
            file.write('\n\n\n')


def compute_func_v2(dir1, input_sentence, corpus):
    """使用 TF-IDF 计算文本相似度"""
    # 1. 得到词典
    vectorizer = TfidfVectorizer()
    vectorizer.fit_transform(corpus + [input_sentence])
    # 2. 得到 TF-IDF 矩阵

    # 3. 计算相似度值


def compute_all(files_dir='data/'):
    for dir in os.listdir(files_dir):
        tmp = files_dir + dir + '/'
        files = os.listdir(tmp)

        dir1 = tmp + [name for name in files if name.startswith('input-')][0]  # 输入pico
        dir2 = tmp + [name for name in files if name.startswith('corpus-')][0]  # 输入该pico的论文库
        input_sentence, corpus = read_data(dir1, dir2)
        compute_func(dir1, input_sentence, corpus)


if __name__ == "__main__":
    compute_all()
