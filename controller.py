import model
from tinydb import TinyDB, where
import datetime
import os
import view
import pdb
import time


class InputError(Exception):
    def __init__(self):
        pass


class CommandNotFound(InputError):
    def __init__(self):
        pass

    def __str__(self):
        return 'La commande est inconnue.'


class InputTimeTournamentError(InputError):
    def __init__(self):
        pass

    def __str__(self):
        return 'La cadence doit être choisie parmi les valeurs suivantes : (bullet, blitz, coup rapide).'


class InputDateError(InputError):
    def __init__(self):
        pass

    def __str__(self):
        return 'La date doit être au format année-mois-jour minimum mais vous pouvez rajouter heure-minute si ' \
               'vous le souhaité.'


class InputNumberRoundTournamentError(InputError):
    def __init__(self):
        pass

    def __str__(self):
        return 'Le nombre de tours du tournois doit être un nombre positif.'


class InputRankingPlayerError(InputError):
    def __init__(self):
        pass

    def __str__(self):
        return 'Le classement du joueur doit être un nombre positif.'


class InputGenderPlayerError(InputError):
    def __init__(self):
        pass

    def __str__(self):
        return 'Le sexe du joueur doit être H ou F.'


class InputDocIdTournamentError(InputError):
    def __init__(self):
        pass

    def __str__(self):
        return "L'identifiant du tournoi est inconnue."


class InputDocIdPlayerError(InputError):
    def __init__(self):
        pass

    def __str__(self):
        return "L'identifiant du joueur est inconnue."


class InputParamCommandShowPlayers(InputError):
    def __init__(self):
        pass

    def __str__(self):
        return 'Le parametre de la commande doit etre A ou C.'


class InputEmptyError(InputError):
    def __init__(self):
        pass

    def __str__(self):
        return 'Le champ ne peut etre vide.'


class InputResultError(InputError):
    def __init__(self):
        pass

    def __str__(self):
        return 'Le résultat doit être choisi parmi les valeurs suivantes (1, 0.5, 0)'


def check_if_input_is_number(a):
    try:
        int(a)
    except ValueError:
        return False
    return True


def check_if_input_is_in(a, iterable):
    return True if a in iterable else False


def check_if_input_is_empty(a):
    if len(a) == 0:
        raise InputEmptyError()
    return a


def check_number_round_input(number_round):
    if not check_if_input_is_number(number_round):
        raise InputNumberRoundTournamentError()
    return int(number_round)


def check_ranking_input(ranking):
    if not check_if_input_is_number(ranking):
        raise InputNumberRoundTournamentError()
    return int(ranking)


def check_time_input(time):
    if not check_if_input_is_in(time, ('bullet', 'blitz', 'coup rapide')):
        raise InputTimeTournamentError()
    return time


def check_gender_input(gender):
    if not check_if_input_is_in(gender, ('H', 'F')):
        raise InputGenderPlayerError()
    return gender


def check_date_input(date):
    try:
        args = [int(s) for s in date.split('-')]
        datetime.datetime(*args)
    except Exception:
        raise InputDateError()
    return date


def check_command_is_valid(key_cmd, key_commands):
    if not check_if_input_is_number(key_cmd):
        raise CommandNotFound()
    if int(key_cmd) not in key_commands:
        raise CommandNotFound()
    return int(key_cmd)


def check_choice_tournament_is_valid(doc_id, docs_id):
    if not check_if_input_is_number(doc_id):
        raise InputDocIdTournamentError()
    if int(doc_id) not in docs_id:
        raise InputDocIdTournamentError()
    return int(doc_id)


def check_choices_players_is_valid(string, doc_ids, doc_ids_tournament):
    for doc_id in string.split(','):
        if not check_if_input_is_number(doc_id):
            raise InputDocIdPlayerError()
        if int(doc_id) not in doc_ids:
            raise InputDocIdPlayerError()
    return [int(doc_id) for doc_id in string.split(',') if int(doc_id) not in doc_ids_tournament]


