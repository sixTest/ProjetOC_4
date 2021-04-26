import datetime
from tinydb import TinyDB, where
import itertools
import copy


class TournamentError(Exception):
    def __init__(self):
        pass


class TooManyPlayersError(TournamentError):
    def __init__(self):
        pass

    def __str__(self):
        return f'Le nombre de joueurs maximum est {Tournament.NUMBER_PLAYER}.'


class PlayersInTournamentEmptyError(TournamentError):
    def __init__(self):
        pass

    def __str__(self):
        return "Aucun joueur n'a encore été importé dans le tournoi."


class NotEnoughPlayersError(TournamentError):
    def __init__(self):
        pass

    def __str__(self):
        return f'Le nombre de joueurs pour commencer un round doit être {Tournament.NUMBER_PLAYER}.'


class RoundNotClosedError(TournamentError):
    def __init__(self):
        pass

    def __str__(self):
        return "Le round n'est pas encore fini."


class RoundNotExistError(TournamentError):
    def __init__(self):
        pass

    def __str__(self):
        return "Aucun round n'a encore été créé"


class RoundAlreadyClosedError(TournamentError):
    def __init__(self):
        pass

    def __str__(self):
        return "Le round est déja clos."


class TournamentIsClosedError(TournamentError):
    def __init__(self):
        pass

    def __str__(self):
        return "Le tournoi est clos."


class DataBaseTinyDBError(Exception):
    def __init__(self):
        pass


class ExportTournamentAlreadyExistError(DataBaseTinyDBError):
    def __init__(self):
        pass

    def __str__(self):
        return 'Un tournoi avec un nom, un lieu, une date identique est présent dans la base de données.'


class ExportPlayerAlreadyExistError(DataBaseTinyDBError):
    def __init__(self):
        pass

    def __str__(self):
        return 'Un Joueur avec un nom et un prénom identique est présent dans la base de données.'


class TournamentTableIsEmptyError(DataBaseTinyDBError):
    def __init__(self):
        pass

    def __str__(self):
        return "Il n'existe aucun tournoi en base de données."


class PlayerTableIsEmptyError(DataBaseTinyDBError):
    def __init__(self):
        pass

    def __str__(self):
        return "Il n'existe aucun joueur en base de données."


class RoundError(Exception):
    def __init__(self):
        pass


class RoundClosedError(RoundError):
    def __init__(self):
        pass

    def __str__(self):
        return 'Le round est fini.'


class RoundMatchNotCompleteError(RoundError):
    def __init__(self):
        pass

    def __str__(self):
        return 'Les résultats des matchs ne sont pas remplis.'


class RoundMatchResultCompleteError(RoundError):
    def __init__(self):
        pass

    def __str__(self):
        return 'Les résultats du round sont complets.'


class RoundPairingError(RoundError):
    def __init__(self):
        pass


def get_date():
    """
    Récupère la date du moment.
    :return: instance de class datetime
    """
    now = datetime.datetime.now()
    return datetime.datetime(now.year, now.month, now.day, now.hour, now.minute)


def get_scores_player_2(s1):
    """
    Calcule le score du joueur 2 en fonction du score du joueur 1 (s1).
    :param s1: float ou int, appartenant aux valeurs (0.5, 1, 0)
    :return: float ou int, appartenant aux valeurs (0.5, 1, 0)
    """
    if s1 == 0.5:
        return 0.5
    else:
        return 1 - s1


def get_all_offsets():
    """
    Récupère l'ensemble des décalages possibles sur 8 joueurs.
    :return: list[tuple[int]], chaque tuple représente un ensemble de décalages pour l'association des pairs de joueurs
    pour un round.
    """
    offsets = []
    for a in range(7):
        for b in range(5):
            for c in range(3):
                for d in range(1):
                    offsets.append((a, b, c, d))
    return offsets


def serialized_tournament(tournament):
    """
    Sérialise une instance de tournoi.
    :param tournament: instance de tournoi
    :return: dictionnaire
    """
    return {'name': tournament.name, 'location': tournament.location, 'date': tournament.date,
            'time': tournament.time, 'numbers_rounds': tournament.numbers_rounds,
            'description': tournament.description, 'indices_players': tournament.indices_players,
            'rounds': [serialized_round(round) for round in tournament.rounds]}


def serialized_player(player):
    """
    Sérialise une instance de joueur.
    :param player: instance de joueur
    :return: dictionnaire
    """
    return {'last_name': player.last_name, 'first_name': player.first_name, 'gender': player.gender,
            'birthdate': player.birthdate, 'ranking': player.ranking}


def serialized_round(round):
    """
    Sérialise une instance de round
    :param round: instance de round
    :return: dictionnaire
    """
    return {'name': round.name, 'start_date': str(round.start_date), 'end_date': str(round.end_date),
            'closed': round.closed,
            'matches': [(serialized_player(p1), s1, serialized_player(p2), s2) for (p1, s1), (p2, s2)
                        in round.matches]}


