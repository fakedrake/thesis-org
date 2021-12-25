from collections import defaultdict
import re
import numpy as np
import matplotlib.pyplot as plt

test_block = """baseline {
./ssb-workload/query-indiv-22000-001.cpp
query:time:1639481778,reads:124736,writes:124864
./ssb-workload/query-indiv-22000-002.cpp
query:time:1639481786,reads:124736,writes:124864
./ssb-workload/query-indiv-22000-003.cpp
query:time:1639481794,reads:124736,writes:124864
./ssb-workload/query-indiv-22000-004.cpp
query:time:1639481803,reads:124736,writes:124864
./ssb-workload/query-indiv-22000-005.cpp
query:time:1639481816,reads:209312,writes:212704
./ssb-workload/query-indiv-22000-006.cpp
query:time:1639481829,reads:212928,writes:216352
./ssb-workload/query-indiv-22000-007.cpp
query:time:1639481842,reads:211296,writes:214432
./ssb-workload/query-indiv-22000-008.cpp
query:time:1639481855,reads:197888,writes:188096
./ssb-workload/query-indiv-22000-009.cpp
query:time:1639481868,reads:197888,writes:188096
./ssb-workload/query-indiv-22000-010.cpp
query:time:1639481881,reads:197888,writes:188096
./ssb-workload/query-indiv-22000-011.cpp
query:time:1639481894,reads:197888,writes:188096
./ssb-workload/query-indiv-22000-012.cpp
query:time:1639481910,reads:190784,writes:190944
}"""

def parse_size(line):
    """
    >>> parse_size("./ssb-workload/query-indiv-22000-001.cpp")
    22000
    """
    m = re.match(r"./ssb-workload/query-[a-z]*-(\d+)-\d+.cpp",line)
    if m is None: return None
    return int(m.group(1))

def parse_line(line):
    """
    >>> parse_line("query:time:1639481778,reads:124736,writes:124864")
    (124736, 124864)

    """
    m = re.match(r"query:time:\d+,reads:(\d+),writes:(\d+)",line)
    if m is None: return None
    return int(m.group(1)), int(m.group(2))

def parse_block_head(line):
    """
    >>> parse_block_head("baseline {")
    'baseline'
    """
    m = re.match(r"([a-z]+) {",line)
    if m is None: return None
    return m.group(1)

def parse_block_tail(line):
    """
    >>> parse_block_tail("}")
    True
    """
    return line == "}"

def parse_block(lines_i):
    """>>> parse_block(iter(test_block.split("\n")))

    ('baseline', 22000, [(124736, 124864), (124736, 124864), (124736,
    124864), (124736, 124864), (209312, 212704), (212928, 216352),
    (211296, 214432), (197888, 188096), (197888, 188096), (197888,
    188096), (197888, 188096), (190784, 190944)])

    """
    l = next(lines_i,None)
    if l is None: return None
    head = parse_block_head(l)
    if head is None: return None
    res = []
    size = -1
    while True:
        l = next(lines_i)
        if parse_block_tail(l):
            break
        size = parse_size(l)
        l = next(lines_i)
        x = parse_line(l)
        if l is None or size is None:
            raise RuntimeError("Bad line: '" + l + "'")

        res.append(x)

    return head,size,res

def parse_file_contents(lines):
    res = defaultdict(lambda:defaultdict(lambda:defaultdict(lambda:[])))
    while True:
        r = parse_block(lines)
        if r is None: return res
        h,s,io = r
        for r,w in io:
            res[s][h]['reads'].append(r)
            res[s][h]['writes'].append(w)
        res[s][h]['reads'] = np.array(res[s][h]['reads'])
        res[s][h]['writes'] = np.array(res[s][h]['writes'])
        res[s][h]['ops'] = res[s][h]['writes'] + res[s][h]['reads']

    return res

def parse_file(fname):
    with open(fname,'r') as f:
        return parse_file_contents((l.strip() for l in f))

def my_len(x):
    return len(x) if isinstance(x,list) else x.shape[0]

def make_plots(data, max_qs):
    """
    >>> make_plots(parse_file('io_perf.txt')[60000]).savefig('io_perf_60000.pdf')
    >>> make_plots(parse_file('io_perf.txt')[22000]).savefig('io_perf_22000.pdf')
    """
    SAMPLES = 30
    # create plot
    fig, ax = plt.subplots()
    index = np.arange(SAMPLES)
    bar_width = 0.5
    opacity = 0.8

    main_data = data['main']['ops']
    baseline_data0 = data['baseline']['ops']

    if isinstance(main_data,list):
        raise RuntimeError("Ooops main" + main_data)
    if isinstance(baseline_data0,list):
        raise RuntimeError("Ooops baseline" + baseline_data0)

    main_len = my_len(main_data)
    base_len = my_len(baseline_data0)
    baseline_data = np.tile(baseline_data0, (main_len // base_len + 1) )[:main_len]

    baseline = plt.bar(index, baseline_data, bar_width,
                       alpha=opacity,
                       color='orange',
                       label='Baseline')

    worklad = plt.bar(index + bar_width, main_data, bar_width,
                     alpha=opacity,
                     color='green',
                     label='Workload')

    plt.xlabel('SSB Query')
    plt.ylabel('# Page IO')
    plt.title('FluiDB performance on SSB TPC-H')
    plt.xticks(index + bar_width,
               ['%d' % (i % max_qs + 1) for i in range(SAMPLES)],
               fontsize='small')
    plt.legend()

    plt.tight_layout()
    return plt


def main():
    for size,max_qs in [(22000,13), (60000,13), (23000,13),(65000,13),(61000,13)]:
        pdf_file = 'io_perf_%d.pdf' % size
        print("building:",pdf_file)
        make_plots(parse_file('io_perf.txt')[size], max_qs).savefig(pdf_file)
