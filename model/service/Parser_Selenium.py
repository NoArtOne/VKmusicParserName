import time
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from pathlib import Path
from selenium.webdriver.common.by import By


def get_path():
    path_ = Path.cwd()
    str_ = ''
    elm = [mass for mass in str(path_).split(f'\\')[:-1]]
    for name_in_elm in elm:
        str_ += f'{name_in_elm}\\'
    str_ += f'chromedriver.exe'
    return str_

def get_path_for_txt_record():
    path_ = Path.home()
    str_ = ''
    elm = [mass for mass in str(path_).split(f'\\')]
    for name_in_elm in elm:
        str_ += f'{name_in_elm}\\'
    str_ += f'list_of_song_for_yandex.txt'
    return str_

service = Service(executable_path=get_path())
driver = webdriver.Chrome(service=service)
driver.get("https://vk.com/")
for i in range(37):
    time.sleep(1)
    print(i, ' - second')
driver.find_element(By.XPATH, '//*[@id="l_pr"]/a/span[1]').click()
time.sleep(5)
value_music = driver.find_element(By.XPATH, '//*[@id="profile_audios"]/a/div/span[2]').text
print(value_music)
driver.find_element(By.XPATH, '//*[@id="l_aud"]/a/span[1]').click()
time.sleep(5)
driver.find_element(By.XPATH, '//*[@id="content"]/div/div[3]/div[1]/h2/ul/li[2]/a').click()
time.sleep(5)
driver.find_element(By.XPATH, '//*[@id="content"]/div/div[3]/div[2]/div[3]/div/div[3]/div/div[1]/div[2]/div/div/div[2]/div/div[1]')
finder = driver.find_element(By.XPATH, '//*[@id="content"]/div/div[3]/div[2]/div[3]/div/div[3]/div[1]/div[1]/div[2]/div/div/div[2]/div/div[1]')
SCROLL_PAUSE_TIME = 0.5

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height
mass_songs = []
for i in range(1, int(value_music)+1):
    elm_song = []
    # all_song = finder.find_elements(By.CLASS_NAME, 'audio_row__title_inner _audio_row__title_inner')
    # for i in all_song:
    #     print(i.text)
        # elm_song.append(i.text)
    if i == 1:
        get_text = finder.find_element(By.XPATH, '//*[@id="content"]/div/div[3]/div[2]/div[3]/div/div[3]/div[1]/div[1]/div[2]/div/div/div[2]/div/div[1]/div[1]/div/div[5]/div[2]/div[1]/a')
        print(get_text.text, 'номер песни - ', {i})
        elm_song.append(get_text)
        get_text = finder.find_element(By.XPATH, '//*[@id="content"]/div/div[3]/div[2]/div[3]/div/div[3]/div[1]/div[1]/div[2]/div/div/div[2]/div/div[1]/div[1]/div/div[5]/div[2]/div[2]/a')
        print(get_text.text)
        elm_song.append(get_text)
    elif i > 1 and i < 11:
        get_text = finder.find_element(By.XPATH, f'//*[@id="content"]/div/div[3]/div[2]/div[3]/div/div[3]/div[1]/div[1]/div[2]/div/div/div[2]/div/div[1]/div[{i}]/div/div[6]/div[2]/div[1]/a')
        print(get_text.text)
        elm_song.append(get_text)
        get_text = finder.find_element(By.XPATH, f'//*[@id="content"]/div/div[3]/div[2]/div[3]/div/div[3]/div[1]/div[1]/div[2]/div/div/div[2]/div/div[1]/div[{i}]/div/div[6]/div[2]/div[2]/a')
        print(get_text.text)
        elm_song.append(get_text)
    elif i > 9 and i < 12:
        get_text = finder.find_element(By.XPATH,  f'//*[@id="content"]/div/div[3]/div[2]/div[3]/div/div[3]/div[1]/div[1]/div[2]/div/div/div[2]/div/div[1]/div[{i}]/div/div[5]/div[2]/div[1]/a[1]')
        print(get_text.text)
        elm_song.append(get_text)
        get_text = finder.find_element(By.XPATH, f'//*[@id="content"]/div/div[3]/div[2]/div[3]/div/div[3]/div[1]/div[1]/div[2]/div/div/div[2]/div/div[1]/div[{i}]/div/div[5]/div[2]/div[2]/a')
        print(get_text.text)
        elm_song.append(get_text)
    elif i > 11:
        get_text = finder.find_element(By.XPATH,  f'//*[@id="content"]/div/div[3]/div[2]/div[3]/div/div[3]/div[1]/div[1]/div[2]/div/div/div[2]/div/div[1]/div[{i}]/div/div[6]/div[2]/div[1]/a')
        print(get_text.text)
        elm_song.append(get_text)
        get_text = finder.find_element(By.XPATH, f'//*[@id="content"]/div/div[3]/div[2]/div[3]/div/div[3]/div[1]/div[1]/div[2]/div/div/div[2]/div/div[1]/div[{i}]/div/div[6]/div[2]/div[2]/a')
        print(get_text.text)
        elm_song.append(get_text)
        #//*[@id="content"]/div/div[3]/div[2]/div[3]/div/div[3]/div[1]/div[1]/div[2]/div/div/div[2]/div/div[1]/div[10]/div/div[5]/div[2]/div[2]/a
        #//*[@id="content"]/div/div[3]/div[2]/div[3]/div/div[3]/div[1]/div[1]/div[2]/div/div/div[2]/div/div[1]/div[11]/div/div[5]/div[2]/div[2]/a
        #//*[@id="content"]/div/div[3]/div[2]/div[3]/div/div[3]/div[1]/div[1]/div[2]/div/div/div[2]/div/div[1]/div[12]/div/div[6]/div[2]/div[2]/a
        #//*[@id="content"]/div/div[3]/div[2]/div[3]/div/div[3]/div[1]/div[1]/div[2]/div/div/div[2]/div/div[1]/div[13]/div/div[6]/div[2]/div[2]/a
        #//*[@id="content"]/div/div[3]/div[2]/div[3]/div/div[3]/div[1]/div[1]/div[2]/div/div/div[2]/div/div[1]/div[15]/div/div[6]/div[2]/div[2]/a
        #//*[@id="content"]/div/div[3]/div[2]/div[3]/div/div[3]/div[1]/div[1]/div[2]/div/div/div[2]/div/div[1]/div[15]/div/div[6]/div[2]/div[2]/a
        #//*[@id="content"]/div/div[3]/div[2]/div[3]/div/div[3]/div[1]/div[1]/div[2]/div/div/div[2]/div/div[1]/div[16]/div/div[5]/div[2]/div[2]/a
        #//*[@id="content"]/div/div[3]/div[2]/div[3]/div/div[3]/div[1]/div[1]/div[2]/div/div/div[2]/div/div[1]/div[19]/div/div[5]/div[2]/div[2]/a
        #//*[@id="content"]/div/div[3]/div[2]/div[3]/div/div[3]/div[1]/div[1]/div[2]/div/div/div[2]/div/div[1]/div[24]/div/div[5]/div[2]/div[2]/a
        #
        #//*[@id="content"]/div/div[3]/div[2]/div[3]/div/div[3]/div[1]/div[1]/div[2]/div/div/div[2]/div/div[1]/div[10]/div/div[5]/div[2]/div[1]/a[1]
        #//*[@id="content"]/div/div[3]/div[2]/div[3]/div/div[3]/div[1]/div[1]/div[2]/div/div/div[2]/div/div[1]/div[11]/div/div[5]/div[2]/div[1]/a[1]
        #//*[@id="content"]/div/div[3]/div[2]/div[3]/div/div[3]/div[1]/div[1]/div[2]/div/div/div[2]/div/div[1]/div[12]/div/div[6]/div[2]/div[1]/a
        #//*[@id="content"]/div/div[3]/div[2]/div[3]/div/div[3]/div[1]/div[1]/div[2]/div/div/div[2]/div/div[1]/div[13]/div/div[6]/div[2]/div[1]/a
        #//*[@id="content"]/div/div[3]/div[2]/div[3]/div/div[3]/div[1]/div[1]/div[2]/div/div/div[2]/div/div[1]/div[15]/div/div[6]/div[2]/div[1]/a
        #//*[@id="content"]/div/div[3]/div[2]/div[3]/div/div[3]/div[1]/div[1]/div[2]/div/div/div[2]/div/div[1]/div[16]/div/div[5]/div[2]/div[1]/a
        #//*[@id="content"]/div/div[3]/div[2]/div[3]/div/div[3]/div[1]/div[1]/div[2]/div/div/div[2]/div/div[1]/div[17]/div/div[5]/div[2]/div[1]/a[1]
        #//*[@id="content"]/div/div[3]/div[2]/div[3]/div/div[3]/div[1]/div[1]/div[2]/div/div/div[2]/div/div[1]/div[19]/div/div[5]/div[2]/div[1]/a[1]
        elm_song.append(get_text)
    mass_songs.append(elm_song)
print(mass_songs)

with open(f'{get_path_for_txt_record()}', 'a+', encoding='UTF-8') as f:
    for i in mass_songs:
        write_text = ""
        write_text += i[0].text
        write_text += ' '
        write_text += i[1].text
        write_text += '\n'
        f.write(f'{write_text}')



driver.quit()