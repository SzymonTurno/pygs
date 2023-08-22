from enum import Enum as __Enum

class component(__Enum):
    ENTI = 0
    PROC = 1
    STORE = 2

class __node:
    def __init__(self, component, nprocs=0):
        self.component = component
        self.id = ''
        self.label = ''
        self.hasinput = False
        self.hasoutput = False
        self.nprocs = nprocs
        self.visible = True

class __flow:
    def __init__(self, left, right, desc, bothdir):
        self.left = left
        self.right = right
        self.desc = desc
        self.bothdir = bothdir
        self.reversed = False

__nodes = [__node(component.PROC, 1)]
__flows = []
__dirlr = False
__attrs = ''

def __dcl_str(i, attrs):
    return 'node' + str(i) + '[' + attrs + '];'

def __get_fillcolor(node):
    if not node.hasinput and node.hasoutput:
        return 'lightgrey'
    if node.hasinput and not node.hasoutput:
        return 'lightblue'
    if node.hasinput and node.hasoutput:
        return 'lightsteelblue'
    return 'white'

def __print_nodes():
    global __nodes
    global __dirlr
    i = 0

    for node in __nodes[1:]:
        i += 1
        if not node.visible:
            continue
        label = node.label if __dirlr else '{' + node.label + '}'
        shape = 'Mrecord' if node.component is component.PROC else 'record'
        style = 'solid'
        fillcolor = ''

        if node.component is component.ENTI:
            style = 'filled'
            fillcolor = ' fillcolor=\"' + __get_fillcolor(node) + '\"'
        label = 'label=\"' + label + '\"'
        shape = ' shape=\"' + shape + '\"'
        style = ' style=\"' + style + '\"'
        print('    ' + __dcl_str(i, label + shape + style + fillcolor))

def __arrow_attr(desc):
    tmp = '[label=\"' + desc

    return tmp + '\" shape=\"box\" color=\"white\" margin=0 height=0]'

def __print_flow_with_desc(name, flow):
    leftstr = 'node' + str(flow.right if flow.reversed else flow.left)
    rightstr = 'node' + str(flow.left if flow.reversed else flow.right)
    lefthead = '[dir=back]' if flow.reversed or flow.bothdir else '[arrowhead=none]'
    righthead = '[arrowhead=none]' if flow.reversed and not flow.bothdir else ''

    print('    ' + name + __arrow_attr(flow.desc))
    print('    ' + leftstr + '->' + name + lefthead + ';')
    print('    ' + name + '->' + rightstr + righthead + ';')

def __print_flows():
    global __flows
    i = 0

    for flow in __flows:
        if flow.desc is not '':
            __print_flow_with_desc('lab'+str(i), flow)
            i += 1
        else:
            leftstr = 'node' + str(flow.right if flow.reversed else flow.left)
            rightstr = 'node' + str(flow.left if flow.reversed else flow.right)
            backstr = '[dir=back];' if flow.reversed else ';'

            print('    ' + leftstr + '->' + rightstr + backstr)

def entity(desc):
    global __nodes
    node = __node(component.ENTI)

    node.label = desc
    __nodes.append(node)
    return len(__nodes) - 1

def process(procid, desc, visible=True):
    global __nodes
    node = __node(component.PROC)

    node.id = __nodes[procid].id + '.' + str(__nodes[procid].nprocs)
    node.label = node.id[1:] + '|' + desc + '\\n\\n'
    node.visible = visible
    __nodes[procid].nprocs += 1
    __nodes.append(node)
    return len(__nodes) - 1

def storage(categ, desc):
    global __nodes
    node = __node(component.STORE)

    __nodes.append(node)
    node.label = '{' + categ + '|{' + desc + '}}'
    return len(__nodes) - 1

def flow(left, right, desc, bothdir=False):
    global __flows
    global __nodes
    flow = __flow(left, right, desc, bothdir)

    __nodes[left].hasoutput = True
    __nodes[right].hasinput = True
    if bothdir:
        __nodes[left].hasinput = True
        __nodes[right].hasoutput = True
    __flows.append(flow)

def reverse_flow(left, right, desc, bothdir=False):
    global __flows

    flow(left, right, desc, bothdir)
    __flows[-1].reversed = True

def rankdir_lr():
    global __dirlr

    __dirlr = True

def rankdir_tb():
    global __dirlr

    __dirlr = False

def attribute(name, val):
    global __attrs

    __attrs = __attrs + '    ' + name + '=\"' + val + '\"' + ';\n'

def fontname(name):
    global __attrs

    __attrs = __attrs + '    node[fontname=\"' + name + '\"];\n'

def print_dfd(name):
    global __dirlr

    print('digraph ' + name + ' {')
    if __dirlr:
        print('    rankdir=\"LR\";')
    else:
        print('    rankdir=\"TB\";')
    print(__attrs, end='')
    print('')
    __print_nodes()
    print('')
    __print_flows()
    print('}')
