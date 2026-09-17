Title: Chern–Simons Invariants and Complex Volume via Quandle Cohomology
Date: 2026-09-03
Description: Research project on reconstructing complex volume and Chern–Simons invariants via 4-fold symmetric quandle cohomology for hyperbolic 3-manifolds and boundary-parabolic representations.
URL: pages/research/csq-complexvolume/
Save_as: pages/research/csq-complexvolume/index.html

<div class="ds-layout-intro">
<div class="ds-card-grid">
<article class="ds-domain-card">
<span class="ds-card-meta">Project Acronym</span>
<h3>CSQ-ComplexVolume</h3>
<p>Reconstructing complex-volume invariants from quandle and 4-fold symmetric quandle cohomology.</p>
</article>
<article class="ds-domain-card">
<span class="ds-card-meta">Recommended Level</span>
<h3>Master's Thesis / Early PhD</h3>
<p>Suited for students with strong preparation in geometric topology, abstract algebra, and hyperbolic geometry.</p>
</article>
<article class="ds-domain-card">
<span class="ds-card-meta">Timeline &amp; Scope</span>
<h3>12–24 Months</h3>
<p>Two individually defensible thesis tracks converging on shared computational infrastructure and a joint paper.</p>
</article>
<article class="ds-domain-card">
<span class="ds-card-meta">Supervision</span>
<h3>Dr. Alejandro Ucan-Puc</h3>
<p>Tecnológico de Monterrey, Campus Monterrey (Department of Mathematics &amp; Data Science).</p>
</article>
</div>
</div>

## Executive Summary

For an oriented hyperbolic 3-manifold $M$, the **hyperbolic volume** $\operatorname{Vol}(M)$ and the **Chern–Simons invariant** $\operatorname{CS}(M)$ combine into a complex-volume-type invariant. Hyperbolic volume has been interpreted as a quandle cocycle invariant for hyperbolic knots (Inoue & Kabaya 2008, 2014), while constructions on 4-fold symmetric quandles reformulate the Chern–Simons invariant of closed 3-manifolds through quandle cocycles (Hatakenaka & Nosaka 2012, Nosaka 2011).

**The central objective of this project is to build an explicit, convention-fixed, and computationally validated bridge between quandle cohomology and complex volume.** Specifically, the project targets cusped 3-manifolds and boundary-parabolic $\operatorname{PSL}(2,\mathbb{C})$-representations, comparing quandle pairings directly with Zickert's simplicial formulas and the extended Bloch group.

