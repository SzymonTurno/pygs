import sys
sys.path.insert(1, '../')
import pygs

pygs.rankdir_tb()
pygs.fontname('Calibri')
pygs.attribute('splines', 'ortho')
pygs.attribute('nodesep', '1')
pygs.attribute('ordering', 'out')

e_csa = pygs.entity('Customer Service Assistant')
e_cust = pygs.entity('Customer')
e_stock = pygs.entity('Third Party|Stock Exchange Center')
e_brok = pygs.entity('Broker')

p_open = pygs.process(0, 'Open Account')
p_dep = pygs.process(0, 'Deposit Cash')
p_with = pygs.process(0, 'Withdraw Cash')
p_ref = pygs.process(0, 'Place order')
pygs.link(p_ref, 'level1.svg')

d_cust = pygs.storage('D', 'Customer')
d_acnt = pygs.storage('D', 'Account')

pygs.flow(e_csa, p_open, 'Customer details')
pygs.flow(p_open, d_cust, 'Customer details')
pygs.flow(p_open, d_acnt, 'Account details')
pygs.flow(e_cust, p_dep, 'Deposit amount')
pygs.flow(p_dep, d_acnt, 'Updated account balance')
pygs.flow(p_with, d_acnt, 'Updated account balance')
pygs.flow(e_cust, p_with, 'Withdraw amount', True)
pygs.flow(e_cust, p_ref, '', True)
pygs.flow(e_brok, p_ref, '')
pygs.flow(p_ref, e_stock, '')

with open('level0.puml', 'w') as sys.stdout:
    print('@startuml level0')
    pygs.print_full('gane_sarson')
    print('@enduml')