class DataBaseTinyDB(object):
    """
    Classe qui centralise les actions sur la base de données.
    """

    def __init__(self):
        self.db = TinyDB('db.json')
        self.players_table = self.db.table('Players')
        self.tournaments_table = self.db.table('Tournaments')

    def add_tournament(self, tournament):
        """
        Ajoute un tournoi en base de données et retourne son index.
        :param tournament: instance de tournoi
        :return: int
        """
        return self.tournaments_table.insert(serialized_tournament(tournament))

    def get_tournaments(self):
        """
        Récupère l'ensemble des tournois de la base de données.
        :return: list[Tournament]
        """
        return [Tournament(**dict_tournament) for dict_tournament in self.tournaments_table]

    def get_tournament_by_id(self, doc_id):
        """
        Récupère un tournoi par son index en base de données.
        :param doc_id: int
        :return: Tournament
        """
        return Tournament(**self.tournaments_table.get(doc_id=doc_id))

    def get_tournaments_docs_id(self):
        """
        Récupère l'ensemble des index des tournois de la base de données.
        :return: list[int]
        """
        return [dict_tournament.doc_id for dict_tournament in self.tournaments_table]

    def update_tournament(self, tournament, doc_id):
        """
        Met a jour les valeurs d'un tournoi en base de données par son index.
        :param tournament: instance de tournoi
        :param doc_id: int
        :return: None
        """
        dict_tournament = serialized_tournament(tournament)
        for k, v in dict_tournament.items():
            self.tournaments_table.update({k: v}, doc_ids=[doc_id])

    def add_player(self, player):
        """
        Ajoute un joueur en base de données et retourne son index.
        :param player: instance de joueur
        :return: int
        """
        return self.players_table.insert(serialized_player(player))

    def get_players(self):
        """
        Récupère l'ensemble des joueurs de la base de données.
        :return: list[Player]
        """
        return [Player(**dict_player) for dict_player in self.players_table]

    def get_player_by_id(self, doc_id):
        """
        Récupère un joueur par son index en base de données.
        :param doc_id: int
        :return: Player
        """
        return Player(**self.players_table.get(doc_id=doc_id))

    def get_players_docs_id(self):
        """
        Récupère l'ensemble des index des joueurs de la base de données.
        :return: list[int]
        """
        return [dict_player.doc_id for dict_player in self.players_table]

    def get_doc_id_by_player(self, player):
        """
        Récupère l'index en base de données d'un joueur en particulier.
        :param player: instance de joueur
        :return: int
        """
        return self.players_table.get(
            (where('last_name') == player.last_name) & (where('first_name') == player.first_name)).doc_id

    def check_if_tournament_already_exist(self, tournament):
        """
        Vérifie si un tournoi existe déjà en base de données.
        :param tournament: instance de tournoi
        :return: None
        """
        if self.tournaments_table.contains(
                (where('name') == tournament.name) & (where('location') == tournament.location)
                & (where('date') == tournament.date)):
            raise ExportTournamentAlreadyExistError()

    def check_if_player_already_exist(self, player):
        """
        Vérifie si un joueur existe déjà en base de données.
        :param player: instance de joueur
        :return: None
        """
        if self.players_table.contains(
                (where('last_name') == player.last_name) & (where('first_name') == player.first_name)):
            raise ExportPlayerAlreadyExistError()

    def check_if_tournament_table_is_empty(self):
        """
        Vérifie qu'il existe au moins un tournoi en base de données.
        :return: None
        """
        if not self.tournaments_table.all():
            raise TournamentTableIsEmptyError()

    def check_if_player_table_is_empty(self):
        """
        Vérifie qu'il existe au moins un joueur en base de données.
        :return: None
        """
        if not self.players_table.all():
            raise PlayerTableIsEmptyError()


DATABASE = DataBaseTinyDB()


class Player(object):
    """
    Classe qui représente le modèle de données pour les joueurs.
    """

    def __init__(self, last_name, first_name, birthdate, gender, ranking, points=0):
        self.last_name = last_name
        self.first_name = first_name
        self.gender = gender
        self.birthdate = birthdate
        self.ranking = ranking
        self.points = points

    def __eq__(self, other):
        if self.last_name == other.last_name and self.first_name == other.first_name:
            return True
        return False


