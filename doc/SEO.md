# SEO Action Plan - ParseWiz

> Last updated: 2026-02-10

## Current Status: SEO Technical 100% ✅ | Distribution Pending

---

## What's Implemented

### SEO Technical ✅
- Meta tags (title, description, OG, Twitter Card)
- OG image (1200x630px)
- Keywords for global data conversion niche
- robots.txt and sitemap.xml
- Schema.org (WebApplication)
- PWA manifest
- Security headers (CSP, X-Content-Type-Options, X-Frame-Options)
- FAQ section (helps with question-based queries)
- "Features" section highlighting 3 key differentiators
- "How It Works" section (3-step visual guide)

### Domain Configuration ✅
- Canonical URL: `https://www.parsewiz.app/`
- Redirect 301: `parsewiz.app` → `www.parsewiz.app`
- DNS: `www.parsewiz.app` CNAME → Railway

### Search Engine Registration ✅

| Platform | Status |
|----------|--------|
| Google Search Console | Indexed, sitemap submitted |
| Bing Webmaster Tools | Sitemap submitted (imported from GSC) |

---

## Distribution Plan (February 2026) — TOP PRIORITY

> SEO technical is complete. The bottleneck is distribution: getting ParseWiz in front of real users. See `doc/DISTRIBUTION.md` for the reusable launch guide and `doc/tasks/todo.md` for the detailed task plan.

### Strategy

1. **Software directories** — Quality backlinks + direct traffic
2. **Tech communities** — Target audience visibility + backlinks
3. **Developer communities** — Data analysts, developers, API users
4. **SEO content (blog)** — Long-tail organic traffic

### Software Directories

| Platform | URL | Priority | Status |
|----------|-----|----------|--------|
| Product Hunt | https://producthunt.com | High | [ ] Pending |
| Hacker News | https://news.ycombinator.com | High | [ ] Pending |
| Peerlist | https://peerlist.io | Medium | [ ] Pending |
| DevHunt | https://devhunt.org | Medium | [ ] Pending |
| Indie Hackers | https://indiehackers.com | Medium | [ ] Pending |
| BetaList | https://betalist.com | Low | [ ] Pending |

**Competitors to reference in AlternativeTo:** ConvertCSV.com, JSON-CSV.com, TableConvert

**Warning:** AlternativeTo rejects simple converters/viewers/formatters. Skip this platform — see `doc/DISTRIBUTION.md` for details.

**Key message:** "Free online tool to convert JSON, CSV, and Excel files with live preview, error fixing, and complex nested JSON handling. No signup, no file uploads to servers."

### Developer & Data Communities

| Channel | Focus | Status |
|---------|-------|--------|
| Reddit r/excel | Data conversion tool for analysts | [ ] Pending |
| Reddit r/sql | CSV to SQL tool (after Phase 2) | [ ] Pending |
| Reddit r/webdev | API response to CSV | [ ] Pending |
| Reddit r/SideProject | Show what you built | [ ] Pending |
| Dev.to | Technical article on nested JSON handling | [ ] Pending |
| LinkedIn | Data analyst pain points, tool announcement | [ ] Pending |
| Twitter/X | #DataAnalytics, #Excel, developer tool | [ ] Pending |

**Tone:** Don't sell. Share genuinely: "I built a free tool to convert JSON/CSV/Excel files instantly in the browser. No signup, no file uploads to servers. Useful when you get data exports in the wrong format."

---

## SEO Content (Blog)

**Impact:** High | **Effort:** Medium
**Format:** Static HTML pages in `frontend/` (no CMS)

### Planned Articles

| # | Title | Target Keywords | Priority |
|---|-------|-----------------|----------|
| 1 | "How to Convert API Response JSON to CSV" | "api response to csv", "convert json api to csv" | High |
| 2 | "How to Generate SQL INSERT Statements from Excel" | "excel to sql insert", "csv to sql generator" | High |
| 3 | "5 Ways to Handle Nested JSON Data" | "nested json to csv", "flatten json online" | Medium |
| 4 | "Fix JSON Syntax Errors Online — No Install Required" | "fix json online", "json syntax error" | Medium |

### Requirements per Article
- Schema.org type `Article` with `datePublished` and `dateModified`
- Meta tags OG and Twitter Card
- Internal links to the app and between articles
- Clear CTA towards ParseWiz
- Update `sitemap.xml` with each new URL

**Note:** Blog is deprioritized until SQL generator is built. Articles 1 and 2 should coincide with Phase 2 launch.

---

## Keyword Strategy

### Competition Analysis

