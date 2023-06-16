import vk_api
import openai  
import time
import requests

# Здесь необходимо указать ваши данные для авторизации в ВКонтакте
BOT_TOKEN = '' # Используйте https://vkhost.github.io/
GROUP_ID = '' # id Вашей группы
CHATGPT_TOKEN = '' # Используйте https://platform.openai.com/account/api-keys

openai.api_key = CHATGPT_TOKEN

# Функция для ChatGPT
def ask(prompt):
    completion = openai.Completion.create(engine="text-davinci-003", 
                                          prompt=prompt, 
                                          temperature=0.65, 
                                          max_tokens=1000)
    
    return ( completion.choices[0]['text'] )


def create_post(message,photo_attachment):
    vk_session = vk_api.VkApi(token=BOT_TOKEN)
    vk = vk_session.get_api()

    # Создание поста
    response = vk.wall.post(owner_id='-' + GROUP_ID, message=message, attachments=photo_attachment)

    # Проверка на успешное создание поста
    if response.get('post_id'):
        return response['post_id']
    else:
        return None


def upload_photo(filename):
    upload_url = f'https://api.vk.com/method/photos.getWallUploadServer?group_id={GROUP_ID}&access_token={BOT_TOKEN}&v=5.131'
    response = requests.get(upload_url).json()

    if 'response' in response:
        upload_url = response['response']['upload_url']

        files = {
            'photo': open(filename, 'rb')
        }

        upload_response = requests.post(upload_url, files=files).json()

        if 'photo' in upload_response:
            photo = upload_response['photo']
            server = upload_response['server']
            hash = upload_response['hash']

            save_url = f'https://api.vk.com/method/photos.saveWallPhoto?group_id={GROUP_ID}&photo={photo}&server={server}&hash={hash}&access_token={BOT_TOKEN}&v=5.131'
            save_response = requests.get(save_url).json()

            if 'response' in save_response:
                photo_info = save_response['response'][0]
                return f'photo{photo_info["owner_id"]}_{photo_info["id"]}'
            else:
                print('Ошибка сохранения фотографии:', save_response)
        else:
            print('Ошибка загрузки фотографии:', upload_response)
    else:
        print('Ошибка получения URL для загрузки фотографии:', response)

    return None

#Функция для отправки сообщения администратору
def Error():
    vk_session = vk_api.VkApi(token='') #Используйте ключ доступа из настроек вашей группы -> работа с API
    vk = vk_session.get_api()

    vk.messages.send(user_id='id пользователя в формате int', random_id=0, message="Проблемы с постом!")


znaks = ['Овна','Тельца','Близнецов','Рака','Льва','Девы','Весов','Скорпиона','Стрельца','Козерога','Водолея','Рыб']

while True:
    if time.localtime().tm_hour == 21 and time.localtime().tm_min == 40: 
        for i in range(12):
            photo_filename = f'image/{i}.jpeg'
            photo_attachment = upload_photo(photo_filename)
            ask_message = f'Составь прикольный гороскоп одним или двумя предложениями на завтра для {znaks[i]}'
            date = str(time.localtime(time.time()+60*60*24).tm_mday) + '.' + str(time.localtime(time.time()+60*60*24).tm_mon) + '.' + str(time.localtime(time.time()+60*60*24).tm_year) # time.time()+60*60*24 используется для сдвига на один день вперёд
            try:
                post_id = create_post(f'Гороскоп для {znaks[i]} {date}\n\n' + ask(ask_message), photo_attachment)
            except:
                Error()
                print("Проблемы с постом!")
            if post_id:
                print('Пост успешно создан. ID поста:', post_id)
            else:
                print('Не удалось создать пост.')
            time.sleep(60)
    elif time.localtime().tm_hour == 12 and  time.localtime().tm_min == 14:
        photo_filename = 'image/xaxa.png'
        photo_attachment = upload_photo(photo_filename)
        ask_message = 'Расскажи смешной анекдот'
        date = str(time.localtime().tm_mday) + '.' + str(time.localtime().tm_mon) + '.' + str(time.localtime().tm_year)
        try:
            post_id = create_post(ask(ask_message), photo_attachment)
        except:
            post_id = False
            Error()
            print("Проблемы с постом!")
        if post_id:
            print('Пост успешно создан. ID поста:', post_id)
        time.sleep(60)
    elif time.localtime().tm_hour == 22 and time.localtime().tm_min == 30:
        photo_filename = 'image/spok.png'
        photo_attachment = upload_photo(photo_filename)
        try:
                post_id = create_post("Доброй ночи ✨", photo_attachment)
        except:
            Error()
            print("Проблемы с постом!")
        if post_id:
            print('Пост успешно создан. ID поста:', post_id)
        else:
            print('Не удалось создать пост.')
        time.sleep(60)