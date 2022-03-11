import tkinter as tk
import pyodbc
import decimal
import pyperclip
#True =  to run with building window, not as console. False - to run as console (not tested after window mode added. Worked before widow mode.
b_run_as_window_not_as_console = True
# window_icon = "barrel_icon.ico"     can not be icluded into one EXE file programm
program_name = "MST7.2 Cement Matrix Evaluator v.1.0.1"
about_program_text = [program_name + "\nThe program is designed to work on MST7.2 of Ignalina Nuclear Power Plant.\n"
                      "It helps to evaluate maximum bulk wastes, what can be loaded into a container on MST7.2, "
                      "and hence cement matrix mass to be loaded after.\n"
                      "The program connects to Tracking database, collects and represents information for present on MST7.2 container or for any other container (for entered barcode).\n\n"
                      "Developer: Jevgenij Kariagin\n"
                      "Used programming language: Python.\n"
                      "email: mahoni1983@mail.ru\n"
                      "2020-04",
                      program_name + "\nПрограмма предназначена для работы на MST7.2 Игналинской атомной электростанции.\n"
                      "Помогает расчитать максимальную массу длинномерных отходов, загружаемых в контейнер, и "
                      "массу цемента, который будет залит после загрузки отходов в этот контейнер.\n"
                      "Программа подсоединяется к базе данных Tracking комплекса по переработке радиоактивных отходов, собирает и показывает информацию по установленному на MST7.2 контейнеру или по другому контейнеру (по введённому штрих-коду).\n\n"
                      "Разработчик: Евгений Карягин\n"
                      "Язык программирования: Python.\n"
                      "email: mahoni1983@mail.ru\n"
                      "2020-04"]
# connector to Access db or Tracking.
connector = None
# version="v.1.0.1"
# path to Access file. The program connects first to it.
path_to_mdb = "D:\\работа\\2020-03-10.mdb"
# used for console. language is English or not.
b_language_en = True
current_language_id = 0  # 0- English, 1 - Russian
# not used. for using dict in lang switching
#current_status_key = None
#  current status for switching lang.
current_status_id = 0
# query to get info for btn_current
query_curent = "select * from UserView_TST16_ContInfo where Container in (select ID_Cont from T_Cont where lastAction_Cont = 700700)"
# query to get info for btn_custom
query_custom = "select * from UserView_TST16_ContInfo where Container="

# to represent answer from SQL in appropriate form for two lang.
list_columns = [
    ["Container", "Drums_count", "Drums_Height_in_mm", "Drums_Mass_in_kg", "Drums_Volume_in_m3",
     "Drums_Density_in_g_per_cm3", "Concrete_Volume_in_m3", "Concrete_Mass_in_kg", "Mass_Drums_and_concrete_in_kg",
     "Density_Drums_and_concrete_in_g_per_cm3", "Total_container_mass_in_kg", "Maximum_steel_bulk_volume_to_add_m3",
     "Maximum_steel_bulk_mass_to_add_kg", "Minimum_concrete_mass_if_bulk_added_kg", "Total_alpha_activity_in_Bq",
     "Total_beta_activity_in_Bq", "Total_gamma_activity_in_Bq", "Used_container_mass_brutto_in_kg",
     "Used_concrete_density_in_g_per_cm3"],
    ["Container Nr.", "Drums loaded count", "Drums height (mm)", "Drums mass (kg)", "Drums volume (m3)",
     "Drums density (g/cm3)", "Concrete volume without bulk (m3)", "Concrete mass without bulk (kg)", "Mass drums and concrete without bulk (kg)",
     "Density drums and concrete without bulk(g/cm3)", "Total container mass without bulk(kg)", "Maximum steel bulk volume to add (m3)",
     "Maximum steel bulk mass to add kg", "Minimum concrete mass if bulk added (kg)", "Total alpha activity (Bq)",
     "Total beta activity (Bq)", "Total gamma activity (Bq)", "Used container mass brutto (kg)",
     "Used concrete density (g/cm3)"],
    ["Номер контейнера", "Количество загруженных бочек", "Высота бочек (мм)", "Масса бочек (кг)", "Объём бочек (м3)",
     "Плотность бочек (г/см3)", "Объём цемента без длинномеров (м3)", "Масса цемента без длинномеров (кг)", "Масса цемента и бочек без длинномеров (кг)",
     "Плотность бочек и цемента без длинномеров (г/см3)", "Полная масса контейнера без длинномеров (кг)",
     "Максимальный объём стальных длинномеров к догрузке (м3)",
     "Максимальная масса стальных длинномеров к догрузке (кг)",
     "Минимальная масса цемента при догрузке стальных длинномеров (кг)", "Сумма альфа активностей (Бк)",
     "Сумма бета активностей (Бк)", "Сумма гамма активностей (Бк)"
        , "Масса пустого контейнера для расчётов (кг)", "Плотность цемента для расчётов (г/см3)"]
]

