from fsm_bot import TelegramBotFSM
from statemachine.contrib.diagram import DotGraphMachine

if __name__ == "__main__":
    fsm = TelegramBotFSM()
    graph = DotGraphMachine(fsm)
    graph().write_png("bot_fsm.png")
    print("Схема FSM для telegram-бота сохранена как bot_fsm.png")