
# Existing Systems Comparison

**Project title:** Development of a System for Automatic Spelling Error Correction in Kazakh-Russian Mixed Texts with Subsequent Translation into Kazakh and English  
**Prepared by:** Zumrad Sherbadalova  
**Document status:** Updated desk-based comparison; test protocol and test cases prepared; empirical benchmark still pending  
**Sources checked:** 20 October 2026

## 1. Purpose and scope

This document compares five existing tools against the planned system's main workflow: accepting text that mixes Kazakh and Russian, identifying spelling errors, letting the user review suggested corrections, and translating the reviewed text into Kazakh or English.

The selected tools do not all serve the same purpose. Google Translate, Microsoft Translator, and DeepL are primarily translation tools; Microsoft Editor and LanguageTool are writing assistants. They are included because together they cover the two main parts of the proposed workflow: translation and writing assistance.

This is a comparison of publicly documented features, not a claim that the proposed system is better. A language being listed as supported does **not** prove that a tool can reliably identify language changes inside one sentence or correct misspellings in mixed Kazakh-Russian text. Those behaviours must be tested with the same examples across tools.

## 2. Systems reviewed

### 2.1 Google Translate

**Main purpose:** General-purpose text and document translation. Its web interface provides text translation and automatic source-language detection. The available language selector should be checked for the required source and target languages when testing.

**Relevance:** A baseline for translating text into Kazakh and English. It is not treated here as a dedicated spelling-correction system.

