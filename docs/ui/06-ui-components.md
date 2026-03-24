# UI Components — Tirana Real Estate Companion

## Purpose of this document

This document defines the main reusable UI components of the application.

Components are implemented as **Jinja2 template partials** (or macros) styled with **Bootstrap 5** classes and a small custom stylesheet for project-specific colors.

## Component list

The first version should include at least these components:

- PrimaryButton
- SecondaryButton
- FilterGroup
- ListingCard
- ListingAttributeTag
- PriceBlock
- EstimateBlock
- ComparableCard
- SectionCard
- PageLayout (base template)

---

## PrimaryButton

A button for main actions such as "Apply filters" or "View details".

- Bootstrap class: `btn btn-primary`
- Custom override: set `--bs-btn-bg` to `#2563EB`, `--bs-btn-hover-bg` to `#1D4ED8`.

Usage:
```html
<button type="submit" class="btn btn-primary">Apply filters</button>
<a href="{{ url_for('listing_detail', listing_id=listing.listing_id) }}" class="btn btn-primary btn-sm">View details</a>
```

---

## SecondaryButton

A button for secondary actions such as "Clear filters".

- Bootstrap class: `btn btn-outline-secondary`

Usage:
```html
<a href="{{ url_for('listings') }}" class="btn btn-outline-secondary">Clear filters</a>
```

---

## FilterGroup

Container for filter controls on the Listings page.

- Use a Bootstrap `card` or `form` wrapper.
- Arrange inputs using Bootstrap grid (`row`, `col-md-*`).
- Include number inputs for price range, bedrooms, bathrooms, square meters.
- Include a select input for furnishing status.
- Include checkboxes for elevator and terrace.
- End with PrimaryButton ("Apply filters") and SecondaryButton ("Clear filters").

Implementation: Jinja2 partial `_filter_group.html` included in the listings page template.

Example structure:
```html
<form method="get" action="{{ url_for('listings') }}" class="card card-body mb-4">
  <div class="row g-3">
    <div class="col-md-3">
      <label class="form-label">Min price (€)</label>
      <input type="number" name="min_price" class="form-control" value="{{ filters.min_price or '' }}">
    </div>
    <!-- more filter inputs -->
    <div class="col-12">
      <button type="submit" class="btn btn-primary">Apply filters</button>
      <a href="{{ url_for('listings') }}" class="btn btn-outline-secondary ms-2">Clear filters</a>
    </div>
  </div>
</form>
```

---

## ListingCard

Card representing a single listing in the listings page.

- Bootstrap class: `card`
- Content:
  - Price using PriceBlock.
  - Address line.
  - Core attributes using ListingAttributeTag elements.
  - "View details" PrimaryButton (small variant).

Implementation: Jinja2 partial `_listing_card.html`.

Example structure:
```html
<div class="card mb-3">
  <div class="card-body">
    <h5 class="card-title">{{ listing.price_in_euro | format_price }} EUR</h5>
    <p class="card-text text-muted">{{ listing.address or 'Address not available' }}</p>
    <div class="d-flex flex-wrap gap-2 mb-2">
      <span class="badge bg-light text-dark">{{ listing.bedrooms }} beds</span>
      <span class="badge bg-light text-dark">{{ listing.bathrooms }} baths</span>
      <span class="badge bg-light text-dark">{{ listing.square_meters }} m²</span>
    </div>
    <a href="{{ url_for('listing_detail', listing_id=listing.listing_id) }}" class="btn btn-primary btn-sm">View details</a>
  </div>
</div>
```

---

## ListingAttributeTag

Small label for displaying a single property attribute.

- Bootstrap class: `badge bg-light text-dark` or `badge bg-secondary`.
- Use for: beds, baths, sqm, floor, elevator, terrace.

Examples:
```html
<span class="badge bg-light text-dark">2 beds</span>
<span class="badge bg-light text-dark">1 bath</span>
<span class="badge bg-light text-dark">85 m²</span>
<span class="badge bg-success text-white">Elevator</span>
<span class="badge bg-success text-white">Terrace</span>
```

---

## PriceBlock

Component to display a price consistently.

- Display the price formatted with thousands separator and "EUR" suffix.
- Use larger font weight for emphasis.

