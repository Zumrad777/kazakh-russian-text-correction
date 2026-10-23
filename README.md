
# Kazakh–Russian Mixed-Text Spelling Correction and Translation System

## Project Overview

This project aims to develop a system that helps users correct spelling errors in text containing a mixture of Kazakh and Russian, then translate the reviewed text into Kazakh or English.

The system is designed to support multilingual text processing while allowing users to review and accept proposed corrections before translation.

The project is currently at the prototype stage. A preliminary web application has been created to demonstrate the main workflow. Further development will focus on improving spelling correction, translation reliability, and overall system functionality.

### Live Demo

- **Web application:** https://tiltuzetu.onrender.com
- **API documentation:** https://tiltuzetu.onrender.com/docs
- **GitHub repository:** https://github.com/Zumrad777/kazakh-russian-text-correction

*Note: The live application is a preliminary MVP. Some features may have limitations, and translation availability depends on the external translation service.*

## Problem Statement

Kazakh–Russian mixed-language text can be difficult to process with tools designed for a single language. Spelling errors, language switching, and mixed-language expressions can affect correction and subsequent translation.

This project investigates a workflow that identifies and corrects spelling errors, allows users to review proposed changes, and translates the approved text into a selected target language.

The goal is to create a convenient tool for working with mixed Kazakh–Russian text and to investigate suitable approaches for multilingual spelling correction and translation.

## Objectives

- Investigate methods for correcting spelling errors in Kazakh–Russian mixed text.
- Compare suitable pretrained text-to-text Transformer models, including ByT5 and mT5.
- Design a user-controlled workflow that allows users to review and accept corrections before translation.
- Investigate and integrate an external translation API for Kazakh and English.
- Evaluate spelling correction and translation separately using a defined test set and documented metrics.
- Develop a usable web prototype and technical documentation.
- Improve the reliability and usability of the system through testing and further development.

## Current Prototype

A preliminary version of TilTüzету has been deployed to Render to demonstrate the main user workflow.

The current prototype includes:

- a web interface for entering text;
- a spelling-correction component based on predefined rules;
- a section for reviewing suggested corrections;
- language selection for translation;
- backend API endpoints implemented with FastAPI;
- integration with the MyMemory translation service;
- a limited offline demonstration fallback for selected example phrases;
- an optional MongoDB integration for storing operation history.

The current spelling-correction component uses predefined rules and is not a trained machine-learning model. The translation component depends on an external service, which may temporarily become unavailable or impose request limits. The offline fallback supports only selected phrases and does not provide general-purpose translation.

The prototype is intended to demonstrate the proposed system workflow. It should not yet be considered a complete or fully evaluated research solution.

## Planned Workflow

1. The user enters Kazakh–Russian mixed-language text.
2. The system validates the input.
3. The spelling-correction component processes the text and generates suggested corrections.
4. The user reviews the suggested version and decides whether to accept the changes or keep the original text.
5. The user selects the target language.
6. The translation component processes the reviewed text.
7. The system displays the translated text or an appropriate error message if the request cannot be completed.

The workflow may be refined as development progresses and the team's requirements are finalized.

## Planned Technology Direction

The following technologies and approaches are being considered for further development.

- **Programming language:** Python.
- **Backend:** FastAPI.
- **Frontend:** HTML, CSS, and JavaScript for the current prototype. React and Next.js may be considered for a future version.
- **Spelling correction:** pretrained multilingual text-to-text Transformer candidates, including ByT5 and mT5. Rule-based correction and string-similarity methods may serve as baselines.
- **Translation:** an external translation API, with the provider selected according to language support, translation quality, latency, usage limits, cost, privacy terms, and technical feasibility.
- **Alternative translation approach:** a pretrained multilingual translation model may be considered if an external API does not meet the project requirements.
- **Database:** MongoDB Atlas as an optional component for persistent operation history.
- **Deployment:** Render for hosting the preliminary web application and backend API.
- **Language codes:** `kk` for Kazakh, `ru` for Russian, and `en` for English.

FastAPI, the HTML/CSS/JavaScript frontend, Render deployment, and the current MyMemory integration are part of the existing prototype. Transformer-based correction, alternative translation providers, and frontend framework changes remain potential future improvements.

The final architecture and technology choices will be confirmed during further development.

## Functional Scope

The planned system is intended to support the following functionality:

