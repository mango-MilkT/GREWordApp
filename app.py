import os
import re
import sys
import pickle
import keyboard
import datetime
import tkinter as tk
from tkinter import font
import ttkbootstrap as ttk
from PIL import Image, ImageTk
from write_dic import write_dic


WriteDic = 0    # 要更新字典的时候设为 1 
FirstOpen = 0   # 初次运行时设为 1, 初始化完毕后设为 0 即可正常使用
StarMode = 0    # 要复习收藏的单词的时候设为 1, 正常模式下设为 0 

start_date = '2024-6-21'    # 记录你第一天开始背单词的时间
day_task = 150              # 每日单词任务量
theme = 'minty'             # 界面主题, 详见ttkbootstrap

if FirstOpen or WriteDic:
    write_dic(range(167))

with open('./pkl cache/dic.pkl', 'rb') as f:
    dic = pickle.load(f)
f.close()
print('Using existing dic.')
print(f"The dic length is: {len(dic)} words.")

if FirstOpen:
    path = './pkl cache/star_list.pkl'
    if not os.path.exists(path):
        with open(path, 'wb') as f:
            star_list = []
            pickle.dump(star_list, f)
        f.close()

    path = './pkl cache/last_pos.pkl'
    if not os.path.exists(path):
        with open(path, 'wb') as f:
            last_pos = 0
            pickle.dump(last_pos, f)
        f.close()

    path = './pkl cache/todays_task.pkl'
    if not os.path.exists(path):
        with open(path, 'wb') as f:
            todays_task = 0
            pickle.dump(todays_task, f)
        f.close()

    path = './pkl cache/todays_all_task.pkl'
    if not os.path.exists(path):
        with open(path, 'wb') as f:
            todays_all_task = 0
            pickle.dump(todays_all_task, f)
        f.close()

    path = './pkl cache/todays_date.pkl'
    if not os.path.exists(path):
        with open(path, 'wb') as f:
            todays_date = '0000-00-00'
            pickle.dump(todays_date, f)
        f.close()

    path = './pkl cache/add_info.pkl'
    if not os.path.exists(path):
        with open(path, 'wb') as f:
            add_info = [''] * len(dic)
            pickle.dump(add_info, f)
        f.close()

    print('Init complete! Please set FirstOpen to 0 and run the code again.')
    sys.exit()

with open('./pkl cache/star_list.pkl', 'rb') as f:
    star_list = pickle.load(f)
f.close()

with open('./pkl cache/last_pos.pkl', 'rb') as f:
    last_pos = pickle.load(f)
f.close()

with open('./pkl cache/todays_task.pkl', 'rb') as f:
    todays_task = pickle.load(f)
f.close()

with open('./pkl cache/todays_all_task.pkl', 'rb') as f:
    todays_all_task = pickle.load(f)
f.close()

with open('./pkl cache/todays_date.pkl', 'rb') as f:
    todays_date = datetime.date.today()
    if todays_date != pickle.load(f):
        if todays_task < 0: todays_task = 0
        todays_task += day_task
        todays_all_task = todays_task    
f.close()

with open('./pkl cache/add_info.pkl', 'rb') as f:
    add_info = pickle.load(f)
f.close()

print(todays_all_task)
print(todays_task)

if not StarMode:
    print(f'Hi! You have {todays_task} words to learn.')

if StarMode and last_pos not in star_list:
    cur_index = star_list[0]
else:
    cur_index = last_pos

DetailShow = [1,1,1,1,1,1,1]

last_index = cur_index # 上一个看的单词

def update_cur_word():
    var_info.set(f"List: {cur_index // 20 + 1}/{len(dic)//20} · Word: {cur_index + 1}/{len(dic)} · Task: {'√' if todays_task <= 0 else todays_task} · Triumph Days: {(todays_date - datetime.datetime.strptime(start_date, '%Y-%m-%d').date()).days + 1}")
    var_word_name.set(dic[cur_index]['word_name'])
    var_pronounce.set(dic[cur_index]['pronounce'])
    var_how2memorize.set(dic[cur_index]['how2memorize'])
    var_ch_meaning.set(dic[cur_index]['ch_meaning'])
    var_en_meaning.set(dic[cur_index]['en_meaning'])
    var_near.set(dic[cur_index]['near'])
    var_oppo.set(dic[cur_index]['oppo'])
    var_example.set(dic[cur_index]['example'])

    var_star.set('⭐' if cur_index in star_list else '')
    var_add_info.set(add_info[cur_index])

