import model
from tinydb import TinyDB, where
import datetime
import os
import view


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


class DataBaseTinyDBError(Exception):
    def __init__(self):
        pass


class TournamentAlreadyExistError(DataBaseTinyDBError):
    def __init__(self):
        pass

    def __str__(self):
        return 'Un tournoi avec un nom, un lieu, une date idendique est présent dans la base de données.'


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


def check_ranking_input(ranking):
    if not check_if_input_is_number(ranking):
        raise InputNumberRoundTournamentError()


def check_time_input(time):
    if not check_if_input_is_in(time, ('bullet', 'blitz', 'coup rapide')):
        raise InputTimeTournamentError()


def check_gender_input(gender):
    if not check_if_input_is_in(gender, ('H', 'F')):
        raise InputGenderPlayerError()


def check_date_input(date):
    try:
        args = [int(s) for s in date.split('-')]
        datetime.datetime(*args)
    except Exception:
        raise InputDateError()


def check_command_is_valid(key_cmd, key_commands):
    try:
        if int(key_cmd) not in key_commands:
            raise CommandNotFound()
    except ValueError:
        raise CommandNotFound()


def check_choice_tournament_is_valid(doc_id, docs_id):
    try:
        if int(doc_id) not in docs_id:
            raise InputDocIdTournamentError()
    except ValueError:
        raise InputDocIdTournamentError()


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
        self.check_if_tournament_already_exist(tournament)
        self.tournaments_table.insert(serialized_tournament(tournament))

    def add_player(self, player):
        self.players_table.insert(serialized_player(player))

    def add_players(self, players):
        for player in players:
            self.add_player(player)

    def get_tournaments(self):
        return [model.Tournament(**dict_tournament) for dict_tournament in self.tournaments_table]

    def get_tournament_by_id(self, doc_id):
        return model.Tournament(**self.tournaments_table.get(doc_id=doc_id))

    def get_tournaments_docs_id(self):
        return [dict_tournament.doc_id for dict_tournament in self.tournaments_table]

    def get_players(self):
        serialized_players = self.players_table.all()
        return [model.Player(**dict_player) for dict_player in serialized_players]

    def check_if_tournament_already_exist(self, tournament):
        if self.tournaments_table.contains(where('name') == tournament.name and where('location') == tournament.location
                                           and where('date') == tournament.date):
            raise TournamentAlreadyExistError()


class Controller(object):
    def __init__(self):
        self.db = DataBaseTinyDB()
        self.focus_tournament = None
        self.stop = False
        self.main_menu = {0: ('Créer un tournoi', self.create_tournament),
                          1: ('Sélectionner un tournoi', self.select_tournament),
                          2: ('Quitter', self.exit)}

        self.sub_menu = {0: ('Ajouter un joueur', self.exit),
                         1: ('Exporter ce tournoi', self.export_tournament),
                         2: ('Retour', self.return_to_main_menu),
                         3: ('Quitter', self.exit)}

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
            cmd_key = int(view.get_input('Choisissez une commande', check_command_is_valid,
                                         self.get_keys_commands_available(), view.format_input_command))
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
        self.focus_tournament = model.Tournament(*view.get_inputs_for_tournament_parameters())
        self.output_function = view.format_output_tournament
        self.output_params = (self.focus_tournament,)

    def select_tournament(self):
        os.system('cls')
        view.show_tournaments_choices(self.db.get_tournaments_docs_id(), self.db.get_tournaments())
        doc_id = int(view.get_input('Choississez un tournoi', check_choice_tournament_is_valid,
                                    self.db.get_tournaments_docs_id(), view.format_input_choice))
        self.focus_tournament = self.db.get_tournament_by_id(doc_id)

        self.output_function = view.format_output_tournament
        self.output_params = (self.focus_tournament,)

    def return_to_main_menu(self):
        self.focus_tournament = None
        self.reset_output()

    def reset_output(self):
        self.output_function = None
        self.output_params = None

    def exit(self):
        self.stop = True

    def export_tournament(self):
        try:
            self.db.add_tournament(self.focus_tournament)
        except DataBaseTinyDBError as e:
            self.output_function = view.format_error
            self.output_params = (e,)