- entering Kazakh–Russian mixed-language text;
- validating input and handling empty text;
- suggesting spelling corrections;
- allowing users to review proposed changes;
- accepting corrections or retaining the original text;
- translating reviewed text into Kazakh or English;
- displaying translation results and clear error messages;
- optionally storing operation history in MongoDB Atlas;
- providing API endpoints for the main application operations.

Some of these capabilities are available in the current prototype, while others require further development and testing.

## API Overview

The current backend provides the following endpoints:

| Endpoint | Method | Purpose |
|---|---|---|
| `/` | GET | Serves the web application. |
| `/api/health` | GET | Reports application and optional database status. |
| `/api/config` | GET | Returns basic configuration information. |
| `/api/correct` | POST | Processes text using the current rule-based correction component. |
| `/api/translate` | POST | Requests translation and uses the limited offline fallback when a supported example is available. |
| `/api/history` | GET | Returns operation history when MongoDB is configured; otherwise, reports that history is disabled. |

Interactive API documentation is available at:

https://tiltuzetu.onrender.com/docs

The API contract and available functionality may change as the project develops.

## Evaluation Plan

Spelling correction and translation will be evaluated separately using a defined test set.

### Spelling Correction

The evaluation may include:

- **Character Error Rate (CER):** measures character-level differences between a prediction and a reference.
- **Word Error Rate (WER):** measures word-level differences.
- **Qualitative review:** checks whether corrections preserve meaning and handle mixed-language text appropriately.

The rule-based prototype can serve as an initial baseline for comparison with more advanced correction approaches.

### Translation

Translation quality will be assessed through:

- preservation of the original meaning;
- fluency and grammatical correctness;
- handling of mixed Kazakh–Russian input;
- correct treatment of terminology and named entities;
- reliability and consistency of translation results.

Automatic metrics such as chrF or BLEU may supplement human evaluation if suitable reference translations are available.

No evaluation scores are reported in this README because experiments and results must be documented after they have been obtained. The final test-set size, preparation procedure, and evaluation methodology will be established as part of the research.

## Team and Responsibilities

- **Zumrad Sherbadalova:** investigate and integrate the translation component; contribute to translation-quality evaluation, user workflow and requirements, and project documentation.
- **Asem Nurlanova:** lead the investigation and development of the spelling-correction component; prepare correction examples and contribute to correction-quality evaluation and shared project documentation.
- **Supervisor:** Shynar Akhmetzhanova.

Responsibilities may be updated if the team's agreed division of work changes.

## Project Management

The project uses GitHub for source control and documentation, and YouTrack for task tracking.

- **GitHub repository:** https://github.com/asemnurlan/Spelling-Error-Correction
- **YouTrack project:** https://mbsloml.youtrack.cloud/projects/KRMC

Team members should coordinate changes to shared files, use clear commit messages, and keep documentation consistent with the implementation.

Access to the repository or YouTrack project may require permission from the project owner.

## Repository Structure

The following is a suggested structure for future development, not a statement that all these files and folders already exist:

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
├── app.py
├── requirements.txt
├── static/
│   ├── index.html
│   ├── style.css
│   └── app.js
├── start.sh
└── tests/
```

The current repository may use a different structure. Documentation and folders should be updated as implementation progresses.

## Development Status and Next Steps

The project currently has a preliminary web interface and a FastAPI backend deployed to Render. The prototype demonstrates text input, correction suggestions, user review, and translation requests.

The next development steps include:

- improving spelling correction for Kazakh–Russian mixed-language text;
- comparing rule-based approaches with pretrained multilingual models;
- improving translation reliability and handling external-service errors;
- evaluating alternative translation providers if necessary;
- configuring and testing MongoDB Atlas if persistent history is required;
- preparing a test dataset and evaluating correction and translation quality;
- expanding automated tests and documenting the results;
- refining the interface and API based on testing and feedback.

The final model selection, translation provider, API contract, and evaluation results remain subject to further development and team decisions.

## Security and Privacy

- Do not commit API keys, passwords, access tokens, or other secrets to GitHub.
- Store service credentials in server-side environment variables or a secret manager.
- Configure sensitive settings through the hosting platform's environment settings.
- Review the privacy and data-handling terms of external services before sending user text to them.
- Avoid including personal or sensitive information in test examples unless there is an approved reason and suitable safeguards.
- Ensure that any stored operation history is handled appropriately.

## License

No license has been specified yet. A license should be added after the team agrees on the terms for sharing, modifying, and reusing the project.
