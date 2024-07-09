[toc]

# chatpdf_api_interface

包括两个主体功能，

1. chatpdf.py对应上传pdf文件和对话交互。

   https://github.com/jrterven/chatpdf_api_interface.git

![image-20240709102132937](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20240709102132937.png)

​	2.针对网安课程，使用api批量批改学生实验报告。

# 1.chatpdf.py

## Description

The `chatpdf_api_interface` is a Python-based graphical user interface application designed to interact with ChatPDF, an API for analyzing and interacting with PDF documents. Developed by Juan Terven, this tool offers a convenient way to upload PDF files, analyze them using ChatPDF, and engage in a chat-based interaction to extract and understand content from the PDFs.

## Features
- Browse and select PDF files for analysis.
- Upload PDFs to ChatPDF using an API key.
- Chat-based interaction for analyzing and querying content from PDF documents.
- Display of conversation history.
- Export functionality for chat conversations.
- Clear data and reset functionality.

## Installation
To run `chatpdf_api_interface`, you need Python installed on your system. Clone this repository to your local machine and install the required dependencies:

```bash
git clone [repository URL]
cd chatpdf_api_interface
pip install -r requirements.txt
```

## Usage
To start the application, run:

```bash
python chatpdf.py
```

1. **Browse and Select PDF**: Use the 'Browse' button to select a PDF file for analysis.
2. **Analyze PDF**: Click 'Analyze PDF' to upload the file to ChatPDF and begin analysis.
3. **Chat Interaction**: Enter prompts in the provided text field and send them to interact with the analyzed PDF.
4. **Export Chat**: You can export the chat history using the 'Export Chat' button.
5. **Clear All**: This button clears all the data and resets the interface.

## Configuration
You need to set an environment variable `CHAT_PDF_KEY` with your ChatPDF API key. This key is necessary for the application to interact with the ChatPDF service.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
Special thanks to all contributors and users of the `chatpdf_api_interface`. Your feedback and contributions are highly appreciated.

---

Feel free to modify this template according to your project's specifics and requirements. Remember to add any additional sections as needed, such as 'Contributing', 'Credits', or 'Changelog'.

# 2.ChatPDFScore.py

## file construction

每周报告的文件夹，内部均解压：

![image-20240709104315067](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20240709104315067.png)

## run Requirments

1. 能够网络连接chatpdf.com网站
2. 注册账号并且从my account得到Chatpdf_api_key
3. 当文件数大于500需要准备多个Chatpdf_api_key。因为免费使用500 questions per mouth, 

## Run

1.修改BATCH_SIZE(表示单次运行进行打分的学生数量)以适应数量，多次运行ChatPDFScore.py直到完全覆盖所有学生文件。

2.得到所有文件输出后运行`combine_and_score.py`中功能，得到最终gpt分数。

## code explanation

`ChatPDFScore.Student_work`中影响打分质量的核心Prompt:

`你现在是一名网络安全实践课程的助教，请使用不变的评分标准为刚才的课程报告pdf进行打分，满分100分，并在回复中使用数字给出最后得分，并且不要出现其他分数，可以有一些评价打分依据。`

`utils.upload_chatpdf_file`：上传文件

`utils.query_chatpdf`：上传prompt并获取回复

网路不稳定导致的上传失败则设置对应报告分数为-1