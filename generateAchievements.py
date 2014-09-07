#!/usr/bin/env python

import copy
import json
from os import path
from pprint import PrettyPrinter


BASE = 'PATH TO PARTICLE CLICKER JSON FOLDER'


def json_from_file(filename):
    """ Load a JSON object from a file. """
    with open(filename) as f:
        return json.load(f)


def format_number(num, digits=0):
    """ Give long numbers an SI prefix. """
    formatstring = '{{:.{}f}}{{}}'.format(digits)
    prefixes = [(1e24, 'Y'), (1e21, 'Z'), (1e18, 'E'), (1e15, 'P'),
                (1e12, 'T'), (1e9, 'G'), (1e6, 'M'), (1e3, 'k')]
    for magnitude, label in prefixes:
        if num >= magnitude:
            return formatstring.format(num / magnitude, label)


def map_out(prototype, items, levels):
    """ Magic! """
    return [{k: v.format(level=level, levelstring=format_number(level), **item)
             for k, v in prototype.items()}
            for item in items for level in levels]

pp = PrettyPrinter(indent=2)

objects = {
    k: json_from_file(path.join(BASE, v)) for k, v in {
        'workers': 'workers.json',
        'upgrades': 'upgrades.json',
        'research': 'research.json'
    }.items()
}

researchPrototype = {
    'key': 'achievement-{key}-{level}',
    'description': '{name} research level {level}!',
    'icon': 'fa-cogs',
    'type': 'research',
    'target': '{key}',
    'threshold': '{level}'
}
discoveryPrototype = copy.copy(researchPrototype)
discoveryPrototype['description'] = '{name} discovery!'
workersPrototype = {
    'key': 'achievement-{key}-{level}',
    'description': '{level} {name} working for you!',
    'icon': 'fa-users',
    'type': 'workers',
    'target': '{key}',
    'threshold': '{level}'
}
firstWorkerPrototype = copy.copy(workersPrototype)
firstWorkerPrototype['description'] = 'The first {name} hired!'
firstWorkerPrototype['icon'] = 'fa-user'
clicksPrototype = {
    'key': 'achievement-clicks-{levelstring}',
    'description': '{levelstring} clicks!',
    'icon': 'fa-hand-o-up',
    'type': 'count',
    'target': 'clicks',
    'threshold': '{level}'
}
firstClickPrototype = copy.copy(clicksPrototype)
firstClickPrototype['description'] = 'Your first click!'
dataCollectedPrototype = {
    'key': 'achievement-data-collected-{levelstring}',
    'description': '{levelstring} data collected!',
    'icon': 'fa-database',
    'type': 'count',
    'target': 'data',
    'threshold': '{level}'
}
fundingCollectedPrototype = {
    'key': 'achievement-funding-collected-{levelstring}',
    'description': 'JTN {levelstring} funding gathered!',
    'icon': 'fa-money',
    'type': 'count',
    'target': 'money',
    'threshold': '{level}'
}
dataProcessedPrototype = {
    'key': 'achievement-data-processed-{levelstring}',
    'description': '{levelstring} data processed!',
    'icon': 'fa-hdd',
    'type': 'count',
    'target': 'dataSpent',
    'threshold': '{level}'
}

achievements = []
achievements += map_out(discoveryPrototype, objects['research'], [1])
achievements += map_out(researchPrototype, objects['research'],
                        [5, 25, 50, 100])
achievements += map_out(firstWorkerPrototype, objects['workers'], [1])
achievements += map_out(workersPrototype, objects['workers'], [5, 25, 50, 100])
achievements += map_out(firstClickPrototype, [{}], [1])
achievements += map_out(clicksPrototype, [{}],
                        [100, 1000, 10000, 100000, 1000000])
achievements += map_out(dataCollectedPrototype, [{}],
                        [100, 10000, int(1e6), int(1e8), int(1e10)])
achievements += map_out(fundingCollectedPrototype, [{}],
                        [100, 10000, int(1e6), int(1e8), int(1e10)])
achievements += map_out(dataProcessedPrototype, [{}],
                        [100, 10000, int(1e6), int(1e8), int(1e10)])

# fix thresholds
for achievement in achievements:
    achievement['threshold'] = int(achievement['threshold'])

pp.pprint(achievements)
