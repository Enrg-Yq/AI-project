from modelscope import AutoTokenizer, AutoModel
import torch



def local_embedding(sentences):

    tokenizer = AutoTokenizer.from_pretrained('BAAI/bge-large-zh-v1.5')
    model = AutoModel.from_pretrained('BAAI/bge-large-zh-v1.5')
    model.eval()

    encoded_input = tokenizer(sentences, padding=True, truncation=True, return_tensors='pt')

    with torch.no_grad():
        model_output = model(**encoded_input)
        sentence_embeddings = model_output[0][:, 0]

    sentence_embeddings = torch.nn.functional.normalize(sentence_embeddings, p=2, dim=1)
    # print("Sentence embeddings:", sentence_embeddings.numpy().tolist())[0]
    return sentence_embeddings.numpy().tolist()

if __name__ == '__main__':
    sentences = ["样例数据-1", "样例数据-2"]
    sentence_embeddings = local_embedding(sentences)
    