| Category | Keywords | Competition | Strategy |
|----------|----------|-------------|----------|
| Avoid | "json to csv converter", "csv to json online", "excel to csv" | High — ConvertCSV, CSVJSON, CodeBeautify | Don't target directly |
| Medium Opportunity | "nested json to csv", "flatten json to csv online", "complex json to csv" | Medium | Target via features + FAQ |
| Best Opportunity | "csv to sql insert statements", "excel to sql generator online" | Low | Build SQL Generator (Phase 2) |
| Long-Tail | Problem-based queries (see below) | Low | Content marketing / blog |

### Long-Tail Keywords (Content Opportunities)

| Keyword | Intent | Content Type |
|---------|--------|--------------|
| "how to convert API response to CSV" | Developer with API data | Blog post + tool demo |
| "flatten hierarchical JSON for Excel" | Analyst with nested data | Tutorial |
| "export Postman collection to spreadsheet" | API tester | Blog post |
| "convert MongoDB export to CSV" | Database admin | Tutorial |
| "json with arrays to excel" | User with complex JSON | FAQ section |
| "fix json syntax errors online" | User with broken JSON | Highlight raw editor |

### Strategic Recommendation

**Prioritize Phase 2 (SQL Generator) over completing Phase 1.**

Rationale:
- The "Excel/CSV to SQL" niche has less competition than JSON/CSV converters
- Developers who need SQL generation are more likely to share/recommend tools
- It creates a genuine differentiator vs. existing converter tools

---

## Key Differentiators

These features set ParseWiz apart from competitors:

| Feature | What It Does | Why It Matters |
|---------|--------------|----------------|
| **Online JSON Error Fixing** | Inline editor with line numbers and error message. Fix and retry. | Competitors show "Parse Error" and fail. |
| **Table-View Preview** | See data in real table format before downloading. | Other tools convert blindly. |
| **Smart Complex JSON Handling** | Detects nested JSON, offers Multi-Table or Single-Row export. | Others fail on complex JSON or force one approach. |

### Messaging Guidelines

**Tagline options:**
- "The only JSON converter that helps you fix errors and handle complex nested data"
- "JSON too messy? Fix it and convert it — all in one place"
- "Convert complex JSON to CSV/Excel — with error fixing built-in"

---

## Target Audience

ParseWiz targets **developers and data analysts who need instant, browser-based file conversion**:
- Data analysts working with exports
- Developers handling API responses
- Database admins migrating data
- Business users dealing with data feeds
- Anyone who needs quick format conversion without coding

---

## SEO Files Reference

| File | Purpose |
|------|---------|
| `frontend/robots.txt` | Search engine crawlers |
| `frontend/sitemap.xml` | Site pages for search engines |
| `frontend/favicon.svg` | Modern SVG favicon (primary) |
| `frontend/favicon-16x16.png` | Classic small favicon |
| `frontend/favicon-32x32.png` | Classic favicon |
| `frontend/apple-touch-icon.png` | iOS home screen icon (180x180) |
| `frontend/og-image.svg` | Source file for OG image |
| `frontend/og-image.png` | Social media preview (1200x630) |

### Meta Tags in index.html

```html
<meta name="description" content="Free online tool to convert JSON, CSV, and Excel files instantly. No signup required. Transform data formats, preview before download, handle complex nested JSON structures.">
<meta name="keywords" content="JSON to CSV, CSV to JSON, Excel converter, data conversion, JSON to Excel, CSV to Excel, file converter, data transformation, online converter">
<meta name="google-site-verification" content="FZ7K4qZyUC4izZpHw8CaJ-K9-zFRlPV9YUZEDMtwlD4">
```

### Structured Data (JSON-LD)

WebApplication schema in index.html with features list, pricing (free), and application category.

---

## Validation Tools

| Tool | URL | Purpose |
|------|-----|---------|
| Schema.org Validator | https://validator.schema.org/ | Validate structured data |
| Facebook Sharing Debugger | https://developers.facebook.com/tools/debug/ | Preview OG tags |
| Twitter Card Validator | https://cards-dev.twitter.com/validator | Preview Twitter cards |
| Google PageSpeed Insights | https://pagespeed.web.dev/ | Performance metrics |
| Lighthouse | Chrome DevTools > Lighthouse | Target: 90+ SEO score |

---

## Maintenance

- **sitemap.xml**: Update `<lastmod>` when significant content changes
- **og-image.png**: Update if branding changes
- **Meta description**: Update if app features change significantly

### Regenerating Assets

```bash
cd frontend
rsvg-convert -w 16 -h 16 favicon.svg -o favicon-16x16.png
rsvg-convert -w 32 -h 32 favicon.svg -o favicon-32x32.png
rsvg-convert -w 180 -h 180 favicon.svg -o apple-touch-icon.png
rsvg-convert -w 1200 -h 630 og-image.svg -o og-image.png
```

---

## Ongoing Tasks

- [ ] Monitor Google Search Console weekly for new query data
- [ ] Track which pages get impressions/clicks
- [ ] Check competitors for new features
- [ ] Update this document as tasks are completed
