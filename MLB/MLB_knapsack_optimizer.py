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

with open('DKSalaries.csv', 'r') as data:
    reader = csv.reader(data)
    reader.next()
    players = []
    for row in reader:
        name = row[0]
        position = row[3]
        salary = int(row[1])
        points = float(row[7])
        value = points / salary
        team = row[4]
        player = Player(position, name, salary, points, value, team)
        players.append(player)

def knapsack(players):
    budget = 50000
    current_team_salary = 0
    constraints = {
        'P':2,
        'C':1,
        '1B':1,
        '2B':1,
        '3B':1,
        'SS':1,
        'OF':3
        }

    counts = {
        'P':0,
        'C':0,
        '1B':0,
        '2B':0,
        '3B':0,
        'SS':0,
        'OF':0
        }

    players.sort(key=lambda x: x.value, reverse=True)
    team = []

    for player in players:
        nam = player.name
        pos = player.position
        if "/" in pos:
            pos=pos[:pos.index("/")]
        if "P" in pos:
            pos="P"
        sal = player.salary
        pts = player.points
        if counts[pos] < constraints[pos] and current_team_salary + sal <= budget:
            team.append(player)
            counts[pos] = counts[pos] + 1
            current_team_salary += sal

    players.sort(key=lambda x: x.points, reverse=True)
    v=2.75
    while(current_team_salary+700<budget and v > 1.5):
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
