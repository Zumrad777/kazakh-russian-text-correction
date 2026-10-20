# Technology Comparison

**Project title:** Development of a System for Automatic Spelling Error
Correction in Kazakh-Russian Mixed Texts with Subsequent Translation
into Kazakh and English\
**Prepared by:** Zumrad Sherbadalova\
**Document status:** Preliminary technology evaluation; final choices
should be validated with a small prototype and the project's test set.

## 1. Purpose

This document compares candidate technologies for the main technical
decisions in the proposed system. The planned workflow is:

1.  Accept text that may contain Kazakh and Russian in the same passage.
2.  Detect and suggest possible spelling corrections.
3.  Let the user review or reject suggested corrections.
4.  Translate the reviewed text into Kazakh or English.
5.  Show the corrected text and translation.

Support for Kazakh and Russian separately does **not** prove that a
technology can reliably correct or translate code-switched text within
the same sentence. This is a key risk and must be tested using the same
examples across alternatives.

## 2. Decision A --- Spelling correction approach

  -----------------------------------------------------------------------
  Alternative       Advantages        Limitations and   Suitability for
                                      risks             this project
  ----------------- ----------------- ----------------- -----------------
  **Dictionary +    Lightweight; easy Needs             **Recommended
  RapidFuzz**       to explain; can   dictionaries and  baseline for the
                    rank words by     thresholds; may   first
                    string            suggest incorrect prototype.**
                    similarity;       changes for       Build separate
                    supports a        names, slang,     Kazakh and
                    user-controlled   loanwords, and    Russian word
                    suggestion list;  words from the    lists where
                    practical for a   other language;   possible,
                    student           does not          preserve the
                    prototype.        understand        original text,
                                      sentence meaning  and let users
                                      by itself.        accept or reject
                                                        suggestions.

  **SymSpell**      Designed for fast Requires suitable A useful
                    spelling          dictionaries and  alternative to
                    correction using  configuration;    benchmark against
                    deletion-based    may not handle    the RapidFuzz
                    lookup; can be    mixed-language    baseline if
                    efficient with a  context or        implementation
                    prepared          morphology        time allows.
                    dictionary.       correctly without 
                                      extra logic;      
                                      dictionary        
                                      coverage is a     
                                      dependency.       

  **Contextual      Can use           More complex to   Consider only if
  language model**  surrounding       integrate and     the simpler
                    context to        evaluate; may     baseline performs
                    propose           rewrite correct   poorly and there
                    corrections       text or change    is enough time to
                    beyond simple     meaning; language evaluate it
                    character         and               safely.
                    similarity.       code-switching    
                                      quality must be   
                                      verified; may     
                                      require more      
                                      compute or an     
                                      external service. 
  -----------------------------------------------------------------------

**Preliminary choice:** Start with a dictionary-based correction
pipeline using RapidFuzz to rank candidate words. Do not automatically
replace the user's text. Display suggestions and allow the user to
accept or reject them. Compare the approach with SymSpell on a shared
test set before making a final performance claim.

## 3. Decision B --- Translation engine

  ------------------------------------------------------------------------
  Alternative       Advantages         Limitations and   Suitability for
                                       risks             this project
  ----------------- ------------------ ----------------- -----------------
  **Meta NLLB-200** Research model     Deployment can    **Recommended
                    designed for       require           research
                    multilingual       significant       candidate** for a
                    translation; the   memory and setup; prototype if it
                    official project   supported         runs within
                    lists Kazakh and   language pairs do available
                    English among      not guarantee     hardware and its
                    supported          good results on   licence is
                    languages and      code-switched     suitable. Test
                    provides model and text; model       Kazakh, Russian,
                    evaluation         licence and       and mixed
                    resources. Can be  intended-use      passages
                    explored without   limitations must  separately.
                    committing to a    be reviewed       
                    commercial         before use.       
                    translation API.                     

  **Google Cloud    Managed            Requires a cloud  Strong candidate
  Translation**     translation        setup and         for a
                    service with       credentials;      hosted-service
                    official           usage may incur   baseline if
                    language-support   charges; data is  access, privacy
                    documentation;     sent to an        requirements, and
                    avoids hosting a   external service; budget permit.
                    translation model  availability and  
                    locally.           quality must be   
                                       checked for the   
                                       exact language    
                                       pairs and text    
                                       types.            

  **Microsoft       Managed API with   Requires an Azure Another
  Translator (Azure official           resource and      hosted-service
  AI Translator)**  language-support   credentials; may  baseline; compare
                    documentation;     incur charges;    actual output
                    Kazakh and Russian support for       quality, setup
                    are listed as      individual        effort, and cost
                    supported          languages does    before choosing.
                    languages.         not establish     
                                       robust            
                                       performance on    
                                       mixed             
                                       Kazakh-Russian    
                                       sentences.        
  ------------------------------------------------------------------------

