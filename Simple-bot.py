#!/usr/bin/env python3

import telebot
from telebot import types
from enum import Enum
import psycopg2
from datetime import datetime

conn = psycopg2.connect(
    database="timetable_bot",
    user="postgres",
    password="poly2212",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

token = '5667034864:AAHQPpaKhz9vBerF-Qi8xZTqj5VJN4Ptd_Q'

class WeekDay(Enum):
    MON = "monday"
    TUE = "tuesday"
    WED = "wednesday"
    THU = "thursday"
    FRI = "friday"
    SAT = "saturday"
    SUN = "sunday"
WEEKDAY_TITLES = {
    WeekDay.MON.value: "понедельник",
    WeekDay.TUE.value: "вторник",
    WeekDay.WED.value: "среду",
    WeekDay.THU.value: "четверг",
    WeekDay.FRI.value: "пятницу",
    WeekDay.SAT.value: "субботу",
    WeekDay.SUN.value: "воскресенье",
}

universal_keyboard = types.ReplyKeyboardMarkup()
universal_keyboard.row("/week", "/nextweek")
universal_keyboard.row("/monday", "/tuesday", "/wednesday")
universal_keyboard.row("/thursday", "/friday", "/saturday")

def is_odd_week():
    delta = datetime.today() - datetime(2022, 8, 29)
    return (delta.days // 7) % 2 == 0

def fetch_day(day):
    cursor.execute("""
    SELECT teacher.subject, room_numb, start_time, full_name
    FROM timetable JOIN teacher ON timetable.subject = teacher.subject
    WHERE day=%s
    ORDER BY start_time ASC;""", (day,))
    records = cursor.fetchall()
    return records

def format_day(day):
    data = fetch_day(day)
    text = f"Расписание на {WEEKDAY_TITLES[day.strip('o')]}:\n"
    for row in data:
        subject = " ".join([str(col) for col in row])
        text += f"------\n{subject}\n"
    if not data:
        text += "занятий нет\n"
    text += "------"
    return text

def format_week(next=False):
    text = f"Расписание на {'следующую' if next else 'текущую'} неделю:"
    odd = (not is_odd_week()) if next else is_odd_week()
    for day in WeekDay:
        text += "\n\n" + format_day(("o" if odd else "") + day.value)
    return text

with open("token", "r") as f:
    global bot
    bot = telebot.TeleBot(f.read())

@bot.message_handler(commands=["start"])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    keyboard.row("Хочу", "/help")
    bot.send_message(message.chat.id, "Привет! Хочите узнать свежую информацию о МТУСИ?", reply_markup=keyboard)

@bot.message_handler(commands=["monday", "tuesday", "wednesday", "thursday", "friday", "saturday"])
def start(message):
    day = message.text[1:]
    if is_odd_week(): day = "o" + day
    bot.send_message(message.chat.id, format_day(day), reply_markup=universal_keyboard)

@bot.message_handler(commands=["week", "nextweek"])
def start(message):
    next = "next" in message.text
    bot.send_message(message.chat.id, format_week(next), reply_markup=universal_keyboard)

@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id, "Я умею выводить расписание для группы БИН2206 и ссылку на официальный сайт МТУСИ (/mtuci)",
        reply_markup=universal_keyboard)

@bot.message_handler(commands=["mtuci"])
def answer(message):
    bot.send_message(message.chat.id, "https://mtuci.ru/", reply_markup=universal_keyboard)

@bot.message_handler(content_types=["text"])
def answer(message):
    if message.text.lower() == "хочу":
        bot.send_message(message.chat.id, "Тогда Вам сюда - https://mtuci.ru/", reply_markup=universal_keyboard)
    else:
        bot.send_message(message.chat.id, "Извините, я вас не понял", reply_markup=universal_keyboard)

bot.polling()