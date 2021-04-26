import controller
import model
import os


def align_multi_strings(champs, empty_counts, placements):
    """
    Aligne plusieurs strings par champs.

    :param champs: list[ [champ1_string1, champ1_string2, ...], [champ2_string1, ...], ... ]
    :param empty_counts: list[int], représentant le nombre de charactère vide apres chaque champ
    :param placements: list[str], représentant des valeurs de placement pour les strings composant chaque champ
                       - '<' pour aligner la valeur du champ a gauche
                       - '>' pour aligner la valeur du champ a droite
                       - '^' pour centrer la valeur du champ
    :return: string
    """
    strings = []
    len_max_champs = [max([len(s) for s in champs[i]]) for i in range(len(champs))]
    for i in range(len(champs[0])):
        string = ''
        for index_champ in range(len(champs)):
            value = champs[index_champ][i]
            max_len = len_max_champs[index_champ]
            empty_count = empty_counts[index_champ]
            placement = placements[index_champ]
            string += f"{value:{placement}{max_len + empty_count}}"
        strings.append(string)

    return '\n'.join(strings)


def format_output_rounds_matches(rounds, players_1, players_2, scores_1, scores_2):
    """
    Configure et retourne l'affichage des matches de chaque round.
    :param rounds: list[Round], représentant les instances des rounds du tournoi
    :param players_1: list[Player], représentant les instances des joueurs 1 de chaque match
    :param players_2: list[Player], représentant les instances des joueurs 2 de chaque match
    :param scores_1: list[int], représentant les scores des joueurs 1 de chaque match
    :param scores_2: list[int], représentant les scores des joueurs 2 de chaque match
    :return: string
    """
    champ1 = [p.last_name+' '+p.first_name for p in players_1]
    champ2 = len(champ1)*['VS']
    champ3 = [p.last_name+' '+p.first_name for p in players_2]
    champ4 = len(champ1)*[':']
    champ5 = [f'({scores_1[i]}, {scores_2[i]})' for i in range(len(champ1))]
    empty_counts = [3, 3, 3, 3, 0]
    placements = 5*['<']
    outputs = align_multi_strings([champ1, champ2, champ3, champ4, champ5], empty_counts, placements).splitlines()
    max_len = max([len(s) for s in outputs])
    n_match_per_round = int(model.Tournament.NUMBER_PLAYER/2)
    outputs = [outputs[i:i+n_match_per_round] for i in range(0, len(outputs), n_match_per_round)]
    rounds_name = [f"{10*'-'+round.name+10*'-':^{max_len}}" for round in rounds]
    outputs = ['\n'.join([rounds_name[i]+'\n', *outputs[i]]) for i in range(len(rounds))]
    return '\n\n'.join(outputs)


def format_output_players_in_tournament(docs_id, players):
    """
    Configure et retourne l'affichage des joueurs du tournoi.
    :param docs_id: list[int], représentant les index en base de données des joueurs du tournoi
    :param players: list[Player], représentant les instances des joueurs du tournoi
    :return: string
    """
    champ1 = [f'* ({doc_id})' for doc_id in docs_id]
    champ2 = [p.last_name+' '+p.first_name for p in players]
    champ3 = [f'Classement {p.ranking},' for p in players]
    champ4 = [f'Points {p.points}' for p in players]
    empty_counts = [3, 3, 3, 0]
    placements = 4 * ['<']
    return align_multi_strings([champ1, champ2, champ3, champ4], empty_counts, placements)


def format_output_players_in_database(docs_id, players):
    """
    Configure et retourne l'affichage des joueurs en base de données.
    :param docs_id: list[int], représentant les index des joueurs en base de données.
    :param players: list[Player], représentant les instances des joueurs en base de données.
    :return: string
    """
    champ1 = [f'* ({doc_id})' for doc_id in docs_id]
    champ2 = [p.last_name+' '+p.first_name for p in players]
    champ3 = [f'Classement {p.ranking}' for p in players]
    empty_counts = [3, 3, 0]
    placements = 3 * ['<']
    return align_multi_strings([champ1, champ2, champ3], empty_counts, placements)


def format_output_tournaments(docs_id, tournaments):
    """
    Configure et retourne l'affichage des tournois en base de données.
    :param docs_id: list[int], représentant les index des tournois en base de données.
    :param tournaments: list[Tournament], représentant les instances des tournois en base de données.
    :return: string
    """
    champ1 = [f'* ({doc_id})' for doc_id in docs_id]
    champ2 = [tournament.name for tournament in tournaments]
    champ3 = [tournament.location for tournament in tournaments]
    champ4 = [tournament.date for tournament in tournaments]
    empty_counts = [3, 3, 3, 0]
    placements = 4 * ['<']
    return align_multi_strings([champ1, champ2, champ3, champ4], empty_counts, placements)


def format_output_last_command(key_cmd, name_command):
    """
    Retourne l'affichage des informations de la dernière commande.
    :param key_cmd: int, représentant l'index de la dernière commande
    :param name_command: string, représentant le nom de la dernière commande
    :return: string
    """
    return f'Derniere action utilisateur : ({key_cmd}) {name_command}'


def format_output_round(round):
    """
    Retourne l'affichage des informations d'un round.
    :param round: instance de round
    :return: string
    """
    return f'{round.name} Début : {round.start_date} Fin {round.end_date}.\n'


