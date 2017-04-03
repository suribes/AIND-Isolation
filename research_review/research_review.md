---
output:
  pdf_document: default
  html_document: default
---

# 1. Deep Blue by the IBM Watson Team paper's goals

The objective is to describe how the Deep Blue computer chess system was developed and how it defeated Gary Kasparov in 1997. The main objective of the team was to build a world-class chess machine.

## 1.1 History

The efforts started at Carnegie Mellon University in the 1980s with ChipTEst and Deep Thought. Later part of the team moved to the IMB T.J. Watson Research center and Deep Thought II was developed.

Deep Blue I was based on a single-chip chess engine and lost against Gary Kasparov in 1996.

Deep Blue II was build with three major enhancements: First a new chess chip with a redesigned evaluation function. Second was to double the number of chess chips in the system and the use of a new SP computer that could support the new processing demands. And third was teh development of a set of visualization and debugging software tools.

## 1.2 System overview

* Deep Blue is a massive parallel system designed specififcally for carrying out chess game tree searches.
* The Chess chip is divided into three parts: the move generator, the evaluation function and the search control. It added extendability by using FPGA, which was never used.
* The same software search that was designed for Deep Thoutght II was used in Deep Blue. It used the following principles: Extend forcing/forced pairs of moves, forced moves are expectation dependent, fractional extensions, delayed extensions, dual credit and preserve the search envelope.
* The hardware search takes place on the chess chip and is fast, but relatively simple. The chess chips were limited to carry out only shallow searches in order to improve the efficiency and complexity of the software search.
* The parallel search uses a processor hierarchy, control distribution, parallelism at different levels and synchronization by nodes of type I and II.
* The evaluation function is the sum of various simple and complex features, which recognizes roughly 8000 patterns.
* The openings in the opening book where chosen to emphasize positions that Deep Blue played well and it was complemented by an extended book which summarizes the information avaliable at each position of a 700,000 game database.

# 2. Deep Blue by the IBM Watson Team's results.

The success of Deep Blue in defeating Gary Kasparov in 1997 was thanks to the large searching capability, non-uniform search, and complex evaluation function. Other factor like endgame databases, the extended book and evaluation function tuning prepared Deep Blue for the 1997 match.

There are still many areas where improvement could be made, but focusing on the strenghts of the system allowed the team to succesfully build Deep Blue.
