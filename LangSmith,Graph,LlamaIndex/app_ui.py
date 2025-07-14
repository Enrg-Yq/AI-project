import gradio as gr
from data_analysis import DataAnalysisApp
import matplotlib.pyplot as plt
from langchain_openai import ChatOpenAI
import os

def main():
    # 设置环境变量
    os.environ['OPENAI_API_KEY'] = 'sk-e2f6d54dee83422fb05bb2684f32d362'
    os.environ['OPENAI_API_BASE'] = 'https://api.deepseek.com/v1'
    # 设置matplotlib中文字体
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'PingFang SC', 'STHeiti', 'SimHei', 'Microsoft YaHei']  # 设置中文字体
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

    # 创建 DataAnalysisApp 类的实例
    app = DataAnalysisApp()
    
    # UI界面
    with gr.Blocks() as demo:
        gr.Markdown("# 智能数据分析助手")

        with gr.Row():
            with gr.Column():
                file_input = gr.File(label="上传数据文件 (CSV 或 Excel)")
                upload_output = gr.Textbox(label="上传状态")
            data_preview = gr.HTML(label="数据预览")

        # 文件上传事件处理
        file_input.upload(
            app.process_file,
            inputs=[file_input],
            outputs=[upload_output, data_preview]
        )

        with gr.Row():
            question_input = gr.Textbox(
                label="输入您的分析问题",
                placeholder="例如：计算每列的基本统计信息"
            )

        with gr.Row():
            with gr.Column():
                analysis_output = gr.Textbox(label="分析结果")
                code_output = gr.Code(
                    label="执行的代码",
                    language="python",
                    interactive=False
                )
            with gr.Column():
                plot_output = gr.Image(label="可视化结果")

        # 问题提交事件处理
        question_input.submit(
            app.analyze_data,
            inputs=[question_input],
            outputs=[analysis_output, plot_output, code_output]
        )

        demo.launch()

if __name__ == "__main__":
    main()
    # 计算不同产品的销售额，并绘制图表