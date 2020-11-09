import os
import jieba
import jieba.posseg as pseg
import re
import jieba.analyse


class Segment(object):
    def __init__(self, stopword_files=[], userdict_files=[], jieba_tmp_dir=None):
        if jieba_tmp_dir:
            jieba.dt.tmp_dir = jieba_tmp_dir
            if not os.path.exists(jieba_tmp_dir):
                os.makedirs(jieba_tmp_dir)

        self.stopwords = set()
        for stopword_file in stopword_files:
            with open(stopword_file, "r", encoding="utf-8") as rf:
                for row in rf.readlines():
                    word = row.strip()
                    if len(word) > 0:
                        self.stopwords.add(word)

        for userdict in userdict_files:
            jieba.load_userdict(userdict)

    def cut(self, text):
        word_list = []
        text.replace('\n', '').replace('\u3000', '').replace('\u00A0', '')
        text = re.sub('[a-zA-Z0-9.。:：,，]', '', text)
        words = pseg.cut(text)

        for word in words:
            # print(word.word, word.flag)
            word = word.strip()
            if word in self.stopwords or len(word) == 0:
                continue
            word_list.append(word)

        return word_list

    def extract_keyword(self, text, algorithm='tfidf', use_pos=True):
        text = re.sub('[a-zA-Z0-9.。:：,，]', '', text)
        if use_pos:
            allow_pos = ('n', 'nr', 'ns', 'vn', 'v')
        else:
            allow_pos = ()

        if algorithm == 'tfidf':
            tags = jieba.analyse.extract_tags(text, withWeight=False)
            return tags
        elif algorithm == 'textrank':
            textrank = jieba.analyse.textrank(text, withWeight=False, allowPOS=allow_pos)
            return textrank


# if __name__ == '__main__':
#     seg = Segment(stopword_files=[], userdict_files=[])
#     text = "孙新军介绍，北京的垃圾处理能力相对比较宽松，全市有44座处理设施，总设计能力是每天处理3.2万吨，焚烧场11座，处理能力是1.67万吨每天，生化设施23座，日处理能力达8130吨，包括餐饮单位厨余垃圾日处理能力2380吨，家庭厨余垃圾日处理能力5750吨。"
#     textrank = seg.extract_keyword(text,algorithm='textrank', use_pos=True)[:10]
#     tfidfs = seg.extract_keyword(text,algorithm='tfidf', use_pos=True)[:10]
#     print(textrank)
#     print(tfidfs)
#     print(set(textrank) & set(tfidfs))
