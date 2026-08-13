// static/app.js
/**
 * BridgeTutor AI Agent Frontend Script.
 * Connects with FastAPI backend endpoints for curriculum graph navigation, problem generation, math validation, hints, and analytics.
 */

document.addEventListener("DOMContentLoaded", () => {
  // UI State
  let currentStudentId = "highschool_student_1";
  let activeConceptId = null;
  let currentProblem = null;
  let curriculumGraph = {};

  // DOM Elements
  const studentSelect = document.getElementById("studentIdSelect");
  const masteryScoreEl = document.getElementById("masteryScore");
  const graphContainer = document.getElementById("graphContainer");

  const conceptTag = document.getElementById("conceptTag");
  const conceptEvalType = document.getElementById("conceptEvalType");
  const conceptTitle = document.getElementById("conceptTitle");
  const conceptDesc = document.getElementById("conceptDesc");
  const resourceBox = document.getElementById("resourceBox");
  const resourceLink = document.getElementById("resourceLink");

  const questionContainer = document.getElementById("questionContainer");
  const answerForm = document.getElementById("answerForm");
  const studentAnswerInput = document.getElementById("studentAnswerInput");
  const btnSubmitAnswer = document.getElementById("btnSubmitAnswer");
  const btnGetHint = document.getElementById("btnGetHint");
  const btnNewProblem = document.getElementById("btnNewProblem");
  const btnResetData = document.getElementById("btnResetData");
  const btnRefreshAnalytics = document.getElementById("btnRefreshAnalytics");

  const feedbackAlert = document.getElementById("feedbackAlert");
  const feedbackStatus = document.getElementById("feedbackStatus");
  const feedbackText = document.getElementById("feedbackText");

  const hintAccordion = document.getElementById("hintAccordion");
  const hintLevel1 = document.getElementById("hintLevel1");
  const hintLevel2 = document.getElementById("hintLevel2");
  const hintLevel3 = document.getElementById("hintLevel3");

  const statMastered = document.getElementById("statMastered");
  const statRate = document.getElementById("statRate");
  const statGaps = document.getElementById("statGaps");
  const gapsList = document.getElementById("gapsList");
  const historyTableBody = document.getElementById("historyTableBody");

  // --- 1. INITIALIZATION ---
  init();

  function init() {
    currentStudentId = studentSelect.value;
    loadCurriculumGraph();
    loadStudentAnalytics();

    studentSelect.addEventListener("change", (e) => {
      currentStudentId = e.target.value;
      loadCurriculumGraph();
      loadStudentAnalytics();
    });

    btnResetData.addEventListener("click", resetStudentState);
    btnRefreshAnalytics.addEventListener("click", loadStudentAnalytics);
    btnNewProblem.addEventListener("click", fetchNewProblem);
    btnGetHint.addEventListener("click", fetchDiagnosticHint);
    answerForm.addEventListener("submit", handleAnswerSubmission);
  }

  // --- 2. CURRICULUM GRAPH FETCHING & RENDERING ---
  async function loadCurriculumGraph() {
    try {
      const res = await fetch(`/api/curriculum?student_id=${encodeURIComponent(currentStudentId)}`);
      const data = await res.json();
      curriculumGraph = data.graph;
      renderCurriculumGraph(data.graph, data.ordered_concepts);
    } catch (err) {
      console.error("Failed to load curriculum:", err);
      graphContainer.innerHTML = `<div class="error-text">Failed to connect to backend server.</div>`;
    }
  }

  function renderCurriculumGraph(graph, orderedConcepts) {
    graphContainer.innerHTML = "";

    orderedConcepts.forEach((conceptId) => {
      const node = graph[conceptId];
      const nodeEl = document.createElement("div");
      nodeEl.className = `node-card ${node.status}`;
      if (conceptId === activeConceptId) nodeEl.classList.add("active");

      let statusBadgeText = "LOCKED";
      let statusClass = "status-locked";
      if (node.status === "mastered") {
        statusBadgeText = "⭐ MASTERED";
        statusClass = "status-mastered";
      } else if (node.status === "unlocked" || node.status === "in_progress") {
        statusBadgeText = "UNLOCKED";
        statusClass = "status-unlocked";
      }

      let prereqText = "Prerequisites: None";
      if (node.prerequisites && node.prerequisites.length > 0) {
        const prereqNames = node.prerequisites
          .map((p) => graph[p] ? graph[p].friendly_name : p)
          .join(", ");
        prereqText = `Prereqs: ${prereqNames}`;
      }

      nodeEl.innerHTML = `
        <div class="node-title-row">
          <h4>${node.friendly_name}</h4>
          <span class="badge-status ${statusClass}">${statusBadgeText}</span>
        </div>
        <div class="node-prereq-list">${prereqText}</div>
      `;

      if (node.status !== "locked") {
        nodeEl.addEventListener("click", () => selectConceptNode(conceptId));
      }

      graphContainer.appendChild(nodeEl);
    });

    // Auto-select first unlocked concept if none selected
    if (!activeConceptId && orderedConcepts.length > 0) {
      const firstUnlocked = orderedConcepts.find((id) => graph[id].status !== "locked");
      if (firstUnlocked) selectConceptNode(firstUnlocked);
    }
  }

  // --- 3. CONCEPT SELECTION & PROBLEM FETCHING ---
  function selectConceptNode(conceptId) {
    activeConceptId = conceptId;
    const node = curriculumGraph[conceptId];
    if (!node) return;

    // Highlight active node in graph
    document.querySelectorAll(".node-card").forEach((el) => el.classList.remove("active"));
    loadCurriculumGraph();

    conceptTitle.textContent = node.friendly_name;
    conceptDesc.textContent = node.description;
    conceptEvalType.textContent = node.eval_type.toUpperCase();

    if (node.resources && node.resources.url) {
      resourceBox.classList.remove("hidden");
      resourceLink.href = node.resources.url;
      resourceLink.textContent = `${node.resources.title} ↗`;
    } else {
      resourceBox.classList.add("hidden");
    }

    fetchNewProblem();
  }

  async function fetchNewProblem() {
    if (!activeConceptId) return;

    // Reset UI states
    feedbackAlert.classList.add("hidden");
    hintAccordion.classList.add("hidden");
    studentAnswerInput.value = "";
    studentAnswerInput.disabled = false;
    btnSubmitAnswer.disabled = false;
    btnGetHint.disabled = false;
    studentAnswerInput.focus();

    questionContainer.innerHTML = `<p class="placeholder-text">Generating problem...</p>`;

    try {
      const res = await fetch(`/api/problem/${activeConceptId}`);
      currentProblem = await res.json();
      renderQuestion(currentProblem);
    } catch (err) {
      console.error("Problem generation error:", err);
      questionContainer.innerHTML = `<p class="error-text">Error fetching problem.</p>`;
    }
  }

  function renderQuestion(prob) {
    questionContainer.innerHTML = "";
    const p = document.createElement("p");
    p.textContent = prob.question;
    questionContainer.appendChild(p);

    // Try rendering KaTeX math if tex string exists
    if (prob.tex_question && window.katex) {
      try {
        const mathSpan = document.createElement("div");
        mathSpan.style.marginTop = "0.5rem";
        katex.render(prob.tex_question, mathSpan, { throwOnError: false, displayMode: true });
        questionContainer.appendChild(mathSpan);
      } catch (e) {
        console.warn("KaTeX render error:", e);
      }
    }
  }

  // --- 4. ANSWER VERIFICATION & HINTING ---
  async function handleAnswerSubmission(e) {
    e.preventDefault();
    const answer = studentAnswerInput.value.trim();
    if (!answer || !currentProblem) return;

    btnSubmitAnswer.disabled = true;

    try {
      const res = await fetch("/api/verify", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          student_id: currentStudentId,
          concept_id: activeConceptId,
          target_value: currentProblem.target_value,
          student_answer: answer,
          question_text: currentProblem.question,
          eval_type: currentProblem.eval_type
        })
      });

      const data = await res.json();
      btnSubmitAnswer.disabled = false;

      feedbackAlert.classList.remove("hidden");
      if (data.is_correct) {
        feedbackAlert.className = "alert-box alert-success";
        feedbackStatus.textContent = "🎉 Correct!";
        feedbackText.textContent = data.feedback;
        hintAccordion.classList.add("hidden");

        // Reload graph & analytics to reflect new mastery / attempt
        loadCurriculumGraph();
        loadStudentAnalytics();

        // Auto-generate next problem after 1.2 seconds so user doesn't have to click
        setTimeout(() => {
          fetchNewProblem();
        }, 1200);
      } else {
        feedbackAlert.className = "alert-box alert-danger";
        feedbackStatus.textContent = "❌ Not Quite Right";
        feedbackText.textContent = data.feedback;

        if (data.diagnosis) {
          renderDiagnosticHints(data.diagnosis);
        }
        loadStudentAnalytics();
      }
    } catch (err) {
      console.error("Verification error:", err);
      btnSubmitAnswer.disabled = false;
    }
  }

  async function fetchDiagnosticHint() {
    if (!currentProblem) return;
    const studentAns = studentAnswerInput.value.trim();

    try {
      const res = await fetch("/api/hint", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          eval_type: currentProblem.eval_type,
          target_value: currentProblem.target_value,
          student_answer: studentAns,
          explanation: currentProblem.explanation
        })
      });

      const diag = await res.json();
      renderDiagnosticHints(diag);
    } catch (err) {
      console.error("Hint error:", err);
    }
  }

  function renderDiagnosticHints(diag) {
    hintAccordion.classList.remove("hidden");
    hintLevel1.textContent = diag.hint_level1;
    hintLevel2.textContent = diag.hint_level2;
    hintLevel3.textContent = diag.hint_level3;
  }

  // --- 5. ANALYTICS & STATE MANAGEMENT ---
  async function loadStudentAnalytics() {
    try {
      const res = await fetch(`/api/student/${encodeURIComponent(currentStudentId)}`);
      const data = await res.json();

      masteryScoreEl.textContent = `${data.mastery_rate}%`;
      statMastered.textContent = `${data.mastered_count} / ${data.total_topics}`;
      statRate.textContent = `${data.mastery_rate}%`;
      statGaps.textContent = data.gaps.length;

      // Render Knowledge Gaps
      gapsList.innerHTML = "";
      if (data.gaps.length === 0) {
        gapsList.innerHTML = `<p class="empty-state">No active knowledge gaps recorded. Excellent progress!</p>`;
      } else {
        data.gaps.forEach((gap) => {
          const gapEl = document.createElement("div");
          gapEl.className = "gap-item";
          gapEl.innerHTML = `
            <div class="gap-info">
              <h5>❌ ${gap.friendly_name}</h5>
              <p>Stuck after ${gap.attempts} attempt(s) | Correct: ${gap.correct_count}</p>
            </div>
            ${gap.resources.url ? `<a href="${gap.resources.url}" target="_blank" class="btn-secondary">Watch Video ↗</a>` : ''}
          `;
          gapsList.appendChild(gapEl);
        });
      }

      // Render Recent Attempts History
      historyTableBody.innerHTML = "";
      if (data.recent_attempts.length === 0) {
        historyTableBody.innerHTML = `<tr><td colspan="4" class="empty-state">No recent practice attempts.</td></tr>`;
      } else {
        data.recent_attempts.forEach((att) => {
          const tr = document.createElement("tr");
          const icon = att.is_correct ? "✅ Pass" : "❌ Incorrect";
          tr.innerHTML = `
            <td style="color: ${att.is_correct ? 'var(--success)' : 'var(--danger)'}">${icon}</td>
            <td><strong>${att.concept_name}</strong></td>
            <td><code>${att.student_answer || '(empty)'}</code></td>
            <td>${att.timestamp}</td>
          `;
          historyTableBody.appendChild(tr);
        });
      }
    } catch (err) {
      console.error("Analytics load error:", err);
    }
  }

  async function resetStudentState() {
    if (!confirm(`Are you sure you want to reset all learning progress for '${currentStudentId}'?`)) return;

    try {
      await fetch("/api/reset", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ student_id: currentStudentId })
      });
      loadCurriculumGraph();
      loadStudentAnalytics();
      fetchNewProblem();
    } catch (err) {
      console.error("Reset error:", err);
    }
  }
});
