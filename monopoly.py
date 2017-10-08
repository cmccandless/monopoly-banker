import os
from sys import exit
import json

players = {}


class Player:
    players = {}

    def __init__(self, name, money=0):
        self.name = name or input('Player name: ')
        self.money = money
        Player.players[self.name] = self

    def __str__(self):
        return '{} ${}M'.format(self.name, self.money)

    def __add__(self, amount):
        newPlayer = Player(self.name, self.money)
        newPlayer.money = round(newPlayer.money + amount, 2)
        while newPlayer.money < 0:
            print('{} now has ${}M'.format(newPlayer.name, newPlayer.money))
            amount = input('Add mortgage amount: ')
            if amount == '':
                print('{} is bankrupt!')
                return
            newPlayer.money += float(amount)
        return newPlayer


if __name__ == '__main__':
    command = None
    players = None
    if os.path.isfile('monopoly.json'):
        try:
            with open('monopoly.json', 'r') as f:
                data = json.load(f)
                _players = {}
                for player in data:
                    _players[player['name']] = Player(**player)
                players = _players
        except:
            pass
    if players is None:
        players = {}
        players['freeparking'] = Player('freeparking', 0)
    while command is None or not command.startswith('q'):
        with open('monopoly.json', 'w') as f:
            data = [player.__dict__ for player in players.values()]
            f.write(json.dumps(data))
        os.system('cls')
        for player in sorted(players.values(),
                             key=lambda p: (p.name != 'freeparking',
                                            p.name)):
            print(player)
        print('Options:')
        print('[a]dd [p]layer [name [money]]')
        print('[p]ay [payer name] <payee name> <amount>')
        print('[q]uit')
        command = input('>')
        action, *args = command.split()
        if action.startswith('q'):
            break
        if action.startswith('a'):
            target = args.pop(0)
            if target.startswith('p'):
                if len(args) >= 1:
                    name = args.pop(0)
                else:
                    name = input('Player name: ')
                if len(args) >= 1:
                    money = args.pop(0)
                else:
                    money = input('Money (default: $15M): ')
                if money == '':
                    money = 15
                players[name] = Player(name, float(money))
                continue
        elif action.startswith('p'):
            if len(args) >= 3:
                payer, payee, amount, *args = args
            elif len(args) >= 2:
                payer = 'bank'
                payee, amount, *args = args
            if payer == 'fp':
                payer = 'freeparking'
            if payee == 'fp':
                payee = 'freeparking'
            if payer not in players and payer not in ['b', 'bank']:
                input('unknown player {}'.format(payer))
                continue
            if payee not in players and payee not in ['b', 'bank']:
                input('unknown player {}'.format(payee))
                continue
            amount = float(amount)
            if payer not in ['b', 'bank']:
                players[payer] += -amount
            if payee not in ['b', 'bank']:
                players[payee] += amount
            continue
        print('invalid command "{}"'.format(command))