class Round(object):
    """
    Classe qui représente le modèle de données pour les tours de matches.
    """

    def __init__(self, name, start_date=None, end_date=None, closed=False, matches=None):
        if start_date is not None:
            self.start_date = start_date
        else:
            self.start_date = get_date()
        if matches is None:
            self.matches = []
        else:
            self.matches = [([Player(**dict_p1), s1], [Player(**dict_p2), s2]) for (dict_p1, s1, dict_p2, s2) in
                            matches]

        self.name = name
        self.end_date = end_date
        self.closed = closed

    def initialise_round(self, paired_players):
        """
        Initialisation des matches du round.
        :param paired_players: list[tuple[Player,Player]], représentant les matches du round
        :return: None
        """
        for p1, p2 in paired_players:
            self.matches.append(([p1, 0], [p2, 0]))

    def get_players_in_match(self, index_match):
        """
        Récupères les deux joueurs d'un match en particulier.
        :param index_match: int
        :return: tuple[Player,Player]
        """
        (p1, s1), (p2, s2) = self.matches[index_match]
        return p1, p2

    def set_result(self, p1, p2, s1, index_match):
        """
        Affecte les résultats d'un match en particulier.
        :param p1: Player, représentant l'instance du joueur 1
        :param p2: Player, représentant l'instance du joueur 2
        :param s1: int, représentant le score du joueur 1
        :param index_match: int
        :return: None
        """
        s2 = get_scores_player_2(s1)
        self.matches[index_match] = ([p1, s1], [p2, s2])

    def get_index_match_to_set_result(self):
        """
        Récupère si possible l'index du premier match trouvé dont les résultats ne sont pas encore complétés.
        :return: int, None
        """
        for (p1, s1), (p2, s2) in self.matches:
            if s1 + s2 == 0:
                return self.matches.index(([p1, s1], [p2, s2]))
        return None

    def close_round(self):
        """
        Effectue les opérations de clôture du round.
        :return: None
        """
        self.check_if_close_round_is_valid()
        self.end_date = get_date()
        self.closed = True

    def check_if_close_round_is_valid(self):
        """
        Vérifie que la clôture du round est possible.
        :return: None
        """
        if self.closed:
            raise RoundClosedError()
        else:
            if self.get_index_match_to_set_result() is not None:
                raise RoundMatchNotCompleteError()

    def check_if_pairing_is_valid(self, player_1, player_2):
        """
        Vérifie que l'association des deux joueurs pour un match est possible.
        :param player_1: Player, représentant l'instance du joueur 1
        :param player_2: Player, représentant l'instance du joueur 2
        :return: None
        """
        for (p1, s1), (p2, s2) in self.matches:
            if p1 in (player_1, player_2) and p2 in (player_1, player_2):
                raise RoundPairingError()

    def check_if_pairings_is_valid(self, paired_players):
        """
        Vérifie que l'association des pairs de joueurs pour des matches soit possible.
        :param paired_players: list[tuple[Player,Player]], représentant les matches du round
        :return: boolean
        """
        for p1, p2 in paired_players:
            try:
                self.check_if_pairing_is_valid(p1, p2)
            except RoundPairingError:
                return False
        return True


