import datetime
from tinydb import TinyDB, where
import itertools


class TournamentError(Exception):
    def __init__(self):
        pass


class TooManyPlayersError(TournamentError):
    def __init__(self):
        pass

    def __str__(self):
        return f'Le nombre de joueurs maximum est {Tournament.NUMBER_PLAYER}.'


class NotEnoughPlayersError(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return f'Le nombre de joueurs pour commencer un round doit être {Tournament.NUMBER_PLAYER}.'


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


def check_if_number_player_to_add_is_valid(number_player, number_new_player):
    if number_player + number_new_player > Tournament.NUMBER_PLAYER:
        raise TooManyPlayersError()


def check_if_number_player_for_start_is_valid(number_player):
    if number_player < Tournament.NUMBER_PLAYER:
        raise NotEnoughPlayersError()


def get_date():
    now = datetime.datetime.now()
    return datetime.datetime(now.year,now.month,now.day,now.hour,now.minute)


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
        return self.players_table.get((where('last_name') == player.last_name) & (where('first_name') == player.first_name)).doc_id

    def get_players(self):
        return [Player(**dict_player) for dict_player in self.players_table]

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


DATABASE = DataBaseTinyDB()


class Player(object):
    """
    Class représentant un joueur
    """
    def __init__(self, last_name, first_name, birthdate, gender, ranking):
        self.last_name = last_name
        self.first_name = first_name
        self.gender = gender
        self.birthdate = birthdate
        self.ranking = ranking
        self.points = 0

    def __eq__(self, other):
        if self.last_name == other.last_name and self.first_name == other.first_name:
            return True
        return False


class Round(object):
    """
    Class représentant un tour de matchs.
    """

    def __init__(self, name, start_date=None, matchs=()):
        self.name = name
        self.start_date = start_date
        self.end_date = None
        self.matchs = matchs
        self.closed = False

    def init_round(self, paired_players):
        self.matchs = [([p1, 0], [p2, 0]) for p1,p2 in paired_players]

    def set_result(self, player_1, player_2, result_1):
        for p1,p2 in self.matchs:
            if p1[0] == player_1 and p2[0] == player_2:
                p1[0].points += result_1
                p1[1] = result_1
                result_2 = 0.5 if result_1 == 0.5 else 1-result_1
                p2[0].points += result_2
                p2[1] = result_2

    def close_round(self):
        self.end_date = get_date()
        self.closed = True

    def check_if_close(self):
        if self.closed:
            raise RoundClosedError()


class Tournament(object):
    """
    Class représentant un tournois
    """
    NUMBER_PLAYER = 8

    def __init__(self, name, location, date, time, description, numbers_rounds=4, indices_players=[], rounds=()):
        self.name = name
        self.location = location
        self.date = date
        self.time = time
        self.description = description
        self.numbers_rounds = numbers_rounds
        self.indices_players = indices_players
        self.rounds = rounds
        self.players = []

    def create_first_round(self, name):
        check_if_number_player_for_start_is_valid(len(self.indices_players))
        self.constructs_players()
        self.set_classification()
        round = Round(name, get_date())
        round.init_round(self.get_pair())
        self.rounds.append(round)

    def add_index_player(self, index):
        check_if_number_player_to_add_is_valid(len(self.indices_players), 1)
        self.indices_players.append(index)

    def add_indexes_players(self, indexes):
        check_if_number_player_to_add_is_valid(len(self.indices_players), len(indexes))
        for index in indexes:
            self.add_index_player(index)

    def constructs_players(self):
        self.players = [DATABASE.get_player_by_id(doc_id) for doc_id in self.indices_players]

    def get_pair(self):
        return [self.players[i:i + 2] for i in range(0, Tournament.NUMBER_PLAYER, 2)]

    def set_classification(self):
        self.players.sort(key=lambda p: p.points, reverse=True)
        self.players = [list(g) for k, g in itertools.groupby(self.players, key=lambda p: p.points)]
        for lp in self.players:
            lp.sort(key=lambda p: p.ranking, reverse=True)
        self.players = [v for l in self.players for v in l]