**Preliminary choice:** Evaluate NLLB-200 as the first research
candidate and compare it with at least one available hosted translator.
The final choice must depend on test results, hardware, licence,
privacy, and budget---not language-support lists alone.

## 4. Decision C --- Application interface and integration

  ------------------------------------------------------------------------
  Alternative       Advantages         Limitations and   Suitability for
                                       risks             this project
  ----------------- ------------------ ----------------- -----------------
  **Python          Fastest way to     Less accessible   Useful for an
  command-line      validate           to non-technical  early proof of
  prototype**       correction and     users; not a      concept and
                    translation        polished          repeatable
                    functions; simple  user-facing       experiments.
                    to test; minimal   interface.        
                    interface work.                      

  **Flask web       Lightweight web    Requires explicit Suitable for a
  application**     framework;         decisions about   small web demo if
                    sufficient for a   validation, error the team prefers
                    small form-based   handling, and     a minimal
                    interface;         project structure framework.
                    relatively         as the            
                    straightforward to application       
                    learn.             grows.            

  **FastAPI         Supports typed     Adds API and      **Recommended if
  application**     request/response   server concepts   the system will
                    models and         that may be       expose correction
                    automatic API      unnecessary for a and translation
                    documentation;     very small        as separate API
                    useful for         prototype; still  endpoints.** A
                    separating backend requires          simple web
                    functions from a   interface work if interface can be
                    future interface.  users need a      added later.
                                       browser form.     
  ------------------------------------------------------------------------

**Preliminary choice:** Implement and test the core correction and
translation functions independently first. If the team needs a
browser-based demo, use FastAPI for a small API or Flask for a simpler
form-based application. Confirm the choice with the team's skills and
implementation deadline.

## 5. Comparison criteria and decision method

The alternatives should be assessed using the same criteria:

-   **Language suitability:** Kazakh and Russian support, including
    mixed passages.
-   **Correction quality:** proportion of intended errors corrected and
    proportion of suggestions that are actually correct.
-   **Translation quality:** meaning preservation, adequacy, and
    fluency, assessed with human review and an appropriate automatic
    metric where feasible.
-   **User control:** whether suggestions can be reviewed before the
    original text is changed.
-   **Integration effort:** time and complexity needed to connect the
    tool to the application.
-   **Cost and access:** local hardware needs, API charges, account
    requirements, and connectivity.
-   **Privacy and licence:** where input text is processed and whether
    the tool's licence permits the intended project use.
-   **Reproducibility:** whether the team can repeat the same test cases
    and record the versions/settings used.

No scores are assigned yet because the team has not completed the
benchmark. Do not interpret the preliminary recommendations as measured
evidence of superior accuracy.

## 6. Initial validation plan

1.  Prepare a small shared test set with clean Kazakh, clean Russian,
    mixed Kazakh-Russian passages, intentional spelling errors, names,
    slang, and sentences containing no errors.
2.  Keep the original input and record each tool's output without
    manually changing the result.
3.  For spelling correction, record intended errors corrected, incorrect
    changes, missed errors, and suggestions accepted by a reviewer.
4.  For translation, use the same source texts and target languages for
    every available alternative. Have a reviewer check meaning
    preservation and fluency; record any automatic metric and its
    configuration if used.
5.  Record tool/model version, language settings, date, latency, setup
    difficulty, and any cost or hardware constraints.
6.  Compare the results before finalizing the technology choices. If a
    service or model cannot be accessed, mark it as not tested rather
    than inventing results.

## 7. Preliminary recommendation

For a manageable first prototype, use a transparent dictionary-based
spelling-correction baseline with RapidFuzz, preserve user control over
corrections, and evaluate NLLB-200 alongside an accessible translation
service. Keep the core functions modular so the translation engine or
correction approach can be replaced after evaluation. A small API can be
added after the correction and translation pipeline works independently.

These are provisional choices, not final empirical conclusions. The
project should report actual test results and limitations after running
the planned evaluation.

## 8. Official references

1.  RapidFuzz documentation: https://rapidfuzz.github.io/RapidFuzz/
2.  SymSpell repository and documentation:
    https://github.com/wolfgarbe/SymSpell
3.  Meta AI, No Language Left Behind (NLLB):
    https://ai.meta.com/research/no-language-left-behind/
4.  Google Cloud Translation --- language support:
    https://docs.cloud.google.com/translate/docs/languages
5.  Microsoft Azure AI Translator --- language support:
    https://learn.microsoft.com/en-us/azure/ai-services/translator/language-support
6.  Flask documentation: https://flask.palletsprojects.com/
7.  FastAPI documentation: https://fastapi.tiangolo.com/

**Accessed:** 20 October 2026. Check current documentation, licence
terms, pricing, and availability again before implementation.
