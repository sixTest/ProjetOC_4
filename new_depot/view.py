import controller
import os
import pdb


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


def format_choice_player(doc_id, player):
    return f'* ({doc_id}) {player.last_name} / {player.first_name}'


def format_output_last_command(key_cmd, name_command):
    return f'Derniere action utilisateur : ({key_cmd}) {name_command}'


def format_output_tournament(tournament):
    return f' * Nom du tournoi             : {tournament.name}\n' \
           f' * Lieu du tournoi            : {tournament.location}\n' \
           f' * Date du tournoi            : {tournament.date}\n' \
           f' * Nombre de tours du tournoi : {tournament.numbers_rounds}\n' \
           f' * Description du tournoi     : {tournament.description}\n' \
           f' * Joueurs                    : {tournament.indices_players}\n'


def format_output_creation_player(player):
    return f' * Nom du joueur               : {player.last_name}\n' \
           f' * Prénom du joueur            : {player.first_name}\n' \
           f' * Sexe du joueur              : {player.gender}\n' \
           f' * Date de naissance du joueur : {player.birthdate}\n' \
           f' * Classement du joueur        : {player.ranking}\n'


def format_output_players(doc_ids, players):
    output = ''
    for i in range(len(doc_ids)):
        output += format_choice_player(doc_ids[i], players[i])+'\n'
    return output


def format_output_tournaments(doc_ids, tournaments):
    output = ''
    for i in range(len(doc_ids)):
        output += format_choice_tournament(doc_ids[i], tournaments[i])+'\n'
    return output


def get_input_with_repetition(input_str, check_function, params):
    while True:
        try:
            ret = input(input_str)
            if params:
                if isinstance(params, tuple):
                    ret = check_function(ret, *params)
                else:
                    ret = check_function(ret, params)
            else:
                ret = check_function(ret)
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
    number_round = get_input('Nombre de tours du tournois', controller.check_number_round_input, format_view=format_input_parameters)
    description = get_input('Description du tournois', format_view=format_input_parameters)
    return name, location, date, time, description, number_round


def get_inputs_for_player_parameters():
    last_name = get_input('Nom du joueur', format_view=format_input_parameters)
    first_name = get_input('Prénom du joueur', format_view=format_input_parameters)
    birthdate = get_input('Date de naissance du joueur', controller.check_date_input, format_view=format_input_parameters)
    gender = get_input('Sexe (H/F)', controller.check_gender_input, format_view=format_input_parameters)
    ranking = get_input('Classement', controller.check_ranking_input, format_view=format_input_parameters)
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
    if isinstance(params, tuple):
        print(function(*params))
    else:
        print(function(params))


def show_tournaments_choices(docs_id, tournaments):
    for i in range(len(docs_id)):
        print(format_choice_tournament(docs_id[i], tournaments[i]))


def show_players_choices(docs_id, players):
    for i in range(len(docs_id)):
        print(format_choice_player(docs_id[i], players[i]))