# for switching lang.
dict_controls = {'btn_about': ["About program", "О программе"],
                 'lbl_language': ["Language", "Язык"],
                 'lbl_current': ["Current container (on MST7.2)", "Контейнер на MST7.2"],
                 'btn_current': ["Show info", "Получить информацию"],
                 'lbl_custom': ["Custom container (through barcode)", "Контейнер по введённому штрих-коду"],
                 'btn_custom': ["Show info", "Получить информацию"],
                 'btn_exit': ["Exit program", "Выход"],
                 'btn_copy_to_clipboard': ["Copy text to clipboard", "Скопировать текст в буфер обмена"],
                 'btn_clear': ["Clear text", "Стереть текст"],
                 # '': ["", ""],
                 }

# not used, for different lang. to choose from. Replaced by list, but dict. looks to suit better.
# dict_status = {'Connecting to Tracking database': ["Connecting to Tracking database", "Устанавливается соединение с базой данных Tracking"],
#                'Connected to Tracking database successfully': ["Connected to Tracking database successfully", "Соединение с базой данных Tracking установлено успешно"],
#                'Failed to connect to a database': ["Failed to connect to Tracking database", "Связь с базой данных Tracking не установлена"],
#                 'Connected to the MS Access database successfully': ["Connected to the MS Access database successfully", "Соединение с базой данных MS Access установлено успешно"],
#                 'Program started': ["Program started", "Программа запущена"]
#                }

# for switching lang.
list_status = [["Program started", "Программа запущена"],
               ["Connecting to Tracking database. Please wait, can take up to a minute", "Устанавливается соединение с базой данных Tracking, может занять до минуты времени."],
               ["Connected to Tracking database successfully",
                "Соединение с базой данных Tracking установлено успешно"],
               ["Failed to connect to Tracking database", "Связь с базой данных Tracking не установлена"],
               ["Connected to the MS Access database successfully",
                "Соединение с базой данных MS Access установлено успешно"],
               ["Failed to connect to Tracking database", "Нет соединения с базой данных Tracking"]
               ]

def connect_to_db():
    """connection to DB, first to Access file to path_to_mdb, second to Tracking"""
    print("connect_to_db started")
    change_status("connecting to a MS Access database")
    # append_text("connecting to a MS Access database")
    try:
        try:
            connector = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + path_to_mdb + ';')
            print("Connected to a MS Access database")
            # append_text("connected to the MS Access database")
            change_status("Connected to the MS Access database successfully")
        except:
            print("Connect to a MS Access database failed")
            # append_text("connecting to a SQL database")
            change_status("Connecting to Tracking database. Please wait, can take up to a minute")
            connector = pyodbc.connect('Driver={SQL Server};'
                                       'Server=GK990-a05;'
                                       'Database=TrackingDBB234;'
                                       'Trusted_Connection=yes;')
            print("Connected to Tracking database")
            append_text("connected to the SQL database")
            change_status("Connected to Tracking database successfully")
    except:
        connector = None
        print("Failed to connect to a database")
        append_text("Failed to connect to a database")
        change_status("Failed to connect to Tracking database")
    return (connector)


