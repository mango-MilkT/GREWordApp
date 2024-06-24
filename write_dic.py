import os
import re
import pickle

def write_dic(page_range):
    dic = []
    # 设置文件夹路径
    for page in page_range:
        folder_path = './wordlist' + '/' + str(page+1)

        # 遍历文件夹内的所有文件
        for filename in os.listdir(folder_path):
            # 检查文件是否为txt文件
            if filename.endswith('.txt'):
                # 构建文件的完整路径
                file_path = os.path.join(folder_path, filename)
                # 读取文件内容
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    search_begin = 0
                    word_name, pronounce, how2memorize, ch_meaning, en_meaning, near, oppo, example = None, None, None, None, None, None, None, None
                    # 使用正则表达式查找所需内容
                    f = re.search(r'单词释义\n(.*?)\n', content[search_begin:])
                    if f:
                        word_name = f.group(1)
                        search_begin += f.span()[1]

                    f = re.search(r'US(.*?)\nUK(.*?)\n', content[search_begin:])
                    if not f:
                        f = re.search(r'US(.*?)\n', content[search_begin:])
                        if not f:
                            f = re.search(r'UK(.*?)\n', content[search_begin:])
                    if f:
                        pronounce = f.group().strip()
                        search_begin += f.span()[1]

                    f = re.search(r'(.*?)\n', content[search_begin:])
                    if f:
                        how2memorize = f.group().strip()
                        search_begin += f.span()[1]

                    f = re.search(r'(.*?)\n', content[search_begin:])
                    if f:
                        ch_meaning = f.group().strip()
                        search_begin += f.span()[1]

                    f = re.search(r'(.*?)\n', content[search_begin:])
                    if f:
                        en_meaning = f.group().strip()
                        search_begin += f.span()[1]

                    f = re.search(r'近义词\n(.*?)\n', content[search_begin:])
                    if f:
                        near = f.group(1)
                        search_begin += f.span()[1]

                    f = re.search(r'反义词\n(.*?)\n', content[search_begin:])
                    if f:
                        oppo = f.group(1)
                        search_begin += f.span()[1]

                    f = re.search(r'例句：\n(.*?)\n(.*?)', content[search_begin:])
                    if f:
                        example = f.group(1) # + '\n' + f.group(2)
                        search_begin += f.span()[1]
                    word = {'word_name':word_name, 'pronounce':pronounce, 'how2memorize':how2memorize, 'ch_meaning':ch_meaning, 'en_meaning':en_meaning, 'near':near, 'oppo':oppo, 'example':example}
                    dic.append(word)

    with open('./pkl cache/dic.pkl', 'wb') as f:
        pickle.dump(dic, f)
    f.close()

    print('Dic update complete!')