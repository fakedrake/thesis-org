#!/usr/bin/env python

import itertools as it
from typing import *

import pandas as pd
import matplotlib.pyplot as plt

class Line(object):
    def __init__(self, txt, num):
        self.txt = txt.strip()
        self.num = num

    def is_cpp_path(self) -> bool:
        return self.txt.endswith(".cpp")

    def get_begin(self) -> Optional[Tuple[str, str]]:
        if self.txt == "":
            return None

        try:
            ty, budget, _bracket = self.txt.split()
        except ValueError:
            raise self.into_error()

        if ty == "main":
            return ("Workload", budget)
        elif ty == "baseline":
            return ("Baseline", budget)
        else:
            return None

    def is_workload_end(self) -> bool:
        return self.txt.startswith("}")

    def parse(self) -> (int, int):
        line = self.txt
        try:
            _q, _t, time, _r, read_s, _w, write_s = \
                it.chain(*[i.split(',') for i in line.split(':')])
        except ValueError:
            raise self.into_error()

        assert _r == "reads" and _w == "writes"
        return int(read_s), int(write_s)

    def into_error(self):
        return ValueError(repr(self))

    def __repr__(self):
        return f"Line({self.num}, {self.txt})"


class Workload(object):
    def __init__(self, wl_type: str, budget: str, queries: List[Tuple[int, int]]):
        self.wl_type = wl_type
        self.budget = budget
        self.queries = queries

    def __repr__(self):
        return f"Workload({self.wl_type}, {self.budget}, {self.queries})"

    def ops(self, repeat_till: int) -> Iterable[int]:
        return list(it.islice(it.cycle((r + w for r, w in self.queries)), repeat_till))

    def __len__(self):
        return len(self.queries)

class LineIter(object):
    def __init__(self, path):
        self.it = (Line(l,i) for i,l in enumerate(open(path, 'r')))

    def parse_workload(self) -> Workload:
        """Get the reads and writes of each iteration."""

        try:
            l = next(self.it)
        except StopIteration:
            return

        beg = l.get_begin()
        assert beg, f"Not the beginning of body: {l}"
        wl_type, budget = beg

        try:
            l = next(self.it)
        except StopIteration:
            return

        fr = []
        while not l.is_workload_end():
            if not l.is_cpp_path():
                fr.append(l.parse())

    if ty == 'bar':
        plt.bar(index, baseline_data, bar_width,
                alpha=opacity,
                color='orange',
                label='Isolated Query FluiDB')

        plt.bar(index + bar_width, main_data, bar_width,
                color='green',
                label='FluiDB')
    elif ty == 'cum':
        x_base = np.arange(len(baseline_data))
        x_main = np.arange(len(main_data))
        plt.plot(x_base,
                 cum(baseline_data),
                 color='orange',
                 label='Isolated Query FluiDB')

        plt.plot(x_main,
                 cum(main_data),
                 alpha=opacity,
                 color='green',
                 label='FluiDB')
    else:
        raise RuntimeError("The ty arg must be 'cum' or 'bar'")


    ax.yaxis.set_major_formatter(lambda x,pos: f"{int(x/1000)}K")
    plt.xlabel('SSB Query')
    plt.ylabel('# Page IO')
    plt.title(f'FluiDB performance on SSB TPC-H ({int(pages / 10)}K  pages)')
    plt.xticks(index + bar_width,
               ['%d' % (i % max_qs + 1) for i in range(SAMPLES)],
               fontsize='small')
    plt.legend()
    plt.tight_layout()
    return plt

    wls = list(wls)
    data_len = max(map(len, wls))
    d = defaultdict(lambda: pd.DataFrame())
    for w in wls:
        d[w.budget][w.wl_type] = w.ops(data_len)

    return d

def plot(budget: str,
         plt_data: pd.DataFrame,
         logarithmic: bool = False,
         max_qs: int = 13,
         with_sqlite: pd.DataFrame = None) -> str:

    from matplotlib.ticker import EngFormatter

    ax = plt_data.plot(
        kind='bar',
        width=.8,
        ylabel='# Page IO',
        xlabel='SSB-TPC-H Query',
        logy=logarithmic,
        title=f'FluiDB SSB-TPCH performance\n(page budget: {budget})')

    if with_sqlite is not None:
        ax.plot(with_sqlite['sqlite'], '--g', label='sqlite')
        ax.legend()

    # ax.yaxis.get_major_formatter().set_scientific(False)
    ax.yaxis.set_major_formatter(EngFormatter())
    ax.set_xticklabels(['%d' % (i % max_qs + 1) for i in range(len(plt_data))])


    fig = ax.get_figure()

    pdf_path = f'/tmp/workload_{budget}%s.pdf' % ("log" if logarithmic else "")
    fig.savefig(pdf_path)
    return pdf_path


# WL_PATH = "ssb-workload/op_perf_prev.txt"
WL_PATH = "ssb-workload/io_perf.txt"
SQLITE_DF = pd.DataFrame({"sqlite": it.islice(
    it.cycle([
        440434,
        440434,
        440434,
        458973,
        458973,
        458973,
        443652,
        443652,
        443652,
        443652,
        462008,
        462008,
        462008,
    ]),
    30)})


BUDGETS = [
    "2200K",
    "6000K",
    "2300K",
    "6100K",
    "6500K",
]

def main():
    df = dataframe(LineIter(WL_PATH).workloads())
    for b in BUDGETS:
        print(f"Plotting: {b}")
        print(plot(b, df[b], logarithmic=True, with_sqlite=SQLITE_DF))
        print(plot(b, df[b], logarithmic=False, with_sqlite=SQLITE_DF))

    print("Plotting bad joins")
    print(plot("1700K", df["1700K"], logarithmic=False))