def get_current_time():
    import time
    secondsSinceEpoch = time.time()
    timeObj = time.localtime(secondsSinceEpoch)
    time_now = '%d-%02d-%02d %02d:%02d:%02d' % (
        timeObj.tm_year, timeObj.tm_mon, timeObj.tm_mday, timeObj.tm_hour, timeObj.tm_min, timeObj.tm_sec)
    #print('Current TimeStamp is : %d-%d-%d %d:%d:%d' % (
        #timeObj.tm_mday, timeObj.tm_mon, timeObj.tm_year, timeObj.tm_hour, timeObj.tm_min, timeObj.tm_sec))
    return (time_now)


def show_results(cursor):
    """
    to work out with SQL results and represent according to lang. choice
    :param cursor: result from SQL
    :return: result taking in an account lang. goes to text widget
    """
    global b_language_en
    global current_language_id
    global list_data
    # column_number - column_from_list_columns_to_print
    column_number = 0
    if current_language_id == 0:
        column_number = 1
    elif current_language_id == 1:
        column_number = 2
    try:
        results = cursor.fetchall()
    except:
        results = []
        print('Error getting results from DB')
    print("debug: len(results): ", len(results))
    result_text = ""
    if len(results) != 0:
        for i in range(0, len(cursor.description)):
            # print(i+1, '\t', cursor.description[i][0], '\t', results[0][i])
            parameter_name = cursor.description[i][0]
            if cursor.description[i][0] in list_columns[0]:
                row_number = list_columns[0].index(cursor.description[i][0])
                # print("debug row_number:", row_number)
                parameter_name = list_columns[column_number][row_number]
            # print("debug parameter_name:", parameter_name)
            print((str(i + 1)+'.').ljust(4) + parameter_name + ':'.ljust(3) + str(results[0][i]))
            result_text = result_text + (str(i + 1)+'.').ljust(4) + parameter_name + ':'.ljust(3) + str(results[0][i]) + '\n'


    else:
        print("No results returned")
        if current_language_id == 0:
            result_text = "No results returned from the database.\n"
        elif current_language_id == 1:
            result_text = "Возвращён нулевой результат из базы данных.\n"
    result_text = get_current_time() + '\n' + result_text
    result_text = result_text + "===================================================\n"
    print("===================================================\n")
    append_text(result_text)


def show_info_about_current_container():
    """
    make connection if not connected yet, take info from db and show results (with show_results())
    :return: none
    """
    print("show_info_about_current_container() started")
    global connector
    if connector == None:
        connector = connect_to_db()
    if connector == None:  # failed to connect to DB
        append_text("Failed to connect to a DB")
    else:
        cursor = connector.cursor()
        cursor.execute(query_curent)
        show_results(cursor)

def show_info_about_custom_container(custom_container):
    """
    make connection if not connected yet, take info from db and show results (with show_results())
    :return: none
    """
    print("show_info_about_current_container() started")
    global connector
    if connector == None:  # check connected to a DB or not
        connector = connect_to_db()
    if connector == None:  # failed to connect to DB
        append_text("Failed to connect to a DB")
    else:
        cursor = connector.cursor()
        try:
            cursor.execute(query_custom + custom_container)
        except:
            print('Error in executing SQL query')
        show_results(cursor)


def show_menu():
    """
    shows menu in console mode
    :return:
    """
    global b_language_en
    if b_language_en:
        print("-----Menu-----")
        print("1. Show info about current container on MST7.2")
        print("2. Show info about custom container (with bar-code)")
        print("8. Меню на русском.")
        print("9. Quit program.")
        chosen_option = input("Please choose an option: ")
    else:
        print("-----Меню-----")
        print("1. Показать информацию о текущем контейнере на MST7.2")
        print("2. Показать информацию о контейнере по штрих-коду")
        print("8. Menu in English.")
        print("9. Выход из программы.")
        chosen_option = input("Пожалуйста выберете пункт: ")
    print("")
    return (chosen_option)