Implementation: Jinja2 macro or inline block.

Example:
```html
<div class="price-block">
  <span class="fs-4 fw-bold text-primary">€{{ "{:,.0f}".format(amount) }}</span>
  {% if label %}<small class="text-muted d-block">{{ label }}</small>{% endif %}
</div>
```

---

## EstimateBlock

Component to show the ML price estimate and fair range on the details page.

- Wrap in a Bootstrap `card` with custom accent border.
- Content:
  - Section heading: "Price estimate".
  - Estimated price (large, bold, primary color).
  - Fair range line: "Fair range: 120,000 – 140,000 EUR".
  - Optional note text.

Implementation: Jinja2 partial `_estimate_block.html`.

Example structure:
```html
<div class="card border-primary mb-4">
  <div class="card-body">
    <h5 class="card-title">Price estimate</h5>
    <p class="fs-3 fw-bold text-primary mb-1">€{{ "{:,.0f}".format(estimated_price) }}</p>
    <p class="text-muted">Fair range: €{{ "{:,.0f}".format(fair_range_low) }} – €{{ "{:,.0f}".format(fair_range_high) }}</p>
    {% if note %}<small class="text-muted">{{ note }}</small>{% endif %}
  </div>
</div>
```

---

## ComparableCard

Card representing one comparable property in the comparable-properties section.

- Bootstrap class: `card`
- Content:
  - Price.
  - Location.
  - Key attributes (beds, baths, sqm).
  - Similarity reason text.
  - Optional "View listing" link.

Implementation: Jinja2 partial `_comparable_card.html`.

Example structure:
```html
<div class="card mb-2">
  <div class="card-body py-3">
    <div class="d-flex justify-content-between">
      <strong>€{{ "{:,.0f}".format(comp.price_in_euro) }}</strong>
      <small class="text-muted">{{ comp.address }}</small>
    </div>
    <div class="d-flex gap-2 my-1">
      <span class="badge bg-light text-dark">{{ comp.bedrooms }} beds</span>
      <span class="badge bg-light text-dark">{{ comp.bathrooms }} baths</span>
      <span class="badge bg-light text-dark">{{ comp.square_meters }} m²</span>
    </div>
    <small class="text-muted fst-italic">{{ comp.similarity_reason }}</small>
  </div>
</div>
```

---

## SectionCard

Generic container for grouping related content on the details page.

- Bootstrap class: `card mb-4`
- Content: heading + arbitrary body content.

Example:
```html
<div class="card mb-4">
  <div class="card-body">
    <h5 class="card-title">{{ title }}</h5>
    <!-- section content -->
  </div>
</div>
```

---

## PageLayout (base template)

Base Jinja2 template that all pages extend.

- Includes Bootstrap 5 CDN links (CSS + JS).
- Includes the custom project stylesheet (`style.css`).
- Defines a fixed header with project title.
- Defines a `{% block content %}` for page-specific content.

Example `base.html`:
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{% block title %}Tirana Real Estate Companion{% endblock %}</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <link href="{{ url_for('static', filename='style.css') }}" rel="stylesheet">
</head>
<body class="bg-light">
  <nav class="navbar navbar-light bg-white border-bottom mb-4">
    <div class="container">
      <a class="navbar-brand fw-bold" href="{{ url_for('listings') }}">Tirana Real Estate Companion</a>
    </div>
  </nav>
  <main class="container">
    {% block content %}{% endblock %}
  </main>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

---

## Component usage rules

- Reuse Jinja2 partials across templates instead of duplicating HTML.
- Use PriceBlock wherever a price is shown, to keep formatting consistent.
- Use EstimateBlock only for the ML estimate and fair range section.
- Use ListingCard only on the Listings page.
- Use ComparableCard only in the comparable properties section.
- Keep all custom CSS in a single `style.css` file that overrides Bootstrap defaults.

---

## Notes for AI coding agents

- Implement each component as a Jinja2 partial or macro in `backend/templates/partials/`.
- Use Bootstrap 5 classes as the primary styling mechanism.
- Add custom CSS only for project-specific colors and minor adjustments.
- Keep component HTML simple and readable for students.
- Prefer composition: for example, ListingCard uses ListingAttributeTag badges and PriceBlock internally.
