#!/usr/bin/python

import json
import datetime
from calendar import timegm
from faker import Factory
from faker.providers import internet,misc,person,address,date_time,user_agent

class player_session:
    fake = Factory.create()
    fake.add_provider(address)
    fake.add_provider(internet)
    fake.add_provider(misc)
    fake.add_provider(person)
    fake.add_provider(date_time)
    fake.add_provider(user_agent)

    session_events = []

    def __init__(self):
        self.games_list = ['Ggame', 'BullAttack', 'MasterOfMyDomain']
        self.events = ['attack', 'level up', 'level down', 'buy', 'open menu', 'use gems']
        self.buy_amount = 0
        self.gem_usage = 0
        self.ops_duration =0


    def SetEventDT(self):
        secs = self.fake.random_int(min=4, max=120)
        self.event_dt = self.event_dt + datetime.timedelta(seconds=secs)
        self.event_unix_ts = timegm(self.event_dt.timetuple())

    def SetEventName(self,isLast= False):
        if isLast==False:
            self.event_name = self.fake.random_element(elements=(self.events))
        else:
            self.event_name = 'logout'

    def SetEvent(self):
        event ={}
        event['user_id'] = self.user_id
        event['game_id'] = self.game_id
        event['event_name'] = self.event_name
        event['event_datetime'] = self.event_dt.strftime('%Y-%m-%d %H:%M:%S.000')
        event['event_ts'] = self.event_unix_ts
        event['ip'] = self.ip_addr
        event['user_agent'] = self.user_agent
        event['buy_amount'] = self.buy_amount
        event['gem_usage'] = self.gem_usage
        event['ops_duration'] = self.ops_duration
        return json.dumps(event)

     # value_when_true if condition else value_when_false
    def DoEvent(self,isLast= False):
        self.SetEventDT()
        self.SetEventName(isLast)
        self.buy_amount = self.fake.random_int(min=1, max=99) if self.event_name == 'buy' else 0
        self.gem_usage = self.fake.random_int(min=1, max=99) if self.event_name == "use gems" else 0
        self.ops_duration = self.fake.random_int(min=1, max=1000)


    def SetLoginEvent(self):
        self.session_events= []
        self.game_id = self.fake.random_element(elements=(self.games_list))
        self.user_id = self.fake.uuid4()
        self.event_dt = self.fake.date_time_between(start_date="-3d", end_date="now", tzinfo=None)
        self.event_unix_ts = timegm(self.event_dt.timetuple())
        self.event_name = 'login'
        self.ip_addr = self.fake.ipv4_public()
        self.user_agent = self.fake.user_agent()
        self.session_events.append(self.SetEvent())


    def CreateSession(self):
        num_of_event_per_session = self.fake.random_int(min=2, max=1000)
        self.SetLoginEvent()

        for x in range(0, num_of_event_per_session):
            self.DoEvent()
            self.session_events.append(self.SetEvent())

        self.DoEvent(True)
        self.session_events.append(self.SetEvent())





'''
ev1 = player_session()

for i in range(0,5):
    ev1.CreateSession()
    for e in ev1.session_events:
        print e
    print '######################################################################################'

'''