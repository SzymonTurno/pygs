import pygs

# Diagram goes from top to bottom.
pygs.rankdir_tb()
pygs.fontname('Calibri')
# Attributes for Graphviz.
pygs.attribute('splines', 'ortho')
pygs.attribute('nodesep', '1')

# Define entity nodes.
e_csa = pygs.entity('Customer Service Assistant')
e_cust = pygs.entity('Customer')
e_brok = pygs.entity('Broker')
e_stock = pygs.entity('Third Party|Stock Exchange Center')

# Define process nodes.
# First argument is a reference process - used for numbering.
p_open = pygs.process(0, 'Open Account')
p_dep = pygs.process(0, 'Deposit Cash')
p_with = pygs.process(0, 'Withdraw Cash')
# False - process not on diagram, used only as a reference.
p_ref = pygs.process(0, '', False)
p_place = pygs.process(p_ref, 'Place Order')
p_check = pygs.process(p_ref, 'Check Transaction')

# Define data storage nodes.
d_cust = pygs.storage('D', 'Customer')
d_acnt = pygs.storage('D', 'Account')
d_taction = pygs.storage('D', 'Transaction')

# Define flows.
pygs.flow(e_csa, p_open, 'Customer details')
pygs.flow(p_open, d_cust, 'Customer details')
pygs.flow(p_open, d_acnt, 'Account details')
pygs.flow(e_brok, p_place, 'Order details')
pygs.flow(e_cust, p_place, 'Order details')
f_details = pygs.flow(p_place, e_stock, 'Transaction details')
pygs.fork(f_details, d_taction)
pygs.reverse_flow(d_taction, p_check, '')
pygs.reverse_flow(p_check, e_cust, 'Transaction history')
pygs.flow(e_cust, p_dep, 'Deposit amount')
pygs.flow(p_dep, d_acnt, 'Updated account balance')
pygs.flow(p_with, d_acnt, 'Updated account balance')
pygs.flow(e_cust, p_with, 'Withdraw amount', True)

print('@startuml dfd')
pygs.print_dfd('gane_sarson')
print('@enduml')
