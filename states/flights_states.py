from telebot.handler_backends import State, StatesGroup


class FlightsStates(StatesGroup):
    waiting_for_origin = State()
    waiting_for_destination = State()
    waiting_for_date = State()