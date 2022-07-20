#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import json
import time
import os
import random
import pandas as pd
from tqdm import tqdm
import chardet
from concurrent.futures import ThreadPoolExecutor, as_completed
from multiprocessing.dummy import Pool as ThreadPool
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent
from functools import partial
import multiprocessing


# In[2]:


class View:

    @staticmethod
    def _start_parse():
        while True:
            try:
                get_str = str(input('Хотите начать парсинг? - Y/N'))
            except:
                """Дописать конкретную ошибку, какой именно except вылетает"""
                print("Напишите клавишу Y или N")
                continue
            if get_str.lower() == 'y':
                return True
            elif get_str.lower() == 'n':
                print("Указите данные заново, если хотите")
                break
            else:
                print("Ошибка вводе")
                continue

    @staticmethod
    def find_out_iter():
        while True:
            try:
                get_num = int(input(
                    "Введите число итераций, через которое будет создаваться новый txt.file"
                    " для дальнейшего скачивания"))
            except:
                print("Ошибка, повторите попытку")
                continue
            return get_num

    @staticmethod
    def get_num_in_iter():
        while True:
            try:
                get_num = int(input("Введите число, которые будет скачиваться за итерацию - стандартно указывайте 100"))
            except:
                print("Ошибка, повторите попытку")
                continue
            return get_num

    @staticmethod
    def get_st_per_end(num_per_iteration):
        while True:
            try:
                get_start = int(input("Введите число с которого начнется скачивание вакансий hhru - пример: 54509900"))
            except:
                print("Ошибка, повторите попытку")
                continue
            try:
                get_finish = int(
                    input("Введите число на котором закончится, скачивание вакансий hhru - пример: 54511900"))
            except:
                print("Ошибка, повторите попытку")
                continue
            if get_start > get_finish:
                print('Ошибка, стартовая вакансия больше по номеру, окончательной')
                continue
            return (get_start, get_start + num_per_iteration, get_finish)

    @staticmethod
    def choose_method_file():
        while True:
            try:
                get_method_file = str(
                    input("Введите 1, если хотите записать файл в txt. Введите 2, если хотите записать в sqllite"))
            except:
                print('Ошибка')
                continue
            if get_method_file == '1':
                return 'method_txt'
            elif get_method_file == '2':
                return 'method_bd'
            else:
                print("Ошибка, введите 1 или 2")
                continue

    @staticmethod
    def choose_name_file():
        while True:
            try:
                get_name = str(
                    input("Введите названия файла используя A-Za-z_0-9, не используйте .txt, .sqllite3 or etc."))
            except:
                print("Ошибка при вводе имени")
                continue
            return get_name


# In[3]:


class Controler:

    def __init__(self):
        self.view_control = View()
        self.model_control = Model()

        'Будем выводить время работы кода'
        self.super_start_time = time.time()

        "Проверяем адекватность ввода пользователем."
        self.num_per_iteration = 100  # self.view_control.get_num_in_iter()
        our_number = self.view_control.get_st_per_end(self.num_per_iteration)
        self.start_num = our_number[0]
        self.end_num = our_number[1]
        self.finish_num = our_number[2]

        "Выбор мод записи text или bd"
        self.name_file_txt = self.view_control.choose_name_file()
        self.method_file_record = self.view_control.choose_method_file()
        self.control_iter = 5000  # self.view_control.find_out_iter()
        """Здесь идет подсчет сколько будет итераций"""
        self.value_of_iter = self.model_control.calc_number_of_iter_parse(self.start_num, self.finish_num,
                                                                          self.num_per_iteration)

        """начинаем работу """
        self.bd = self.create_bd(self.method_file_record)
        self.parse()

    def create_bd(self, method_file_record):
        if method_file_record == 'method_txt':
            return Bd_text()
        else:
            print("Извините bd_sqllite не доступна - выбран мод bd_text")
            return Bd_text()

    def parse(self):
        if self.view_control._start_parse() == True:
            """Хранение количество бесплатных прокси"""
            self.model_control.free_proxies = self.model_control.list_free_proxies()
            for i in range(0, self.value_of_iter):
                print(f"Этап {i} из {self.value_of_iter}-{self.start_num, self.end_num}")
                self.model_control.links = self.model_control.get_vacancies(self.start_num, self.end_num)
                self.model_control.answer = self.model_control.checker()
                if self.model_control.answer is not None:
                    self.bd.record(self.name_file_txt, self.model_control.answer, self.value_of_iter, self.control_iter)
                self.model_control.answer = ''
                self.start_num += self.num_per_iteration
                self.end_num += self.num_per_iteration
                print("--- %s seconds время работы этапа " f"{i} ---" % (time.time() - self.super_start_time))
                print("ИТОГО --- %s seconds время работы всего кода итого---" % (time.time() - self.super_start_time))


class Bd_text:
    def __init__(self):
        self.number_file = 10

    def record(self, name_file_txt, results, value_of_iter, control_iter):
        with open(f"{name_file_txt}{self.number_file}.json", "a+", encoding='UTF-8') as outfile:
            outfile.write(results)
        if value_of_iter % control_iter == 0:
            self.number_file += 1


# In[4]:


