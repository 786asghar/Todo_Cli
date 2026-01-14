# constitution.md - Project Constitution

## Core Governance Principles

This document serves as the permanent constitution for the AI-driven hackathon project. All participants, both human and AI agents, must adhere to these governance principles throughout the hackathon lifecycle.

## Development Model: Spec-Driven Development (SDD)

The project strictly follows spec-driven development methodology:
- Specifications are the sole source of truth for behavior and scope
- Human participants author and refine specifications exclusively
- AI agents generate implementation strictly from provided specifications
- Manual code writing or editing by humans is prohibited
- Implementation must not exceed what is explicitly defined in specifications

## Critical Constraints (Hackathon Rules)

The following constraints are non-negotiable and must be strictly enforced:

1. **No Direct Application Code Creation**: AI agents must NOT write any application code directly
2. **No Feature Implementation**: AI agents must NOT implement features outside of specification scope
3. **No Executable File Generation**: AI agents must NOT generate executable files or configurations without explicit specification
4. **Specification Adherence Only**: Output is limited to the constitution.md document as specified

## Phase Governance Requirements

- The project progresses incrementally through clearly defined phases
- At any given time, only ONE phase is considered active
- Active phase scope is defined exclusively in specification files
- This constitution does not encode phase-specific features or implementations
- Transitioning to new phases requires specification updates, not constitutional changes

## Role Definitions and Responsibilities

### Human Participant Role
- Authors and refines project specifications
- Designs system behavior through written specifications, not code
- Reviews AI-generated output for alignment with specifications
- Resolves issues by updating specifications only, never through direct code modification
- Maintains separation between governance, specifications, and generated code

### AI Agent (Claude Code) Role
- Reads constitution.md and all relevant specifications before performing any action
- Generates implementation strictly from provided specifications only
- Must not assume, infer, or invent requirements beyond what is specified
- Must request clarification when specifications are ambiguous or incomplete
- Must stop and request specification clarification when encountering errors or inconsistencies
- Must not perform silent fixes, undocumented changes, or speculative behavior

## Specification Discipline Requirements

Specifications must adhere to the following standards:
- Must be explicit, reviewable, and phase-scoped
- Implementation must not exceed specification-defined scope
- Future-phase functionality must not be anticipated or implemented prematurely
- Conflicting specifications must be reported before any implementation attempt
- All requirements must be clearly documented in specification files before implementation

## Error and Conflict Handling Protocol

When errors or inconsistencies are encountered:
1. AI agents must immediately stop processing
2. AI agents must request specification clarification from human participants
3. No silent fixes or undocumented changes are permitted
4. No speculative behavior or assumption-making is allowed
5. Conflicting specifications must be reported before any implementation work

## Repository Governance Standards

Maintain clear separation between:
- Governance documents (constitution.md)
- Specifications (spec files)
- Generated code and implementation artifacts

Specifications act as the binding contract between human participants and AI agents.

## Compliance Verification

All participants must verify compliance with these constitutional requirements:
- Regular audits of specification adherence
- Verification that no direct code modification has occurred
- Confirmation that all implementation stems from explicit specifications
- Validation that phase governance is properly maintained