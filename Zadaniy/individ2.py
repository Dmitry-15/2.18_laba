#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import click
import sys
import os
from dotenv import load_dotenv


@click.group()
def clic():
    pass


@clic.command()
@click.argument('data')
@click.option("-n", "--name")
@click.option("-z", "--zodiac")
@click.option("-yr", "--year")
def add(data, name, zodiac, year):
    """
    Добавить данные о человеке.
    """
    if os.path.exists(data):
        load_dotenv()
        dotenv_path = os.getenv("PEOPLE_DATA")
        if not dotenv_path:
            click.secho("The file is missing", fg="red")
            sys.exit(1)
        if os.path.exists(dotenv_path):
            people = load_people(dotenv_path)
        else:
            people = []
        people.append(
            {
                'name': name,
                'zodiac': zodiac,
                'year': year,
            }
        )
        with open(dotenv_path, "w", encoding="utf-8") as fout:
            json.dump(people, fout, ensure_ascii=False, indent=4)
        click.secho("Человек добавлен", fg='blue')
    else:
        click.secho("The file is missing", fg="orange")

@clic.command()
@click.argument('filename')
def display(filename):
    """
    Отобразить список людей.
    """
    # Заголовок таблицы.
    if os.path.exists(filename):
        load_dotenv()
        dotenv_path = os.getenv("PEOPLE_DATA")
        if not dotenv_path:
            click.secho('Файл отсутствует', fg='red')
            sys.exit(1)
        if os.path.exists(dotenv_path):
            people = load_people(dotenv_path)
        else:
            people = []
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 20,
            '-' * 20
        )
        print(line)
        print(
            '| {:^4} | {:^30} | {:^20} | {:^20} |'.format(
                "№",
                "Ф.И.О.",
                "Знак Зодиака",
                "Дата рождения"
            )
        )
        print(line)
        # Вывести данные о всех людях.
        for idx, human in enumerate(people, 1):
            print(
                '| {:>4} | {:<30} | {:<20} | {:>20} |'.format(
                    idx,
                    human['name'],
                    human['zodiac'],
                    ' '.join((str(i) for i in human['year']))
                )
            )
        print(line)


@click.command()
@click.argument('filename')
def select(filename):
    """
    Выбрать человека по фамилии.
    """
    if os.path.exists(filename):
        load_dotenv()
        dotenv_path = os.getenv("PEOPLE_DATA")
        if not dotenv_path:
            click.secho("The file is missing", fg="red")
            sys.exit(1)
        if os.path.exists(dotenv_path):
            people = load_people(dotenv_path)
        else:
            people = []
        who = input('Кого ищем?: ')
        count = 0
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 20,
            '-' * 20
        )
        print(line)
        print(
            '| {:^4} | {:^30} | {:^20} | {:^20} |'.format(
                "№",
                "Ф.И.О.",
                "Знак Зодиака",
                "Дата рождения"
            )
        )
        print(line)
        for i, num in enumerate(people, 1):
            if who == num['name']:
                count += 1
                print(
                    '| {:^4} | {:^30} | {:^20} | {:^20} |'.format(
                        count,
                        num['name'],
                        num['zodiac'],
                        ' '.join((str(i) for i in num['year']))))
        print(line)
        if count == 0:
            print('Никто не найден')


def load_people(file_name):
    """
    Загрузить всех людей из файла JSON
    """
    with open(file_name, "r", encoding="utf-8") as fin:
        return json.load(fin)


if __name__ == '__main__':
    clic()