class Model:

    def __init__(self):
        """url - Поменятей на свой proxy_list, но тогда нужно изменить get_free_proxies()"""
        self.url = "https://free-proxy-list.net/"
        '''Линки которые будет скачивать в моменте(в одной итераций)'''
        self.links = None
        '''Здесь хранятся результаты answer'''
        self.answer = ''
        """Здесь хранятся бесплатные прокси"""
        self.free_proxies = None
        """Это тестовая вакансия, мы с ней работаем, менять её нет смысла"""

        self.test_proxies = 40010200

    def get_parse(self):
        self.answer = ''
        text_for_txt = ''
        self.test_proxies += 1
        """ Здесь я использую своё ip"""
        results = ''
        tester = None
        t = None
        try:
            testing_ = requests.get(f'https://api.hh.ru/vacancies/{self.test_proxies}', timeout=30)
            t = True
        except:
            t = False
            pass
        if t == True:
            testing__ = testing_.text
            testing__ = testing__[2:8]
            print(testing__)
            if testing_.status_code == 200 or testing_.status_code == 404 and testing__ != 'errors':
                try:
                    pool = ThreadPool(13)
                    results = pool.map(requests.get, self.links)
                    tester = True
                except:
                    tester = False
                pool.close()
                pool.join()
            elif testing_.status_code == 403:
                tester = False
            else:
                pass
            if tester == True:
                for i in tqdm(results):
                    if i.status_code == 200 or i.status_code == 404:
                        print('success MyIP')
                        return self.insteding_information(results)
            else:
                pass
        else:
            pass
        """Теперь мы парсим с помощью чужих proxies"""
        for proxy in tqdm(self.free_proxies):
            s = self._get_session(proxy)
            self.test_proxies += 1
            try:
                testing = s.get(f'https://api.hh.ru/vacancies/{self.test_proxies}', timeout=30)
            except Exception as e:
                continue
            if testing.status_code == 200 or testing.status_code == 404:
                testing = testing.text
                testing = testing[2:8]
                if testing == 'errors':
                    continue
                else:
                    my_tuples = [(link, proxy, 30) for link in self.links]
                    try:
                        print('Parse')
                        pool = ThreadPool(13)
                        self.answer = pool.map(self.smart_parse, my_tuples)
                    except Exception as e:
                        continue
                    pool.close()
                    pool.join()
                    self.answer = [value for value in self.answer if value]
                    self.answer = self.insteding_information()
                    return self.answer
            else:
                continue
        return 'Error'

    # """Здесь идет подсчет сколько будет итераций"""
    @staticmethod
    def calc_number_of_iter_parse(start_num, finall_num, num_iter):
        return int((finall_num - start_num) / num_iter)

    def _get_session(self, proxy):
        proxy = (f"http://{proxy}")
        session = requests.Session()
        session.proxies = {"http": proxy, "https": proxy}
        return session

    def get_free_proxies(self):
        # получаем ответ HTTP и создаем объект soup
        soup = bs(requests.get(self.url).content, "html.parser")
        proxies = []
        for row in tqdm(soup.find("table", attrs={"class": "table table-striped table-bordered"}).find_all("tr")[1:]):
            tds = row.find_all("td")
            try:
                ip = tds[0].text.strip()
                port = tds[1].text.strip()
                host = f"{ip}:{port}"
                proxies.append(host)
            except IndexError:
                continue
        result = [i for i in proxies if i]
        return proxies

    def list_free_proxies(self, timeout=0.75):
        mass = []
        free_proxies = self.get_free_proxies()
        for elm in tqdm(free_proxies):
            s = self._get_session(elm)
            try:
                s = s.get("http://icanhazip.com", timeout=timeout)
            except:
                continue
            s = s.text.strip()
            test = elm.split(':')
            test = test[0]
            count = 0
            if len(test) == len(s):
                for i in range(0, len(s)):
                    if test[i] == s[i]:
                        count += 1
                    else:
                        continue
            if count == len(test) == len(s):
                mass.append(elm)
            else:
                continue
        return mass

    def get_vacancies(self, start_num, end_num):
        links = []
        for num in tqdm(range(start_num, end_num)):
            req = f'https://api.hh.ru/vacancies/{num}'
            links.append(req)
        return links

    def checker(self):
        #         self.free_proxies
        results = self.get_parse()
        if results == 'Error' or results == None:
            print("Пересборка прокси")
            self.free_proxies = self.list_free_proxies()
            results = self.checker()
        else:
            return results


    def smart_parse(self, some_tuple):
        link = some_tuple[0]
        proxy = some_tuple[1]
        timeout = some_tuple[2]
        answer = None
        s = self._get_session(proxy)
        try:
            r = s.get(link, timeout=timeout)
        except Exception as e:
            answer = 'Error'
        if answer != 'Error':
            testing = r.text
            testing = testing[2:8]
            #             print(testing)
            if r.status_code == 200 and testing != 'errors':
                return r
        else:
            return None

    def insteding_information(self):
        text_for_txt = ''
        for ans in self.answer:
            if ans != None and ans.status_code == 200:
                text_for_txt += f'{ans.text} \n'
            else:
                pass
        return text_for_txt


# In[5]:


Controler()

# In[6]:


# print(control.end_num,
#      control.finish_num,
#      control.method_file_record,
#      control.name_file_num,
#      control.name_file_txt,
#      control.num_per_iteration,
#      control.start_num,
#      control.value_of_iter)


# In[7]:


# with open("hhru_test1.txt", 'r', encoding='utf-8') as x:
#     print(x.readlines())


# In[8]:


"""50792468 - 54509799"""
