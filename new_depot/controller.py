import model
from tinydb import TinyDB, where
import datetime
import os
import view
import pdb

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
        return 'Le parametre de la commande doit etre A ou C'


class DataBaseTinyDBError(Exception):
    def __init__(self):
        pass


class ExportTournamentAlreadyExistError(DataBaseTinyDBError):
    def __init__(self):
        pass

    def __str__(self):
        return 'Un tournoi avec un nom, un lieu, une date idendique est présent dans la base de données.'


class ExportPlayerAlreadyExistError(DataBaseTinyDBError):
    def __init__(self):
        pass

    def __str__(self):
        return 'Un Joueur avec un nom et un prénom idendique est présent dans la base de données.'


def check_if_input_is_number(a):
    try:
        int(a)
    except ValueError:
        return False
    return True


def check_if_input_is_in(a, iterable):
    return True if a in iterable else False


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
    if not check_if_input_is_in(param, ('A','C')):
        raise InputParamCommandShowPlayers()
    return param


def serialized_tournament(tournament):
    return {'name': tournament.name, 'location': tournament.location, 'date': tournament.date,
            'time': tournament.time, 'numbers_rounds': tournament.numbers_rounds,
            'description': tournament.description, 'indices_players': tournament.indices_players,
            'rounds': tournament.rounds}


def serialized_player(player):
    return {'last_name': player.last_name, 'first_name': player.first_name, 'gender': player.gender,
            'birthdate': player.birthdate, 'ranking': player.ranking}


def serialized_round(round):
    return {'name': round.name, 'start_date': round.start_date, 'matchs': round.matchs}


class DataBaseTinyDB(object):
    def __init__(self):
        self.db = TinyDB('db.json')
        self.players_table = self.db.table('Players')
        self.tournaments_table = self.db.table('Tournaments')

    def add_tournament(self, tournament):
        return self.tournaments_table.insert(serialized_tournament(tournament))

    def add_player(self, player):
        return self.players_table.insert(serialized_player(player))

    def get_tournaments(self):
        return [model.Tournament(**dict_tournament) for dict_tournament in self.tournaments_table]

    def get_tournament_by_id(self, doc_id):
        return model.Tournament(**self.tournaments_table.get(doc_id=doc_id))

    def get_tournaments_docs_id(self):
        return [dict_tournament.doc_id for dict_tournament in self.tournaments_table]

    def get_player_by_id(self, doc_id):
        return model.Player(**self.players_table.get(doc_id=doc_id))

    def get_players_docs_id(self):
        return [dict_player.doc_id for dict_player in self.players_table]

    def get_doc_id_by_player(self, player):
        return self.players_table.get((where('last_name') == player.last_name) & (where('first_name') == player.first_name)).doc_id

    def get_players(self):
        return [model.Player(**dict_player) for dict_player in self.players_table]

    def check_if_tournament_already_exist(self, tournament):
        if self.tournaments_table.contains((where('name') == tournament.name) & (where('location') == tournament.location)
                                           & (where('date') == tournament.date)):
            raise ExportTournamentAlreadyExistError()

    def check_if_player_already_exist(self, player):
        if self.players_table.contains((where('last_name') == player.last_name) & (where('first_name') == player.first_name)):
            raise ExportPlayerAlreadyExistError()

    def update_tournament(self, tournament, doc_id):
        dict_tournament = serialized_tournament(tournament)
        for k, v in dict_tournament.items():
            self.tournaments_table.update({k: v}, doc_ids=[doc_id])


