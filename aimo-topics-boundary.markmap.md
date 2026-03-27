---
markmap:
  colorFreezeLevel: 3
  duration: 500
  maxWidth: 300
  initialExpandLevel: 2
  spacingVertical: 20
  spacingHorizontal: 80
  paddingX: 8
  autoFit: true
  pan: true
  zoom: true
---
# AIMO 3: Math Topic Boundaries & Constraints
## 1. Problem Constraints (The "Rules")
### Format Constraints
- **Final Answer:** Must be an integer between `0` and `99999` (inclusive).
- **No Variations:** No decmials, no fractions, no algebraic expressions in the final answer.
- **Modulo:** Modulo operations will be explicitly stated if the true answer exceeds bounds.
- **Language:** Fully text-based with **LaTeX** formatting.
### Visual Constraints
- **NO Diagrams:** All geometry problems must be solved purely from text descriptions. 
### Difficulty Target
- **Floor:** National Olympiad Level (e.g., AIME, USAMO).
- **Ceiling:** International Mathematical Olympiad (IMO) standard.
- **Nature:** "AI Hard" - Requires multi-step genuine mathematical reasoning.

## 2. Included Subjects (The 4 Pillars)
### 2.1 Algebra
- **Polynomials:** Roots, Vieta's formulas, factor theorem, symmetric polynomials.
- **Inequalities:** AM-GM, Cauchy-Schwarz, Jensen's, rearrangement inequality (mostly restricted to integer bounds for the final answer).
- **Sequences & Series:** Arithmetic/geometric progressions, telescoping sums, recurrence relations.
- **Functional Equations:** Finding functions or values of functions given algebraic rules.
- **Complex Numbers:** Roots of unity, De Moivre's theorem (applied to algebra/geometry).
### 2.2 Combinatorics (Discrete Math)
- **Advanced Counting:** Permutations, combinations, stars & bars, principle of inclusion-exclusion (PIE).
- **Generating Functions:** Using polynomials/series to count configurations.
- **Pigeonhole Principle:** Formulating worst-case bounds.
- **Discrete Probability:** Only where answers map to integers/modulos (e.g. expected values, counting favorable outcomes).
- **Graph Theory & Game Theory:** Tournaments, coloring problems, invariants, monovariants (No diagrams, must map to integer answers).
### 2.3 Geometry (Text-Only)
- **Triangle/Circle Geometry:** Incenter, circumcenter, orthocenter, 9-point circle, Euler line.
- **Cyclic Quadrilaterals:** Ptolemy's theorem, inscribed angles, Power of a Point.
- **Transformations:** Homothety, inversion, rotation, translation.
- **Analytic/Trigonometric:** Law of sines/cosines, coordinate geometry, complex numbers in geometry.
- *Strict Rule:* Must practice translating purely verbal geometric constructions into abstract models/code.
### 2.4 Number Theory
- **Divisibility & Primes:** Prime factorization, greatest common divisor (GCD), Euclidean algorithm.
- **Modular Arithmetic:** Fermat's Little Theorem, Euler's Totient function, Chinese Remainder Theorem (CRT).
- **Diophantine Equations:** Pell's equation, Pythagorean triples, finding integer solutions to polynomial equations.
- **Advanced Tools:** Lifting the Exponent Lemma (LTE), order of an element modulo n.

## 3. STRICTLY OUT OF SCOPE (Avoid these when generating datasets!)
### Excluded Math Domains 🚫
- **Calculus:** Limits, Derivatives, Integration, Differential Equations (Not tested in IMO/AIME).
- **Advanced Linear Algebra:** Matrix transformations, eigenvalues/eigenvectors, vector spaces.
- **Abstract Algebra:** Group theory, Ring theory, Fields.
- **Continuous Statistics:** Normal distributions, standard deviations, t-tests, continuous random variables.
### Unusable Formats 🚫
- Problems requiring a diagram to understand the setup.
- Problems where the answer is negative, a fraction (like $3/4$), $\pi$, or an irrational number (like $\sqrt{2}$).
- *Note:* If the theoretical answer is $3/4$, the problem MUST ask for the answer under a modulo (e.g. $p \times q^{-1} \pmod{M}$) or ask for $p+q$. Don't generate raw fractional answers.