def check_param_cmd_show_players_is_valid(param):
    if not check_if_input_is_in(param, ('A', 'C')):
        raise InputParamCommandShowPlayers()
    return param


def sort_players(param, players):
    if param == 'A':
        players.sort(key=lambda player: player.last_name)
    else:
        players.sort(key=lambda player: player.ranking, reverse=True)


def check_if_result_is_valid(result):
    if not check_if_input_is_in(result, ('1', '0', '0.5')):
        raise InputResultError()
    return float(result)


class Controller(object):
    def __init__(self):
        self.db = model.DATABASE
        self.focus_tournament = None
        self.focus_tournament_doc_id = None
        self.stop = False
        self.main_menu = {0: ('Créer un tournoi', self.create_tournament),
                          1: ('Ajouter un joueur en mémoire', self.add_player_in_database),
                          2: ('Afficher tous les tournois en mémoire', self.show_tournaments_in_database),
                          3: ('Afficher tous les joueurs en mémoire', self.show_players),
                          4: ('Sélectionner un tournoi', self.select_tournament),
                          5: ('Quitter', self.exit)}

        self.sub_menu = {0: ('Importer des joueurs dans le tournoi', self.select_players),
                         1: ('Exporter ce tournoi', self.export_tournament),
                         2: ('Afficher tous les joueurs du tournoi', self.show_players),
                         3: ('Afficher les rounds', self.show_rounds),
                         4: ('Afficher les matchs', self.show_matches),
                         5: ('Créer un nouveau round', self.create_round),
                         6: ('Cloturer le round', self.close_round),
                         7: ('Retour', self.return_to_main_menu),
                         8: ('Quitter', self.exit)}

        self.output_function = None
        self.output_params = None
        self.last_cmd_key = None
        self.last_cmd_name = None

    def get_command(self):
        while not self.stop:
            os.system('cls')
            if self.output_function:
                view.show_output(self.last_cmd_key, self.last_cmd_name, self.output_function, self.output_params)
                view.show_transition()
            view.show_menu(self.get_menu())
            cmd_key = view.get_input('Choisissez une commande', check_command_is_valid,
                                     self.get_keys_commands_available(), view.format_input_command)
            self.last_cmd_key = cmd_key
            self.last_cmd_name = self.get_menu()[cmd_key][0]
            self.apply_command(cmd_key)

    def apply_command(self, cmd_key):
        self.get_function_for_command(cmd_key)()

    def get_function_for_command(self, cmd_key):
        return self.get_menu()[cmd_key][1]

    def get_menu(self):
        return self.main_menu if not self.focus_tournament else self.sub_menu

    def get_keys_commands_available(self):
        return [k for k, v in self.get_menu().items()]

    def set_output(self, output_function, output_params):
        self.output_function = output_function
        self.output_params = output_params

    def create_tournament(self):
        tournament = model.Tournament(*view.get_inputs_for_tournament_parameters())
        try:
            self.db.check_if_tournament_already_exist(tournament)
            self.focus_tournament = tournament
            self.focus_tournament_doc_id = None
            self.set_output(view.format_output_tournament, self.focus_tournament)
        except model.DataBaseTinyDBError as e:
            self.set_output(view.format_error, e)

    def select_tournament(self):
        os.system('cls')
        view.show_tournaments_choices(self.db.get_tournaments_docs_id(), self.db.get_tournaments())
        doc_id = view.get_input('Choisissez un tournoi', check_choice_tournament_is_valid,
                                self.db.get_tournaments_docs_id(), view.format_input_choice)
        self.focus_tournament = self.db.get_tournament_by_id(doc_id)
        self.focus_tournament_doc_id = doc_id
        self.set_output(view.format_output_tournament, self.focus_tournament)

    def select_players(self):
        os.system('cls')
        view.show_players_choices(self.db.get_players_docs_id(), self.db.get_players())
        doc_ids = view.get_input("Choisissez un joueur ou des joueur avec le marqueur ','",
                                 check_choices_players_is_valid,
                                 (self.db.get_players_docs_id(), self.focus_tournament.indices_players),
                                 view.format_input_choice)
        try:
            self.focus_tournament.add_indexes_players(doc_ids)
            self.set_output(view.format_output_players_in_database, (doc_ids, [self.db.get_player_by_id(doc_id) for doc_id in doc_ids]))
        except model.TooManyPlayersError as e:
            self.set_output(view.format_error, e)

    def return_to_main_menu(self):
        self.focus_tournament = None
        self.reset_output()

    def add_player_in_database(self):
        player = model.Player(*view.get_inputs_for_player_parameters())
        try:
            self.db.check_if_player_already_exist(player)
            self.db.add_player(player)
            self.set_output(view.format_output_creation_player, player)
        except model.DataBaseTinyDBError as e:
            self.set_output(view.format_error, e)

    def reset_output(self):
        self.output_function = None
        self.output_params = None

    def exit(self):
        self.stop = True

    def export_tournament(self):
        if self.focus_tournament_doc_id:
            self.db.update_tournament(self.focus_tournament, self.focus_tournament_doc_id)
        else:
            self.db.add_tournament(self.focus_tournament)

    def show_tournaments_in_database(self):
        doc_ids = self.db.get_tournaments_docs_id()
        tournaments = [self.db.get_tournament_by_id(doc_id) for doc_id in doc_ids]
        self.set_output(view.format_output_tournaments, (doc_ids, tournaments))

    def show_players(self):
        try:
            param = view.get_input('Choisissez un parametre entre tri alphabétique (A) ou Classement (C)',
                                   check_param_cmd_show_players_is_valid, format_view=view.format_input_parameters)
            if self.focus_tournament:
                players = self.focus_tournament.get_players()
                output_function = view.format_output_players_in_tournament
            else:
                players = [self.db.get_player_by_id(doc_id) for doc_id in self.db.get_players_docs_id()]
                output_function = view.format_output_players_in_database
            sort_players(param, players)
            doc_ids = [self.db.get_doc_id_by_player(player) for player in players]
            self.set_output(output_function, (doc_ids, players))
        except model.PlayersEmptyError as e:
            self.set_output(view.format_information, e)

    def create_round(self):
        try:
            name = view.get_input('Nom du round', check_if_input_is_empty, format_view=view.format_input_parameters)
            self.focus_tournament.create_round(name)
            self.set_output(view.format_output_round, self.focus_tournament.get_last_round())
        except model.TournamentError as e:
            self.set_output(view.format_error, e)

    def close_round(self):
        try:
            round = self.focus_tournament.get_last_round()
            while round.get_index_match_to_set_result() is not None:
                index_match = round.get_index_match_to_set_result()
                p1, p2 = round.get_players_in_match(index_match)
                name_p1 = p1.last_name + ' ' + p1.first_name
                score_1 = view.get_input(f'Entrez le résultat de {name_p1} : ', check_if_result_is_valid,
                                         format_view=view.format_input_parameters)
                round.set_result(p1, p2, score_1, index_match)
            self.focus_tournament.close_round()
            self.show_matches()
        except (model.RoundError, model.TournamentError) as e:
            self.set_output(view.format_error, e)

    def show_rounds(self):
        try:
            self.set_output(view.format_output_rounds, self.focus_tournament.get_rounds())
        except model.RoundNotExistError as e:
            self.set_output(view.format_information, e)

    def show_matches(self):
        try:
            players_1 = []
            players_2 = []
            scores_1 = []
            scores_2 = []
            rounds = self.focus_tournament.get_rounds()
            for round in rounds:
                for (p1,s1), (p2,s2) in round.matches:
                    players_1.append(p1)
                    scores_1.append(s1)
                    players_2.append(p2)
                    scores_2.append(s2)
            self.set_output(view.format_output_matches, (players_1, players_2, scores_1, scores_2))
        except model.RoundNotExistError as e:
            self.set_output(view.format_information, e)