class Controller(object):
    def __init__(self):
        self.db = DataBaseTinyDB()
        self.focus_tournament = None
        self.focus_tournament_doc_id = None
        self.focus_players = []
        self.stop = False
        self.main_menu = {0: ('Créer un tournoi', self.create_tournament),
                          1: ('Ajouter un joueur en mémoire', self.add_player_in_database),
                          2: ('Afficher tous les tournois en mémoire', self.show_tournaments_in_database),
                          3: ('Afficher tous les joueurs en mémoire', self.show_players_in_database),
                          4: ('Sélectionner un tournoi', self.select_tournament),
                          5: ('Quitter', self.exit)}

        self.sub_menu = {0: ('Ajouter un joueur dans le tournoi', self.add_player_in_tournament),
                         1: ('Importer des joueurs dans le tournoi', self.select_players),
                         2: ('Exporter ce tournoi', self.export_tournament),
                         3: ('Retour', self.return_to_main_menu),
                         4: ('Quitter', self.exit)}

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

    def create_tournament(self):
        tournament = model.Tournament(*view.get_inputs_for_tournament_parameters())
        try:
            self.db.check_if_tournament_already_exist(tournament)
            self.focus_tournament = tournament
            self.focus_tournament_doc_id = None
            self.output_function = view.format_output_tournament
            self.output_params = self.focus_tournament
        except DataBaseTinyDBError as e:
            self.output_function = view.format_error
            self.output_params = e

    def select_tournament(self):
        os.system('cls')
        view.show_tournaments_choices(self.db.get_tournaments_docs_id(), self.db.get_tournaments())
        doc_id = view.get_input('Choisissez un tournoi', check_choice_tournament_is_valid,
                                self.db.get_tournaments_docs_id(), view.format_input_choice)
        self.focus_tournament = self.db.get_tournament_by_id(doc_id)
        self.focus_tournament_doc_id = doc_id
        self.output_function = view.format_output_tournament
        self.output_params = self.focus_tournament

    def select_players(self):
        os.system('cls')
        view.show_players_choices(self.db.get_players_docs_id(), self.db.get_players())
        doc_ids = view.get_input("Choisissez un joueur ou des joueur avec le marqueur ','",
                                 check_choices_players_is_valid,
                                 (self.db.get_players_docs_id(), self.focus_tournament.indices_players),
                                 view.format_input_choice)
        self.focus_tournament.indices_players.extend(doc_ids)
        self.output_function = view.format_output_players
        self.output_params = (doc_ids, [self.db.get_player_by_id(doc_id) for doc_id in doc_ids])

    def return_to_main_menu(self):
        self.focus_tournament = None
        self.reset_output()

    def add_player_in_tournament(self):
        player = model.Player(*view.get_inputs_for_player_parameters())
        try:
            self.db.check_if_player_already_exist(player)
            self.focus_players.append(player)
            self.output_function = view.format_output_creation_player
            self.output_params = player
        except DataBaseTinyDBError as e:
            self.output_function = view.format_error
            self.output_params = e

    def add_player_in_database(self):
        player = model.Player(*view.get_inputs_for_player_parameters())
        try:
            self.db.check_if_player_already_exist(player)
            self.db.add_player(player)
            self.output_function = view.format_output_creation_player
            self.output_params = player
        except DataBaseTinyDBError as e:
            self.output_function = view.format_error
            self.output_params = e

    def reset_output(self):
        self.output_function = None
        self.output_params = None

    def exit(self):
        self.stop = True

    def export_tournament(self):
        doc_ids = []
        for player in self.focus_players:
            doc_ids.append(self.db.add_player(player))
        self.focus_tournament.indices_players.extend(doc_ids)
        if self.focus_tournament_doc_id:
            self.db.update_tournament(self.focus_tournament, self.focus_tournament_doc_id)
        else:
            self.db.add_tournament(self.focus_tournament)

    def show_tournaments_in_database(self):
        self.output_function = view.format_output_tournaments
        doc_ids = self.db.get_tournaments_docs_id()
        tournaments = [self.db.get_tournament_by_id(doc_id) for doc_id in doc_ids]
        self.output_params = (doc_ids, tournaments)

    def show_players_in_database(self):
        param = view.get_input('Choisissez un parametre entre tri alphabétique (A) ou Classement (C)',
                               check_param_cmd_show_players_is_valid, format_view=view.format_input_parameters)
        players = [self.db.get_player_by_id(doc_id) for doc_id in self.db.get_players_docs_id()]
        if param == 'A':
            players.sort(key = lambda player : player.last_name)
        else:
            players.sort(key = lambda player : player.ranking)
        doc_ids = [ self.db.get_doc_id_by_player(player) for player in players]
        self.output_function = view.format_output_players
        self.output_params = (doc_ids, players)