def wordshift_last():
    global cur_index, StarMode, star_list, todays_task, last_index
    if StarMode:
        if cur_index != star_list[0]:
            last_index = cur_index
            cur_index = star_list[star_list.index(cur_index)-1]
    elif cur_index:
        last_index = cur_index
        cur_index -= 1
        todays_task += 1
        var_progress.set(todays_all_task - todays_task)
        # print(var_progress.get())
    update_cur_word()

def wordshift_next():
    global cur_index, StarMode, star_list, todays_task, last_index
    if StarMode:
        if cur_index != star_list[-1]:
            last_index = cur_index
            cur_index = star_list[star_list.index(cur_index)+1]
    elif cur_index < len(dic) - 1:
        last_index = cur_index
        cur_index += 1 
        todays_task -= 1
        var_progress.set(todays_all_task - todays_task)
        # print(var_progress.get())
        if todays_task == 0: print("Congrats! You have completed today's task!")
    update_cur_word()

def wordshift_back():
    global cur_index, last_index
    cur_index = last_index
    update_cur_word()

def detail_pack_control(container, index):
    index -= 1
    global DetailShow
    if DetailShow[index]:
        container.pack_forget()
        # print(f"{index} off!")
    else:
        container.pack(fill='both',expand='yes')
        # print(f"{index} on!")
    DetailShow[index] = not DetailShow[index]

def next_list():
    global cur_index, StarMode, last_index
    cur_list = cur_index // 20
    if not StarMode and cur_list < len(dic)//20: 
        last_index = cur_index
        cur_index = 20*(cur_list+1)
    update_cur_word()
    print('jump to next list!')
    
def last_list():
    global cur_index, StarMode, last_index
    cur_list = cur_index // 20
    if not StarMode and cur_list > 0: 
        last_index = cur_index
        cur_index = 20*(cur_list-1)
    update_cur_word()
    print('back to last list!')

def star_word():
    global cur_index, StarMode, star_list, last_index
    if cur_index not in star_list:
        star_list.append(cur_index)
    else:
        if StarMode:
            cur_index_cp = cur_index
            if cur_index != star_list[-1]:
                cur_index = star_list[star_list.index(cur_index)+1]
            elif cur_index != star_list[0]:
                cur_index = star_list[0]
            else:
                cur_index = 0
                StarMode = 0
                print('You complete all star words! Now back to the beginning.')
            last_index = cur_index
            star_list.remove(cur_index_cp)
        else:
            star_list.remove(cur_index)
    print([i+1 for i in star_list])
    update_cur_word()

def jump_to_searched_word(event):
    global cur_index, var_entry, StarMode, last_index
    # print(event.keysym)
    if len(var_entry.get()):
        if var_entry.get()[0] == ' ':
            add_info[cur_index] = var_entry.get().strip()
        else:
            if StarMode:
                StarMode = 0
                print('You can only search outside star mode. Now set to normal mode!')
            searched_name = var_entry.get()
            if searched_name.isdigit(): 
                searched_index = int(searched_name) - 1
                if searched_index >= 0 and searched_index < len(dic):
                    last_index = cur_index
                    cur_index = searched_index
            else:
                print(searched_name)
                for i, w in enumerate(dic):
                    if w['word_name'] == searched_name:
                        last_index = cur_index
                        cur_index = i
                        print('found the word!')
                        break
    update_cur_word()

def progress_update(bar):
    bar["value"] = todays_all_task - todays_task

def on_key_press(event):
    """事件触发时要执行的函数"""
    if event.name == "esc":
        root.destroy()  # 按下“Esc”键关闭窗口
    elif event.name == "left":
        wordshift_last()
    elif event.name == "right":
        wordshift_next()
    elif event.name == "page down":
        next_list()
    elif event.name == "page up":
        last_list()
    elif event.name == "down":
        star_word()
    elif event.name == "up":
        wordshift_back()

