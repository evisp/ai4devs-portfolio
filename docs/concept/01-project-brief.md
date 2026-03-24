# Project Overview — Tirana Real Estate Companion

## Purpose of this document

This document defines the project at a high level so that students, mentors, and AI coding agents can quickly understand what the application is supposed to do.

It describes the product goal, target users, main functionalities, and the scope of the first working version.

## Project summary

Tirana Real Estate Companion is a small web application for exploring residential property listings in Tirana.

The application combines listing browsing with machine learning to help users understand property prices through an estimated value, a fair price range, and comparable listings.

## Main goal

The goal of the project is to build a simple, clear, and locally runnable product that allows a user to:

- Browse property listings.
- Filter listings by relevant criteria.
- Open a listing details page.
- View an ML-based price estimate.
- View a fair price range.
- View comparable properties that support the estimate.

## Target users

This project is intended for the following users:

### 1. Property explorers
Users who want to browse apartments or other residential listings in Tirana and better understand pricing.

### 2. AI4Devs students
Students who want to study how a practical AI product is built step by step, from data understanding to a working application.

### 3. Developers and reviewers
People who need to understand the repository structure, implementation scope, and product behavior quickly.

## Core product functionalities

The application should include the following main features.

### Listings browser
- Display a list of properties from the dataset.
- Show key listing information such as price, size, bedrooms, bathrooms, and address.
- Make it easy to scan multiple listings quickly.

### Filters
Users should be able to filter listings by at least:
- Price range.
- Bedrooms.
- Bathrooms.
- Square meters.
- At least one additional feature such as furnishing, elevator, or terrace.

### Listing details page
When a user opens a listing, the application should show:
- Price.
- Bedrooms.
- Bathrooms.
- Square meters.
- Floor.
- Furnishing status.
- Elevator and terrace information.
- Address.
- Description text.

### ML price estimate
The listing details page should include:
- An estimated property price in EUR.
- A fair price range shown as low to high.

The estimate should come from a baseline machine learning model that is stable, understandable, and suitable for a first version of the product.

### Comparable properties
For each listing, the application should show 5 comparable properties.

Comparable properties should be selected using similarity rules based on factors such as:
- Nearby location.
- Similar size.
- Similar number of rooms.
- Similar relevant features.

Each comparable property should include a short explanation of why it is considered similar.

## Product principles

The project should follow these principles:

- Product-first design.
- Clear and understandable output.
- Simple local execution.
- Explainable ML behavior.
- Step-by-step development.
- Clean repository structure.
- Documentation that is useful for both humans and AI coding agents.

## Scope of the first version

The first version should focus on the minimum complete experience:

- Load and preprocess the dataset.
- Create a stable listing identifier.
- Build a listings page with filters.
- Build a listing details page.
- Train or load a baseline ML model.
- Generate a price estimate and fair range.
- Select and display 5 comparable properties.

The first version does not need advanced features if the main flow is already complete and reliable.

## Expected project flow

A user should be able to complete this flow:

1. Open the application.
2. Browse available listings.
3. Apply filters.
4. Open one listing.
5. Read the listing details.
6. See the ML price estimate and fair range.
7. Review comparable properties.