def choice_selection(chosen_option):
    """
    for console mode. run a way from selected option
    :param chosen_option:
    :return:
    """
    global b_language_en
    try:
        if chosen_option == "1":
            print("Option 1: Showing info about current container on MST7.2")
            show_info_about_current_container()
        elif chosen_option == "2":
            print("Option 2")
            custom_container = input("Please type in container number: \n")
            show_info_about_custom_container(custom_container)
        elif chosen_option == "8":
            print("Option 8")
            if b_language_en:
                b_language_en = False
                print("Switching to Russian\n")
            else:
                b_language_en = True
                print("Переключаем язык на английский\n")
        elif chosen_option == "9":
            print("Option 9")
            return (True)
        else:
            print("Not correct option")
    except:
        print("Error: connection to a database failed\n")
        return None


def run_console():
    """
    to run console in console mode
    :return:
    """
    b_to_quit = False
    while not b_to_quit:
        chosen_option = show_menu()
        b_to_quit = choice_selection(chosen_option)
    print("End program")


def show_about():
    """
    shows about dialog
    :return:
    """
    print("show_about called")
    global window
    from tkinter import messagebox
    # messagebox = tk.messagebox()
    # messagebox.showinfo("Information", "Informative message")
    if current_language_id == 0:
        tk.messagebox.showinfo(title="About Program", message=about_program_text[0])  # , **options)
    elif current_language_id == 1:
        tk.messagebox.showinfo(title="О программе", message=about_program_text[1])
    # window.build_window().show_custom()
    # window.show_custom()
    # window.txt_info.insert(1.0, "about")


def exit_program():
    print("exit called")
    window.destroy()


def append_text(text):
    """
    appends text (parameter) to Text widget txt_info.
    :param text:
    :return:
    """
    global txt_info
    txt_info.configure(state='normal')
    txt_info.insert(tk.END, text + '\n')
    # global window
    # window.update()
    txt_info.see(tk.END)
    txt_info.configure(state='disabled')


def change_status(new_status_to_set_eng):
    """
    changes status taking in account lang. using list_status
    :param new_status_to_set_eng:
    :return:
    """
    global lbl_status
    global current_status_id
    new_status = new_status_to_set_eng
    if current_status_id != 'None':
        global list_status
        #new_status = new_status_to_set_eng
        for i in range(len(list_status)):
            #print('list_status[i][0] ', list_status[i][0])
            if list_status[i][0] == new_status_to_set_eng:
                new_status = list_status[i][current_language_id]
                current_status_id = i
                break
    # commented part is to work with status texts stored in dictionary
    #global current_language_id
    #new_status = 'text'
    # if text in dict_status:
    #     new_status = dict_status[text][current_language_id]
    #     global current_status_key
    #     current_status_key = text
    # else:
    #     new_status = text
    #current_status = lbl_status['text']
    # global list_status
    # new_status = new_status_to_set_eng
    # for i in range(len(list_status)):
    #     print('list_status[i][0] ', list_status[i][0])
    #     if list_status[i][0] == new_status_to_set_eng:
    #         new_status = list_status[i][current_language_id]
    #         print('new_status: ', new_status)
    #         #change_status(list_status[i][new_language_id])
    #         break
    lbl_status.config(text=new_status)

    global window
    window.update()


def show_current():
    """
    shows current container info when clicked btn_current
    :return:
    """
    print("show_current called")
    show_info_about_current_container()


def show_custom():
    """
    shows custom container info when clicked btn_custom
    :return:
    """
    print("show_custom called")
    global window
    global ent_barcode

    barcode = ent_barcode.get()
    if barcode == "":
        append_text("Please enter a barcode")
    else:
        print("barcode: ", barcode)
        if current_language_id == 0:
            append_text("entered barcode: " + barcode + '\n')
        elif current_language_id == 1:
            append_text("Введён штрих-код: " + barcode + '\n')
        show_info_about_custom_container(barcode)


# def get_all_children_widgets (parent_widget) :
#     """ gets all of the widgets within one entire window.
#     it is needed to switch language for all possible widgets"""
#     _list = parent_widget.winfo_children()
#
#     for item in _list :
#         if item.winfo_children() :
#             _list.extend(item.winfo_children())
#     return _list