<div class="ds-cta-box">
<strong>Working Target:</strong> Given an oriented compact tame 3-manifold $M$ and a boundary-parabolic representation $\rho: \pi_1(M) \to \operatorname{PSL}(2,\mathbb{C})$, construct a quandle-theoretic invariant $I_Q(M,\rho)$ satisfying:
<p style="text-align: center; margin: 0.8rem 0; font-size: 1.15rem;">
$$I_Q(M,\rho) \equiv \operatorname{CV}(M,\rho) \pmod{\Lambda}$$
</p>
where $\operatorname{CV}(M,\rho)$ denotes a fixed normalization of complex volume (such as Zickert's simplicial regulator) and $\Lambda$ is its period lattice (e.g. $\pi^2\mathbb{Z}$ or $2\pi^2\mathbb{Z}$).
</div>

---

## Aims and Objectives

### Primary Aim

Construct an explicit complex-valued quandle or symmetric quandle cocycle pairing whose evaluation on shadow colorings recovers both hyperbolic volume and the Chern–Simons contribution for hyperbolic knot complements and their Dehn fillings.

### Secondary Objectives

1. **Connect Diagrammatic and Geometric Invariants:** Bridge diagrammatic knot invariants, quandle cohomology, ideal triangulations, and secondary characteristic classes of hyperbolic 3-manifolds.
2. **Computable Realization:** Provide an explicit algebraic-topological realization of secondary classes that can be computed algorithmically from knot diagrams and triangulations.
3. **Link with the Extended Bloch Group:** Connect quandle homology directly to the extended Bloch group $\mathcal{B}_{\mathrm{PSL}_2}(\mathbb{C})$ and the Cheeger–Chern–Simons regulator class.
4. **Extend Beyond Geometric Representations:** Investigate boundary-parabolic $\operatorname{PSL}(2,\mathbb{C})$-representations near the geometric component in character varieties.
5. **Foundations for Higher Structures:** Lay groundwork for future research on higher-dimensional hyperbolic volume cocycles, higher-rank representation invariants, and complex Kleinian groups.

---

## Research Questions

| ID | Question | Track Lead |
| :--- | :--------- | :----------- |
| **RQ1** | Which quandle structure best encodes boundary-parabolic $\operatorname{PSL}(2,\mathbb{C})$-representations? | Joint |
| **RQ2** | Can one define an explicit complex-valued quandle cocycle? | Tracks A & B |
| **RQ3** | How does the quandle cocycle evaluation compare with the extended Bloch-group element and Cheeger–Chern–Simons regulator associated with a representation? | Tracks A & B |
| **RQ4** | What are the precise period lattice $\Lambda$, orientation conventions, lifting choices, and branch cuts needed for a well-defined comparison theorem? | Joint (Phase 1) |
| **RQ5** | Does the complex quandle invariant distinguish manifolds or representations with equal hyperbolic volume but distinct Chern–Simons data? | Joint |
| **RQ6** | How does the invariant behave under Dehn filling, orientation reversal, complex conjugation of representations, and mutation? | Student Track B |

---

## Theoretical Hypotheses

<div class="ds-card-grid">
<article class="ds-domain-card">
<span class="ds-card-meta">Hypothesis 1</span>
<h3>Chern–Simons via Symmetric Quandles</h3>
<p>For a suitably chosen 4-fold symmetric quandle and cocycle representative, the quandle cocycle pairing reproduces a fixed normalization of the Chern–Simons invariant of a closed hyperbolic 3-manifold modulo the correct period lattice.</p>
</article>

<article class="ds-domain-card">
<span class="ds-card-meta">Hypothesis 2</span>
<h3>Unified Complex Cocycle</h3>
<p>A compatible extension of the Inoue–Kabaya volume cocycle and a symmetric-quandle Chern–Simons cocycle can be packaged into a complex-valued cocycle pairing representing complex volume.</p>
</article>

<article class="ds-domain-card">
<span class="ds-card-meta">Hypothesis 3</span>
<h3>Discriminating Power</h3>
<p>The complex-valued quandle invariant contains strictly more topological information than hyperbolic volume alone, separating pairs of representations with identical volumes but distinct Chern–Simons values.</p>
</article>

<article class="ds-domain-card">
<span class="ds-card-meta">Hypothesis 4</span>
<h3>Simplicial Comparison</h3>
<p>For boundary-parabolic representations, the quandle construction maps chain-wise to Zickert's decorated ideal triangulation complex and extended Bloch-group regulator under explicit flattening hypotheses.</p>
</article>
</div>

---

## Computational Benchmark Suite

The theoretical constructions are validated against reference calculations on curated hyperbolic families:

1. **Figure-Eight Knot Complement ($4_1$):** Standard initial testbed with well-documented volume $\operatorname{Vol}(4_1) \approx 2.0298832128$ and vanishing Chern–Simons invariant.
2. **Twist Knot Complements ($5_2, 6_1, \dots$):** Systematic family with accessible Wirtinger presentations and non-trivial Chern–Simons values.
3. **Two-Bridge Knots and Links:** Support explicit $\operatorname{PSL}(2,\mathbb{C})$-character variety descriptions and manageable shadow colorings.
4. **Dehn Surgeries:** Hyperbolic manifolds obtained by $(p,q)$-surgery, bridging cusped and closed computations.
5. **Equal-Volume / Distinct-CS Pairs:** Explicit pairs used to test whether the complex quandle pairing discriminates topological information invisible to volume alone.

---

## Expected Outcomes and Publication Plan

### Ladder of Project Outcomes

- **Minimum Viable Outcome (Month 8):** Verified, reproducible computational implementation of Inoue–Kabaya (2014) and Hatakenaka–Nosaka (2012) algorithms, alongside a complete convention concordance.
- **Target Outcome (Month 24):** Explicit comparison theorems for both cusped and closed families, pinned-down period lattices, proof of discriminating power, and three submitted papers.
- **Stretch Outcome:** General comparison theorem extending beyond named knot families without case-by-case re-proof, and analysis of non-geometric boundary-parabolic representations.
- **Negative-but-Publishable Outcome:** Rigorous obstruction proof demonstrating why ordinary quandle cohomology cannot encode the full Chern–Simons invariant without decorated/extended structures.

### Publication Strategy

| Paper | Lead Authors | Target Content | Candidate Venues |
| :------ | :------------- | :--------------- | :----------------- |
| **Paper 1** | Track A Lead | Explicit quandle-cocycle comparison theorem for complex volume of boundary-parabolic representations (twist-knot family) | *J. Knot Theory Ramifications*, *Topology Appl.* |
| **Paper 2** | Track B Lead | Explicit 4-fold symmetric quandle Chern–Simons formula for closed manifolds and the Dehn-filling bridge | *J. Knot Theory Ramifications*, *Topology Appl.* |
| **Paper 3** | Joint | Computational framework, benchmark dataset, high-precision dilogarithm tracking, and distinguishing-power results | *Experimental Mathematics*, *J. Appl. Comput. Topology* |

---

## Contact and Inquiries

Interested graduate students (prospective master's or PhD candidates) and researchers interested in collaborating on quandle cohomology, geometric topology, or computational invariants are encouraged to get in touch.

<div class="ds-cta-box">
<h3 style="margin-top: 0;">Project Supervision and Contact</h3>
<p><strong>Dr. Alejandro Ucan-Puc</strong><br>
Department of Science, Tecnológico de Monterrey (Campus Monterrey)<br>
Office: A7-222</p>
<ul class="ds-reference-list">
<li>Email: <a href="mailto:alejandro.ucan-puc@tec.mx?subject=CSQ-ComplexVolume%20Project%20Inquiry">alejandro.ucan-puc@tec.mx</a></li>
<li>ORCID: <a href="https://orcid.org/0000-0002-0037-9394">0000-0002-0037-9394</a></li>
<li>Institutional Profile: <a href="https://research.tec.mx/vivo-tec/display/PID_318207">research.tec.mx (PID 318207)</a></li>
<li>General Contact Page: <a href="/pages/contact/">Contact Alejandro Ucan-Puc</a></li>
</ul>
<p style="margin-bottom: 0;">When inquiring about student positions, please mention your background in topology, abstract algebra, and any programming experience in Python/SageMath.</p>
</div>

---

## Related Content

<div class="ds-related-module">
<p>Explore related research hubs, publications, and activities:</p>
<ul class="ds-reference-list">
<li><a href="/pages/research/projects/">Research Projects Portfolio</a></li>
<li><a href="/pages/research/">Research Hub</a></li>
<li><a href="/pages/research/publications/">Selected Publications</a></li>
<li><a href="/pages/seminar/">Undergraduate Seminar</a></li>
<li><a href="/pages/repositories/">GitHub Repositories and Code</a></li>
</ul>
</div>