class Myapp(ttk.Frame):
    def __init__(self,master):
        super().__init__(master)
        self.filepath = ''
        self.filepath_display = ttk.StringVar(value=self.filepath)
        self.create_frame_word()
        self.create_frame_detail_and_base()
        self.create_frame_side()
        self.create_frame_corner()
        self.create_frame_top()
        keyboard.on_press(on_key_press)  # 监听键盘事件

    def create_frame_side(self):
        frame_left = ttk.Frame(style='light')
        frame_left.place(relx=0,rely=0.1,relheight=0.85,relwidth=0.05)
        frame_right = ttk.Frame(style='light')
        frame_right.place(relx=0.95,rely=0.1,relheight=0.85,relwidth=0.05)
        
        container_left_button = ttk.Frame(master=frame_left)
        container_left_button.pack(fill='both',expand='yes')
        container_right_button = ttk.Frame(master=frame_right)
        container_right_button.pack(fill='both',expand='yes')

        # 将图像转换为Tkinter可用的格式
        photo_left_button = tk.PhotoImage(file="./photo/left button.png")
        photo_right_button = ImageTk.PhotoImage(Image.open("./photo/right button.png"))

        button_left = ttk.Button(master=container_left_button, style='secondary-outline-toolbutton', command=wordshift_last)
        # button_left.pack(side='left')
        button_right = ttk.Button(master=container_right_button, style='secondary-outline-toolbutton', command=wordshift_next)
        # button_right.pack(side='right')
    def create_frame_corner(self):
        frame_left_corner = ttk.Frame(style='light')
        frame_left_corner.place(relx=0,rely=0.95,relheight=0.05,relwidth=0.05)
        frame_right_corner = ttk.Frame(style='light')
        frame_right_corner.place(relx=0.95,rely=0.95,relheight=0.05,relwidth=0.05)
        
        container_list_choice = ttk.Frame(master=frame_left_corner)
        container_list_choice.pack(fill='both',expand='yes')
        container_star_button = ttk.Frame(master=frame_right_corner)
        container_star_button.pack(fill='both',expand='yes')

        pady = 0
        list_choice = ttk.Button(master=container_list_choice, text='nl', style='secondary-outline-toolbutton', command=next_list)
        # list_choice.pack(side='top',fill='x')
        button_star = ttk.Button(master=container_star_button, text='star', style='secondary-outline-toolbutton', command=star_word)
        # button_star.pack(side='top',fill='x')
    def create_frame_top(self):
        frame_top = ttk.Frame(style='light')
        frame_top.place(relx=0,rely=0,relheight=0.05,relwidth=1)

        container_info = ttk.Frame(master=frame_top, style='')
        container_info.pack(fill='both',expand='yes')

        label_info = ttk.Label(master=container_info, textvariable=var_info, style='secondary', font=('微软雅黑', 10))
        bar_todays_progress = ttk.Progressbar(master=container_info, maximum=todays_all_task, variable=var_progress, bootstyle='info-striped')
        entry_search = ttk.Entry(master=container_info, textvariable=var_entry, style='info')
        entry_search.bind("<KeyPress-Return>", jump_to_searched_word)
        
        label_info.place(relx=0.025, rely=0.175, relheight=0.65, relwidth=0.3)
        entry_search.place(relx=0.4, rely=0.175, relheight=0.65, relwidth=0.2)
        bar_todays_progress.place(relx=0.75, rely=0.175, relheight=0.65, relwidth=0.2)

        # label_info.grid(row=0, column=0, pady=5, sticky='w'+'e')
        # entry_search.grid(row=0, column=1, pady=5, sticky='w'+'e')
        # bar_todays_progress.grid(row=0, column=2, pady=5, sticky='w'+'e')

        # for i in range(3):
        #     container_info.grid_columnconfigure(i, weight=1)

    def create_frame_word(self):
        frame_word = ttk.Frame(style='light')
        frame_word.place(relx=0.05,rely=0.1,relheight=0.5,relwidth=0.9)
        
        container_word = ttk.Frame(master=frame_word)
        container_word.pack(fill='both',expand='yes')

        label_word = ttk.Label(master=container_word, textvariable=var_word_name, bootstyle='default', font=("微软雅黑", 120))
        label_word.pack(expand='yes')

        label_star = ttk.Label(master=container_word, textvariable=var_star, bootstyle='default', font=("微软雅黑",12))
        label_star.pack(expand='yes')
        
        label_add_info = ttk.Label(master=container_word, textvariable=var_add_info, bootstyle='default', font=("微软雅黑",12))
        label_add_info.pack(expand='yes')

    def create_frame_detail_and_base(self):
        frame_detail = ttk.Frame()
        frame_detail.place(relx=0.05,rely=0.6,relheight=0.3,relwidth=0.9)
        
        container_detail_left = ttk.Frame(master=frame_detail)
        container_detail_left.place(relx=0,rely=0,relheight=1,relwidth=0.5)

        container_detail_right = ttk.Frame(master=frame_detail)
        container_detail_right.place(relx=0.55,rely=0,relheight=1,relwidth=0.45)

        container_t1 = ttk.Frame(master=container_detail_left)
        container_t1.pack(fill='both',expand='yes')
        container_t2 = ttk.Frame(master=container_detail_left)
        container_t2.pack(fill='both',expand='yes')
        container_t3 = ttk.Frame(master=container_detail_left)
        container_t3.pack(fill='both',expand='yes')
        container_t4 = ttk.Frame(master=container_detail_left)
        container_t4.pack(fill='both',expand='yes')

        container_t5 = ttk.Frame(master=container_detail_right)
        container_t5.pack(fill='both',expand='yes')
        container_t6 = ttk.Frame(master=container_detail_right)
        container_t6.pack(fill='both',expand='yes')
        container_t7 = ttk.Frame(master=container_detail_right)
        container_t7.pack(fill='both',expand='yes')

        label_t1 = ttk.Label(master=container_t1, text='中文释义：', bootstyle='success', wraplength = 700, font=("微软雅黑",12))
        label_d1 = ttk.Label(master=container_t1, textvariable=var_ch_meaning, bootstyle='success', wraplength = 700, font=("微软雅黑",12))
        label_t2 = ttk.Label(master=container_t2, text='英英翻译：', bootstyle='info', wraplength = 700, font=("微软雅黑",12))
        label_d2 = ttk.Label(master=container_t2, textvariable=var_en_meaning, bootstyle='info', wraplength = 700, font=("微软雅黑",12))
        label_t3 = ttk.Label(master=container_t3, text='单词发音：', bootstyle='secondary', wraplength = 700, font=("微软雅黑",12))
        label_d3 = ttk.Label(master=container_t3, textvariable=var_pronounce, bootstyle='secondary', wraplength = 700, font=("微软雅黑",12))
        label_t4 = ttk.Label(master=container_t4, text='记忆方法：', bootstyle='default', wraplength = 700, font=("微软雅黑",12))
        label_d4 = ttk.Label(master=container_t4, textvariable=var_how2memorize, bootstyle='default', wraplength = 700, font=("微软雅黑",12))
        label_t5 = ttk.Label(master=container_t5, text='近义词：', bootstyle='warning', wraplength = 700, font=("微软雅黑",12))
        label_d5 = ttk.Label(master=container_t5, textvariable=var_near, bootstyle='warning', wraplength = 700, font=("微软雅黑",12))
        label_t6 = ttk.Label(master=container_t6, text='反义词：', bootstyle='danger', wraplength = 700, font=("微软雅黑",12))
        label_d6 = ttk.Label(master=container_t6, textvariable=var_oppo, bootstyle='danger', wraplength = 700, font=("微软雅黑",12))
        label_t7 = ttk.Label(master=container_t7, text='例句：', bootstyle='default', wraplength = 700, font=("微软雅黑",12))
        label_d7 = ttk.Label(master=container_t7, textvariable=var_example, bootstyle='default', wraplength = 700, font=("微软雅黑",12))
        padx, pady = 1, 1
        label_t1.pack(side='left', padx=padx, pady=pady)
        label_d1.pack(side='left', padx=padx, pady=pady)
        label_t2.pack(side='left', padx=padx, pady=pady)
        label_d2.pack(side='left', padx=padx, pady=pady)
        label_t3.pack(side='left', padx=padx, pady=pady)
        label_d3.pack(side='left', padx=padx, pady=pady)
        label_t4.pack(side='left', padx=padx, pady=pady)
        label_d4.pack(side='left', padx=padx, pady=pady)
        padx, pady = 1, 1
        label_t5.pack(side='left', padx=padx, pady=pady)
        label_d5.pack(side='left', padx=padx, pady=pady)
        label_t6.pack(side='left', padx=padx, pady=pady)
        label_d6.pack(side='left', padx=padx, pady=pady)
        label_t7.pack(side='left', padx=padx, pady=pady)
        label_d7.pack(side='left', padx=padx, pady=pady)

        frame_base = ttk.Frame(style='light')
        frame_base.place(relx=0.05,rely=0.95,relheight=0.05,relwidth=0.9)
      
        container_base_button = ttk.Frame(master=frame_base)
        container_base_button.pack(fill='both',expand='yes')

        padx = 1
        pady = 1
        button_b1 = ttk.Button(master=container_base_button, text='中文释义', style='success-outline-toolbutton', command=lambda: detail_pack_control(container_t1,1))
        button_b1.grid(row=0, column=0, padx=padx, pady=pady, sticky='ew')
        button_b2 = ttk.Button(master=container_base_button, text='英英翻译', style='info-outline-toolbutton', command=lambda: detail_pack_control(container_t2,2))
        button_b2.grid(row=0, column=1, padx=padx, pady=pady, sticky='ew')
        button_b3 = ttk.Button(master=container_base_button, text='单词发音', style='secondary-outline-toolbutton', command=lambda: detail_pack_control(container_t3,3))
        button_b3.grid(row=0, column=2, padx=padx, pady=pady, sticky='ew')
        button_b4 = ttk.Button(master=container_base_button, text='记忆方法', style='default-outline-toolbutton', command=lambda: detail_pack_control(container_t4,4))
        button_b4.grid(row=0, column=3, padx=padx, pady=pady, sticky='ew')
        button_b5 = ttk.Button(master=container_base_button, text='近义词', style='warning-outline-toolbutton', command=lambda: detail_pack_control(container_t5,5))
        button_b5.grid(row=0, column=4, padx=padx, pady=pady, sticky='ew')
        button_b6 = ttk.Button(master=container_base_button, text='反义词', style='danger-outline-toolbutton', command=lambda: detail_pack_control(container_t6,6))
        button_b6.grid(row=0, column=5, padx=padx, pady=pady, sticky='ew')
        button_b7 = ttk.Button(master=container_base_button, text='例句', style='default-outline-toolbutton', command=lambda: detail_pack_control(container_t7,7))
        button_b7.grid(row=0, column=6, padx=padx, pady=pady, sticky='ew')

        for i in range(7):
            container_base_button.grid_columnconfigure(i, weight=1)
        
