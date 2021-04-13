from tinydb import TinyDB

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