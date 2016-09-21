import random
import lens

class Console:
    def log(self, msg):
        print(msg)

    def newline(self):
        print('')


class Logger:
    def __init__(self, console):
        self.console = console

    def attack(self, a_ty, d_ty):
        self.console.log(attack_message(a_ty, d_ty))

    def damage(self, a_ty, d_ty, d_damage):
        self.console.log(damage_message(a_ty, d_ty, d_damage))

    def health(self, ty, health):
        self.console.log(health_message(ty, health))

def attack_message(a_ty, d_ty):
    return a_ty + ' attacks ' + d_ty + '.'

def damage_message(a_ty, d_ty, d_damage):
    return a_ty + ' did ' + str(d_damage) + ' damage to ' + d_ty + '.'

def health_message(ty, health):
    return ty + ' has ' + str(health) + ' health.'


class Battle:
    def __init__(self, logger):
        self.logger = logger

    def attack(self, a, d):
        a_ty = a['ty']
        d_ty = d['ty']
        self.logger.attack(a_ty, d_ty)
        def hurt(health):
            damage, health2 = calc_damage_and_health(a_ty, d_ty, health)
            self.logger.damage(a_ty, d_ty, damage)
            self.logger.health(d_ty, health2)
            return health2
        return lens.over(lens.key('health'), d, hurt)

def calc_damage_and_health(a_ty, d_ty, d_health):
    max_damage = attack_table[a_ty][d_ty]
    damage = d_health if max_damage > d_health else max_damage
    return damage, d_health - damage

attack_table = {
    'infant': {
        'infant': 4,
        'bazooker': 5,
        'jeeper': 1,
    },
    'bazooker': {
        'infant': 2,
        'bazooker': 2,
        'jeeper': 7,
    },
    'jeeper': {
        'infant': 8,
        'bazooker': 4,
        'jeeper': 2,
    },
}

# !

def wire():
    console = Console()
    logger = Logger(console)
    battle = Battle(logger)
    return {
        'console': console,
        'logger': logger,
        'battle': battle,
    }

def main(system):
    console = system['console']
    battle = system['battle']

    units = [
        {
            'ty': random.choice(['infant', 'bazooker', 'jeeper']),
            'health': 10,
        },
        {
            'ty': random.choice(['infant', 'bazooker', 'jeeper']),
            'health': 10,
        },
    ]

    console.log('this is waaaarrrhh!!!11')
    console.newline()

    order = { 'atk': 0, 'def': 1 }
    while units[order['atk']]['health'] > 0 and units[order['def']]['health'] > 0:
        units[order['def']] = battle.attack(units[order['atk']], units[order['def']])
        console.newline()
        order['atk'], order['def'] = order['def'], order['atk']

if __name__ == "__main__":
    main(wire())
