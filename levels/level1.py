from level0 import *

pygs.attribute('ordering', '')

e_up = pygs.entity('UP')
pygs.link(e_up, 'level0.svg')
pygs.node_info(e_up, 'Go to level 0')

e_error = pygs.entity('ERROR')
pygs.node_color(e_error, 'red')

p_place = pygs.process(p_ref, 'Place Order')
p_check = pygs.process(p_ref, 'Check Transaction')

d_taction = pygs.storage('D', 'Transaction')

nodes = [
    e_up,
    e_error,
    p_place,
    p_check,
    d_taction
]

f1_details = pygs.output(p_place, f0_details)
flows = [
    pygs.input(f0_brokdets, p_place),
    pygs.input(f0_custdets, p_place),
    pygs.reverse_flow(d_taction, p_check, ''),
    pygs.output(p_check, f0_history, True),
    pygs.fork(f1_details, d_taction),
    pygs.fork(f1_details, e_error)
]
flows.append(f1_details)

with open('level1.puml', 'w') as sys.stdout:
    print('@startuml level1')
    pygs.print_part('gane_sarson', nodes, flows)
    print('@enduml')
