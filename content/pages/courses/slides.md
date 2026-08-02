Title: Slides
Date: 2026-07-09
Description: Slide decks and embedded LaTeX Hands-On webcourse resources for mathematics and data science teaching.
URL: pages/courses/slides/
Save_as: pages/courses/slides/index.html

This page hosts course slide decks and external course material integrated into the site.

## Current decks

* MA1028: Mathematical Foundations (deck under development).
* MA1033: Análisis de Ecuaciones Diferenciales (deck under development).
* MA1034 / MA1035: Modeling sequence (starter deck below).
* MA2007B: Geometría y Topología para Ciencia de Datos (deck under development).

## LaTeX Hands-On webcourse

[Open LaTeX Hands-On in a new tab](https://alejandroucanpuc.github.io/Latex-Hands-On/)

If the embedded view does not load in your browser, use the direct link above.

<div class="ds-media-embed">
  <iframe
    src="https://alejandroucanpuc.github.io/Latex-Hands-On/"
    title="LaTeX Hands-On webcourse"
    class="ds-iframe-course"
    loading="lazy"
    referrerpolicy="no-referrer-when-downgrade">
  </iframe>
</div>

## Example deck

The deck below is a starter template that can be duplicated and adapted for each course.

<style>
@import url("https://cdn.jsdelivr.net/npm/reveal.js@5/dist/reveal.css");
@import url("https://cdn.jsdelivr.net/npm/reveal.js@5/dist/theme/white.css");
</style>

<div class="reveal ds-reveal-shell">
  <div class="slides">
    <section>
      <h2>Course overview</h2>
      <p>Use this deck for goals, grading, and timeline.</p>
    </section>
    <section>
      <h2>Key topics</h2>
      <p>Add the weekly modules or lecture blocks here.</p>
    </section>
    <section>
      <h2>Resources</h2>
      <p>Link notes, readings, and assignments from the class page.</p>
    </section>
  </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/reveal.js@5/dist/reveal.js"></script>
<script>
  window.addEventListener('load', function () {
    if (window.Reveal) {
      Reveal.initialize({
        hash: true,
        slideNumber: true,
        transition: 'slide'
      });
    }
  });
</script>