class Tournament(object):
    """
    Classe qui représente le modèle de données pour les tournois.
    """
    NUMBER_PLAYER = 8

    def __init__(self, name, location, date, time, description, numbers_rounds=4, indices_players=None, rounds=None):
        if indices_players is None:
            indices_players = []
        if rounds is None:
            self.rounds = []
        else:
            self.rounds = [Round(**dict_round) for dict_round in rounds]
        self.name = name
        self.location = location
        self.date = date
        self.time = time
        self.description = description
        self.numbers_rounds = numbers_rounds
        self.indices_players = indices_players
        self.players = []
        self.init_tournament()

    def init_tournament(self):
        """
        Initialise si besoin les instances des joueurs participant au tournoi et leur points.
        :return: None
        """
        if self.indices_players:
            self.constructs_players()
            self.construct_players_points()

    def add_player_from_database(self, index):
        """
        Ajoute une instance de joueur au tournoi par son index en base de données.
        :param index: int
        :return: None
        """
        self.check_if_number_player_to_add_is_valid(1)
        self.indices_players.append(index)
        self.players.append(DATABASE.get_player_by_id(index))

    def add_players_from_database(self, indexes):
        """
        Ajoute des instances de joueur au tournoi par leur index en base de données.
        :param indexes: list[int]
        :return: None
        """
        self.check_if_number_player_to_add_is_valid(len(indexes))
        for index in indexes:
            self.add_player_from_database(index)

    def constructs_players(self):
        """
        Construit les instances des joueurs participant au tournoi.
        :return: None
        """
        self.players = [DATABASE.get_player_by_id(doc_id) for doc_id in self.indices_players]

    def construct_players_points(self):
        """
        Construit les points des joueurs avec les résultats des matches des rounds précédents.
        :return: None
        """
        for round in self.rounds:
            for match in round.matches:
                (p1, s1), (p2, s2) = match
                self.set_points(p1, s1)
                self.set_points(p2, s2)

    def set_points(self, player, score):
        """
        Ajoute le score d'un match d'un joueur a ses points dans le tournoi.
        :param player: instance de joueur
        :param score: float, int
        :return: None
        """
        for p in self.players:
            if p == player:
                p.points += score

    def get_players(self):
        """
        Récupère les joueurs participant au tournoi.
        :return: list[Player]
        """
        self.check_if_players_exist()
        return self.players

    def create_round(self, name):
        """
        Crée et ajoute un round au tournoi.
        :param name: string
        :return: None
        """
        self.check_if_number_player_for_start_is_valid()
        self.check_if_create_round_is_valid()
        round = Round(name)
        if self.is_first_round():
            self.set_classification()
            paired_players = self.first_pairing()
            round.initialise_round(paired_players)
            self.rounds.append(round)
        else:
            self.set_classification()
            round.initialise_round(self.get_new_pairings())
            self.rounds.append(round)

    def get_rounds(self):
        """
        Récupère les rounds du tournoi.
        :return: list[Round]
        """
        self.check_if_round_exist()
        return self.rounds

    def get_last_round(self):
        """
        Récupère le round courant.
        :return: Round
        """
        return self.get_rounds()[-1]

    def is_first_round(self):
        """
        Détermine si le round courant est le premier round ou non.
        :return: boolean
        """
        return True if len(self.rounds) == 0 else False

    def close_round(self):
        """
        Clôture le dernier round créé du tournoi et affecte les résultats aux instances des joueurs correspondants.
        :return: None
        """
        self.rounds[-1].close_round()
        for match in self.rounds[-1].matches:
            (p1, s1), (p2, s2) = match
            self.set_points(p1, s1)
            self.set_points(p2, s2)

    def set_classification(self):
        """
        Tri les instances des joueurs par points, puis par classement en cas d'égalité.
        :return: None
        """
        self.players.sort(key=lambda p: p.points, reverse=True)
        self.players = [list(g) for k, g in itertools.groupby(self.players, key=lambda p: p.points)]
        for lp in self.players:
            lp.sort(key=lambda p: p.ranking, reverse=True)
        self.players = [value for li in self.players for value in li]

    def get_pair(self):
        """
        Associe les instances des joueurs 2 a 2 en partant du bas.
        :return: list[list[Player,Player]]
        """
        return [self.players[i:i + 2] for i in range(0, Tournament.NUMBER_PLAYER, 2)]

    def first_pairing(self):
        """
        Associe les joueurs pour le premier round.
        :return: list[tuple[Player,Player]]
        """
        return [(self.players[i], self.players[i + 4]) for i in range(int(len(self.players) / 2))]

    def get_new_pairings(self):
        """
        Récupère l'association des joueurs pour les matchs du round suivant.
        :return: list[tuple[Player,Player]]
        """
        offsets = get_all_offsets()
        for m in offsets:
            cp_players = copy.deepcopy(self.players)
            pairings = []

            for i in m:
                nearest = cp_players[1:][i]
                pairings.append((cp_players[0], nearest))
                cp_players.pop(cp_players.index(cp_players[0]))
                cp_players.pop(cp_players.index(nearest))

            if self.check_if_pairings_is_valid(pairings):
                return pairings

        return None

    def check_if_number_player_to_add_is_valid(self, number_new_player):
        """
        Vérifie qu'on puisse ajouter un certain nombre de joueurs au tournoi.
        :param number_new_player: int
        :return: None
        """
        if len(self.players) + number_new_player > Tournament.NUMBER_PLAYER:
            raise TooManyPlayersError()

    def check_if_number_player_for_start_is_valid(self):
        """
        Vérifie qu'on ait assez de joueurs pour commencer le tournoi.
        :return: None
        """
        if len(self.players) < Tournament.NUMBER_PLAYER:
            raise NotEnoughPlayersError()

    def check_if_create_round_is_valid(self):
        """
        Vérifie qu'on puisse créer un nouveau round.
        :return: None
        """
        try:
            if not self.rounds[-1].closed:
                raise RoundNotClosedError()
            if len(self.rounds) >= self.numbers_rounds:
                raise TournamentIsClosedError()
        except IndexError:
            pass

    def check_if_players_exist(self):
        """
        Vérifie qu'il existe au moins un joueur dans le tournoi.
        :return: None
        """
        if not self.players:
            raise PlayersInTournamentEmptyError()

    def check_if_round_exist(self):
        """
        Vérifie qu'il existe au moins un round dans le tournoi.
        :return: None
        """
        try:
            self.rounds[-1]
        except IndexError:
            raise RoundNotExistError()

    def check_if_pairings_is_valid(self, paired_players):
        """
        Vérifie que l'association des joueurs est possible.
        :param paired_players: list[tuple[Player,Player]]
        :return: boolean
        """
        for round in self.rounds:
            if not round.check_if_pairings_is_valid(paired_players):
                return False
        return True
