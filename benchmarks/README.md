# Sampa-Benchmarks

Which machine should I use? Well, it depends on what you are running. Here we collect results from specific structures to determine the best way to use our computational resources. The structures are:

1) Calcite + water, 337 atoms, self-consistent calculation (qe, pw)
2) Gold surface, 112 atoms, self-consistent calculation (qe, pw)

## Results

How many seconds/minutes/hours are needed to solve these calculations? Please include basic analysis of the data and a suggestion in case someone is running something similar.


### 1_calcite337

Benchmark input files and results by Prof. James Moraes de Almeida (Jul 2020).

| Machine                  | Cores/Boards  | PWSCF (CPU, s) | Cost Efficiency |
| -----------------------  |:-------------:|:--------------:| ---------------:|
| Tesla V100 SXM2 32GB GPU | 008           |     165        |    65.91 %      |
| ---                      | 004           |     255        |    76.35 %      |
| AMD Epyc 7532 (cpu)      | 128           |     348        |   100.00 %      |
| ---                      | 064           |     623        | **111.71 %**    |
| nanopetro-intel (cpu)    | 028           |     ---        |   ???.?? %      |
| nanopetro-amd   (cpu)    | 064           |    3137        |    19.86 %      |

**Observations**
- It was considered a price ratio (GPU/CPU) = 3.2 to estimate the cost efficiency;
- GPU/CPU price ratio has to go down to lower than 2.5 to favor GPUs over CPUs
- CPUs still present an advantage over GPUs considering price;
- For DFT, the best strategy is still scaling down CPU cores until max. performance;
- nanopetro nodes included as a reference.


### 2_ausurf112

This SCF calculation test was forked from [here](https://github.com/electronic-structure/benchmarks). Calculations were performed in May 2020 by @camilofs.

| Machine                 | Cores      | PWSCF (CPU, h) |    Efficiency  |
| ----------------------- |:----------:|:--------------:| --------------:|
| nanopetro-intel (cpu)   | 28         |     0.14244    |   100.00 %     |
| ---                     | 14         |     0.27366    |   104.11 %     |
| ---                     | 12         |     0.29512    | **112.62 %**   |
| ---                     | 08         |     0.37400    | **133.00 %**   |
| nanopetro-amd   (cpu)   | 64         |     0.36804    |   100.00 %     |
| ---                     | 32         |     0.65282    |   112.75 %     |
| ---                     | 16         |     1.26667    |   116.75 %     |
| ---                     | 08         |     2.01667    | **146.00 %**   |

**Observations**
- CPU time only; running quantum-espresso 6.4.0 & openmpi-3.1.4, Jul 2020. Efficiency estimated based on a full node allocation;
- nanopetro-amd --> AMD Opteron 6376; 
- nanopetro-intel -->  Intel Xeon Gold 5120;
- **Best options are highlighted**. In nanopetro-intel, use a combination of 12+8+8 cores (three jobs).
