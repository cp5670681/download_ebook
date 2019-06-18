import requests
from PIL import Image
import os
import threading
from queue import Queue
from urllib.request import urlretrieve
import urllib.error
import re

basedir = os.path.abspath(os.path.dirname(__file__))


class DownloadEbook(object):

    def __init__(self, thread_num=10):
        self.thread_num = thread_num
        self.q=Queue()
        for i in range(1,thread_num+1):
            self.q.put(i)
            self.qi=i+1
        self.L=[]
        self.already_num = 0
        self.working = thread_num

    def download_img(self, base_url, window):
        while True:
            if self.q.empty():
                break
            i = self.q.get_nowait()
            if i in self.L:
                self.q.put(self.qi)
                self.qi += 1
                self.already_num += 1
                window.label_2.setText('已下载%d张图片' % self.already_num)
                continue
            url = '%s%03d.jpg' % (base_url, i)
            print('开始下载: ' + url)
            filename = 'output%03d.jpg' % i
            filepath = os.path.join(basedir, 'ebook_temp', filename)
            r = requests.get(url)
            if r.status_code==200:
                with open(filepath, 'wb') as f:
                    f.write(r.content)
                self.q.put(self.qi)
                self.qi += 1
                self.already_num += 1
                print('下载结束：'+ url)
                window.label_2.setText('已下载%d张图片' % self.already_num)
            else:
                self.working -= 1
                if self.working == 0:
                    window.label_2.setText('下载完成，已下载%d张图片' % self.already_num)
                    window.pushButton.setEnabled(True)
                    window.pushButton_2.setEnabled(True)
                    window.pushButton_3.setEnabled(True)
                break



    def get_L(self):  # 传入存储的list
        for file in os.listdir(os.path.join(basedir,'ebook_temp')):
            if '.jpg' in file and 'output' in file:
                n = int(re.sub("\D", "", file))
                self.L.append(n)
        self.L.sort()


    def rea(self, pdf_name, window):
        file_list = os.listdir(os.path.join(basedir,'ebook_temp'))
        pic_name = []
        im_list = []
        for x in file_list:
            if ("jpg" in x or 'png' in x or 'jpeg' in x) and 'output' in x:
                pic_name.append(x)

        pic_name.sort()
        new_pic = []

        for x in pic_name:
            if "jpg" in x:
                new_pic.append(x)

        for x in pic_name:
            if "png" in x:
                new_pic.append(x)

        im1 = Image.open(os.path.join(basedir, 'ebook_temp', new_pic[0]))
        new_pic.pop(0)
        for i in new_pic:
            img = Image.open(os.path.join(basedir, 'ebook_temp', i))
            # im_list.append(Image.open(i))
            if img.mode == "RGBA":
                img = img.convert('RGB')
                im_list.append(img)
            else:
                im_list.append(img)
        try:
            im1.save(pdf_name, "PDF", resolution=100.0, save_all=True, append_images=im_list)
            print("输出文件名称：", pdf_name)
            window.label_2.setText('导出成功')
        except Exception as e:
            print(e)


if __name__=='__main__':
    d=DownloadEbook()
    d.download_img('https://resources.pearsonactivelearn.com/r00/r0082/r008257/r00825750/current/OPS/images/combined-')


'''
if option == '1':
    base_url = input('请输入图片url:')
    base_url = re.split(r'\d{0,5}.jpg', base_url)[0]
    with open('config.txt', 'w') as f:
        f.write(base_url)
    for i in range(thread_num):
        threading.Thread(target=download_img, args=(n, base_url, a)).start()
        time.sleep(1)
elif option == '2':
    flag=0
    with open('config.txt', 'r') as f:
        base_url=f.read()
    L=[]
    listdir(basedir, L)
    if L[-1]==len(L):
        r = requests.get('%s%03d.jpg' % (base_url, L[-1] + 1))
        if r.status_code==404:
            print('文件完全下载完毕，可以进行第四步')
            flag=1
    else:
        print('文件未下载完全，继续下载……')
    if flag==0:
        for i in range(thread_num):
            threading.Thread(target=download_img, args=(n, base_url, a, L)).start()
            time.sleep(1)
elif option == '3':
    i=0
    with open('config.txt', 'r') as f:
        base_url=f.read()
    L=[]
    listdir(basedir, L)
    while True:
        i+=1
        if i in L:
            continue
        url = '%s%03d.jpg' % (base_url, i)

        filename = 'output%03d.jpg' % i
        try:
            urlretrieve(url, filename)
            print(url)
        except urllib.error.HTTPError:
            print('文件完全下载完毕，可以进行第四步')
            break

elif option == '4':
    pdf_name = 'output'
    if ".pdf" in pdf_name:
        rea(pdf_name=pdf_name)
    else:
        rea(pdf_name="{}.pdf".format(pdf_name))
else:
    print('选项输入错误')

a=input('按任意键结束')
'''
# base_url='https://resources.pearsonactivelearn.com/r00/r0082/r008257/r00825750/current/OPS/images/combined-001.jpg'
