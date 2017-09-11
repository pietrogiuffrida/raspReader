#!/usr/bin/env python3

logfilename = "reader.log"

channels = [
  {"name": "channel_a", "pin": 37, "status": 1},
  {"name": "channel_b", "pin": 35, "status": 1},
  {"name": "channel_c", "pin": 33, "status": 1},
  {"name": "channel_d", "pin": 31, "status": 1},
  {"name": "channel_e", "pin": 29, "status": 1},
  {"name": "channel_f", "pin": 23, "status": 1},
  {"name": "channel_g", "pin": 21, "status": 1},
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
