from gensim.models import Word2Vec
import jieba

with open('docs.txt', 'r',encoding='utf-8') as file:
    content = file.read()
# print(content)

# 可以监视words，查看分词效果
words = list(jieba.cut(content))

sentences = [words]
model = Word2Vec(sentences,vector_size=100,window=5,min_count=1)
word = words[0]
if word in model.wv:
    vector = model.wv[word]
    print(f"词语'{word}'的词向量")
    print(vector)