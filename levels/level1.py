from level0 import *

e_up = pygs.entity('UP')
pygs.link(e_up, 'level0.svg')

p_place = pygs.process(p_ref, 'Place Order')
p_check = pygs.process(p_ref, 'Check Transaction')

d_taction = pygs.storage('D', 'Transaction')

nodes = [
    e_up,
    e_brok,
    e_stock,
    p_place,
    p_check,
    d_taction,
    e_cust
]

f_details = pygs.flow(p_place, e_stock, 'Transaction details')
flows = [
    pygs.flow(e_brok, p_place, 'Order details'),
    pygs.flow(e_cust, p_place, 'Order details'),
    pygs.reverse_flow(d_taction, p_check, ''),
    pygs.reverse_flow(p_check, e_cust, 'Transaction history'),
    pygs.fork(f_details, d_taction)
]
flows.append(f_details)

with open('level1.puml', 'w') as sys.stdout:
    print('@startuml level1')
    pygs.print_part('gane_sarson', nodes, flows)
    print('@enduml')
