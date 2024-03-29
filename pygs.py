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
        self.href = ''
        self.info = ''
        self.color = ''

class __flow:
    def __init__(self, leftstr, rightstr, desc, bothdir):
        self.leftstr = leftstr
        self.rightstr = rightstr
        self.desc = desc
        self.bothdir = bothdir
        self.reversed = False
        self.info = ''

__nodes = [__node(component.PROC, 1)]
__flows = []
__noutputs = 0
__ninputs = 0
__dirlr = False
__attrs = ''

def __get_fillcolor(node):
    if node.color is not '':
        return node.color
    if not node.hasinput and node.hasoutput:
        return 'lightgrey'
    if node.hasinput and not node.hasoutput:
        return 'lightblue'
    if node.hasinput and node.hasoutput:
        return 'lightsteelblue'
    if node.href is not '':
        return 'lightgreen'
    return 'white'

def __print_nodes(ids):
    global __nodes
    global __dirlr

    for id in ids:
        node = __nodes[id]
        if not node.visible:
            continue
        attrs = ''
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
        attrs = label + shape + style + fillcolor
        if node.href is not '':
            attrs += ' href=\"' + node.href + '\"'
        if node.info is not '':
            attrs += ' tooltip=\"' + node.info + '\"'
        print('    ' + 'node' + str(id) + '[' + attrs + '];')

def __arrow_attr(desc, info):
    if desc is '.':
        return '[shape=\"point\"]'
    if info is not '':
        info = ' tooltip=\"' + info + '\"'
    return '[label=\"' + desc + '\"' + info + ' shape=\"box\" color=\"white\" margin=0 height=0]'

def __print_flow_with_desc(name, flow):
    lefthead = '[dir=back]' if flow.reversed or flow.bothdir else '[arrowhead=none]'
    righthead = '[arrowhead=none]' if flow.reversed and not flow.bothdir else ''

    print('    ' + name + __arrow_attr(flow.desc, flow.info))
    print('    ' + flow.leftstr + '->' + name + lefthead + ';')
    print('    ' + name + '->' + flow.rightstr + righthead + ';')

def __print_flows(ids):
    global __flows

    for id in ids:
        flow = __flows[id]
        if flow.desc is not '':
            __print_flow_with_desc('flow' + str(id), flow)
        else:
            backstr = '[dir=back];' if flow.reversed else ';'
            print('    ' + flow.leftstr + '->' + flow.rightstr + backstr)

def __connect(left, right, bothdir):
    global __nodes

    __nodes[left].hasoutput = True
    __nodes[right].hasinput = True
    if bothdir:
        __nodes[left].hasinput = True
        __nodes[right].hasoutput = True

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
    flow = __flow('node' + str(left), 'node' + str(right), desc, bothdir)

    __connect(left, right, bothdir)
    __flows.append(flow)
    return len(__flows) - 1

def invisible_flow(left, right):
    global __flows
    flow = __flow('node' + str(left), 'node' + str(right) + '[style=\"invis\"]', '', False)

    __flows.append(flow)
    return len(__flows) - 1

def reverse_flow(left, right, desc, bothdir=False):
    global __flows
    flow = __flow('node' + str(right), 'node' + str(left), desc, bothdir)

    flow.reversed = True
    __connect(left, right, bothdir)
    __flows.append(flow)
    return len(__flows) - 1

def fork(flowid, right):
    global __flows
    flow = __flow('flow' + str(flowid), 'node' + str(right), '', False)

    if __flows[flowid].desc is '':
        __flows[flowid].desc = '.'
    __flows.append(flow)
    return len(__flows) - 1

def input(flowid, nodeid, reversed=False):
    global __flows
    global __ninputs
    left = 'node' + str(nodeid) if reversed else 'input' + str(__ninputs)
    right = 'input' + str(__ninputs) if reversed else 'node' + str(nodeid)
    flow = __flow(left, right, __flows[flowid].desc, False)

    flow.reversed = reversed
    flow.info = __flows[flowid].info
    __ninputs = __ninputs + 1
    __flows.append(flow)
    return len(__flows) - 1

def output(nodeid, flowid, reversed=False):
    global __flows
    global __noutputs
    left = 'output' + str(__noutputs) if reversed else 'node' + str(nodeid)
    right = 'node' + str(nodeid) if reversed else 'output' + str(__noutputs)
    flow = __flow(left, right, __flows[flowid].desc, False)

    flow.reversed = reversed
    flow.info = __flows[flowid].info
    __noutputs = __noutputs + 1
    __flows.append(flow)
    return len(__flows) - 1

def node_info(nodeid, info):
    global __nodes

    __nodes[nodeid].info = info

def flow_info(flowid, info):
    global __flows

    __flows[flowid].info = info

def node_color(nodeid, color):
    global __nodes

    __nodes[nodeid].color = color

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

def link(nodeid, href):
    __nodes[nodeid].href = href

def print_part(name, nodeids, flowids):
    global __dirlr

    print('digraph ' + name + ' {')
    if __dirlr:
        print('    rankdir=\"LR\";')
    else:
        print('    rankdir=\"TB\";')
    print(__attrs, end='')
    print('')
    for i in range(__noutputs):
        print('    output' + str(i) + '[style=invis];')
    for i in range(__ninputs):
        print('    input' + str(i) + '[style=invis];')
    print('')
    __print_nodes(nodeids)
    print('')
    __print_flows(flowids)
    print('}')

def print_full(name):
    global __nodes
    global __flows

    print_part(name, range(1, len(__nodes)), range(len(__flows)))
