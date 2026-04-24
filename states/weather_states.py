from telebot.handler_backends import State, StatesGroup


class WeatherStates(StatesGroup):
    waiting_for_city = State()