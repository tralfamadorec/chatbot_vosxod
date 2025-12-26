from statemachine import StateMachine, State


class TelegramBotFSM(StateMachine):
    # главное меню
    main_menu = State(initial=True)

    # задание 1
    task1_menu = State()
    task1_input_manual = State()
    task1_input_random = State()
    task1_execute = State()
    task1_show_result = State()

    # задание 5
    task5_menu = State()
    task5_input_manual = State()
    task5_input_random = State()
    task5_execute = State()
    task5_show_result = State()

    # задание 8
    task8_menu = State()
    task8_input_manual = State()
    task8_input_random = State()
    task8_execute = State()
    task8_show_result = State()

    # переходы из главного меню
    to_task1 = main_menu.to(task1_menu)
    to_task5 = main_menu.to(task5_menu)
    to_task8 = main_menu.to(task8_menu)
    to_all_tasks = main_menu.to(main_menu)  # остаёмся в меню

    # задание 1: переходы
    task1_manual = task1_menu.to(task1_input_manual)
    task1_random = task1_menu.to(task1_input_random)
    task1_exec = task1_menu.to(task1_execute)
    task1_result = task1_menu.to(task1_show_result)
    task1_back_from_menu = task1_menu.to(main_menu)
    task1_back_from_manual = task1_input_manual.to(main_menu)
    task1_back_from_random = task1_input_random.to(main_menu)
    task1_back_from_execute = task1_execute.to(main_menu)
    task1_back_from_result = task1_show_result.to(main_menu)

    # задание 5: переходы
    task5_manual = task5_menu.to(task5_input_manual)
    task5_random = task5_menu.to(task5_input_random)
    task5_exec = task5_menu.to(task5_execute)
    task5_result = task5_menu.to(task5_show_result)
    task5_back_from_menu = task5_menu.to(main_menu)
    task5_back_from_manual = task5_input_manual.to(main_menu)
    task5_back_from_random = task5_input_random.to(main_menu)
    task5_back_from_execute = task5_execute.to(main_menu)
    task5_back_from_result = task5_show_result.to(main_menu)

    # задание 8: переходы
    task8_manual = task8_menu.to(task8_input_manual)
    task8_random = task8_menu.to(task8_input_random)
    task8_exec = task8_menu.to(task8_execute)
    task8_result = task8_menu.to(task8_show_result)
    task8_back_from_menu = task8_menu.to(main_menu)
    task8_back_from_manual = task8_input_manual.to(main_menu)
    task8_back_from_random = task8_input_random.to(main_menu)
    task8_back_from_execute = task8_execute.to(main_menu)
    task8_back_from_result = task8_show_result.to(main_menu)

    # после ввода/выполнения - возврат в меню задания
    # задание 1
    task1_input_done_manual = task1_input_manual.to(task1_menu)
    task1_input_done_random = task1_input_random.to(task1_menu)
    task1_exec_done = task1_execute.to(task1_menu)
    task1_result_done = task1_show_result.to(task1_menu)

    # задание 5
    task5_input_done_manual = task5_input_manual.to(task5_menu)
    task5_input_done_random = task5_input_random.to(task5_menu)
    task5_exec_done = task5_execute.to(task5_menu)
    task5_result_done = task5_show_result.to(task5_menu)

    # задание 8
    task8_input_done_manual = task8_input_manual.to(task8_menu)
    task8_input_done_random = task8_input_random.to(task8_menu)
    task8_exec_done = task8_execute.to(task8_menu)
    task8_result_done = task8_show_result.to(task8_menu)