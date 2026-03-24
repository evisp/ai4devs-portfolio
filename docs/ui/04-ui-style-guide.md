# UI Style Guide — Tirana Real Estate Companion

## Purpose of this document

This document defines the visual style of the application: colors, typography, spacing, and basic components.

It is intended for students, designers, developers, and AI coding agents so that the UI looks consistent and readable.

## Design goals

- Simple and clean.
- Easy to scan listings.
- High contrast for readability.
- Works well on laptop screens.
- Minimal distraction from the price estimate and comparable properties.

## CSS framework

This project uses **Bootstrap 5** as the CSS framework.

- Use Bootstrap's grid system (`container`, `row`, `col-*`) for page layout.
- Use Bootstrap's spacing utilities (`m-*`, `p-*`) for margins and padding.
- Use Bootstrap components (`card`, `btn`, `form-control`, `badge`) as the base for UI components.
- Override Bootstrap's default colors with the custom palette below using CSS custom properties or a small custom stylesheet.

The custom colors and typography below should be applied on top of Bootstrap's defaults, not as replacements for Bootstrap itself.

## Color palette

### Primary colors

- Primary: `#2563EB` (blue)  
  Usage: main buttons, active states, key highlights.

- Primary Dark: `#1D4ED8`  
  Usage: hover states for primary buttons.

### Neutral colors

- Background: `#F9FAFB`  
  Usage: app background.

- Surface / Card: `#FFFFFF`  
  Usage: listing cards, panels, detail sections.

- Border / Divider: `#E5E7EB`  
  Usage: card borders, separators, input outlines.

- Text Primary: `#111827`  
  Usage: main text, titles.

- Text Secondary: `#6B7280`  
  Usage: secondary text, labels, helper text.

### Accent colors

- Accent: `#10B981` (green)  
  Usage: subtle highlights, tags for “Fair” or positive messages.

- Warning: `#F97316` (orange)  
  Usage: potential “Overpriced” labels or warning messages.

- Error: `#EF4444`  
  Usage: error states, validation messages.

## Typography

Use a clean, sans-serif font that is widely available.

- Base font family: `system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`.

### Text styles

- Page title:  
  - Font size: 24–28 px  
  - Weight: 600–700  
  - Usage: screen titles such as “Listings” or “Property details”.

- Section title:  
  - Font size: 18–20 px  
  - Weight: 600  
  - Usage: sections like “Price estimate”, “Comparable properties”.

- Body text:  
  - Font size: 14–16 px  
  - Weight: 400  
  - Usage: general text, descriptions, labels.

- Caption / meta text:  
  - Font size: 12–13 px  
  - Weight: 400  
  - Usage: helper text, very small labels.

## Spacing and layout

- Base spacing unit: 4 px.  
- Common spacing values: 8, 12, 16, 24 px.

Guidelines:
- Use 16–24 px padding inside cards and panels.
- Use 16 px vertical spacing between sections.
- Use 8–12 px spacing between related elements (for example label and field).

## Buttons

### Primary button

- Background: Primary (`#2563EB`)
- Text: white
- Border radius: 4–6 px
- Padding: 8–12 px vertical, 16–20 px horizontal
- Hover: Primary Dark (`#1D4ED8`)
- Usage: main actions like “Apply filters”, “View details”.

### Secondary button

- Background: white
- Border: 1 px solid Border (`#E5E7EB`)
- Text: Primary text color
- Hover: light gray background (`#F3F4F6`)
- Usage: secondary actions, such as “Clear filters”.

## Inputs and filters

- Background: white
- Border: 1 px solid Border (`#E5E7EB`)
- Border radius: 4 px
- Padding: 8–10 px
- Focus state: border color changes to Primary (`#2563EB`)

Labels:
- Font size: 13–14 px
- Color: Text Secondary (`#6B7280`)

## Cards

Listing cards and other panel-like components should:

- Use Surface background (`#FFFFFF`).
- Have a subtle border (`#E5E7EB`) or a soft shadow.
- Use 16–24 px internal padding.
- Include clear hierarchy: title, price, key attributes, and secondary details.

## Iconography (optional)

Icons are optional for the first version.

If used, keep them simple and minimal:
- Small icons for beds, baths, and square meters.
- Simple markers for amenities like elevator, terrace, and parking.

## Responsive behavior (minimum expectations)

- The layout should work on typical laptop resolutions (1280 px width and above).
- On smaller widths, the layout can stack filters above the results.
- Full mobile optimization is not required for the first version but should remain possible.

## Consistency rules

- Use the primary blue color only for interactive and important elements.
- Use green for positive or confirming states, not for primary actions.
- Use one main font and consistent sizes across screens.
- Avoid adding new colors unless necessary; reuse the defined palette.

## Important Notes

- Use the color codes exactly as defined here.
- Keep font sizes within the described ranges.
- Use consistent spacing multiples (4 px units).
- Implement reusable components for buttons, inputs, and cards where possible.
