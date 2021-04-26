import model
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
        return 'Le nombre de tours du tournoi doit être un nombre positif.'


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
    def __init__(self, doc_ids):
        self.doc_ids = doc_ids

    def __str__(self):
        if len(self.doc_ids) > 1:
            return f"Les identifiants {','.join(self.doc_ids)} sont inconnues."
        return f"L'identifiant {str(self.doc_ids[0])} sont inconnues."


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
    """
    Vérifie qu'un input puisse etre casté en nombre.
    :param a: string
    :return: boolean
    """
    try:
        int(a)
    except ValueError:
        return False
    return True


def check_if_input_is_in(a, iterable):
    """
    Vérifie qu'un input appartient à des valeurs particulières.
    :param a: string
    :param iterable: iterable contenant les valeurs de comparaison souhaitée
    :return: boolean
    """
    return True if a in iterable else False


def check_if_input_is_empty(a):
    """
    Vérifie qu'un input n'est pas vide
    :param a: string
    :return: string
    """
    if len(a) == 0:
        raise InputEmptyError()
    return a


def check_number_round_input(number_round):
    """
    Vérifie que l'input du paramètre nombre de round est valide.
    :param number_round: string
    :return: int
    """
    if not check_if_input_is_number(number_round):
        raise InputNumberRoundTournamentError()
    return int(number_round)


def check_ranking_input(ranking):
    """
    Vérifie que l'input du paramètre classement du joueur est valide.
    :param ranking: string
    :return: int
    """
    if not check_if_input_is_number(ranking):
        raise InputNumberRoundTournamentError()
    return int(ranking)


def check_time_input(time):
    """
    Vérifie que l'input du paramètre cadence est valide.
    :param time: string
    :return: string
    """
    if not check_if_input_is_in(time, ('bullet', 'blitz', 'coup rapide')):
        raise InputTimeTournamentError()
    return time


def check_gender_input(gender):
    """
    Vérifie que l'input du paramètre sexe du joueur est valide.
    :param gender: string
    :return: string
    """
    if not check_if_input_is_in(gender, ('H', 'F')):
        raise InputGenderPlayerError()
    return gender


def check_date_input(date):
    """
    Vérifie que l'input d'un paramètre date est valide.
    :param date: string
    :return: objet de type datetime
    """
    try:
        args = [int(s) for s in date.split('-')]
        datetime.datetime(*args)
    except Exception:
        raise InputDateError()
    return date


def check_command_is_valid(key_cmd, key_commands):
    """
    Vérifie que l'input d'une commande est valide.
    :param key_cmd: string
    :param key_commands: list[int], représentant les index des commandes disponibles
    :return: int
    """
    if not check_if_input_is_number(key_cmd):
        raise CommandNotFound()
    if int(key_cmd) not in key_commands:
        raise CommandNotFound()
    return int(key_cmd)


def check_choice_tournament_is_valid(doc_id, docs_id):
    """
    Vérifie que l'input de choix d'un index de tournoi est valide.
    :param doc_id: string
    :param docs_id: list[int], représentant les index des tournois en base de données.
    :return: int
    """
    if not check_if_input_is_number(doc_id):
        raise InputDocIdTournamentError()
    if int(doc_id) not in docs_id:
        raise InputDocIdTournamentError()
    return int(doc_id)


def check_choices_players_is_valid(string, doc_ids, doc_ids_players_in_tournament):
    """
    Vérifie que l'input du choix multiple de joueurs est valide.
    :param string: string, représentant le choix multiple d'index de joueur séparé par des virgules
    :param doc_ids: list[int], représentant les index des joueurs en base de données.
    :param doc_ids_players_in_tournament: list[int], représentant les index en base de données des joueurs du tournoi
    :return: list[int], représentant les index des joueurs choisis en base de données.
    """
    doc_id_errs = []
    for doc_id in string.split(','):
        if not check_if_input_is_number(doc_id):
            doc_id_errs.append(doc_id)
        elif not check_if_input_is_in(int(doc_id), doc_ids):
            doc_id_errs.append(doc_id)
    if doc_id_errs:
        raise InputDocIdPlayerError(doc_id_errs)
    return [int(doc_id) for doc_id in string.split(',') if int(doc_id) not in doc_ids_players_in_tournament]


