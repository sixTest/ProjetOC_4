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


class Round(object):
    """
    Class représentant un tour de matchs.
    """

    def __init__(self, name, start_date=None, end_date=None, matchs=()):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.matchs = matchs


class Tournament(object):
    """
    Class représentant un tournois
    """
    def __init__(self, name, location, date, time, description, numbers_rounds=4, indices_players=[], rounds = ()):
        self.name = name
        self.location = location
        self.date = date
        self.time = time
        self.description = description
        self.numbers_rounds = numbers_rounds
        self.indices_players = indices_players
        self.rounds = rounds