**Official sources:**
- [Google Translate](https://translate.google.kz/?hl=en)
- [Google Translate Help](https://support.google.com/translate?hl=en)

### 2.2 Microsoft Translator (Azure AI Translator)

**Main purpose:** Cloud translation for text and documents. Microsoft's language table lists Kazakh (`kk`) and Russian (`ru`) for cloud text translation. The language table distinguishes text translation from other features, so availability should be checked for the exact endpoint and language direction used.

**Relevance:** A potential translation baseline and a possible API-based alternative if the project later needs programmatic translation. API integration, pricing, access requirements, and exact source/target combinations should be checked before implementation.

**Official source:**
- [Microsoft Translator language support](https://learn.microsoft.com/en-us/azure/ai-services/translator/language-support)

### 2.3 DeepL Translator

**Main purpose:** General-purpose translation. DeepL's current supported-language page lists Kazakh, Russian, and English. The page notes that some features are not available for every language, so the required language pair and feature must be confirmed for the specific product/API before selection.

**Relevance:** An additional translation baseline. Its support for these languages does not establish how it will translate code-switched Kazakh-Russian input.

**Official source:**
- [DeepL Translator supported languages](https://support.deepl.com/hc/en-us/articles/360019925219-DeepL-Translator-languages)

### 2.4 Microsoft Editor

**Main purpose:** Writing assistance, including spelling and grammar checks in supported applications. Microsoft's language availability table lists spell checking for Kazakh and Russian. The table does not list grammar checking or writing refinements for Kazakh.

**Relevance:** A useful point of comparison for spelling suggestions. Support for each language separately does not prove that Editor can correctly handle a single text that switches between Kazakh and Russian.

**Official sources:**
- [Microsoft Editor feature overview](https://support.microsoft.com/en-us/word/microsoft-editor-checks-grammar-and-more-in-documents-mail-and-the-web)
- [Microsoft Editor language availability](https://support.microsoft.com/en-us/word/editor-s-spelling-grammar-and-refinement-availability-by-language)

### 2.5 LanguageTool

**Main purpose:** Spelling, grammar, and style checking. Its current help page lists Russian among the languages supported by the free version; Kazakh is not included in that list. The same page says the premium version supports the same languages, with additional checks for selected languages.

**Relevance:** A writing-assistance comparison, particularly for Russian text. Based on the reviewed language list, it is not a complete out-of-the-box solution for Kazakh-Russian mixed text.

**Official source:**
- [LanguageTool supported languages](https://help.languagetool.org/hc/en-us/articles/39254526141463-What-languages-does-LanguageTool-support)

## 3. Comparison criteria

Eight criteria were selected because they map to the system's core requirements:

1. **Primary purpose** — whether the tool focuses on translation or writing assistance.
2. **Kazakh support** — whether official documentation lists Kazakh for a relevant feature.
3. **Russian support** — whether official documentation lists Russian for a relevant feature.
4. **English support** — whether English is listed for a relevant feature.
5. **Translation into Kazakh and English** — whether translation is a documented feature and the target languages are listed.
6. **Spelling correction** — whether spelling suggestions/checking are documented.
7. **Mixed Kazakh-Russian handling** — whether the reviewed documentation explicitly confirms support for code-switching within one text.
8. **Integrated correction-review-translation workflow** — whether the cited feature documentation confirms all stages in one workflow.

### Legend

- **Yes** — explicitly supported by the official source reviewed for the stated feature.
- **Partial** — only part of the requirement is documented, or language/feature availability needs checking.
- **Not confirmed** — the reviewed official documentation does not establish the capability. This does not prove it is impossible.
- **No documented feature** — the source reviewed does not describe that feature as part of the product.

## 4. Comparison matrix

| Criterion | Google Translate | Microsoft Translator | DeepL Translator | Microsoft Editor | LanguageTool |
|---|---|---|---|---|---|
| 1. Primary purpose | Translation | Translation | Translation | Writing assistance | Writing assistance |
| 2. Kazakh support | Listed in the translation interface; verify pair during testing | Yes for cloud text translation (`kk`) | Listed; check exact pair and feature | Spell check: yes; grammar/refinements: not listed for Kazakh | Not listed in reviewed free-language list; premium lists the same languages |
| 3. Russian support | Listed in the translation interface | Yes for cloud text translation (`ru`) | Listed | Spell check, grammar check, and refinements listed | Listed in supported languages |
| 4. English support | Yes | Yes | Yes | Spell check, grammar check, and refinements listed | Yes |
| 5. Translation into Kazakh and English | Yes; confirm selected pair in interface | Yes; both languages are listed for cloud text translation | Both languages are listed; confirm exact pair and feature availability | No translation feature documented in cited sources | No translation feature documented in cited source |
| 6. Spelling correction | No dedicated spelling-correction workflow established by the reviewed sources | No dedicated spelling-correction workflow established by the reviewed language-support page | No dedicated spelling-correction workflow established by the reviewed source | Yes, for listed languages | Yes, for supported languages |
| 7. Explicit mixed Kazakh-Russian handling | Not confirmed | Not confirmed | Not confirmed | Not confirmed | Not confirmed; Kazakh is absent from the reviewed language list |
| 8. One integrated correction-review-translation workflow | Not confirmed | Not confirmed | Not confirmed | Not documented in cited sources | Not documented in cited source |

**Interpretation note:** This matrix compares documented features, not measured accuracy. A “not confirmed” entry should not be read as a proven product limitation. The systems also differ in purpose, so the table is not a claim that they are directly interchangeable.

## 5. Findings and implications for the project

1. **Translation is already available in several tools.** Google Translate, Microsoft Translator, and DeepL list the languages relevant to the project. Therefore, the project's contribution should not be described simply as “translating Kazakh and Russian text.”
2. **Spelling support varies by language and product.** Microsoft Editor lists Kazakh spell checking as well as Russian spelling and grammar checking. LanguageTool's reviewed language list includes Russian but not Kazakh.
3. **Code-switching remains an open evaluation question.** The reviewed feature lists do not establish reliable correction or translation of sentences that alternate between Kazakh and Russian, particularly when misspellings are present.
4. **The potential contribution is the integrated workflow.** The proposed system aims to combine mixed-text spelling correction, user review of suggested changes, and translation of the reviewed text into Kazakh or English. This is a design objective to validate, not a proven claim that no existing product offers similar functionality.
5. **A practical benchmark is needed.** Feature lists alone are insufficient to claim a performance advantage. The same controlled examples should be tested across selected tools and the results recorded.

## 6. Recommended practical comparison

This practical comparison is a proposed next step; it has **not** yet been conducted and no results are claimed here.

### 6.1 Prepare a small test set

Create a documented set of examples containing:

- correctly written Kazakh-only text;
- correctly written Russian-only text;
- sentences that alternate between Kazakh and Russian;
- intentional spelling mistakes in Kazakh words;
- intentional spelling mistakes in Russian words;
- mixed-language sentences containing both a spelling mistake and code-switching.

For every example, keep the original input and a manually reviewed reference version. Avoid using personal or confidential text.

### 6.2 Run comparable tests

For each tool, record:

- whether the tool accepts the input;
- whether it identifies the source language correctly, if applicable;
- which spelling suggestions it offers, if any;
- whether the original meaning is preserved after correction;
- the translation into Kazakh and English, where supported;
- obvious omissions, mistranslations, or changes to the intended meaning;
- whether correction and translation require separate manual steps;
- the date, interface/API used, and any relevant settings.

Do not mark a tool as failing solely because the documentation does not mention code-switching. Record only observed test outcomes as results.

### 6.3 Suggested evaluation measures

- **Correction precision:** proportion of proposed corrections that are appropriate.
- **Correction recall:** proportion of known errors that the tool correctly identifies or fixes.
- **Meaning preservation:** human assessment of whether the corrected sentence preserves the intended meaning.
- **Translation quality:** human review against a reference translation; automated metrics such as chrF or BLEU may be added if suitable references and a consistent evaluation setup are available.
- **Workflow effort:** number of manual steps needed to go from original mixed text to reviewed text translated into the target language.

Define the scoring rules before evaluating the examples and report the size and composition of the test set. Do not report scores until tests have actually been performed.


### 6.4 Test cases prepared for the empirical benchmark

The following small starter set is intended for a pilot test. It is not a substitute for a larger, independently reviewed dataset. The mixed-language examples are illustrative and should be checked by a fluent Kazakh-Russian speaker before they are treated as gold-standard references. Do not count the examples below as test results.

| ID | Test category | Input text | Expected check | Reference / notes |
|---|---|---|---|---|
| T01 | Kazakh, no intentional error | `Мен бүгін университетке барамын.` | Does the tool preserve the sentence's meaning? | Reference: unchanged text is acceptable. |
| T02 | Russian, no intentional error | `Сегодня я иду в университет.` | Does the tool preserve the sentence's meaning? | Reference: unchanged text is acceptable. |
| T03 | Kazakh spelling error | `Мен бугін университетке барамын.` | Does a writing assistant flag `бугін`? | Candidate correction: `бүгін`; validate with a fluent speaker. |
| T04 | Russian spelling error | `Я сегоднЯ иду в университет.` | Does a writing assistant flag the misspelling/capitalization issue? | Candidate correction: `Я сегодня иду в университет.` |
| T05 | Code-switching, no intentional error | `Бүгін у меня лекция в университете.` | Does the tool preserve both languages rather than translating or rewriting unexpectedly? | Mixed-language behaviour is an observation, not an assumed capability. |
| T06 | Code-switching + likely Kazakh typo | `Мен бугін на пару барамын.` | Does the tool identify the Kazakh spelling error without damaging Russian words? | Candidate correction: `Мен бүгін на пару барамын.` Validate naturalness with a fluent speaker. |
| T07 | Code-switching + Russian typo | `Мен бүгін пойду в универститет.` | Does the tool identify the Russian typo without changing the Kazakh segment? | Candidate correction: `Мен бүгін пойду в университет.` Validate naturalness with a fluent speaker. |
| T08 | Translation to English | `Мен бүгін университетке барамын.` | Is the English translation faithful to the source? | A human-reviewed reference translation is required before scoring. |
| T09 | Translation to Kazakh | `Сегодня я иду в университет.` | Is the Kazakh translation faithful to the source? | A human-reviewed reference translation is required before scoring. |
| T10 | Mixed-text translation | `Бүгін у меня лекция в университете.` | Does the translation preserve the intended meaning of both language segments? | Record output and reviewer comments; do not assume success/failure in advance. |

### Blank observation log

Fill in this log only after running each tool on the same input. Use `N/A` where a feature is not offered. Save exact outputs or screenshots separately if permitted by the course rules.

| Tool | Test ID | Input accepted? | Suggested correction / output | Meaning preserved? (Y/N/Unclear) | Error or note | Date / settings |
|---|---|---|---|---|---|---|
| Google Translate | T01–T10 | To be tested | To be recorded | To be reviewed | To be recorded | To be recorded |
| Microsoft Translator | T01–T10 | To be tested | To be recorded | To be reviewed | To be recorded | To be recorded |
| DeepL | T01–T10 | To be tested | To be recorded | To be reviewed | To be recorded | To be recorded |
| Microsoft Editor | T01–T10 | To be tested | To be recorded | To be reviewed | To be recorded | To be recorded |
| LanguageTool | T01–T10 | To be tested | To be recorded | To be reviewed | To be recorded | To be recorded |

### Scoring rules to decide before testing

- **Correction precision** = appropriate proposed corrections ÷ all proposed corrections reviewed. If a tool proposes no corrections, mark this metric `N/A`, not zero.
- **Correction recall** = known errors correctly flagged or fixed ÷ all known errors in the test set. Define in advance whether a flag and an accepted correction count equally.
- **Meaning preservation** = count of outputs judged to preserve meaning ÷ outputs reviewed. Use at least one fluent reviewer for Kazakh-Russian examples; record disagreements.
- **Translation quality** = human rating against a reference translation. If an automatic metric such as chrF or BLEU is used, document the tool/version, reference translations, and tokenization setup; do not compare scores from inconsistent setups.
- **Workflow effort** = number of user actions or separate tools needed to reach a reviewed and translated result. Define what counts as an action before counting.

Report the number of examples, tool version/interface, language direction, date, settings, and reviewer method with any eventual results. A small pilot set can reveal obvious issues but is not sufficient by itself to support broad claims about overall product quality.


## 8. Limitations

- This is a desk-based comparison of official product documentation, not a benchmark of output quality.
- Product features, supported languages, and API conditions can change; verify them again before final submission and implementation.
- Support for Kazakh and Russian individually does not establish support for code-switching within one sentence.
- Availability of a language does not necessarily mean that every feature, API endpoint, or language direction is available under the same conditions.
- The comparison does not prove that no competing system integrates correction and translation. The project's novelty claim should be refined after practical testing and literature review.

## 9. Conclusion

The reviewed tools cover important parts of the proposed workflow, but the available official documentation does not establish that they reliably correct spelling in mixed Kazakh-Russian text and then translate the reviewed text into Kazakh or English in one integrated process. The project should therefore focus its evaluation on the specific mixed-language use case and the usability of the integrated correction-review-translation workflow. Practical testing is required before making stronger claims about gaps in existing systems or the proposed system's advantages.

## 10. References

1. Google Translate. Official web interface. https://translate.google.kz/?hl=en (accessed 20 October 2026).
2. Google Translate Help. https://support.google.com/translate?hl=en (accessed 20 October 2026).
3. Microsoft Learn. *Microsoft Translator language support*. https://learn.microsoft.com/en-us/azure/ai-services/translator/language-support (accessed 20 October 2026).
4. DeepL Help Center. *DeepL Translator languages*. https://support.deepl.com/hc/en-us/articles/360019925219-DeepL-Translator-languages (accessed 20 October 2026).
5. Microsoft Support. *Microsoft Editor checks grammar and more in documents, mail, and the web*. https://support.microsoft.com/en-us/word/microsoft-editor-checks-grammar-and-more-in-documents-mail-and-the-web (accessed 20 October 2026).
6. Microsoft Support. *Editor's spelling, grammar, and refinement availability by language*. https://support.microsoft.com/en-us/word/editor-s-spelling-grammar-and-refinement-availability-by-language (accessed 20 October 2026).
7. LanguageTool Help Center. *What languages does LanguageTool support?* https://help.languagetool.org/hc/en-us/articles/39254526141463-What-languages-does-LanguageTool-support (accessed 20 October 2026).
