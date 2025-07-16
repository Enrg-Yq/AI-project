# import warnings
# warnings.filterwarnings("ignore", message="pkg_resources is deprecated as an API")

# from modelscope.pipelines import pipeline
# from modelscope.utils.constant import Tasks
# from datasets.data_files import (
#     get_data_patterns,
# )
# # 使用 ModelScope 提供的标准模型
# model_id = 'ccutwuxiao/bert-chinese-sentiment-c3-v1'
# text_classification_pipeline = pipeline(Tasks.text_classification, model=model_id)

# # 输入文本
# text = "这是一个正面的评论。"

# # 进行推理
# result = text_classification_pipeline(text)
# print(result)
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks

semantic_cls = pipeline(Tasks.text_classification, 'iic/nlp_structbert_sentiment-classification_chinese-base')
semantic_cls(input='启动的时候很大声音，然后就会听到1.2秒的卡察的声音，类似齿轮摩擦的声音')