def check_param_cmd_show_players_is_valid(param):
    """
    Vérifie que le paramètre de la commande qui affiche les joueurs soit valide.
    :param param: string
    :return: string
    """
    if not check_if_input_is_in(param, ('A', 'C')):
        raise InputParamCommandShowPlayers()
    return param


def sort_players(param, players):
    """
    Tri les joueurs de manière alphabétique ou par classement.
    :param param: string
    :param players: list[Player]
    :return: None
    """
    if param == 'A':
        players.sort(key=lambda player: player.last_name)
    else:
        players.sort(key=lambda player: player.ranking, reverse=True)


def check_if_result_is_valid(result):
    """
    Vérifie que l'input d'un résultat de match est valide.
    :param result: string
    :return: float
    """
    if not check_if_input_is_in(result, ('1', '0', '0.5')):
        raise InputResultError()
    return float(result)


def get_inputs_for_tournament_parameters():
    """
    Récupère l'ensemble des inputs pour la création d'un tournoi.
    :return: tuple
    """
    name = view.get_input('Nom du tournois', check_if_input_is_empty, format_view=view.format_input_parameters)
    location = view.get_input('Lieu du tournois', check_if_input_is_empty, format_view=view.format_input_parameters)

    date = view.get_input('Date du tournoi (Ex : 2020-01-01)',
                          check_date_input, format_view=view.format_input_parameters)

    time = view.get_input('Cadence du tournois (bullet, blitz, coup rapide)', check_time_input,
                          format_view=view.format_input_parameters)

    number_round = view.get_input('Nombre de tours du tournois', check_number_round_input,
                                  format_view=view.format_input_parameters)

    description = view.get_input('Description du tournois', format_view=view.format_input_parameters)
    return name, location, date, time, description, number_round


def get_inputs_for_player_parameters():
    """
    Récupère l'ensemble des inputs pour la création d'un joueur.
    :return: tuple
    """
    last_name = view.get_input('Nom du joueur', check_if_input_is_empty, format_view=view.format_input_parameters)
    first_name = view.get_input('Prénom du joueur', check_if_input_is_empty, format_view=view.format_input_parameters)

    birthdate = view.get_input('Date de naissance du joueur (Ex: 2000-01-01)', check_date_input,
                               format_view=view.format_input_parameters)

    gender = view.get_input('Sexe (H/F)', check_gender_input, format_view=view.format_input_parameters)
    ranking = view.get_input('Classement', check_ranking_input, format_view=view.format_input_parameters)
    return last_name, first_name, birthdate, gender, ranking


