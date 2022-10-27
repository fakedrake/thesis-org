Both examiners were impressed by the amount of work presented in the
thesis and by the level of technical detail that describes the
work. The quality of the technical work is good.


The current state of the thesis is not yet satisfactory. The thesis
contains many typos and needs an additional proof reading. In
addition, the thesis needs to improve in three main points:


- The thesis needs to better highlight the contributions made. The
  introduction chapter should explicitly list the main contributions
  made by the thesis and explain how it advances the knowledge in the
  field. *(in the beginning of every chapter contribution were made
  clear)*

  The introduction chapter would greatly benefit from an (possibly
  graphical) overview of the entire database system. Each technical
  chapter would greatly benefit from clarifying its individual
  contributions early on, and how it relates to the overall thesis.
  *(added at the end of the chapter)*

- The thesis needs a Related Work chapter that discusses related work
  (from industry and academia) and relates the work presented in the
  thesis critically to it. Areas that should be covered include: multi
  query optimizations (e.g., the work in Sellis, ACM TODS 1988),
  analytical query processing (e.g., as performed in factorized DBs in
  ACM PODS 2015 and in the PGM-based ACM PODS 2016 (best paper award),
  research related to the functional programming techniques used in
  the technical chapters. *see the end of Background chapter*

- The thesis needs an improved evaluation chapter. The evaluation
  chapter should be improved to include:

  - A comparison to performance results obtained for the same query
    workload using a standard open source DB, such as PostgreSQL. This
    is intended to put things in context. The committee understands
    that it is hard to create an even comparison field but an effort
    could be made using this DB without indexes and bounding available
    memory. *(sqlite IO metrics were added to all grpahs)*
  - A discussion of the overheads introduced, on what they depend on,
    and a clarification of the data-size independence of said
    overheads. Evaluation here could focus on experimenting with
    long-running queries where overheads such as compilation times
    represent a small percentage of overall query times. *(we were
    unable to make large enough data input that would make the 10s of
    seconds of compilation seem low)* # copy paste from the test. "More specifically this is the test from the thesis"
  - A characterization of the best- and worst-case scenarios for the
    presented technique, possibly using synthetic workloads, which
    allow control of possible data sharing among queries in the
    workload. *(a discussion of best and worst case scenario was added
    in the evaluation section)*
  - A sensitivity analysis of the impact of the memory budget –
    especially with respect to the role of the garbage collector (GC)
    and benefits the proposed system makes even when enough memory is
    available and no GC is needed. This will help bring to the fore
    and crystalize the benefits of the proposed system. *(One of the
    experiment covers this, it is highlighed in the text)*
  - A better description of the experimental setup, including a better
    justification for the various sizes used and a description of the
    used hardware *(The experimental setup was discussed in the
    evaluation section.)*


Some individual chapters, such as chapter 5, would benefit from
evaluations of the individual component discussed in the chapter. The
student is encouraged to include additional evaluations for them. *(It
was exceptionally hard to isolate the component in a useful scenario
so this particular point was left unadressed).*

(remember to do spellcheck)

Antisthenis is a system very tightly coupled with FluiDB, it can't be
trivially be isolated from the FluiDB context. In fact FluiDB depends
on antisthenis-dictated order of operations to ensure termination so
it's not trivial to replace Antisthenis in FluiDB without making
fundamental changes to FluiDB's workflow.


very embedded, timers dont make sense, in order to not compromize the
and in order tonot make sumething that maps to reality i didn't make:

- impact: measurement antisthenis in an isolated fashion changes FluiDB so much that it is a different system: the skew will.
- it cant be replaced


Spell check the thesis. many.
