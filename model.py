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


class PlayersEmptyError(TournamentError):
    def __init__(self):
        pass

    def __str__(self):
        return "Aucun joueur n'a encore était importer dans le tournois."


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
        return "Aucun round n'a encore etait crée"


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
        return 'Un tournoi avec un nom, un lieu, une date idendique est présent dans la base de données.'


class ExportPlayerAlreadyExistError(DataBaseTinyDBError):
    def __init__(self):
        pass

    def __str__(self):
        return 'Un Joueur avec un nom et un prénom idendique est présent dans la base de données.'


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
        return 'Les résultat des matchs ne sont pas rempli.'


class RoundMatchResultCompleteError(RoundError):
    def __init__(self):
        pass

    def __str__(self):
        return 'Les résultats du round sont rempli.'


class RoundPairingError(RoundError):
    def __init__(self):
        pass


def get_date():
    now = datetime.datetime.now()
    return datetime.datetime(now.year, now.month, now.day, now.hour, now.minute)


def get_scores_player_2(s1):
    if s1 == 0.5:
        return 0.5
    else:
        return 1 - s1


def get_matrice():
    matrice = []
    for a in range(7):
        for b in range(5):
            for c in range(3):
                for d in range(1):
                    matrice.append((a, b, c, d))
    return matrice


def get_nearest(player, players, index_priority):
    return players[players.index(player) + 1:][index_priority]


def serialized_tournament(tournament):
    return {'name': tournament.name, 'location': tournament.location, 'date': tournament.date,
            'time': tournament.time, 'numbers_rounds': tournament.numbers_rounds,
            'description': tournament.description, 'indices_players': tournament.indices_players,
            'rounds': [serialized_round(round) for round in tournament.rounds]}


def serialized_player(player):
    return {'last_name': player.last_name, 'first_name': player.first_name, 'gender': player.gender,
            'birthdate': player.birthdate, 'ranking': player.ranking}


def serialized_round(round):
    return {'name': round.name, 'start_date': str(round.start_date), 'end_date': str(round.end_date),
            'closed': round.closed,
            'matches': [(serialized_player(p1), s1, serialized_player(p2), s2) for (p1, s1), (p2, s2) in round.matches]}


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
        return [Tournament(**dict_tournament) for dict_tournament in self.tournaments_table]

    def get_tournament_by_id(self, doc_id):
        return Tournament(**self.tournaments_table.get(doc_id=doc_id))

    def get_tournaments_docs_id(self):
        return [dict_tournament.doc_id for dict_tournament in self.tournaments_table]

    def get_player_by_id(self, doc_id):
        return Player(**self.players_table.get(doc_id=doc_id))

    def get_players_docs_id(self):
        return [dict_player.doc_id for dict_player in self.players_table]

    def get_doc_id_by_player(self, player):
        return self.players_table.get(
            (where('last_name') == player.last_name) & (where('first_name') == player.first_name)).doc_id

    def get_players(self):
        return [Player(**dict_player) for dict_player in self.players_table]

    def check_if_tournament_already_exist(self, tournament):
        if self.tournaments_table.contains(
                (where('name') == tournament.name) & (where('location') == tournament.location)
                & (where('date') == tournament.date)):
            raise ExportTournamentAlreadyExistError()

    def check_if_player_already_exist(self, player):
        if self.players_table.contains(
                (where('last_name') == player.last_name) & (where('first_name') == player.first_name)):
            raise ExportPlayerAlreadyExistError()

    def update_tournament(self, tournament, doc_id):
        dict_tournament = serialized_tournament(tournament)
        for k, v in dict_tournament.items():
            self.tournaments_table.update({k: v}, doc_ids=[doc_id])


DATABASE = DataBaseTinyDB()


class Player(object):
    """
    Class représentant un joueur
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
    Class représentant un tour de matchs.
    """

    def __init__(self, name, start_date=None, end_date=None, closed=False, matches=None):
        if matches is None:
            matches = []

        self.name = name
        if start_date is not None:
            self.start_date = start_date
        else:
            self.start_date = get_date()

        if matches:
            self.matches = [([Player(**dict_p1), s1], [Player(**dict_p2), s2]) for (dict_p1, s1, dict_p2, s2) in
                            matches]
        else:
            self.matches = matches

        self.end_date = end_date
        self.closed = closed

    def construct_round(self, paired_players):
        for p1, p2 in paired_players:
            self.matches.append(([p1, 0], [p2, 0]))

    def get_index_match_to_set_result(self):
        for (p1, s1), (p2, s2) in self.matches:
            if s1 + s2 == 0:
                return self.matches.index(([p1, s1], [p2, s2]))
        return None

    def get_players_in_match(self, index_match):
        (p1, s1), (p2, s2) = self.matches[index_match]
        return p1, p2

    def set_result(self, p1, p2, s1, index_match):
        s2 = get_scores_player_2(s1)
        self.matches[index_match] = ([p1, s1], [p2, s2])

    def close_round(self):
        self.check_if_close_round_is_valid()
        self.end_date = get_date()
        self.closed = True

    def check_if_close_round_is_valid(self):
        if self.closed:
            raise RoundClosedError()
        else:
            if self.get_index_match_to_set_result() is not None:
                raise RoundMatchNotCompleteError()

    def check_if_pairing_is_valid(self, player_1, player_2):
        for (p1, s1), (p2, s2) in self.matches:
            if player_1 == p1 and player_2 == p2:
                raise RoundPairingError()

    def check_if_pairings_is_valid(self, paired_players):
        for p1, p2 in paired_players:
            try:
                self.check_if_pairing_is_valid(p1, p2)
            except RoundPairingError:
                return False
        return True


