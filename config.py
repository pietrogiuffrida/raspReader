#!/usr/bin/env python3

logfilename = "log/reader.log"

stati = {0: 'ON', 1: 'OFF'}

delay = 2

channels = {

  37: {
    "channel": "A",
    "status": 1,
    'name': 'pompa 1',
    'events': {
      0: {
        'send': True,
        'message': 'POMPA 1 ON',
      },
      1: {
        'send': True,
        'message': 'pompa 1 off',
      }
    }
  },

  35: {
    "channel": "B",
    "status": 1,
    'name': 'pompa 2',
    'events': {
      0: {
        'send': True,
        'message': 'POMPA 2 ON',
      },
      1: {
        'send': True,
        'message': 'pompa 2 off',
      }
    }
  },

  33: {
    "channel": "C",
    "status": 1,
    'name': 'pompa 3',
    'events': {
      0: {
        'send': True,
        'message': 'POMPA 3 ON',
      },
      1: {
        'send': True,
        'message': 'pompa 3 off',
      }
    }
  },

  31: {
    "channel": "D",
    "status": 1,
    'name': 'livello 1',
    'events': {
      0: {
        'send': True,
        'message': 'RAGGIUNTO LIVELLO FIUME 1',
      },
      1: {
        'send': True,
        'message': 'livello fiume 1 off',
      }
    }
  },

  29: {
    "channel": "E",
    "status": 1,
    'name': 'livello 2',
    'events': {
      0: {
        'send': True,
        'message': 'RAGGIUNTO LIVELLO FIUME 2',
      },
      1: {
        'send': True,
        'message': 'livello fiume 2 off',
      }
    }
  },

  23: {
    "channel": "F",
    "status": 1,
    'name': 'livello 3',
    'events': {
      0: {
        'send': True,
        'message': 'RAGGIUNTO LIVELLO FIUME 3',
      },
      1: {
        'send': True,
        'message': 'livello fiume 3 off',
      }
    }
  },

  21: {
    "channel": "G",
    "status": 1,
    'name': 'livello 4',
    'events': {
      0: {
        'send': True,
        'message': 'RAGGIUNTO LIVELLO FIUME 4',
      },
      1: {
        'send': True,
        'message': 'livello fiume 4 off',
        }
    }
  },
}
