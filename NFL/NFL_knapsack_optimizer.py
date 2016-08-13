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

with open('DKRotoProj.csv', 'r') as data:
    reader = csv.reader(data)
    reader.next()
    players = []
    for row in reader:
        name = row[0]
        position = row[1]
        salary = int(row[8])
        points = float(row[9])
        value = float(row[10])
        team = row[2]
        player = Player(position, name, salary, points, value, team)
        players.append(player)

def knapsack(players):
    budget = 50000
    current_team_salary = 0
    constraints = {
        'QB':1,
        'RB':2,
        'WR':3,
        'TE':1,
        'D':1,
        'FLEX':1
        }

    counts = {
        'QB':0,
        'RB':0,
        'WR':0,
        'TE':0,
        'D':0,
        'FLEX':0
        }

    players.sort(key=lambda x: x.value, reverse=True)
    team = []

    for player in players:
        nam = player.name
        pos = player.position
        sal = player.salary
        pts = player.points
        if counts[pos] < constraints[pos] and current_team_salary + sal <= budget:
            team.append(player)
            counts[pos] = counts[pos] + 1
            current_team_salary += sal
            continue
        if counts['FLEX'] < constraints['FLEX'] and current_team_salary + sal <= budget and pos in ['RB','WR','TE']:
            team.append(player)
            counts['FLEX'] = counts['FLEX'] + 1
            current_team_salary += sal

    players.sort(key=lambda x: x.points, reverse=True)
    v=3.0
    while(current_team_salary+400<budget and v > 1.5):
        for player in players:
            nam = player.name
            pos = player.position
            sal = player.salary
            pts = player.points
            val = player.value

            if player not in team:
                pos_players = [ x for x in team if x.position == pos]
                pos_players.sort(key=lambda x: x.points)
                for pos_player in pos_players:
                    if (current_team_salary + sal - pos_player.salary) <= budget and pts > pos_player.points and val>v:
                        val_Added = ((sal-pos_player.salary)/(pts-pos_player.points)) #rough idea of value added by swapping players, needs improvement
                        if val_Added<1000:
                            team[team.index(pos_player)] = player
                            current_team_salary = current_team_salary + sal - pos_player.salary
                            points = 0
                            salary = 0
                            print "Player to be inserted: ", player
                            print "Salary/Projection: ", val
                            print "Player to be swapped out: ", pos_player
                            print "Value added with swap: ",  val_Added
                            print "\n"
                            for p in team:
                                points += p.points
                                salary += p.salary
                                print p
                            print "\nPoints: {}".format(points)
                            print "Salary: {}".format(salary)
                            print "\n"
                            break
        v-=0.15
    return team


team = knapsack(players)
points = 0
salary = 0
print "\n"
print "Final optimized team: "
print "\n"
for player in team:
    points += player.points
    salary += player.salary
    print player
print "\nPoints: {}".format(points)
print "Salary: {}".format(salary)
