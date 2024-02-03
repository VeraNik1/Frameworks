import requests
import time
import os


URLS = [
    'https://i.ytimg.com/vi/trgsdb1wgRw/maxresdefault.jpg',
    'https://i.pinimg.com/736x/bd/0c/31/bd0c3178e30a229021d8614e31c78d08.jpg',
    'https://mayak72.ru/upload/iblock/948/xott3yxomxfmlbd2iaor6gpv8dxs1p88.jpg',
    'https://cs14.pikabu.ru/post_img/2022/09/09/11/og_og_1662746575240240099.jpg',
    'https://main-website-blogs.s3.us-east-2.amazonaws.com/6e8813b4-4f27-4485-8304-0db8ac4921df-2_Audi.jpg',
    'https://static.tildacdn.com/tild3265-6366-4664-b036-303138643733/th.jpeg',
    'https://russiskskolebergendotcom.files.wordpress.com/2019/02/img10.jpg',
    'https://cs11.pikabu.ru/post_img/2018/10/02/8/og_og_1538486795226679873.jpg'
    ]

start_func_time = time.time()
def img_saver(urls):
    if not os.path.exists('images_sync'):
        os.makedirs('images_sync')
    for url in urls:
        start_time = time.time()
        response = requests.get(url)
        file_name = f'{url.split("/")[-1]}'
        with open(f'images_sync/{file_name}', 'wb') as f:
            f.write(response.content)
        print(f'{file_name} загружен, время загрузки {(time.time() - start_time) * 1000:.0f} мс')


if __name__ == '__main__':
    img_saver(URLS)
    print(f'Общее время загрузки файлов: {(time.time() - start_func_time)* 1000:.0f} мс')