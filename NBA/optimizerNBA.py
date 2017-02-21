#!/Python27/python
import csv

class Player():
    def __init__(self, position, name, salary, points, value, team):
        self.self = self
        self.position = position
        self.name = name
        self.salary = salary
        self.points = points
        self.value = value
        self.team = team

    def __iter__(self):
        return iter(self.list)

    def __str__(self):
        return "{} {} {} {} {}".format(self.name,self.position,self.salary, self.points, self.team)

with open('/home/maielld1/mysite/tmp/rotogrindNBA.csv', 'r') as data:
    reader = csv.reader(data)
    reader.next()
    players = []
    G = ['PG', 'SG']
    F = ['SF', 'PF']
    U = ['PG', 'SG', 'SF', 'PF', 'C']
    for row in reader:
        name = row[0]
        position = row[3]
        salary = int(row[1])
        points = float(row[7])
        value = (points / salary)*1000
        team = row[2]
        player = Player(position, name, salary, points, value, team)
        players.append(player)

def knapsack(players):
    budget = 50000
    current_team_salary = 0
    constraints = {
        'PG':1,
        'SG':1,
        'SF':1,
        'PF':1,
        'C':1,
        'G':1,
        'F':1,
        'U':1
        }

    counts = {
        'PG':0,
        'SG':0,
        'SF':0,
        'PF':0,
        'C':0,
        'G':0,
        'F':0,
        'U':0
        }

    players.sort(key=lambda x: x.value, reverse=True)
    team = {
        'PG':0,
        'SG':0,
        'SF':0,
        'PF':0,
        'C':0,
        'G':0,
        'F':0,
        'U':0
    }
    for player in players:
        nam = player.name
        pos=[]
        if "/" in player.position:
            positions = player.position.split('/')
            pos.append(positions[0])
            pos.append(positions[1])
        else:
            pos.append(player.position)
        sal = player.salary
        pts = player.points
        for p in pos:
            if player not in team.values():
                if counts[p] < constraints[p] and current_team_salary + sal <= budget:
                    team[p] = player
                    counts[p] = counts[p] + 1
                    current_team_salary += sal
                    continue
                if counts['G'] < constraints['G'] and current_team_salary + sal <= budget and p in G:
                    team['G'] = player
                    counts['G'] = counts['G'] + 1
                    current_team_salary += sal
                    continue
                if counts['F'] < constraints['F'] and current_team_salary + sal <= budget and p in F:
                    team['F'] = player
                    counts['F'] = counts['F'] + 1
                    current_team_salary += sal
                    continue
                if counts['U'] < constraints['U'] and current_team_salary + sal <= budget and p in U:
                    team['U'] = player
                    counts['U'] = counts['U'] + 1
                    current_team_salary += sal

    players.sort(key=lambda x: x.points, reverse=True)
    value=6.0
    while(current_team_salary+100<budget and value > 4.5):
        for player in players:
            nam = player.name
            pos=[]
            if "/" in player.position:
                positions = player.position.split('/')
                pos.append(positions[0])
                pos.append(positions[1])
            else:
                pos.append(player.position)
            sal = player.salary
            pts = player.points
            val = player.value

            if player not in team.values():
                pos_players = []
                for p in pos:
                    for x in team.values():
                        if p in x.position:
                            pos_players.append(x)
                pos_players.sort(key=lambda x: x.points)
                for pos_player in pos_players:
                    if (current_team_salary + sal - pos_player.salary) <= budget and pts > pos_player.points and val>value:
                        val_Added = ((sal-pos_player.salary)/(pts-pos_player.points)) #rough idea of value added by swapping players, needs improvement

                        if val_Added<500:
                            key = [k for k, v in team.items() if v == pos_player][0]
                            team[key] = player
                            current_team_salary = current_team_salary + sal - pos_player.salary
                            break
        value-=0.5
    return team

def optimize():
    return knapsack(players)
