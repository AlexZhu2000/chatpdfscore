"""
@Time : 2024/7/8 0008 14:55
@Auth : Davinstein
@File : combine_and_score.py
"""
from openpyxl import Workbook, load_workbook
import os
import pandas as pd
def concat_excel():
    column_list = ['id', 'name', 'file', 'score', 'comment']
    # 设置包含Excel文件的目录
    current_path = os.getcwd()
    directory = current_path
    # 初始化一个空的DataFrame，用于存储最终合并后的数据
    final_df = pd.DataFrame()
    data_frames = []
    # 遍历目录下所有的Excel文件
    for filename in os.listdir(directory):
        # 检查文件扩展名是否为xlsx或xls
        if filename.endswith('.xlsx') or filename.endswith('.xls'):
            # 构建文件的完整路径
            print(f'process file {filename}')
            file_path = os.path.join(directory, filename)
            # 读取Excel文件
            df = pd.read_excel(file_path, header=None)
            if df.empty:
                continue
            df.columns = column_list
            df = df[df['score'] != -1]
            data_frames.append(df)
            # 假设第一列是学号，我们将其重命名为'student_id'用于合并
            # df.rename(columns=lambda x: 'student_id' if x == df.columns[0] else x, inplace=True)
            # df['student_id'] = df['student_id'].astype('str')
            # # 如果final_df为空，直接赋值
            # if final_df.empty:
            #     final_df = df
            # else:
            #     # 基于'student_id'列合并数据
            #     final_df = pd.merge(final_df, df, on='student_id', how='outer')
    combine_df = pd.concat(data_frames, ignore_index=True)
    combine_df['id'] = combine_df['id'].astype(str)
    stu_count = combine_df.groupby('id').size()
    print('student count:', len(stu_count))
    # 显示合并后的DataFrame
    combine_df.to_excel(os.path.join(directory, 'merge.xlsx'), index = False)
# print(combine_df)

def read_concat_excel_and_average():
    path = 'merge.xlsx'
    df = pd.read_excel(path)
    student_id_column = df.iloc[:, 0]
    # print(student_id_column)
    student_counts = df.groupby(student_id_column).size()
    scores_sum = df.groupby(student_id_column).sum()[f'{df.columns[3]}']
    student_counts_df = student_counts.reset_index(name='counts')
    scores_sum_df = scores_sum.reset_index(name='total_score')

    # 合并两个DataFrame
    result_df = pd.concat([student_counts_df, scores_sum_df], axis=1)
    print(result_df)
    out = 'score.xlsx'
    result_df.to_excel(out, index=False)
def final_respond():
    score_path = 'score.xlsx'
    id_name_path = 'responding.xls'
    df_names = pd.read_excel('responding.xls',dtype=str)  # 确保使用正确的编码
    df_names['id'] = df_names['id'].astype(str)
    print(df_names['id'])
    # 读取包含学号和分数的文件（b.xlsx）
    df_scores = pd.read_excel('score.xlsx')
    df_scores['id'] = df_scores['id'].astype(str)
    merged_df = pd.merge(df_names, df_scores, on='id', how='outer')
    output_excel = 'final.xlsx'
    merged_df.to_excel(output_excel, index=False)  # 不将索引写入 Excel 文件
if __name__ == '__main__':
    final_respond()