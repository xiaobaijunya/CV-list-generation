file_path = 'risku式CVVC_0.8.ini'
start_string = '[VOWEL]'
end_string = '[CONSONANT]'
pinyin_number = 4

def process_text(input_text):
    result = []
    for line in input_text.split('\n'):
        # 删除开头两个等号前的内容和结尾等号以后的内容
        equal_count = 0
        for i, char in enumerate(line):
            if char == '=':
                equal_count += 1
                if equal_count == 2:
                    line = line[i + 1:]
                    break

        if '=' in line:
            line = line[:line.rindex('=')]

        # 按照逗号分割拼音
        pinyin_list = line.split(',')

        # 每行四个拼音，由下划线分割，然后加入结果列表
        for i in range(0, len(pinyin_list), pinyin_number):
            result.append('_'.join(pinyin_list[i:i + 4]))

    return result

print('读取文本进行预处理')

# 读取文件内容
with open(file_path, 'r') as file:
    content = file.read()

# 找到指定的开始和结束字符串在内容中的位置
start_index = content.find(start_string)
end_index = content.find(end_string, start_index + len(start_string))

if start_index != -1 and end_index != -1:
    # 从开始字符串处到结束字符串处截取内容
    truncated_content = content[start_index + len(start_string):end_index]
    print(truncated_content)
    print("预处理完成")
else:
    print("指定的开始或结束字符串未找到。")

# 初始处理完成开始传入函数

# 处理文本并保存结果到文件
processed_text = process_text(truncated_content)
with open('CV_processed_output.txt', 'w') as output_file:
    for line in processed_text:
        output_file.write(line + '\n')

print("处理结果已保存到 CV_processed_output.txt 文件中。")