def switch_language():
    """
    to switch lang.
    :return:
    """
    global var_language
    global current_language_id
    global current_status_id

    new_language_id = var_language.get()
    if current_language_id != new_language_id:
        print("changing language, old language_id: ", current_language_id)
        print("new language id: ", var_language.get())

        for key in dict_controls:
             if key in globals():
                 # print("switching language: ", key)
                 globals().get(key)['text'] = dict_controls[key][new_language_id]
        global lbl_status
      #  print(list_status.index([lbl_status['text']])[])
      #  for element in list_status[current_language_id]

        # status language change block


        current_language_id = new_language_id

        lbl_status['text'] = list_status[current_status_id][current_language_id]
        #change_status(lbl_status['text'])
        # if current_status_key != None:
        #     change_status(current_status_key)
        # else:
        #     change_status(lbl_status['text'])
    # window.update()


def clear_text():
    print("clear text started")
    # global txt_info
    txt_info.configure(state='normal')
    txt_info.delete(1.0, tk.END)
    txt_info.configure(state='disabled')

def copy_to_clipboard():
    print("copy_to_clipboard started")
    pyperclip.copy(txt_info.get("1.0",tk.END))

# Window elements
window = tk.Tk()
#window.iconbitmap(window_icon)     can not be icluded into one EXE file programm
window.geometry('+0+0')
fr1_1_2 = tk.Frame(window, borderwidth=10)
fr1 = tk.Frame(fr1_1_2, borderwidth=10)
lbl_name = tk.Label(master=fr1, text=program_name)
btn_about = tk.Button(master=fr1, text="About program", command=show_about)

fr1_2 = tk.Frame(fr1_1_2, borderwidth=10)
lbl_language = tk.Label(master=fr1_2, text="Language")
var_language = tk.IntVar()
radbtn1 = tk.Radiobutton(fr1_2, text='English', variable=var_language, value=0, command=switch_language)
radbtn2 = tk.Radiobutton(fr1_2, text='Русский', variable=var_language, value=1, command=switch_language)

fr2_3 = tk.Frame(window)
fr2 = tk.Frame(fr2_3, borderwidth=2, relief=tk.GROOVE)
lbl_current = tk.Label(master=fr2, text="Current container (on MST7.2)")
btn_current = tk.Button(master=fr2, text="Show info", command=show_current)
fr3 = tk.Frame(fr2_3, borderwidth=2, relief=tk.GROOVE)
lbl_custom = tk.Label(master=fr3, text="Custom container (through barcode)")
ent_barcode = tk.Entry(fr3, width=16)
btn_custom = tk.Button(master=fr3, text="Show info", command=show_custom)
lbl_status = tk.Label(master=window, text="Program started")
fr4 = tk.Frame(master=window, borderwidth=2)
txt_info = tk.Text(fr4, width=65, height=23, yscrollcommand=True)
scrollb = tk.Scrollbar(fr4, command=txt_info.yview)

fr5 = tk.Frame(window, borderwidth=10)
btn_exit = tk.Button(master=fr5, text="Exit program", command=exit_program)
btn_copy_to_clipboard = tk.Button(master=fr5, text="Copy text to clipboard", command=copy_to_clipboard)
btn_clear = tk.Button(master=fr5, text="Clear text", command=clear_text)


