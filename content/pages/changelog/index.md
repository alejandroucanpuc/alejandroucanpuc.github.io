Title: Site changelog
Date: 2026-07-16
Description: Versioned updates to site content, structure, and operations.
URL: pages/changelog/
Save_as: pages/changelog/index.html

This changelog tracks versioned updates to the site.

RSS updates feed (optional): [/feeds/updates.xml](/feeds/updates.xml)

## v1.4.0 - 2026-07-18 {#v140}

- Hardened production canonical URL defaults for GitHub Pages project-site deployments.
- Added `SITE_CANONICAL_URL` override support in CI via repository variables.
- Added CI fallback canonical URL calculation to reduce domain misconfiguration risk.
- Added fallback behavior to ORCID sync: retain existing generated research pages if external API sync fails.
- Added fallback behavior to GitHub sync: retain existing generated repositories page if external API sync fails.

## v1.3.0 - 2026-07-16 {#v130}

- Added a custom 404 page for GitHub Pages and direct deep links.
- Added automated generation for sitemap.xml and robots.txt after build.
- Added optional updates RSS feed generated from changelog entries.
- Added this versioned changelog page for operational tracking.