root = ttk.Window(title='Gtmd GRE',themename=theme)
# cosmo - flatly - journal - literal - lumen - minty - pulse - sandstone - united - yeti（浅色主题） 推荐minty
# cyborg - darkly - solar - superhero（深色主题） 推荐solar
# root.geometry('1000x800')
# root.resizable(True,True)

# print(font.families())

var_info = ttk.StringVar()
var_word_name = ttk.StringVar()
var_pronounce = ttk.StringVar()
var_how2memorize = ttk.StringVar()
var_ch_meaning = ttk.StringVar()
var_en_meaning = ttk.StringVar()
var_near = ttk.StringVar()
var_oppo = ttk.StringVar()
var_example = ttk.StringVar()

var_entry = ttk.StringVar()

var_progress = ttk.IntVar()
var_progress.set(todays_all_task - todays_task)

var_star = ttk.StringVar()
var_add_info = ttk.StringVar()

update_cur_word()

Myapp(root)
root.state('zoomed')
root.mainloop()

with open('./pkl cache/star_list.pkl', 'wb') as f:
    pickle.dump(star_list, f)
f.close()

print(f'Star list updated! All star words: {len(star_list)}.')

if not StarMode: last_pos = cur_index
with open('./pkl cache/last_pos.pkl', 'wb') as f:
    pickle.dump(last_pos, f)
f.close()

with open('./pkl cache/todays_date.pkl', 'wb') as f:
    pickle.dump(todays_date, f)
f.close()

with open('./pkl cache/todays_task.pkl', 'wb') as f:
    pickle.dump(todays_task, f)
f.close()

with open('./pkl cache/todays_all_task.pkl', 'wb') as f:
    pickle.dump(todays_all_task, f)
f.close()

with open('./pkl cache/add_info.pkl', 'wb') as f:
    pickle.dump(add_info, f)
f.close()