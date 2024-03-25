import wave
import os


def frames_to_seconds(frames, framerate):
    return frames / float(framerate)


def split_wav(input_file, output_folder, split_times, num_parts):
    # 打开输入的wav文件
    with wave.open(input_file, 'rb') as wav:
        # 获取基本信息
        params = wav.getparams()
        # 获取文件名（不带扩展名）
        file_name = os.path.splitext(os.path.basename(input_file))[0]
        # 获取采样率
        framerate = params.framerate

        # 遍历每个切割时间
        for i, (start_time, end_time) in enumerate(split_times[:num_parts]):
            # 计算起始帧和结束帧
            start_frame = int(start_time * framerate)
            end_frame = int(end_time * framerate)

            # 读取指定范围内的数据
            wav.setpos(start_frame)
            frames = wav.readframes(end_frame - start_frame)

            # 如果文件名中存在下划线，则根据下划线拆分成多个文件名
            parts = file_name.split('_')
            # 如果有下划线且索引在范围内，则使用拆分后的文件名，否则直接使用原文件名
            part_file_name = parts[i] if len(parts) > i else file_name

            # 拼接新的文件路径
            output_file = os.path.join(output_folder, f"{part_file_name}.wav")
            # 打开新文件进行写入
            with wave.open(output_file, 'wb') as new_wav:
                # 设置参数
                new_wav.setparams(params)
                # 写入相应部分的数据
                new_wav.writeframes(frames)


# 示例切割时间，单位为秒
split_times = [(1, 2.5), (2, 3.5), (3, 4.5), (4, 5.5)]

# 输入文件夹路径
input_folder = "input"
# 输出文件夹路径
output_folder = "output"


# 遍历输入文件夹中的所有文件
for root, _, files in os.walk(input_folder):
    for file in files:
        # 确保文件是wav文件
        if file.endswith('.wav'):
            # 构建输入文件路径
            input_file = os.path.join(root, file)
            # 构建输出文件夹路径
            output_subfolder = os.path.relpath(root, input_folder)
            output_subfolder_path = os.path.join(output_folder, output_subfolder)
            # 构建输出文件路径
            output_file = os.path.join(output_subfolder_path, file)

            # 获取文件名中的下划线数量
            num_parts = file.count('_') + 1

            # 切割wav文件
            split_wav(input_file, output_subfolder_path, split_times, num_parts)
