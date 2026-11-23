# Engine name

Last verified: YYYY-MM-DD
Verified against: engine version, driver or package version
Maintained by: your handle (independent, or "on behalf of the vendor" if that is true)

<!--
Copy this file to references/engines/<engine>.md and delete these comments.
Keep it to what an agent would otherwise get wrong. Link the official docs for everything else.
Every claim carries the version it applies to. Test against the real engine.
-->

## Identity

<!-- What it is in two lines: server or embedded, license, how to run it locally with no account. -->

## Packages and drivers

<!-- The current package names per language, and any old or renamed ones agents still reach for. -->

## Query language

<!-- Which language and version it implements, and how to ask the engine which version it is running. -->

## Schema introspection

<!-- The exact calls that return labels or tables, relationship types, properties, constraints and indexes. -->

## Reading a query plan

<!-- How to EXPLAIN or PROFILE, and what an unanchored scan or a Cartesian product looks like in the output. -->

## Dialect gaps

<!-- Where it differs from what an agent trained mostly on other engines will assume. One row per gap. -->

| Agent assumes | This engine | Since version |
|---|---|---|

## Limits and safety

<!-- Timeouts, memory limits, read-only modes, and the operations that are expensive here. -->

## Vendor resources

<!-- The vendor's own agent skills if they exist, then the official docs. -->
