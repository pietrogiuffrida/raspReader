#!/usr/bin/env python3

logfilename = "reader.log"

stati = {0: 'ON', 1: 'OFF'}

channels = [
  {"channel": "A", "pin": 37, "status": 1, 'name': 'pompa 1'},
  {"channel": "B", "pin": 35, "status": 1, 'name': 'pompa 2'},
  {"channel": "C", "pin": 33, "status": 1, 'name': 'pompa 3'},
  {"channel": "D", "pin": 31, "status": 1, 'name': 'livello 1'},
  {"channel": "E", "pin": 29, "status": 1, 'name': 'livello 2'},
  {"channel": "F", "pin": 23, "status": 1, 'name': 'livello 3'},
  {"channel": "G", "pin": 21, "status": 1, 'name': 'livello 4'},
]

delay = 2

mongo_error_message = "IMPOSSIBILE CONNETTERSI A MONGODB"
mongo_error_sbj = "IMPOSSIBILE CONNETTERSI A MONGODB"

messages = {

  37 : {
    0: {'send': True,
        'message': 'accensione 37',
        },
    1: {'send': True,
        'message': 'spegnimento 37',
        }
  },

  35 : {
    0: {'send': True,
        'message': 'accensione 35',
        },
    1: {'send': True,
        'message': 'spegnimento 35',
        }
  },

  33 : {
    0: {'send': True,
        'message': 'accensione 33',
        },
    1: {'send': True,
        'message': 'spegnimento 33',
        }
  },

  31 : {
    0: {'send': True,
        'message': 'accensione 31',
        },
    1: {'send': True,
        'message': 'spegnimento 31',
        }
  },

  29 : {
    0: {'send': True,
        'message': 'accensione 29',
        },
    1: {'send': True,
        'message': 'spegnimento 29',
        }
  },

  23 : {
    0: {'send': True,
        'message': 'accensione 23',
        },
    1: {'send': True,
        'message': 'spegnimento 23',
        }
  },

  21 : {
    0: {'send': True,
        'message': 'accensione 21',
        },
    1: {'send': True,
        'message': 'spegnimento 21',
        }
  },

}
