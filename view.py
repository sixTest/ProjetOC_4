import controller
import os


def format_input_parameters(input_name):
    return '    -' + input_name + ' : '


def format_input_command(input_name):
    return f'{input_name} >> '


def format_input_choice(input_choice):
    return f'{input_choice} : '


def format_transition():
    return os.get_terminal_size().columns*'-'


def format_menu(key_cmd, str_description):
    return f'({str(key_cmd)}) {str_description}.'


def format_error(err):
    return f'Erreur : {err}'


def format_choice_tournament(doc_id, tournament):
    return f'* ({doc_id}) {tournament.name} / {tournament.location} / {tournament.date}'


def format_output_last_command(key_cmd, name_command):
    return f'Derniere action utilisateur : ({key_cmd}) {name_command}'


def format_output_tournament(tournament):
    return f' * Nom du tournoi             : {tournament.name}\n' \
           f' * Lieu du tournoi            : {tournament.location}\n' \
           f' * Date du tournoi            : {tournament.date}\n' \
           f' * Nombre de tours du tournoi : {tournament.numbers_rounds}\n' \
           f' * Description du tournoi     : {tournament.description}\n'


def get_input_with_repetition(input_str, check_function, params):
    while True:
        try:
            ret = input(input_str)
            if params:
                check_function(ret, params)
            else:
                check_function(ret)
            break
        except controller.InputError as e:
            show_error(e)
    return ret


def get_input(name, check_function=None, params=None, format_view=None):
    format = lambda n: format_view(n) if format_view else n
    if check_function:
        param = get_input_with_repetition(format(name), check_function, params)
    else:
        param = input(format(name))
    return param


def get_inputs_for_tournament_parameters():
    name = get_input('Nom du tournois', format_view=format_input_parameters)
    location = get_input('Lieu du tournois', format_view=format_input_parameters)
    date = get_input('Date du tournois', controller.check_date_input, format_view=format_input_parameters)
    time = get_input('Cadence du tournois (bullet, blitz, coup rapide)', controller.check_time_input, format_view=format_input_parameters)
    number_round = int(get_input('Nombre de tours du tournois', controller.check_number_round_input, format_view=format_input_parameters))
    description = get_input('Description du tournois', format_view=format_input_parameters)
    return name, location, date, time, description, number_round


def get_inputs_for_player_parameters():
    last_name = get_input('Nom du joueur', format_view=format_input_parameters)
    first_name = get_input('Prénom du joueur', format_view=format_input_parameters)
    birthdate = get_input('Date de naissance du joueur', controller.check_date_input, format_view=format_input_parameters)
    gender = get_input('Sexe (H/F)', controller.check_gender_input, format_view=format_input_parameters)
    ranking = int(get_input('Classement', controller.check_ranking_input, format_view=format_input_parameters))
    return last_name, first_name, birthdate, gender, ranking


def show_menu(dict_menu):
    for k,v in dict_menu.items():
        print(format_menu(k, v[0]))


def show_error(err):
    print(format_error(err))


def show_transition():
    print(format_transition())


def show_output(key_cmd, function_name, function, params):
    print(format_output_last_command(key_cmd, function_name))
    print(function(*params))


def show_tournaments_choices(docs_id, tournaments):
    for i in range(len(docs_id)):
        print(format_choice_tournament(docs_id[i], tournaments[i]))


