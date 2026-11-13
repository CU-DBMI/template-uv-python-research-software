______________________________________________________________________

## name: formal-verification description: Use when selecting or checking correctness properties in Python or Rust research software.

# Formal Verification

## Goal

Improve research software correctness through small, independently checked properties.

## Process

1. Inspect production code and existing tests.
1. Identify high-risk invariants: indexing, identity, schema, dimensions, numeric boundaries, and transformations.
1. Select the smallest useful property that existing tests do not establish.
1. Use Hypothesis for concrete Python examples, including arrays, dataframes, and numerical behavior.
1. Use CrossHair for supported pure Python production functions with precise contracts.
1. Use Kani harnesses that call actual Rust production functions.
1. Consider Nagini or Verus only when stronger proofs justify the maintenance cost.
1. Keep existing pytest and cargo test workflows intact.
1. Record the property, tool version, date, result, assumptions, bounds, and gaps in `verification/README.md`.

## Tool selection

- Hypothesis tests generated concrete examples. It does not establish a mathematical proof.
- CrossHair searches for contract violations through symbolic execution. It does not exhaustively prove all inputs.
- Kani checks actual Rust functions under the harness assumptions and bounds. An insufficient unwind bound is not success.
- Nagini and Verus support stronger deductive results for supported code. Specifications and tool assumptions still limit those results.

CrossHair fits indexing, offsets, identifier normalization, validation, and small pure transformations.
Use Hypothesis and integration tests for unsupported NumPy/Pandas operations, native extensions, external services, and complex mutable state.
Kani fits integer arithmetic, conversions, indexing, parsing state, and bounds checks.

## Rules

- Never weaken specifications or add unjustified assumptions to pass checks.
- Never claim that a verified copy proves production code correct.
- Never label a timeout, unknown result, skipped check, or missing harness as a proof.
- Prefer targeted verification over broad, superficial coverage.
- Keep verification separate from the normal Python/OS matrix and normal cargo test path.
- Do not install Nagini or Verus without a concrete assessment and an explicit maintenance decision.
- When verification is disabled, assess the property first. Do not install a toolchain only because this skill exists.

## Local checks

For projects with verification enabled, use the commands and pinned tool versions in `verification/README.md`.
The Python example is instructional. Attach contracts to the production implementation for meaningful package assurance.
Before a verified claim, inspect the complete tool output and record its limits in the inventory.
