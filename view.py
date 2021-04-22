import controller
import os
import pdb


def format_output(champs, empty_counts, placements):
    strings = []
    len_max_champs = [max([len(s) for s in champs[i]]) for i in range(len(champs))]
    for i in range(len(champs[0])):
        string = ''
        for index_champ in range(len(champs)):
            value = champs[index_champ][i]
            max_len = len_max_champs[index_champ]
            empty_count = empty_counts[index_champ]
            placement = placements[index_champ]
            string+=f"{value:{placement}{max_len + empty_count}}"
        strings.append(string)

    return '\n'.join(strings)


def format_output_matches(players_1, players_2, scores_1, scores_2):
    champ1 = [p.last_name+' '+p.first_name for p in players_1]
    champ2 = len(champ1)*['VS']
    champ3 = [p.last_name+' '+p.first_name for p in players_2]
    champ4 = len(champ1)*[':']
    champ5 = [f'({scores_1[i]}, {scores_2[i]})' for i in range(len(champ1))]
    empty_counts = [3,3,3,3,0]
    placements = 5*['<']
    return format_output([champ1,champ2,champ3,champ4,champ5],empty_counts,placements)


def format_output_players_in_tournament(docs_id, players):
    champ1 = [f'* ({doc_id})' for doc_id in docs_id]
    champ2 = [p.last_name+' '+p.first_name for p in players]
    champ3 = [f'Classement {p.ranking},' for p in players]
    champ4 = [f'Points {p.points}' for p in players]
    empty_counts = [3, 3, 3, 0]
    placements = 4 * ['<']
    return format_output([champ1, champ2, champ3, champ4], empty_counts, placements)


def format_output_players_in_database(docs_id, players):
    champ1 = [f'* ({doc_id})' for doc_id in docs_id]
    champ2 = [p.last_name+' '+p.first_name for p in players]
    champ3 = [f'Classement {p.ranking}' for p in players]
    empty_counts = [3, 3, 0]
    placements = 3 * ['<']
    return format_output([champ1, champ2, champ3], empty_counts, placements)


def format_output_tournaments(docs_id, tournaments):
    champ1 = [f'* ({doc_id})' for doc_id in docs_id]
    champ2 = [tournament.name for tournament in tournaments]
    champ3 = [tournament.location for tournament in tournaments]
    champ4 = [tournament.date for tournament in tournaments]
    empty_counts = [3, 3, 3, 0]
    placements = 4 * ['<']
    return format_output([champ1, champ2, champ3, champ4], empty_counts, placements)


def format_output_last_command(key_cmd, name_command):
    return f'Derniere action utilisateur : ({key_cmd}) {name_command}'


def format_output_round(round):
    return f'{round.name} Début : {round.start_date} Fin {round.end_date}.\n'


def format_output_tournament(tournament):
    return f' * Nom du tournoi             : {tournament.name}\n' \
           f' * Lieu du tournoi            : {tournament.location}\n' \
           f' * Date du tournoi            : {tournament.date}\n' \
           f' * Nombre de tours du tournoi : {tournament.numbers_rounds}\n' \
           f' * Description du tournoi     : {tournament.description}\n' \
           f' * Indices des joueurs        : {tournament.indices_players}\n'


def format_output_creation_player(player):
    return f' * Nom du joueur               : {player.last_name}\n' \
           f' * Prénom du joueur            : {player.first_name}\n' \
           f' * Sexe du joueur              : {player.gender}\n' \
           f' * Date de naissance du joueur : {player.birthdate}\n' \
           f' * Classement du joueur        : {player.ranking}\n'


def format_output_rounds(rounds):
    output = ''
    for round in rounds:
        output += format_output_round(round)
    return output


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


def format_information(information):
    return f'Information : {information}'


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
    print(format_output_tournaments(docs_id, tournaments))


def show_players_choices(docs_id, players):
    print(format_output_players_in_database(docs_id, players))

