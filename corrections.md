Both examiners were impressed by the amount of work presented in the
thesis and by the level of technical detail that describes the
work. The quality of the technical work is good.


The current state of the thesis is not yet satisfactory. The thesis
contains many typos and needs an additional proof reading. In
addition, the thesis needs to improve in three main points:


- The thesis needs to better highlight the contributions made. The
  introduction chapter should explicitly list the main contributions
  made by the thesis and explain how it advances the knowledge in the
  field.

  *in the beginning of every chapter contribution were made clear and
  on pdf page 36 the contributions of the thesis were also made clear.*

  The introduction chapter would greatly benefit from an (possibly
  graphical) overview of the entire database system. Each technical
  chapter would greatly benefit from clarifying its individual
  contributions early on, and how it relates to the overall thesis.

  *Added at pdf page 34.*

- The thesis needs a Related Work chapter that discusses related work
  (from industry and academia) and relates the work presented in the
  thesis critically to it. Areas that should be covered include: multi
  query optimizations (e.g., the work in Sellis, ACM TODS 1988),
  analytical query processing (e.g., as performed in factorized DBs in
  ACM PODS 2015 and in the PGM-based ACM PODS 2016 (best paper award),
  research related to the functional programming techniques used in
  the technical chapters.

  *A large section was added at the end of Background chapter at pdf
   page 59.*

- The thesis needs an improved evaluation chapter. The evaluation
  chapter should be improved to include:

  - A comparison to performance results obtained for the same query
    workload using a standard open source DB, such as PostgreSQL. This
    is intended to put things in context. The committee understands
    that it is hard to create an even comparison field but an effort
    could be made using this DB without indexes and bounding available
    memory.

    *sqlite3 IO metrics were added to all grpahs in the evaluation
    section.*

  - A discussion of the overheads introduced, on what they depend on,
    and a clarification of the data-size independence of said
    overheads. Evaluation here could focus on experimenting with
    long-running queries where overheads such as compilation times
    represent a small percentage of overall query times.

    *Discussion regarding the overheads was added to the evaluation
    chapter (pdf page 213)*


  - A characterization of the best- and worst-case scenarios for the
    presented technique, possibly using synthetic workloads, which
    allow control of possible data sharing among queries in the
    workload.

    *A section discussing of best and worst case scenario was added
    in the evaluation chapter (pdf page 211)*

  - A sensitivity analysis of the impact of the memory budget –
    especially with respect to the role of the garbage collector (GC)
    and benefits the proposed system makes even when enough memory is
    available and no GC is needed. This will help bring to the fore
    and crystalize the benefits of the proposed system.

    *Highlighed in the text in pdf page 209.*

  - A better description of the experimental setup, including a better
    justification for the various sizes used and a description of the
    used hardware

    *The experimental setup is now discussed in the evaluation
    section in pdf page 204.*


Some individual chapters, such as chapter 5, would benefit from
evaluations of the individual component discussed in the chapter. The
student is encouraged to include additional evaluations for them.

*Antisthenis is a system very deeply embedded in the operation of
FluiDB and the particular characteristics of the algorithm are
essential to avoid non-termination of the planning process. For that
reason it is not possible to replace it with a simpler algorithm for
comaprison. Timing the planning process itself, and especially
individual compponents of said process, falls beyond the scope of this
thesis as Antisthenis is not fine tuned for performant planning but
for producing performant plans and the numbers obtained would not be
useful.*

*Similarly, the HCntT-based logical framework was specifically
designed for FluiDB and and was not rigorously optimized internally.*
