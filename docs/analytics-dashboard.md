# Analytics and Actionable Dashboards (GA4)

Measurement ID configured in site settings:

- `G-5HZK1LYQBX`

## What is tracked

### 1. Page performance

Custom events:

- `page_performance`: `load_ms`, `ttfb_ms`, `dom_interactive_ms`
- `web_vital_lcp`: `value_ms`
- `web_vital_cls`: `value`

Use these to monitor slow pages and prioritize template/content optimization.

### 2. Outbound clicks

Custom event:

- `outbound_click`

Key parameters:

- `outbound_type`: `github`, `orcid`, `seminar`, `other`
- `link_host`
- `link_url`
- `link_text`

### 3. Course engagement

Custom events:

- `course_page_view`
- `course_material_click`
- `course_scroll_depth` (50% and 90%)
- `course_engaged_session` (>= 45 seconds on course pages)

### 4. Goal events (recommended conversions)

Custom events:

- `contact_click`
- `repository_visit`
- `repository_outbound_click`
- `seminar_registration_click`

## Conversion setup in GA4

In GA4 Admin:

1. Go to **Admin -> Events** and confirm the events are arriving.
2. Go to **Admin -> Conversions**.
3. Mark these events as conversions:
   - `contact_click`
   - `repository_outbound_click`
   - `seminar_registration_click`

`repository_visit` is usually better as a funnel step than a conversion, but can be marked as conversion if desired.

## Recommended dashboard widgets

Create a GA4 dashboard (Reports snapshot or Explore) with these cards:

1. **Top pages by traffic and performance**
   - Metric: users, views
   - Breakdown: page path
   - Overlay metric: avg `load_ms` (from `page_performance` custom metric)

2. **Outbound clicks by destination type**
   - Event count for `outbound_click`
   - Breakdown: `outbound_type`
   - Secondary breakdown: `link_host`

3. **Course engagement funnel**
   - Steps:
     - `course_page_view`
     - `course_scroll_depth` (>= 50)
     - `course_material_click`

4. **Seminar registration funnel**
   - Steps:
     - page view on `/pages/seminar/`
     - `seminar_registration_click`

5. **Research narrative pathing**
   - Path exploration starting from `/pages/research/`
   - Check transitions to `/pages/research/projects/`, `/pages/research/publications/`, `/pages/seminar/`, `/pages/repositories/`

## Decision examples

- If `outbound_type=github` is high but `repository_outbound_click` is low on repository pages, improve repository card clarity and CTA language.
- If seminar page views are high but `seminar_registration_click` is low, move registration links upward and simplify session blocks.
- If course pages get views but low `course_material_click`, increase above-the-fold links to slides/materials.
- If `load_ms` and LCP worsen on specific pages, optimize images and embed loading strategies.