def build_window():
    global window
    window.title(program_name)
    # window.rowconfigure(0, weight=1)
    # window.columnconfigure(0, weight=1)
    # window.columnconfigure(1, weight=1)

    #    fr1 = tk.Frame(window, borderwidth=10)
    global fr1_1_2
    global fr1
    ##fr1.columnconfigure([0, 1], minsize=100, weight=1)
    ##fr1.rowconfigure(0, minsize=100, weight=1)
    ##fr1.grid(row=0, column=0)
    global lbl_name
    # lbl_name=tk.Label(master=fr1, text=program_name)
    lbl_name.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
    ##lbl1.grid(row=0, column=0, padx=5, pady=5)
    # btn_about=tk.Button(master=fr1, text="About program", command=show_about)
    global btn_about
    btn_about.pack(fill=tk.BOTH, side=tk.TOP, padx=10, pady=5)

    global lbl_language
    lbl_language.pack(fill=tk.BOTH, side=tk.TOP, padx=10, pady=1)
    global radbtn1
    global radbtn2
    radbtn1.pack(side=tk.TOP, anchor=tk.W, padx=10, pady=1)
    radbtn2.pack(side=tk.TOP, anchor=tk.W, padx=10, pady=1)
    fr1.pack(side=tk.LEFT, expand=True)
    fr1_2.pack(side=tk.LEFT, expand=True)

    fr1_1_2.pack()#expand=True)

    # btn_exit=tk.Button(master=fr1,  text="Exit program", command=exit_program)
    #    global btn_exit                            #place to bottom
    # btn1.grid(row=0, column=1, padx=5, pady=5)
    #    btn_exit.pack(fill=tk.BOTH, side=tk.RIGHT, expand=True)                            #place to bottom

    # fr1.grid(row=0, column=0)
    # fr2.pack()

    # fr2_3 = tk.Frame(window)
    # fr2 = tk.Frame(fr2_3, borderwidth=2, relief=tk.GROOVE)
    # lbl_current=tk.Label(master=fr2, text="Current container (on MST7.2)")
    global fr2_3
    global fr2
    global lbl_current
    lbl_current.pack(padx=10)
    # btn_current=tk.Button(master=fr2,  text="Show info", command=show_current)
    global btn_current
    btn_current.pack(fill=tk.BOTH, side=tk.TOP, expand=True, padx=10)
    fr2.pack(side=tk.LEFT, padx=10, pady=5)

    # fr3 = tk.Frame(fr2_3, borderwidth=2, relief=tk.GROOVE)
    # lbl_custom=tk.Label(master=fr3, text="Custom container (through barcode)")
    global fr3
    global lbl_custom
    lbl_custom.pack(padx=10)
    # ent_barcode = tk.Entry(fr3, width=16)
    global ent_barcode
    ent_barcode.pack(side=tk.LEFT, padx=10)
    # btn_custom=tk.Button(master=fr3,  text="Show info", command=show_custom)
    global btn_custom
    btn_custom.pack(side=tk.RIGHT, expand=True, padx=10)
    fr3.pack(side=tk.RIGHT, pady=5)

    fr2_3.pack()

    # lbl_status=tk.Label(master=window, text="...current status...")
    global lbl_status
    lbl_status.pack(pady=5)

    # fr4 = tk.Frame(master=window, borderwidth=2)
    global fr4
    # txt_info = tk.Text(fr4, width=70, height=30, yscrollcommand=True)
    global txt_info
    txt_info.config(state="disabled")
    # txt_info.insert(1.0, "Hello.....\n")
    # txt_info.insert(1.0, "24	state	It the state is set to DISABLED, the widget becomes unresponsive\n to the mous\ne and keyboard unresponsive\n                    25	ta\nbs	This option controls how the tab character is used to position the text.\nt represents the width of the widget in characters.")
    txt_info.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH, expand=True)
    # scrollb = tk.Scrollbar(fr4, command=txt_info.yview)
    global scrollb
    scrollb.pack(side=tk.RIGHT, fill=tk.BOTH)
    txt_info['yscrollcommand'] = scrollb.set
    fr4.pack(fill=tk.BOTH, expand=True)

    global fr5
    global btn_exit
    global btn_clear
    btn_clear.pack(fill=tk.BOTH, side=tk.LEFT, padx=10, pady=5)
    btn_copy_to_clipboard.pack(fill=tk.BOTH, side=tk.LEFT, padx=10, pady=5)
    btn_exit.pack(fill=tk.BOTH, side=tk.RIGHT, padx=10, pady=5)
    fr5.pack(fill=tk.X)

    window.mainloop()


# build_window() - uncomment to run as window application
if b_run_as_window_not_as_console:
    build_window()
else:
    run_console()
# run_console() - uncomment to run as console
# run_console()
