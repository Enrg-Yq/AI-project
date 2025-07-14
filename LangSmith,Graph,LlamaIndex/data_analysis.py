import contextlib
import os.path
import os
import re
import sys
import matplotlib.pyplot as plt
import pandas as pd
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI
from langchain.agents.agent_types import AgentType
class CodeCapture:
    def __init__(self):
        self.code = []
        self.output = []

    def clean_ansi_codes(self, text):
        # 清理ANSI颜色代码和其他特殊字符
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)

    def clean_code(self, code):
        # 清理代码中的特殊字符和格式
        code = self.clean_ansi_codes(code)
        code = code.strip()
        if code.startswith("```python"):
            code = code[9:].strip()
        if code.startswith("```"):
            code = code[3:].strip()
        if code.endswith("```"):
            code = code[:-3].strip()
        return code

    def write(self, text):
        # 捕获所有输出
        self.output.append(text)
        # 尝试从输出中提取代码
        if "Action:" in text and "Action Input:" in text:
            code_match = re.search(r"Action Input:(.*?)(?=\nObservation:|$)", text, re.DOTALL)
            if code_match:
                code = code_match.group(1).strip()
                code = self.clean_code(code)
                if code:  # 只有在代码非空时才添加
                    self.code.append(code)

    def get_code(self):
        return '\n'.join(self.code)

    def get_output(self):
        return ''.join(self.output)



class DataAnalysisApp:                                                                                  

    def __init__(self):
        self.df = None
        self.agent = None
        
    def create_agent(self):
        if self.df is not None:
	    # 创建一个能够处理pandas DataFrame的agent
            self.agent = create_pandas_dataframe_agent(
            ChatOpenAI(
                temperature=0,
                model="deepseek-chat",
                model_kwargs={
                    "messages": [
                        {"role": "system", "content": "你是一个专业的数据分析师，请用中文回答所有问题。"}
                    ]
                }
            ),
            self.df,
            verbose=True,
            agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            allow_dangerous_code=True
        )

    def process_file(self, file):
        # 获取文件扩展名
        file_ext = os.path.splitext(file.name)[1].lower()

        try:
            # 根据文件类型读取数据
            if file_ext == '.csv':
                self.df = pd.read_csv(file.name)
            elif file_ext in ['.xlsx', '.xls']:
                self.df = pd.read_excel(file.name)
            else:
                return "不支持的文件格式。请上传CSV或Excel文件。", None

            # 创建数据分析代理
            self.create_agent()
            # 返回成功信息和数据预览
            return f"文件已成功加载。数据形状: {self.df.shape}", self.df.head().to_html()
        except Exception as e:
            return f"处理文件时出错: {str(e)}", None

    def analyze_data(self, question):
        if self.df is None:
            return '请先上传数据文件', None, ""
        if self.agent is None:
            return 'Agent未初始化', None, ""
        try:
            # 创建新的代码捕获实例
            self.code_capture = CodeCapture()
            # 捕获标准输出
            with contextlib.redirect_stdout(self.code_capture):
                # 执行分析并获取结果
                result = self.agent.invoke({"input": question})
            # 获取执行的代码
            executed_code = self.code_capture.get_code()
            # 打印调试信息到实际的终端
            sys.__stdout__.write(f"Captured Output: {self.code_capture.get_output()}\n")
            sys.__stdout__.write(f"Executed Code: {executed_code}\n")
            sys.__stdout__.write(f"Result: {result}\n")
            # 检查是否生成了新的图表
            if plt.get_fignums():
                plt.savefig('tmp_plot.png')
                plt.close()
                return result['output'], 'tmp_plot.png', executed_code
            return result['output'], None, executed_code
        except Exception as e:
            return f'分析过程中出错: {str(e)}', None, ""


if __name__ == "__main__":

    os.environ["LANGSMITH_TRACING"] = "true"
    os.environ["LANGSMITH_ENDPOINT"] = "https://api.smith.langchain.com"
    os.environ["LANGSMITH_API_KEY"] = "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"
    os.environ["LANGSMITH_BASE_URL"] = "data_analysis"
    app = DataAnalysisApp()
    file_name = r"E:\MYS\vscode pro\7.10\sales_data.csv"
    app.process_file(file_name)
    print(app.df)


  