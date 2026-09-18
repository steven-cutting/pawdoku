---
title: "Purpose and scope"
kind: "project"
audience: [user, contributor, maintainer, agent]
canonical_for: [project_purpose, project_non_goals]
requires: []
---

# Purpose and scope

Pawdoku is a Biscuit Games game: A sudoku puzzle game for Biscuit Games. It runs
entirely in the browser as a static site: there is no server, no account and no database,
and the platform package `@steven-cutting/biscuit-games` supplies the look, the shared
components and the cell and key a play surface is built from, so what this repository
decides is the game.

## What it does

Today, nothing yet: the page carries the platform's header with this game's lockup and an
empty main landmark. What the game will do is stated first in `docs/specs/`, one rule at a
time, and built second; see [Specifications](../explanation/specifications.md). Rewrite
this section as the rules arrive, and keep it to what a player would notice.

## What it deliberately does not do

- **No accounts, no sync.** Whatever the game remembers belongs to one browser on one
  device. Clearing browser data clears it, and nothing can restore it.
- **No server.** Nothing is uploaded, and nothing is recorded anywhere but the device.
- **No analytics or telemetry.** See [Security model](../explanation/security-model.md).

## Who it is for

A single player, on their own device. Everything else follows from that, and this section
is the game's to rewrite when it knows more.

## Related pages

- [Repository map](repository-map.md)
- [Terminology](terminology.md)
- [Architecture](../explanation/architecture.md)