class Controller(object):
    """
    Classe qui centralise les actions entre l'utilisateur et les modèles de données.
    """
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

        self.sub_menu = {0: ('Importer des joueurs dans le tournoi', self.import_players_in_tournament),
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
        self.last_cmd_key = ''
        self.last_cmd_name = ''

    def start(self):
        """
        Affiche les vues, récupère les commandes, exécute les commandes et boucle
        tant que l'utilisateur n'a pas quitté.
        :return: None
        """
        while not self.stop:
            os.system('cls')
            view.show_output(self.last_cmd_key, self.last_cmd_name, self.output_function, self.output_params)
            view.show_transition()
            view.show_menu(self.get_menu())
            cmd_key = view.get_input('Choisissez une commande', check_command_is_valid,
                                     self.get_keys_commands_available(), view.format_input_command)
            self.last_cmd_key = cmd_key
            self.last_cmd_name = self.get_menu()[cmd_key][0]
            self.apply_command(cmd_key)

    def apply_command(self, cmd_key):
        """
        Execute une commande par son index.
        :param cmd_key: int
        :return: None
        """
        self.get_function(cmd_key)()

    def get_function(self, cmd_key):
        """
        Récupère la fonction d'une commande grace à son index
        :param cmd_key: int
        :return: fonction
        """
        return self.get_menu()[cmd_key][1]

    def get_menu(self):
        """
        Récupère le menu qui doit être affiché.
        :return: dictionnaire
        """
        return self.main_menu if not self.focus_tournament else self.sub_menu

    def get_keys_commands_available(self):
        """
        Récupère les index des commandes du menu.
        :return: list[int]
        """
        return [k for k, v in self.get_menu().items()]

    def set_output(self, output_function, output_params):
        """
        Affecte l'affichage de la zone output.
        :param output_function: fonction d'affichage
        :param output_params: paramètres de la fonction d'affichage
        :return: None
        """
        self.output_function = output_function
        self.output_params = output_params

    def reset_output(self):
        """
        Reset les paramètres d'affichage de la zone output.
        :return: None
        """
        self.output_function = None
        self.output_params = None

    def return_to_main_menu(self):
        """
        Reset le tournoi courant et les paramètres d'affichage de la zone output.
        :return: None
        """
        self.focus_tournament = None
        self.reset_output()

    def exit(self):
        """
        Permet de sortir de la fonction start.
        :return: None
        """
        self.stop = True

    def create_tournament(self):
        """
        Crée un tournoi et l'affecte à l'attribut qui definit le tournoi courant.
        :return: None
        """
        tournament = model.Tournament(*get_inputs_for_tournament_parameters())
        try:
            self.db.check_if_tournament_already_exist(tournament)
            self.focus_tournament = tournament
            self.focus_tournament_doc_id = None
            self.set_output(view.format_output_tournament, self.focus_tournament)
        except model.DataBaseTinyDBError as e:
            self.set_output(view.format_error, e)

    def select_tournament(self):
        """
        Affiche la vue de séléction d'un tournoi parmis les tournois de la base de données.
        Récupère un tournoi et l'affecte à l'attribut qui definit le tournoi courant.
        :return: None
        """
        try:
            self.db.check_if_tournament_table_is_empty()
            os.system('cls')
            view.show_tournaments_choices(self.db.get_tournaments_docs_id(), self.db.get_tournaments())
            doc_id = view.get_input('Choisissez un tournoi', check_choice_tournament_is_valid,
                                    self.db.get_tournaments_docs_id(), view.format_input_choice)
            self.focus_tournament = self.db.get_tournament_by_id(doc_id)
            self.focus_tournament_doc_id = doc_id
            self.set_output(view.format_output_tournament, self.focus_tournament)
        except model.TournamentTableIsEmptyError as e:
            self.set_output(view.format_error, e)

    def export_tournament(self):
        """
        Exporte ou met a jour le tournoi courant dans la base de données.
        :return: None
        """
        if self.focus_tournament_doc_id:
            self.db.update_tournament(self.focus_tournament, self.focus_tournament_doc_id)
        else:
            self.db.add_tournament(self.focus_tournament)

    def add_player_in_database(self):
        """
        Ajoute un joueur en base de données.
        :return: None
        """
        player = model.Player(*get_inputs_for_player_parameters())
        try:
            self.db.check_if_player_already_exist(player)
            self.db.add_player(player)
            self.set_output(view.format_output_player, player)
        except model.DataBaseTinyDBError as e:
            self.set_output(view.format_error, e)

    def import_players_in_tournament(self):
        """
        Affiche la vue de séléction des joueurs parmis les joueurs en base de données.
        Récupère les joueurs sélectionnés et les affectes au tournoi courant.
        :return: None
        """
        try:
            self.db.check_if_player_table_is_empty()
            os.system('cls')
            view.show_players_choices(self.db.get_players_docs_id(), self.db.get_players())
            doc_ids = view.get_input("Choisissez un joueur ou des joueur avec le marqueur ','",
                                     check_choices_players_is_valid,
                                     (self.db.get_players_docs_id(), self.focus_tournament.indices_players),
                                     view.format_input_choice)
            if doc_ids:
                self.focus_tournament.add_players_from_database(doc_ids)
                self.set_output(view.format_output_players_in_database,
                                (doc_ids, [self.db.get_player_by_id(doc_id) for doc_id in doc_ids]))
            else:
                self.reset_output()
        except (model.TooManyPlayersError, model.PlayerTableIsEmptyError) as e:
            self.set_output(view.format_error, e)

    def create_round(self):
        """
        Ajoute un round au tournoi courant.
        :return: None
        """
        try:
            name = view.get_input('Nom du round', check_if_input_is_empty, format_view=view.format_input_parameters)
            self.focus_tournament.create_round(name)
            self.set_output(view.format_output_round, self.focus_tournament.get_last_round())
        except model.TournamentError as e:
            self.set_output(view.format_error, e)

    def close_round(self):
        """
        Entre les résultats des matches du dernier round du tournoi courant et clos le round.
        :return: None
        """
        try:
            round = self.focus_tournament.get_last_round()
            while round.get_index_match_to_set_result() is not None:
                index_match = round.get_index_match_to_set_result()
                p1, p2 = round.get_players_in_match(index_match)
                name_p1 = p1.last_name + ' ' + p1.first_name
                score_1 = view.get_input(f'Entrez le résultat de {name_p1}', check_if_result_is_valid,
                                         format_view=view.format_input_parameters)
                round.set_result(p1, p2, score_1, index_match)
            self.focus_tournament.close_round()
            self.show_matches()
        except (model.RoundError, model.TournamentError) as e:
            self.set_output(view.format_error, e)

    def show_tournaments_in_database(self):
        """
        Prépare l'affichage des tournois en base de données pour la zone output.
        :return: None
        """
        try:
            self.db.check_if_tournament_table_is_empty()
            doc_ids = self.db.get_tournaments_docs_id()
            tournaments = [self.db.get_tournament_by_id(doc_id) for doc_id in doc_ids]
            self.set_output(view.format_output_tournaments, (doc_ids, tournaments))
        except model.TournamentTableIsEmptyError as e:
            self.set_output(view.format_error, e)

    def show_players(self):
        """
        Prépare l'affichage des joueurs du tournoi courant si il existe ou alors les joueurs de la base de données.
        :return: None
        """
        try:
            self.db.check_if_player_table_is_empty()
            param = view.get_input('Choisissez un paramètre entre tri alphabétique (A) ou Classement (C)',
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
        except (model.PlayersInTournamentEmptyError, model.PlayerTableIsEmptyError) as e:
            self.set_output(view.format_information, e)

    def show_rounds(self):
        """
        Prépare l'affichage des rounds pour la zone output.
        :return: None
        """
        try:
            self.set_output(view.format_output_rounds, self.focus_tournament.get_rounds())
        except model.RoundNotExistError as e:
            self.set_output(view.format_information, e)

    def show_matches(self):
        """
        Prépare l'affichage des matches de chaque round pour la zone output.
        :return: None
        """
        try:
            players_1 = []
            players_2 = []
            scores_1 = []
            scores_2 = []
            rounds = self.focus_tournament.get_rounds()
            for round in rounds:
                for (p1, s1), (p2, s2) in round.matches:
                    players_1.append(p1)
                    scores_1.append(s1)
                    players_2.append(p2)
                    scores_2.append(s2)
            self.set_output(view.format_output_rounds_matches, (rounds, players_1, players_2, scores_1, scores_2))
        except model.RoundNotExistError as e:
            self.set_output(view.format_information, e)