class Tournament(object):
    """
    Class représentant un tournois
    """
    NUMBER_PLAYER = 8

    def __init__(self, name, location, date, time, description, numbers_rounds=4, indices_players=None, rounds=None):
        if rounds is None:
            rounds = []
        if indices_players is None:
            indices_players = []
        self.name = name
        self.location = location
        self.date = date
        self.time = time
        self.description = description
        self.numbers_rounds = numbers_rounds
        self.indices_players = indices_players
        if rounds:
            self.rounds = [Round(**dict_round) for dict_round in rounds]
        else:
            self.rounds = rounds
        self.players = []
        self.init_tournament()

    def init_tournament(self):
        if self.indices_players:
            self.constructs_players()
            self.construct_players_points()

    def create_round(self, name):
        self.check_if_number_player_for_start_is_valid()
        self.check_if_create_round_is_valid()
        round = Round(name)
        if self.is_first_round():
            self.set_classification()
            paired_players = self.first_pairing()
            round.construct_round(paired_players)
            self.rounds.append(round)
        else:
            self.set_classification()
            round.construct_round(self.get_new_pairings())
            self.rounds.append(round)

    def close_round(self):
        self.rounds[-1].close_round()
        for match in self.rounds[-1].matches:
            (p1, s1), (p2, s2) = match
            self.set_points(p1, s1)
            self.set_points(p2, s2)

    def is_first_round(self):
        return True if len(self.rounds) == 0 else False

    def add_index_player(self, index):
        self.check_if_number_player_to_add_is_valid(1)
        self.indices_players.append(index)
        self.players.append(DATABASE.get_player_by_id(index))

    def add_indexes_players(self, indexes):
        self.check_if_number_player_to_add_is_valid(len(indexes))
        for index in indexes:
            self.add_index_player(index)

    def set_points(self, player, score):
        for p in self.players:
            if p == player:
                p.points += score

    def constructs_players(self):
        self.players = [DATABASE.get_player_by_id(doc_id) for doc_id in self.indices_players]

    def construct_players_points(self):
        for round in self.rounds:
            for match in round.matches:
                (p1, s1), (p2, s2) = match
                self.set_points(p1, s1)
                self.set_points(p2, s2)

    def get_pair(self):
        return [self.players[i:i + 2] for i in range(0, Tournament.NUMBER_PLAYER, 2)]

    def first_pairing(self):
        return [ (self.players[i],self.players[i+4]) for i in range(int(len(self.players)/2))]

    def set_classification(self):
        self.players.sort(key=lambda p: p.points, reverse=True)
        self.players = [list(g) for k, g in itertools.groupby(self.players, key=lambda p: p.points)]
        for lp in self.players:
            lp.sort(key=lambda p: p.ranking, reverse=True)
        self.players = [v for l in self.players for v in l]

    def get_players(self):
        self.check_if_players_exist()
        return self.players

    def get_rounds(self):
        self.check_if_round_exist()
        return self.rounds

    def get_last_round(self):
        return self.get_rounds()[-1]

    def check_if_number_player_to_add_is_valid(self, number_new_player):
        if len(self.players) + number_new_player > Tournament.NUMBER_PLAYER:
            raise TooManyPlayersError()

    def check_if_number_player_for_start_is_valid(self):
        if len(self.players) < Tournament.NUMBER_PLAYER:
            raise NotEnoughPlayersError()

    def check_if_create_round_is_valid(self):
        try:
            if not self.rounds[-1].closed:
                raise RoundNotClosedError()
            if len(self.rounds) >= self.numbers_rounds:
                raise TournamentIsClosedError()
        except IndexError:
            pass

    def check_if_players_exist(self):
        if not self.players:
            raise PlayersEmptyError()

    def check_if_round_exist(self):
        try:
            self.rounds[-1]
        except IndexError:
            raise RoundNotExistError()

    def check_if_pairings_is_valid(self, paired_players):
        for round in self.rounds:
            if not round.check_if_pairings_is_valid(paired_players):
                return False
        return True

    def get_new_pairings(self):
        matrice = get_matrice()
        for m in matrice:
            cp_players = copy.deepcopy(self.players)
            pairings = []

            for i in m:
                nearest = get_nearest(cp_players[0], cp_players, i)
                pairings.append((cp_players[0], nearest))
                cp_players.pop(cp_players.index(cp_players[0]))
                cp_players.pop(cp_players.index(nearest))

            if self.check_if_pairings_is_valid(pairings):
                return pairings

        return None



