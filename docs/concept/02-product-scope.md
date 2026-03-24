# Product Scope — Tirana Real Estate Companion

## Purpose of this document

This document defines what the first version of the project must include, what it should not include, and what outcomes are expected from the MVP.

## Scope objective

The objective of the first version is to deliver a small, locally runnable web application that allows users to explore Tirana property listings and understand pricing through machine learning and comparable properties.

The focus is on a complete and understandable user flow, not on advanced features or maximum model complexity.

## In scope

The following items are included in the first version of the project.

### 1. Data loading and preprocessing
- Load the provided dataset from the repository.
- Validate required fields.
- Handle missing values with a clear and consistent strategy.
- Create a stable internal listing identifier if no reliable source identifier exists.
- Prepare cleaned data for both the application and the ML pipeline.

### 2. Listings browser
- Display a list of available property listings.
- Show essential summary fields for each listing.
- Support browsing multiple listings in a simple and readable layout.

### 3. Filters
The application must support filtering listings by at least:
- Price range.
- Bedrooms.
- Bathrooms.
- Square meters.
- One additional field such as furnishing status, elevator, or terrace.

### 4. Listing details page
Each listing must have a details view that shows:
- Price.
- Bedrooms.
- Bathrooms.
- Square meters.
- Floor.
- Furnishing status.
- Elevator information.
- Terrace information.
- Address.
- Description text.

### 5. ML price estimate
The details page must display:
- A predicted price in EUR.
- A fair price range with a lower and upper bound.

The first version may use a baseline regression model as long as the output is stable and the implementation is understandable.

### 6. Comparable properties
The details page must display 5 comparable listings.

Comparable properties should be selected using similarity rules based on:
- Nearby location.
- Similar square meters.
- Similar bedroom count or bathroom count.
- Other relevant structured features when available.

Each comparable property should include a short reason explaining why it is similar.

### 7. Local execution
The full project must run locally for demonstration and learning purposes.

The repository must include enough setup instructions so another student or reviewer can run the project without guesswork.

## Out of scope

The following items are not required in the first version.

- User authentication.
- User accounts or profiles.
- Real-time messaging.
- External paid APIs.
- Production deployment.
- Advanced map integrations.
- Full-text semantic search.
- Image management pipelines.
- Retraining from inside the web interface.
- Complex explainability dashboards.
- Mobile app development.

These items can be added later only after the core product flow is complete and stable.

## MVP requirements

A version can be considered a valid MVP only if all of the following are true:

1. A user can open the application locally.
2. A user can browse listings.
3. A user can apply filters.
4. A user can open a listing details page.
5. A user can see an ML price estimate.
6. A user can see a fair price range.
7. A user can see 5 comparable properties with simple explanations.

If any of these core steps is missing, the project should not be treated as complete.

## Functional expectations

The first version should satisfy the following functional expectations:

- The listings page should load usable property data.
- Filters should update the visible results correctly.
- The details page should show the main property information clearly.
- The estimate should be generated from project data, not hardcoded.
- The fair range should be generated consistently.
- Comparable properties should come from the dataset and not be random.
- The app should be understandable without reading the source code.

## Non-functional expectations

The first version should also follow these quality expectations:

- Clear project structure.
- Readable code.
- Predictable local setup.
- Reasonable error handling for missing or incomplete listing data.
- Consistent naming across backend, frontend, and documentation.
- Documentation that supports step-by-step learning and AI-assisted development.

## Data assumptions

The project assumes the dataset may contain:
- Missing values.
- Inconsistent records.
- Outliers.
- Missing unique identifiers.
- Optional location or feature fields.

The implementation must handle these cases with simple and explicit rules rather than hidden assumptions.

## Feature prioritization

Features should be implemented in this priority order:

1. Data loading and preprocessing.
2. Listings browser.
3. Filters.
4. Listing details page.
5. ML baseline model.
6. Fair price range logic.
7. Comparable properties logic.
8. UI polish and optional enhancements.

This order is important because later features depend on the earlier ones.

## Change rules

If a new feature does not directly improve the core user flow, it should be postponed.

The project should prefer a smaller complete version over a larger incomplete version.

## Definition of done

The first version is done when:
- The application runs locally.
- The main browsing-to-details flow works.
- ML estimation is integrated into the product.
- Comparable properties are shown with simple justification.
- The repository includes clear setup and usage instructions.
- The codebase is organized enough for a student or AI coding agent to continue development safely.
