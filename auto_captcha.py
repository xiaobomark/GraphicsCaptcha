# coding:utf-8
import os
import subprocess
from PIL import Image


def get_captcha(driver, captcha_id, full_screen_img_path, captcha_img_path, captcha_final_path, txt_path, ocr_path):
    # 浏览器界面截图
    driver.save_screenshot(full_screen_img_path)
    # 找到验证码图片，得到它的坐标
    element = driver.find_element_by_id(captcha_id)
    left = element.location['x']
    top = element.location['y']
    right = element.location['x'] + element.size['width']
    bottom = element.location['y'] + element.size['height']
    left, top, right, bottom = int(left), int(top), int(right), int(bottom)
    img = Image.open(full_screen_img_path)
    img = img.crop((left, top, right, bottom))
    # 得到验证码图片
    img.save(captcha_img_path)
    # 打开验证码图片
    img = Image.open(captcha_img_path)
    # 颜色直方图，255种颜色，255为白色
    # 新建一张图片(大小和原图大小相同，背景颜色为255白色)
    img_new = Image.new('P', img.size, 255)
    for x in range(img.size[1]):
        for y in range(img.size[0]):
            # 遍历图片的xy坐标像素点颜色
            pix = img.getpixel((y, x))
            # print(pix)
            # 自己调色，r=0，g=0，b>0为蓝色
            if pix[0] < 20 and pix[1] < 20 and pix[2] > 50:
                # 把遍历的结果放到新图片上，0为透明度，不透明
                img_new.putpixel((y, x), 0)
    img_new.save(captcha_final_path, format='png')

    # 通过tesseract工具解析验证码图片，生成文本
    os.system(ocr_path)

    # 读取txt文件里面的验证码
    with open(txt_path, 'r') as f:
        if f.read():
            t = f.read().strip()
            # 去掉中间空格
            if ' ' in t:
                t = t.replace(' ', '')
            if t.isdigit() and len(t) == 4:
                return t
            else:
                return 'fail'


def check_resp(result, msg):
    if msg in result:
        return 'pass'
    else:
        return 'failed'


# 接口 - 识别验证码
def get_captcha(captcha_img_path, captcha_final_path, txt_path, ocr_path):

    # 打开验证码图片
    img = Image.open(captcha_img_path)

    # 新建一张图片(大小和原图大小相同，背景颜色为255白色)
    img_new = Image.new('P', img.size, 55)
    for x in range(img.size[1]):
        for y in range(img.size[0]):
            # 遍历图片的xy坐标像素点颜色
            pix = img.getpixel((y, x))
            # print(pix)
            # 自己调色，r=0，g=0，b>0为蓝色
            if pix[0] < 20 and pix[1] < 20 and pix[2] > 50:
                # 把遍历的结果放到新图片上，0为透明度，不透明
                img_new.putpixel((y, x), 0)
    img_new.save(captcha_final_path, format='png')

    # 通过tesseract工具解析验证码图片，生成文本，【Tesseract-OCR必须和jpg的根目录必须相同，如C盘、D盘！！！】
    os.system(ocr_path)

    # 读取txt文件里面的验证码
    with open(txt_path, 'r') as f:
        if r.read():
            t = f.read().strip()
            # 去掉中间空格
            if ' ' in t:
                t = t.replace(' ', '')
            # 如果是数字且长度为4，就返回数字，如果不是就返回 fail
            if t.isdigit() and len(t) == 4:
                return t
            else:
                return fail