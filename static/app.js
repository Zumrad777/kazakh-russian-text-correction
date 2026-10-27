const $ = (id) => document.getElementById(id);
const source = $("sourceText");
const corrected = $("correctedText");
const translated = $("translatedText");
let reviewedText = "";
let latestSuggestion = "";

source.addEventListener("input", () => {
  $("count").textContent = `${source.value.length} / 5000 characters`;
  showMessage("correctionMessage", "");
});
function showMessage(id, message, kind = "") {
  const el = $(id); el.textContent = message; el.className = "message" + (kind ? " " + kind : "");
}
async function getJSON(path) {
  const response = await fetch(path);
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(data.detail || `Request failed (${response.status})`);
  return data;
}
async function postJSON(path, body) {
  const response = await fetch(path, {
    method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(body)
  });
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(data.detail || `Request failed (${response.status})`);
  return data;
}
for (const button of document.querySelectorAll("[data-example]")) {
  button.addEventListener("click", () => {
    source.value = button.dataset.example;
    source.dispatchEvent(new Event("input"));
    source.focus();
  });
}
$("correctBtn").addEventListener("click", async () => {
  const text = source.value.trim();
  if (!text) { showMessage("correctionMessage", "Please enter some text first.", "error"); source.focus(); return; }
  const btn = $("correctBtn"); btn.disabled = true; btn.textContent = "Checking…";
  showMessage("correctionMessage", "");
  try {
    const data = await postJSON("/api/correct", {text});
    latestSuggestion = data.corrected_text;
    corrected.value = latestSuggestion;
    $("acceptBtn").disabled = false; $("keepBtn").disabled = false;
    const note = data.changes.length ? `Suggested changes: ${data.changes.join("; ")}` : "No changes suggested.";
    showMessage("correctionMessage", note, "success");
    showMessage("reviewMessage", "Review the suggestion, then accept it or keep your original text.");
    reviewedText = ""; translated.value = ""; $("translateBtn").disabled = true;
    showMessage("translationMessage", "");
  } catch (e) {
    showMessage("correctionMessage", `Could not connect to the API: ${e.message}. Is the server running?`, "error");
  } finally { btn.disabled = false; btn.innerHTML = 'Suggest corrections <span>→</span>'; }
});
$("acceptBtn").addEventListener("click", () => {
  reviewedText = latestSuggestion;
  showMessage("reviewMessage", "Correction accepted. You can translate this text.", "success");
  $("translateBtn").disabled = !reviewedText;
});
$("keepBtn").addEventListener("click", () => {
  reviewedText = source.value.trim(); corrected.value = reviewedText;
  showMessage("reviewMessage", "Original text kept. You can translate it.", "success");
  $("translateBtn").disabled = !reviewedText;
});
$("translateBtn").addEventListener("click", async () => {
  if (!reviewedText) { showMessage("translationMessage", "Accept a suggestion or keep the original text first.", "error"); return; }
  const btn = $("translateBtn"); btn.disabled = true; btn.textContent = "Translating…";
  translated.value = ""; showMessage("translationMessage", "");
  try {
    const data = await postJSON("/api/translate", {text: reviewedText, source_language: $("sourceLanguage").value, target_language: $("targetLanguage").value});
    translated.value = data.translated_text;
    showMessage("translationMessage", "Translation complete.", "success");
  } catch (e) {
    showMessage("translationMessage", e.message, "error");
  } finally { btn.disabled = false; btn.innerHTML = 'Translate text <span>→</span>'; }
});

function validateLanguages() { const same = $("sourceLanguage").value === $("targetLanguage").value; $("translateBtn").title = same ? "Choose different source and target languages" : ""; }
$("sourceLanguage").addEventListener("change", validateLanguages); $("targetLanguage").addEventListener("change", validateLanguages); validateLanguages();
