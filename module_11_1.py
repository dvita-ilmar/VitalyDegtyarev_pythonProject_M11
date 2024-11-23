"""
coding: utf-8
Дегтярев Виталий (группа 22/08)
Домашнее задание №11.1
Домашнее задание по теме "Обзор сторонних библиотек Python"
Требуется рисунок в файле Logo_Fakestoreapi.png (также выложен в проект на GitHub)

Программа запрашивает с сайта https://fakestoreapi.com и выводит в консоль список всех пользователей сайта,
затем запрашивает у пользователя номер из списка пользователей - у которого он желает посмотреть товары
отложенные в корзины "покупок" с этого сайта.
Далее программа запрашивает корзины всех пользователей и выводит в консоль также запрошенные с сайта списки и
фото товаров в тех корзинах, которые принадлежат выбранному пользователю.
Фото товаров пользователя сохраняются в файлы с названиями: именем, фамилией и названием товара.
По желанию пользователя изображения найденных товаров выдаются на экран.
(Не у всех пользователей на сайте есть корзины с выбранными товарами. Если нет результатов - это не ошибка!)
"""


import datetime, string, requests
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt


if __name__ == '__main__':

    #Запрашиваем всех пользователей сайта
    url = 'https://fakestoreapi.com/users'
    response_users = requests.get(url).json()

    #Показываем список пользователей
    print('На сайте "https://fakestoreapi.com" обретаются следующие пользователи:\n(номер имя фамилия пользователя)')

    #Демонстрация пользователю списка пользователей сайта
    for item in response_users:
        print(f'{item["id"]} {item["name"]["firstname"]} {item["name"]["lastname"]}')

    #Запрос выбора идентификатора пользователя у пользователя
    result = False
    while not result:
        value = int(input('\nВведите номер пользователя, у которого желаете заглянуть в корзины товаров: '))
        for item in response_users:
            if value == item["id"]:
                user_first_name = item["name"]["firstname"]
                user_last_name = item["name"]["lastname"]
                result = True
                break
        if not result:
            print('Введен неверный номер пользователя')

    #Запрос информации о всех корзинах пользователей (Cart)
    url = 'https://fakestoreapi.com/carts'
    response_cart = requests.get(url).json()

    #Демонстрация содержимого корзин выбранного пользователя
    print(f'\nИзображения найденных в корзине пользователя товаров будут сохранены в файл')
    user_input = input('Выводить изображение товара на экран? (введите "да", любое иное - нет: ')
    show_image = False
    if user_input.lower() == 'да':
        show_image = True
    logotype = Image.open('Logo_Fakestoreapi.png') # Загрузка логотипа из файла
    safe_chars = f"-_.() {string.ascii_letters}{string.digits}" # f-строка разрешенных символов в имени файла для проверки
    print(f'У пользователя {user_first_name} {user_last_name} есть корзины со следующими товарами:')
    for item in response_cart: #У пользователя может быть несколько корзин
        if item["userId"] == value:
            print(f'\nНомер корзины: {item["id"]}\nДата создания: {datetime.datetime.strptime(item["date"],"%Y-%m-%dT%H:%M:%S.%fZ")}\nВ корзине находятся следующие товары:')
            for item_product in item["products"]: #У пользователя может быть несколько товаров в корзине
                url = 'https://fakestoreapi.com/products/'+str(item_product["productId"])
                response_product = requests.get(url).json()
                print(f'- {response_product["title"]} - Цена: {response_product["price"]} - Количество: {item_product["quantity"]}')

                # Работа с изображением товара с помощью библиотеки Pillow
                resp = requests.get(response_product["image"], stream=True).raw
                base_img = Image.open(resp)
                base_img.paste(logotype, (10,10)) # Помещение изображения логотипа на изображение товара
                drawing = ImageDraw.Draw(base_img)
                black = (3, 8, 12)
                font = ImageFont.truetype("arial.ttf", 40)
                drawing.text((70, 10), 'fakestoreapi.com', fill=black, font=font)

                # Запись измененного изображения товара в файл в другом формате (.png)
                filename_image = str(user_first_name + '_' + user_last_name + '_' + response_product["title"] + '.png')
                # Проверка имени файла в части названия товара на запрещенные символы и их удаление - если они есть
                filename_image = filename_image.translate(str.maketrans('', '', ''.join(set(string.punctuation) - set(safe_chars))))
                base_img.save(filename_image, 'png')

                # Вывод изображения товара на экран если пользователь захотел
                # (у меня почему-то не работает вывод с помощью метода show() от Pyllow - ОС 'Windows 10 Pro')
                if show_image: # Демонстрация работы библиотеки 'matplotlib'
                    plt.imshow(base_img)
                    plt.show()

    print(f'\n(В текущий каталог сохранены изображения товаров: <имя>_<фамилия>_<название товара>)')