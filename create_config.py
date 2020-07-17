#!/usr/bin/env python3


import sys
sys.path.append("../tahoe0.7-dev")



from tahoe import Instance, Attribute
from tahoe.identity.config import InputConfig
from tahoe.identity import Identity

from loadconfig import get_identity_backend


import random 


_BACKEND = get_identity_backend()

Identity._backend = _BACKEND

data = Attribute('seconds_between_fetches', 500, _backend=_BACKEND)

obj = InputConfig(
                     plugin= "test secs bewteen fethces",
                     name= input("name: "),
                     typetag = "typetag-secs",
                     orgid="org--abc",
                     timezone="US/pacific",
                     data=data,
                     enabled=random.choice([True, True]),
                     _backend = _BACKEND
                  )



