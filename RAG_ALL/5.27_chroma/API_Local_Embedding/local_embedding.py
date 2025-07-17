from modelscope import AutoTokenizer, AutoModel
import torch



def local_embedding(sentences):

    tokenizer = AutoTokenizer.from_pretrained('BAAI/bge-large-zh-v1.5')
    model = AutoModel.from_pretrained('BAAI/bge-large-zh-v1.5')
    model.eval()

    encoded_input = tokenizer(sentences, padding=True, truncation=True, return_tensors='pt')
    # padding 填充操作，使所有句子长度相同，不足的部分用0填充
    # truncation 截断操作，使所有句子长度不超过max_length，超过的部分被截断
    # return_tensors='pt' 返回的是张量：多维数组，在深度学习里，模型的输入、输出以及参数


    with torch.no_grad():
        # 关闭梯度计算，减少内存占用，加速计算
        model_output = model(**encoded_input)
        # **encoded_input 是将字典中的键值对作为参数传递给函数，这里是将encoded_input中的键值对作为参数传递给model
        sentence_embeddings = model_output[0][:, 0]
        # 输出元组的第一个元素，取所有行的第 0 列元素

    sentence_embeddings = torch.nn.functional.normalize(sentence_embeddings, p=2, dim=1)
    # 对句子向量进行归一化，p=2 表示使用 L2 范数，dim=1 表示对每一行进行归一化
    return sentence_embeddings.numpy().tolist()
    # 将张量转换为 numpy 数组，再转换为列表
   
if __name__ == '__main__':
    sentences = ["样例数据-1", "样例数据-2"]
    sentence_embeddings = local_embedding(sentences)
    