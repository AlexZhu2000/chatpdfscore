import os
import sys
import requests
BAD_SOURCE_ID = '$$$response donot contain a source_id$$$'

def get_api_key(var_name):
    """
    Retrieve the API key from environment variables and exit the program if not found.

    :return: str, API key if found
    """
    # zzh
    # api_key = os.environ.get(var_name, 'sec_rD2WAd1bO7ELLJ0lNMBPkANi7Ux2ndN9')

    #ZWL
    api_key = os.environ.get(var_name, 'sec_gUKCF92a9fGRIltq4vCWUWgqbtqwuryQ')

    if not api_key:
        print(f"{var_name} key not found.")
        sys.exit()

    return api_key

from requests.exceptions import ConnectionError, Timeout
def upload_chatpdf_file(file_path, chatpdf_api_key):
    files = [
        ('file', ('file', open(file_path, 'rb'), 'application/octet-stream'))
    ]
    headers = {
        'x-api-key': chatpdf_api_key
    }
    try:
        response = requests.post(
            'https://api.chatpdf.com/v1/sources/add-file', headers=headers, files=files, timeout=30)
    except Timeout:
        print('请求超时')
        return None
    except ConnectionError:
        print('连接错误，远程主机强迫关闭了一个现有的连接')
        return None
    except requests.HTTPError as http_err:
        print(f'HTTP 错误发生了: {http_err}')
        return None
    except requests.RequestException as err:
        print(f'请求发生了其他错误: {err}')
        return None
    except Exception as e:
        print( e)
        return None
    else:
        print(response.status_code, response.text)
        try:
            source_id = response.json()['sourceId']
            print(f'Source ID: {source_id}')
        except KeyError:
            source_id = BAD_SOURCE_ID
            print('no source id found....')
        return source_id

    #
    # if response.status_code == 200:
    #     print("File uploaded successfully")
    #     source_id = response.json()['sourceId']
    #     print(f'Source ID: {source_id}')
    #     return source_id
    # else:
    #     print('Status:', response.status_code)
    #     print('Error:', response.text)
    #     return None
    

def query_chatpdf(chatpdf_api_key, source_id, prompt):
    data = {
      "sourceId": source_id,
      "messages": [
        {
          "role": "user",
          "content": prompt
        }
      ]
    }

    headers = {
      'x-api-key': chatpdf_api_key,
      'Content-Type': 'application/json',
    }

    response = requests.post(
      'https://api.chatpdf.com/v1/chats/message', json=data, headers=headers, timeout=30)

    if response.status_code == 200:
        result = response.json()['content']
        return result
    else:
        print('Status:', response.status_code)
        print('Error:', response.text)
        return None

def Get_Score_from_response(response):
    '''
    after query_chatpdf, we need extract score from text.
    Args:
        reeponse: output of query_chatpdf

    Returns: int score(0 -- 100)

    '''
    import re

    number_list = [int(number) for number in re.findall(r'\d+', response)]
    print(number_list)
    if number_list:
        for number in number_list:
            if number >=0 and number <= 100:
                return number
    else:
        print('No scores included in the response...')

def Get_Chinese_listdir(root_path):
    '''

    Args:
        root_path:

    Returns:

    '''
    from pathlib import Path
    path = Path(root_path)
    file_list = []
    for item in path.iterdir():
        if item.is_file():
            file_list.append(item.name)
            print(item.name)
        else:
            print('this is not a file:', item.name)
    return file_list

import zipfile
import os,io
def extract_double_layer_zip(outer_zip_file, output_dir):
    '''
    针对超星平台输出的双层压缩，进行解压
    Args:
        outer_zip_file:
        output_dir:

    Returns:

    '''
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    # 打开外部压缩包
    with zipfile.ZipFile(outer_zip_file, 'r') as outer_zip:
        # 遍历外部压缩包中的文件
        for inner_zip_info in outer_zip.infolist():
            inner_zip_name = inner_zip_info.filename

            # 判断文件是否为内部压缩包（假设内部压缩包以 .zip 结尾）
            if inner_zip_name.endswith('.zip'):
                print(f"Extracting {inner_zip_name}...")

                # 构造内部压缩包的输出路径
                inner_zip_output_dir = os.path.join(output_dir, os.path.splitext(inner_zip_name)[0])

                # 创建内部压缩包的输出目录
                os.makedirs(inner_zip_output_dir, exist_ok=True)

                # 解压内部压缩包
                with outer_zip.open(inner_zip_name) as inner_zip_file:
                    inner_zip_content = inner_zip_file.read()

                    # 使用 BytesIO 将内容包装成文件对象
                    inner_zip_bytesio = io.BytesIO(inner_zip_content)

                    # 使用 zipfile.ZipFile 打开内部压缩包
                    with zipfile.ZipFile(inner_zip_bytesio, 'r') as inner_zip:
                        inner_zip.extractall(path=inner_zip_output_dir)

                        # 打印解压后的文件列表
                        print(f"Extracted files in {inner_zip_output_dir}:")
                        for extracted_file in inner_zip.namelist():
                            print(f"  - {extracted_file}")


if __name__ == '__main__':
    outer_zip_file = r'F:\zzh\PHD\Work&Course\助教\16203140.01-第六周实验报告提交(word).zip'
    output_directory = './第六周/'
    extract_double_layer_zip(outer_zip_file, output_directory)
    # text = '根据网络安全实践的标准，我给以上同学的PDF课程报告打分为85分,'
    # test_path1 = r'F:\zzh\Course&work\学生工作\助教\011930115-李在勇'
    # Get_Chinese_listdir(test_path1)
    # print(Get_Score_from_response(text))