def format_output_tournament(tournament):
    """
    Retourne l'affichage des informations d'un tournoi.
    :param tournament: instance de tournoi
    :return: string
    """
    return f' * Nom du tournoi             : {tournament.name}\n' \
           f' * Lieu du tournoi            : {tournament.location}\n' \
           f' * Date du tournoi            : {tournament.date}\n' \
           f' * Nombre de tours du tournoi : {tournament.numbers_rounds}\n' \
           f' * Description du tournoi     : {tournament.description}\n' \
           f' * Indices des joueurs        : {tournament.indices_players}\n'


def format_output_player(player):
    """
    Retourne l'affichage des informations d'un joueur.
    :param player: instance de joueur
    :return: string
    """
    return f' * Nom du joueur               : {player.last_name}\n' \
           f' * Prénom du joueur            : {player.first_name}\n' \
           f' * Sexe du joueur              : {player.gender}\n' \
           f' * Date de naissance du joueur : {player.birthdate}\n' \
           f' * Classement du joueur        : {player.ranking}\n'


def format_output_rounds(rounds):
    """
    Retourne l'affichage des informations des rounds du tournoi.
    :param rounds: list[Round]
    :return: string
    """
    output = ''
    for round in rounds:
        output += format_output_round(round)
    return output


def format_input_parameters(input_name):
    """
    Retourne l'affichage d'une demande d'input d'un paramètre.
    :param input_name: string, information sur l'input voulu
    :return: string
    """
    return '    -' + input_name + ' : '


def format_input_command(input_name):
    """
    Retourne l'affichage d'une demande d'input d'une commande.
    :param input_name: string
    :return: string
    """
    return f'{input_name} >> '


def format_input_choice(input_choice):
    """
    Retourne l'affichage d'une demande d'input de type choix.
    :param input_choice: string, information sur l'input voulu.
    :return: string
    """
    return f'{input_choice} : '


def format_transition():
    """
    Retourne l'affichage de transition entre la zone output et la zone de menu.
    :return: string
    """
    return os.get_terminal_size().columns*'-'


def format_cmd_menu(key_cmd, str_description):
    """
    Retourne l'affichage d'une commande du menu.
    :param key_cmd: int, représentant l'index de la commande du menu
    :param str_description: string, représentant la description de la commande
    :return: string
    """
    return f'({str(key_cmd)}) {str_description}.'


def format_error(err):
    """
    Retourne l'affichage pour les erreurs.
    :param err: objet de type exception
    :return: string
    """
    return f'Erreur : {err}'


def format_information(information):
    """
    Retourne l'affichage pour les informations.
    :param information: string, représentant l'information
    :return: string
    """
    return f'Information : {information}'


def get_input_with_repetition(input_str, check_function, params):
    """
    Fait une demande d'input de paramètre avec vérification sur l'input et boucle tant que l'input n'est pas valide.
    :param input_str: string, représentant le nom du paramètre
    :param check_function: fonction de vérification de l'input
    :param params: paramètres de la fonction de vérification.
    :return: paramètre
    """
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
    """
    Fait une demande d'input de parametre avec ou sans vérification sur l'input.
    :param name: string, représentant le paramètre
    :param check_function: fonction de vérification de l'input
    :param params: paramètres de la fonction de vérification
    :param format_view: fonction d'affichage de la demande d'input
    :return: paramètre
    """
    def format(n): return format_view(n) if format_view else n
    if check_function:
        param = get_input_with_repetition(format(name), check_function, params)
    else:
        param = input(format(name))
    return param


def show_menu(dict_menu):
    """
    Affiche le menu.
    :param dict_menu: dictionnaire, représentant le menu
    :return: None
    """
    for k, v in dict_menu.items():
        print(format_cmd_menu(k, v[0]))


def show_error(err):
    """
    Affiche les erreurs.
    :param err: objet de type exception
    :return: None
    """
    print(format_error(err))


def show_transition():
    """
    Affiche la transition entre la zone output et la zone du menu.
    :return: None
    """
    print(format_transition())


def show_output(key_cmd, function_name, function, params):
    """
    Affiche les outputs.
    :param key_cmd: int, représentant l'index de la dernière commande
    :param function_name: string, représentant le nom de la dernière commande.
    :param function: fonction d'affichage des outputs
    :param params: paramètres de la fonction d'affichage des outputs
    :return: None
    """
    print(format_output_last_command(key_cmd, function_name))
    if isinstance(params, tuple):
        print(function(*params))
    else:
        if function:
            print(function(params))


def show_tournaments_choices(docs_id, tournaments):
    """
    Affiche la vue pour le choix d'un tournoi de la base de données.
    :param docs_id: list[int], représentant les index des tournois en base de données.
    :param tournaments: list[Tournament], représentant les instances des tournois en base de données.
    :return: None
    """
    print(format_output_tournaments(docs_id, tournaments))


def show_players_choices(docs_id, players):
    """
    Affiche la vue pour le choix des joueurs en base de données.
    :param docs_id: list[int], représentant les index des joueurs en base de données.
    :param players: list[Player], représentant les instances des joueurs en base de données.
    :return: None
    """
    print(format_output_players_in_database(docs_id, players))
