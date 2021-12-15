from Models.ams import AMS
from Models.negotiatoragent import NegotiatorAgent
from Models.supplierAgent import SupplierAgent
from Models.item import item
from Models.message import AgentMessage
import random

types = ['A','T']
places = ["LYN","TNG","PRS","COL","MDR","DUB","BRX","NYC","MNL"]


ams = AMS()

def generate_items(n):
    items = []
    for i in range(n):
        dep = random.choice(places)
        arrival = get_random_but_one(dep,places)
        t_type = random.choice(types)
        price_min = random.randrange(100,700)
        price_max = random.randrange(100,300) + price_min
        items.append(item(t_type,dep,arrival,price_max,price_min,"12/11"))
    return items


def generate_negotiators(n):
    n_agents = []
    for i in range(n):
        t_type = random.choice(types)
        dep = random.choice(places)
        arrival = get_random_but_one(dep,places)
        price_min = random.randrange(100,300)
        price_max = random.randrange(100,250) + price_min
        increase = random.uniform(0.1,0.25)
        n_agents.append(NegotiatorAgent(ams,"A"+str(i),t_type,dep,arrival,price_max,price_min,"12/11","12/11", increase=increase))
    return n_agents

def generate_suppliers(n,items):
    n_supp = []
    for i in range(n):
        nbr = random.randrange(len(items))
        tmp = random.sample(items,nbr)
        n_supp.append(SupplierAgent("S"+str(i),tmp,ams))
    return n_supp

def get_random_but_one(one,lst):
    choice = one
    while choice == one:
        choice = random.choice(lst)
    return choice


items = generate_items(100)
n_supp = generate_suppliers(7,items)
n_agents = generate_negotiators(20)
agents = n_agents + n_supp

# for i in range(100):
#     print("======================= Round : ", i, "==================================")
#     for agent in agents:
#         agent.run(ams)

# for agent in n_agents:
#     print(agent.item)

for agent in agents:
    agent.start()

