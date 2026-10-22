# Kazakh–Russian Mixed-Text Spelling Correction and Translation System

## Project overview

This project aims to develop a prototype that helps users correct spelling errors in text containing a mixture of Kazakh and Russian, then translate the reviewed text into Kazakh or English. The system is intended to support multilingual text processing while keeping the user in control of proposed corrections.

The project is an academic prototype. Features and technical choices described as planned below should not be interpreted as already implemented or evaluated unless confirmed by the current code and test results.

## Problem statement

Kazakh–Russian mixed-language text can be difficult to process with tools designed for a single language. Spelling errors, language switching, and mixed-language expressions can affect correction and subsequent translation. The project will investigate a workflow that identifies and corrects spelling errors, allows the user to review proposed changes, and translates the approved text into a selected target language.

## Objectives

- Investigate methods for correcting spelling errors in Kazakh–Russian mixed text.
- Compare suitable pretrained text-to-text Transformer candidates, including ByT5 and mT5.
- Design a user-controlled workflow so users can review and accept corrections before translation.
- Investigate and integrate an external translation API for Kazakh and English, subject to language-support, quality, latency, usage-limit, cost, privacy, and feasibility checks.
- Evaluate spelling correction and translation separately using a defined test set and documented metrics.
- Deliver a usable prototype and technical documentation.

## Planned workflow

1. The user enters Kazakh–Russian mixed text.
2. The system validates the input and processes it through the spelling-correction component.
3. The system presents correction results or suggestions for user review.
4. The user reviews and accepts the text to be translated.
5. The user selects Kazakh or English as the target language.
6. The translation component sends the approved text to the selected translation service.
7. The system displays the translated text or a clear error message if processing fails.

The final interaction details will follow the implementation and team-approved requirements.

## Planned technology direction

The following is the current planned direction, aligned with the team's technology comparison:

- **Programming language:** Python.
- **Backend:** FastAPI is the preferred framework.
- **Spelling correction:** compare pretrained text-to-text Transformer candidates such as ByT5 and mT5. A rule-based or string-similarity approach may be used as a baseline if appropriate.
- **Translation:** an external translation API is the planned primary approach. The provider must be selected after checking support for translation into Kazakh and English, quality, latency, usage limits, cost, privacy terms, and feasibility. A pretrained multilingual translation model may be considered if an API is unsuitable.
- **Frontend:** responsive web interface using React and Next.js; a Progressive Web App (PWA) is optional.
- **Language codes:** `kk` for Kazakh and `en` for English are proposed for the integration contract and must be used consistently across frontend and backend.

These are planned choices, not claims that the tools have already been integrated. The final provider, API contract, and model selection must match the implementation agreed by the team.

## Functional scope

The prototype is planned to support:

- entering Kazakh–Russian mixed-language text;
- rejecting empty or whitespace-only input with a clear validation message;
- spelling correction or correction suggestions;
- user review and acceptance of proposed changes;
- translation of the reviewed text into Kazakh or English;
- clear success and error responses;
- separate evaluation of spelling correction and translation quality.

## Evaluation plan

Spelling correction and translation will be evaluated separately on a held-out test set. For correction, the team plans to consider Character Error Rate (CER) and Word Error Rate (WER), alongside qualitative review of whether corrections preserve meaning and handle mixed-language text appropriately. Translation will be reviewed for meaning preservation, fluency, terminology and named entities, handling of mixed-language input, and reliability. Automatic translation metrics such as chrF or BLEU may supplement human review if suitable reference translations are available.

No performance scores are reported here because they should only be added after the experiments have been conducted. The final test-set size, preparation responsibility, and evaluation procedure should be recorded in the project documentation once agreed.

## Team and responsibilities

- **Zumrad Sherbadalova:** investigate and integrate the translation component; contribute to translation-quality evaluation, user workflow and requirements, and project documentation.
- **Asem Nurlanova:** lead investigation and development of the spelling-correction component; prepare correction examples and contribute to correction-quality evaluation and shared project documentation.
- **Supervisor:** Shynar Akhmetzhanova.

The team should keep shared documents consistent with the actual division of work and update these responsibilities if the plan changes.

## Project management

- **GitHub repository:** https://github.com/asemnurlan/Spelling-Error-Correction
- **YouTrack project:** https://mbsloml.youtrack.cloud/projects/KRMC

The team uses GitHub for source control and project documentation, and YouTrack for tracking project tasks. Team members should work through the shared repository, use clear commit messages, and coordinate changes to shared documents. Access to the private repository or YouTrack project must be granted by the project owner.

## Repository structure

The structure below is a suggested organization and should be adjusted to match the actual repository:

```text
.
├── README.md
├── docs/
│   ├── project-proposal.docx
│   ├── requirements-specification.docx
│   ├── literature-review.docx
│   ├── technology-comparison.docx
│   ├── existing-systems-comparison.docx
│   ├── verification-and-evaluation-plan.docx
│   └── translation-component-integration.docx
├── backend/
├── frontend/
└── tests/
```

Folders and filenames should only be added when they exist in the repository. The implementation may use a different structure as development progresses.

## Current status

The project direction, planned workflow, and documentation structure have been defined for the academic prototype. The spelling-correction model, translation provider, final API contract, and evaluation results must be confirmed against the implementation and team decisions. This README does not claim that the application is fully implemented or tested.

## Security and privacy

- Do not commit API keys, passwords, tokens, or other secrets to GitHub.
- Store translation-service credentials in server-side environment configuration or a secret manager.
- Review the selected provider's privacy and data-handling terms before sending user text to an external service.
- Avoid including personal or sensitive information in test examples unless there is an approved reason and suitable safeguards.

## License

No license has been specified yet. Add a license only after the team agrees on the terms for sharing and reuse.
