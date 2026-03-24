# UI Screens and Flow — Tirana Real Estate Companion

## Purpose of this document

This document describes the main screens, their content, and the navigation flow.

It is intended for students, designers, developers, and AI coding agents so that the final UI structure is clear before implementation.

## Overview of screens

The first version of the application should include three main screen types:

1. Listings page (home / browse).
2. Listing details page.
3. Optional: technical or “about” page for explanations (can be added later).

The core user journey is: open app → view listings → filter → open details → review estimate and comps.

## Screen 1 — Listings page

### Purpose

Allow the user to:
- View a list of property listings.
- Apply filters to narrow the results.
- Open a property to see more details.

### Layout structure

Recommended layout:

- Top bar:
  - Project title: “Tirana Real Estate Companion”.
  - Optional simple subtitle.

- Left or top filter panel:
  - Price range controls.
  - Bedrooms filter.
  - Bathrooms filter.
  - Square meters filter.
  - One additional filter (for example: furnishing, elevator, or terrace).
  - “Apply filters” primary button.
  - “Clear filters” secondary button.

- Main content area:
  - List of listing cards in a vertical layout.

### Listing card contents

Each listing card should include:

- Price (prefer `price_in_euro` if available).
- Location: formatted address or city zone.
- Core attributes:
  - Bedrooms.
  - Bathrooms.
  - Square meters.
  - Floor (if available).
- Key amenities:
  - Elevator (yes/no).
  - Terrace (yes/no).
- Action:
  - “View details” button or clickable card.

Optional:
- Short snippet of the description (first one or two lines).

### Interactions

- Changing filters and clicking “Apply filters” updates the list.
- Clicking on a card or “View details” navigates to the Listing details page for that listing.

## Screen 2 — Listing details page

### Purpose

Allow the user to:
- See full details of a specific listing.
- Understand the ML price estimate and fair range.
- See comparable properties and why they are similar.

### Layout structure

Recommended layout (desktop):

- Top bar:
  - Back link or button to “Back to listings”.
  - Project title.

- Main content area:
  - Left or top: Property details section.
  - Right or bottom: ML estimate section and comparable properties section.

### Property details section

Include:

- Property title (for example: address or simple heading).
- Display price (original listing price).
- Core attributes:
  - Bedrooms.
  - Bathrooms.
  - Square meters.
  - Floor.
  - Furnishing status.
- Amenities:
  - Elevator.
  - Terrace.
  - Other available features (parking, garden, etc., if relevant).
- Address:
  - Formatted address.
- Description:
  - Full listing description text.

### ML price estimate section

Include:

- Section title: “Price estimate”.
- Estimated price in EUR (highlighted).
- Fair price range:
  - Text representation such as “Fair range: 120,000 – 140,000 EUR”.
- Optional short explanation text, for example:
  - “Based on similar listings by size, rooms, and location.”

The design should visually distinguish the ML estimate from the original listing price.

### Comparable properties section

Include:

- Section title: “Comparable properties”.
- A list of 5 comparable listings.

For each comparable listing:

- Price.
- Location (short address or zone).
- Key attributes:
  - Bedrooms.
  - Bathrooms.
  - Square meters.
- Short explanation line, for example:
  - “Similar size and 2 bedrooms, located in the same area.”
- Optional link or button “View listing” (can open in a new details view or just show key info inline).

Layout options:

- Simple vertical list.
- Card layout with stacked cards.

### Interactions

- “Back to listings” returns to the filtered listings page.
- If implemented, clicking a comparable listing can navigate to its own details page.

## Optional Screen — About or Help

This screen is optional for the first version.

If added later, it can include:
- A short explanation of what the app does.
- A plain-language description of the ML estimate and fair range.
- Limitations and assumptions.

## Navigation flow

Basic flow:

1. User opens the application → lands on Listings page.
2. User adjusts filters and applies them.
3. User chooses a listing → navigates to Listing details page.
4. User reviews:
   - Original listing price.
   - ML estimate and fair range.
   - Comparable properties.
5. User can go back to the Listings page to explore more properties.

## Mobile and small-screen considerations

For smaller widths:

- Place filters in a collapsible section at the top.
- Stack sections vertically on the Listing details page:
  - Property details.
  - ML estimate.
  - Comparable properties.

Full responsive design is not required for the first version but the layout should degrade gracefully.

## Notes for AI coding agents

- Keep the number of screens limited.
- Implement the described layout in a simple and maintainable way.
- Reuse components (cards, buttons, inputs) across screens.
- Ensure a clear hierarchy of information, especially on the Listing details page:
  - Original price.
  - ML estimate and fair range.
  - Comparable properties.

The primary goal is clarity of the main user flow, not visual complexity.
