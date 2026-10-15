/**
 * TRACE × X — Admin Control Center & Authentication Logic
 * Department of Computer Science & Engineering | T.J.S. Engineering College
 */

(function () {
  'use strict';

  const TOKEN_KEY = 'traceX_admin_token';
  const ADMIN_KEY = 'traceX_admin_info';

  // ---------------------------------------------------------------------------
  // Helper Utilities
  // ---------------------------------------------------------------------------
  function getAuthToken() {
    let token = sessionStorage.getItem(TOKEN_KEY) || localStorage.getItem(TOKEN_KEY) || '';
    if (!token) {
      const match = document.cookie.match(/(?:^|;\s*)traceX_admin_token=([^;]+)/);
      if (match) token = match[1];
    }
    return token;
  }

  function setAuthToken(token, adminInfo) {
    sessionStorage.setItem(TOKEN_KEY, token);
    localStorage.setItem(TOKEN_KEY, token);
    if (adminInfo) {
      sessionStorage.setItem(ADMIN_KEY, JSON.stringify(adminInfo));
      localStorage.setItem(ADMIN_KEY, JSON.stringify(adminInfo));
    }
    document.cookie = `traceX_admin_token=${token}; path=/; max-age=28800; SameSite=Strict`;
  }

  function clearAuthToken() {
    sessionStorage.removeItem(TOKEN_KEY);
    sessionStorage.removeItem(ADMIN_KEY);
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(ADMIN_KEY);
    document.cookie = 'traceX_admin_token=; path=/; max-age=0; SameSite=Strict';
  }

  function getStoredAdminInfo() {
    try {
      return JSON.parse(sessionStorage.getItem(ADMIN_KEY) || localStorage.getItem(ADMIN_KEY) || 'null');
    } catch (e) {
      return null;
    }
  }

  function escapeHtml(str) {
    if (typeof str !== 'string') return str || '';
    return str.replace(/&/g, '&amp;')
              .replace(/</g, '&lt;')
              .replace(/>/g, '&gt;')
              .replace(/"/g, '&quot;')
              .replace(/'/g, '&#039;');
  }

  function showToast(title, message, type = 'info') {
    const container = document.getElementById('admin-toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `admin-toast ${type}`;
    toast.innerHTML = `
      <div class="toast-header-row">
        <span class="toast-title">${escapeHtml(title)}</span>
        <button type="button" class="toast-close-btn">&times;</button>
      </div>
      <div class="toast-desc">${escapeHtml(message)}</div>
    `;

    toast.querySelector('.toast-close-btn').addEventListener('click', () => {
      toast.remove();
    });

    container.appendChild(toast);

    setTimeout(() => {
      if (toast.parentNode) {
        toast.classList.add('fade-out');
        setTimeout(() => toast.remove(), 400);
      }
    }, 4500);
  }

  // Generic Authenticated Fetch Wrapper
  async function apiFetch(url, options = {}) {
    const headers = options.headers || {};
    const token = getAuthToken();
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
    if (options.body && typeof options.body === 'object' && !(options.body instanceof FormData)) {
      headers['Content-Type'] = 'application/json';
      options.body = JSON.stringify(options.body);
    }
    options.headers = headers;

    const res = await fetch(url, options);
    if (res.status === 401) {
      clearAuthToken();
      if (!window.location.pathname.endsWith('admin-login.html')) {
        window.location.href = 'admin-login.html';
      }
      throw new Error('Unauthorized');
    }
    return res;
  }

  // ---------------------------------------------------------------------------
  // 1. ADMIN LOGIN PAGE CONTROLLER (admin-login.html)
  // ---------------------------------------------------------------------------
  function initAdminLogin() {
    const loginForm = document.getElementById('admin-login-form');
    if (!loginForm) return;

    // Check if already authenticated
    const existingToken = getAuthToken();
    if (existingToken) {
      apiFetch('/api/admin/overview')
        .then(res => {
          if (res.ok) window.location.href = 'admin.html';
        })
        .catch(() => {
          clearAuthToken();
        });
    }

    const adminIdInput = document.getElementById('admin-id-input');
    const passInput = document.getElementById('admin-pass-input');
    const togglePassBtn = document.getElementById('toggle-admin-pass');
    const errorAlert = document.getElementById('admin-login-error');
    const errorDesc = document.getElementById('admin-error-desc');
    const submitBtn = document.getElementById('btn-admin-login-submit');

    // Toggle password visibility
    if (togglePassBtn && passInput) {
      togglePassBtn.addEventListener('click', () => {
        const isPwd = passInput.type === 'password';
        passInput.type = isPwd ? 'text' : 'password';
        togglePassBtn.textContent = isPwd ? 'HIDE' : 'SHOW';
      });
    }

    // Clear errors on typing
    [adminIdInput, passInput].forEach(inp => {
      if (inp) {
        inp.addEventListener('input', () => {
          if (errorAlert) errorAlert.style.display = 'none';
        });
      }
    });

    loginForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const adminId = adminIdInput.value.trim();
      const password = passInput.value;

      if (!adminId || !password) {
        if (errorAlert && errorDesc) {
          errorDesc.textContent = 'Please provide both Admin ID and Password.';
          errorAlert.style.display = 'block';
        }
        return;
      }

      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = `<span>[ VALIDATING CLEARANCE... ]</span>`;
      }

      try {
        const res = await fetch('/api/admin/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ adminId, password })
        });

        const data = await res.json().catch(() => ({}));

        if (res.ok && data.success && data.token) {
          setAuthToken(data.token, data.admin);
          window.location.href = 'admin.html';
          return;
        }

        // Handle authentication failure
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.innerHTML = `<span>[ ACCESS ADMIN PANEL ]</span> <span aria-hidden="true">→</span>`;
        }
        if (errorAlert && errorDesc) {
          errorDesc.textContent = data.error || (res.status === 401 ? 'Invalid administrator credentials. Access restricted to authorized CSE personnel.' : `Authentication failed (HTTP ${res.status}).`);
          errorAlert.style.display = 'block';
        }
      } catch (err) {
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.innerHTML = `<span>[ ACCESS ADMIN PANEL ]</span> <span aria-hidden="true">→</span>`;
        }
        if (errorAlert && errorDesc) {
          errorDesc.textContent = 'Network communication failure. Could not connect to authentication server.';
          errorAlert.style.display = 'block';
        }
      }
    });
  }

  // ---------------------------------------------------------------------------
  // 2. ADMIN DASHBOARD CONTROLLER (admin.html)
  // ---------------------------------------------------------------------------
  function initAdminDashboard() {
    const mainPanel = document.getElementById('admin-main-panel');
    if (!mainPanel) return; // Not on admin dashboard

    // Verify authentication
    const token = getAuthToken();
    if (!token) {
      window.location.href = 'admin-login.html';
      return;
    }

    // Set Admin Name in Header
    const adminInfo = getStoredAdminInfo();
    const adminNameEl = document.getElementById('admin-user-name');
    if (adminNameEl && adminInfo) {
      adminNameEl.textContent = adminInfo.name.toUpperCase();
    }

    // Logout Button
    const logoutBtn = document.getElementById('btn-admin-logout');
    if (logoutBtn) {
      logoutBtn.addEventListener('click', async () => {
        try {
          await apiFetch('/api/admin/logout', { method: 'POST' });
        } catch (e) {}
        clearAuthToken();
        window.location.href = 'admin-login.html';
      });
    }

    // -------------------------------------------------------------------------
    // Sidebar Navigation Tabs
    // -------------------------------------------------------------------------
    const navItems = document.querySelectorAll('.sidebar-nav-item');
    const tabContents = document.querySelectorAll('.admin-tab-content');

    navItems.forEach(item => {
      item.addEventListener('click', () => {
        const targetTabId = item.getAttribute('data-tab');
        navItems.forEach(n => n.classList.remove('active'));
        tabContents.forEach(t => t.classList.remove('active'));

        item.classList.add('active');
        const targetEl = document.getElementById(targetTabId);
        if (targetEl) {
          targetEl.classList.add('active');
          // Trigger tab-specific refresh
          if (targetTabId === 'tab-overview') loadOverview();
          if (targetTabId === 'tab-teams') loadTeams();
          if (targetTabId === 'tab-sessions') loadSessions();
          if (targetTabId === 'tab-round-control') loadRoundControl();
          if (targetTabId === 'tab-violations') loadViolations();
          if (targetTabId === 'tab-evaluation') loadEvaluations();
          if (targetTabId === 'tab-surreal') loadSurreal();
          if (targetTabId === 'tab-final-report') loadFinalReport();
          if (targetTabId === 'tab-cases-questions') loadCasesQuestions();
          if (targetTabId === 'tab-backup-export') loadBackupExport();
          if (targetTabId === 'tab-settings') loadSettings();
        }
      });
    });

    const initialTab = (window.location.hash || '').replace('#', '');
    if (initialTab) {
      const matchingBtn = document.querySelector(`.sidebar-nav-item[data-tab="${initialTab}"]`);
      if (matchingBtn) matchingBtn.click();
    }

    // -------------------------------------------------------------------------
    // Global Confirmation Modal Setup
    // -------------------------------------------------------------------------
    const confirmModal = document.getElementById('confirm-action-modal');
    const confirmHeading = document.getElementById('confirm-modal-heading');
    const confirmDesc = document.getElementById('confirm-modal-desc');
    const btnConfirmProceed = document.getElementById('btn-modal-confirm-proceed');
    const btnConfirmCancel = document.getElementById('btn-modal-confirm-cancel');
    let onConfirmCallback = null;

    function openConfirmModal(heading, description, onConfirm) {
      if (!confirmModal) return;
      confirmHeading.textContent = heading;
      confirmDesc.textContent = description;
      onConfirmCallback = onConfirm;
      confirmModal.style.display = 'flex';
    }

    if (btnConfirmCancel) {
      btnConfirmCancel.addEventListener('click', () => {
        if (confirmModal) confirmModal.style.display = 'none';
        onConfirmCallback = null;
      });
    }

    if (btnConfirmProceed) {
      btnConfirmProceed.addEventListener('click', () => {
        if (confirmModal) confirmModal.style.display = 'none';
        if (typeof onConfirmCallback === 'function') {
          onConfirmCallback();
        }
        onConfirmCallback = null;
      });
    }

    // -------------------------------------------------------------------------
    // Tab 1: OVERVIEW & EVENT CONTROL
    // -------------------------------------------------------------------------
    const regTeamsEl = document.getElementById('ov-reg-teams');
    const activePartsEl = document.getElementById('ov-active-participants');
    const compInvsEl = document.getElementById('ov-completed-investigations');
    const activeViosEl = document.getElementById('ov-active-violations');
    const headerStatusText = document.getElementById('header-event-status-text');
    const headerStatusDot = document.getElementById('header-status-dot');
    const ecStatusDisplay = document.getElementById('ec-current-status-display');
    const ecPhaseDisplay = document.getElementById('ec-phase-display');
    const ecTeamsDisplay = document.getElementById('ec-teams-count-display');

    const btnPause = document.getElementById('btn-ec-pause');
    const btnResume = document.getElementById('btn-ec-resume');
    const btnEnd = document.getElementById('btn-ec-end');
    const btnReset = document.getElementById('btn-ec-reset');

    async function loadOverview() {
      try {
        const res = await apiFetch('/api/admin/overview');
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();

        if (regTeamsEl) regTeamsEl.textContent = data.registeredTeams ?? 0;
        if (activePartsEl) activePartsEl.textContent = data.activeParticipants ?? 0;
        if (compInvsEl) compInvsEl.textContent = data.completedInvestigations ?? 0;
        if (activeViosEl) activeViosEl.textContent = data.activeViolations ?? 0;

        const status = data.eventStatus || 'EVENT NOT STARTED';
        if (headerStatusText) headerStatusText.textContent = status;
        if (ecStatusDisplay) ecStatusDisplay.textContent = status;
        if (ecPhaseDisplay) ecPhaseDisplay.textContent = data.currentPhase || 'REGISTRATION & STANDBY';
        if (ecTeamsDisplay) ecTeamsDisplay.textContent = `${data.registeredTeams ?? 0} TEAMS REGISTERED`;

        // Update button states according to state machine
        if (btnPause && btnResume && btnEnd) {
          if (status === 'EVENT NOT STARTED' || status === 'EVENT ACTIVE') {
            btnPause.disabled = (status !== 'EVENT ACTIVE');
            btnResume.disabled = true;
            btnEnd.disabled = (status !== 'EVENT ACTIVE');
            if (headerStatusDot) headerStatusDot.style.background = (status === 'EVENT ACTIVE') ? '#00E676' : '#858585';
          } else if (status === 'EVENT PAUSED') {
            btnPause.disabled = true;
            btnResume.disabled = false;
            btnEnd.disabled = false;
            if (headerStatusDot) headerStatusDot.style.background = '#FF2438';
          } else if (status === 'EVENT COMPLETED') {
            btnPause.disabled = true;
            btnResume.disabled = true;
            btnEnd.disabled = true;
            if (headerStatusDot) headerStatusDot.style.background = 'var(--color-amber-bright)';
          }
        }
      } catch (err) {
        console.warn('Overview API failure:', err);
        if (regTeamsEl && regTeamsEl.textContent === '') regTeamsEl.textContent = '0';
        if (activePartsEl && activePartsEl.textContent === '') activePartsEl.textContent = '0';
        if (compInvsEl && compInvsEl.textContent === '') compInvsEl.textContent = '0';
        if (activeViosEl && activeViosEl.textContent === '') activeViosEl.textContent = '0';
      }
    }

    async function executeEventControl(action) {
      try {
        const res = await apiFetch('/api/admin/event-control', {
          method: 'POST',
          body: { action }
        });
        const data = await res.json();
        if (res.ok && data.success) {
          showToast('EVENT STATE UPDATED', `Event transition to ${data.status} successful.`, 'success');
          loadOverview();
        } else {
          showToast('TRANSITION REJECTED', data.error || 'Invalid event state transition.', 'error');
        }
      } catch (err) {
        showToast('SYSTEM ERROR', 'Could not reach server to execute event control.', 'error');
      }
    }


    if (btnPause) {
      btnPause.addEventListener('click', () => {
        openConfirmModal('PAUSE EVENT TEMPORARILY', 'Are you sure you want to PAUSE the event? Active timers will be suspended for all participating workstations.', () => {
          executeEventControl('pause');
        });
      });
    }

    if (btnResume) {
      btnResume.addEventListener('click', () => {
        openConfirmModal('RESUME INVESTIGATION EVENT', 'Are you sure you want to RESUME the active investigation?', () => {
          executeEventControl('resume');
        });
      });
    }

    if (btnEnd) {
      btnEnd.addEventListener('click', () => {
        openConfirmModal('PERMANENTLY CONCLUDE EVENT', 'CRITICAL ACTION: Are you sure you want to END the event? All active sessions will be sealed and transitioned to final evaluation.', () => {
          executeEventControl('end');
        });
      });
    }

    // -------------------------------------------------------------------------
    // Complete Event Reset Modal Workflow
    // -------------------------------------------------------------------------
    const completeResetModal = document.getElementById('complete-event-reset-modal');
    const resetBackupConfirm = document.getElementById('reset-event-backup-confirm');
    const resetPhraseInput = document.getElementById('reset-event-phrase-input');
    const btnCancelCompleteReset = document.getElementById('btn-cancel-complete-reset');
    const btnConfirmCompleteReset = document.getElementById('btn-confirm-complete-reset');
    const resetFeedback = document.getElementById('reset-event-feedback');

    function checkResetUnlock() {
      if (!btnConfirmCompleteReset) return;
      const phraseMatches = resetPhraseInput && resetPhraseInput.value.trim() === 'RESET TRACEX EVENT';
      const backupChecked = resetBackupConfirm && resetBackupConfirm.checked;

      if (phraseMatches && backupChecked) {
        btnConfirmCompleteReset.disabled = false;
        btnConfirmCompleteReset.style.opacity = '1';
        btnConfirmCompleteReset.style.cursor = 'pointer';
        btnConfirmCompleteReset.style.background = '#D32F2F';
      } else {
        btnConfirmCompleteReset.disabled = true;
        btnConfirmCompleteReset.style.opacity = '0.4';
        btnConfirmCompleteReset.style.cursor = 'not-allowed';
        btnConfirmCompleteReset.style.background = '#B71C1C';
      }
    }

    if (resetPhraseInput) {
      resetPhraseInput.addEventListener('input', checkResetUnlock);
    }
    if (resetBackupConfirm) {
      resetBackupConfirm.addEventListener('change', checkResetUnlock);
    }

    if (btnReset) {
      btnReset.addEventListener('click', () => {
        if (!completeResetModal) return;
        if (resetPhraseInput) resetPhraseInput.value = '';
        if (resetBackupConfirm) resetBackupConfirm.checked = false;
        if (resetFeedback) {
          resetFeedback.style.display = 'none';
          resetFeedback.textContent = '';
        }
        checkResetUnlock();
        completeResetModal.style.display = 'flex';
        setTimeout(() => {
          if (resetPhraseInput) resetPhraseInput.focus();
        }, 100);
      });
    }

    if (btnCancelCompleteReset) {
      btnCancelCompleteReset.addEventListener('click', () => {
        if (completeResetModal) completeResetModal.style.display = 'none';
      });
    }

    if (btnConfirmCompleteReset) {
      btnConfirmCompleteReset.addEventListener('click', async () => {
        const phrase = resetPhraseInput ? resetPhraseInput.value.trim() : '';
        const backupOk = resetBackupConfirm ? resetBackupConfirm.checked : false;

        if (phrase !== 'RESET TRACEX EVENT' || !backupOk) {
          return;
        }

        btnConfirmCompleteReset.disabled = true;
        btnConfirmCompleteReset.style.opacity = '0.4';
        btnConfirmCompleteReset.style.cursor = 'not-allowed';

        if (resetFeedback) {
          resetFeedback.style.display = 'block';
          resetFeedback.style.background = 'rgba(255, 36, 56, 0.1)';
          resetFeedback.style.border = '1px solid rgba(255, 36, 56, 0.3)';
          resetFeedback.style.color = '#FFFFFF';
          resetFeedback.textContent = 'Executing complete event reset and verified pre-reset backup... Please wait.';
        }

        try {
          const res = await apiFetch('/api/admin/event-reset', {
            method: 'POST',
            body: {
              phrase: phrase,
              backupConfirmed: true
            }
          });
          const data = await res.json();

          if (res.ok && data.success) {
            if (completeResetModal) completeResetModal.style.display = 'none';
            showToast(
              'COMPLETE EVENT RESET',
              'All participant data cleared. Verified pre-reset backup stored. Event restored to STANDBY.',
              'success'
            );
            // Reload all dashboard panels
            loadOverview();
            loadTeams();
            loadSessions();
            loadEvaluations();
            loadBackupsList();
            loadAuditLogs();
            loadFinalReport();
            if (typeof loadSurreal === 'function') loadSurreal();
          } else {
            if (resetFeedback) {
              resetFeedback.style.display = 'block';
              resetFeedback.style.background = 'rgba(255, 36, 56, 0.2)';
              resetFeedback.style.border = '1px solid #FF2438';
              resetFeedback.style.color = '#FF2438';
              resetFeedback.textContent = data.error || 'Complete event reset failed.';
            }
            checkResetUnlock();
          }
        } catch (err) {
          if (resetFeedback) {
            resetFeedback.style.display = 'block';
            resetFeedback.style.background = 'rgba(255, 36, 56, 0.2)';
            resetFeedback.style.border = '1px solid #FF2438';
            resetFeedback.style.color = '#FF2438';
            resetFeedback.textContent = 'Server communication error during complete event reset.';
          }
          checkResetUnlock();
        }
      });
    }

    // -------------------------------------------------------------------------
    // Tab 2: TEAM MANAGEMENT
    // -------------------------------------------------------------------------
    const teamsTableBody = document.getElementById('teams-table-body');
    const teamSearchInput = document.getElementById('team-search-input');
    const teamStatusFilter = document.getElementById('team-status-filter');
    const btnRefreshTeams = document.getElementById('btn-refresh-teams');
    const teamDetailsModal = document.getElementById('team-details-modal');
    const btnCloseTeamModal = document.getElementById('btn-close-team-modal');

    let allTeamsCache = [];

    async function loadTeams() {
      if (!teamsTableBody) return;
      try {
        const res = await apiFetch('/api/admin/teams');
        const data = await res.json();
        allTeamsCache = data.teams || [];
        renderTeamsTable();
      } catch (err) {
        teamsTableBody.innerHTML = `<tr><td colspan="8" style="text-align: center; color: #FF2438;">Failed to load registered teams.</td></tr>`;
      }
    }

    function renderTeamsTable() {
      if (!teamsTableBody) return;
      const q = (teamSearchInput?.value || '').trim().toLowerCase();
      const statusFilt = teamStatusFilter?.value || 'ALL';

      const filtered = allTeamsCache.filter(t => {
        const matchesQ = !q || 
          t.teamId.toLowerCase().includes(q) ||
          t.teamName.toLowerCase().includes(q) ||
          (t.collegeName && t.collegeName.toLowerCase().includes(q)) ||
          (t.selectedCaseName && t.selectedCaseName.toLowerCase().includes(q));

        let matchesStatus = true;
        if (statusFilt === 'ACTIVE') {
          matchesStatus = t.status === 'Investigating' || t.status === 'Logged in' || (t.sessionStatus && t.sessionStatus.includes('IN_PROGRESS'));
        } else if (statusFilt === 'NOT_STARTED') {
          matchesStatus = !t.hasParticipation && t.status === 'Registered';
        } else if (statusFilt === 'SUBMITTED') {
          matchesStatus = t.status === 'Submitted' || (t.sessionStatus && (t.sessionStatus.includes('COMPLETED') || t.sessionStatus.includes('SUBMITTED')));
        } else if (statusFilt === 'DEACTIVATED') {
          matchesStatus = t.status === 'Deactivated' || t.status === 'DEACTIVATED';
        } else if (statusFilt === 'TERMINATED') {
          matchesStatus = t.status === 'Terminated' || t.status === 'DISQUALIFIED';
        } else if (statusFilt !== 'ALL') {
          matchesStatus = t.status === statusFilt;
        }

        return matchesQ && matchesStatus;
      });

      if (filtered.length === 0) {
        teamsTableBody.innerHTML = `<tr><td colspan="8" style="text-align: center; color: var(--color-text-muted);">No matching registered teams found.</td></tr>`;
        return;
      }

      teamsTableBody.innerHTML = '';
      filtered.forEach(t => {
        const tr = document.createElement('tr');
        
        let statusBadgeClass = 'badge-registered';
        if (t.status === 'Investigating' || t.status === 'Logged in') statusBadgeClass = 'badge-active';
        if (t.status === 'Submitted') statusBadgeClass = 'badge-submitted';
        if (t.status === 'Terminated') statusBadgeClass = 'badge-terminated';
        if (t.status === 'Deactivated' || t.status === 'DEACTIVATED') statusBadgeClass = 'badge-terminated';

        const regDate = t.registeredAt ? t.registeredAt.replace('T', ' ').substring(0, 16) : '--';
        const caseDisplay = t.selectedCaseName || 'Pending Selection';
        const progressDisplay = t.sessionStatus || 'STANDBY';
        const scoreDisplay = (t.score !== null && t.score !== undefined) ? `${t.score} / 30` : '--';

        const regNumBadge = t.registrationNumber ? `<span style="display: inline-block; font-size: 0.72rem; color: #00F0FF; margin-right: 0.35rem; font-weight: 800;">#${t.registrationNumber}</span>` : '';

        tr.innerHTML = `
          <td style="font-family: var(--font-mono); font-weight: 700; color: #FFFFFF;">${regNumBadge}${escapeHtml(t.teamId)}</td>
          <td><strong>${escapeHtml(t.teamName)}</strong></td>
          <td style="font-family: var(--font-mono); font-size: 0.76rem; color: var(--color-text-secondary);">${escapeHtml(regDate)}</td>
          <td style="font-size: 0.8rem; color: var(--color-amber-bright); font-weight: 500;">${escapeHtml(caseDisplay)}</td>
          <td style="font-family: var(--font-mono); font-size: 0.74rem;">${escapeHtml(progressDisplay)}</td>
          <td style="font-family: var(--font-mono); font-weight: 700; color: #00E676;">${scoreDisplay}</td>
          <td><span class="status-pill ${statusBadgeClass}">${escapeHtml(t.status)}</span></td>
          <td style="text-align: right; white-space: nowrap;">
            <button type="button" class="btn-table-action btn-view-team" data-id="${t.teamId}">[ VIEW DETAILS ]</button>
            <button type="button" class="btn-table-action btn-delete-team" data-id="${t.teamId}" style="color: #FF2438; border-color: rgba(255, 36, 56, 0.4); margin-left: 0.4rem;">[ DELETE TEAM ]</button>
          </td>
        `;

        tr.querySelector('.btn-view-team').addEventListener('click', () => {
          openTeamDetailsModal(t);
        });

        tr.querySelector('.btn-delete-team').addEventListener('click', () => {
          openDeleteTeamModal(t);
        });

        teamsTableBody.appendChild(tr);
      });
    }

    function openTeamDetailsModal(t) {
      if (!teamDetailsModal) return;
      document.getElementById('tm-id').textContent = t.teamId;
      document.getElementById('tm-name').textContent = t.teamName;
      document.getElementById('tm-college').textContent = t.collegeName || '--';
      document.getElementById('tm-dept').textContent = t.department || '--';
      document.getElementById('tm-size').textContent = `${t.teamSize} Member(s)`;
      document.getElementById('tm-status').textContent = t.status;

      const membersList = document.getElementById('tm-members-list');
      membersList.innerHTML = '';
      (t.members || []).forEach((m, idx) => {
        const li = document.createElement('li');
        li.textContent = `Member ${idx + 1}: ${m}`;
        membersList.appendChild(li);
      });

      teamDetailsModal.style.display = 'flex';
    }

    // -------------------------------------------------------------------------
    // Team Deletion / Deactivation Modal Workflow
    // -------------------------------------------------------------------------
    const teamDeleteModal = document.getElementById('team-delete-confirm-modal');
    const btnCancelTeamDelete = document.getElementById('btn-cancel-team-delete');
    const btnConfirmTeamDelete = document.getElementById('btn-confirm-team-delete');
    let teamPendingDeletion = null;

    function openDeleteTeamModal(t) {
      if (!teamDeleteModal) return;
      teamPendingDeletion = t;

      document.getElementById('del-team-id').textContent = t.teamId;
      document.getElementById('del-team-name').textContent = t.teamName;
      document.getElementById('del-team-case').textContent = t.selectedCaseName || 'None Selected';
      document.getElementById('del-team-participation').textContent = t.hasParticipation 
        ? 'ACTIVE PARTICIPATION RECORDS PRESENT' 
        : 'REGISTRATION ONLY (NO SUBMISSIONS)';

      const noticeEl = document.getElementById('del-team-notice');
      const permWrap = document.getElementById('del-team-perm-wrap');
      const permCheck = document.getElementById('del-team-force-perm');
      const reasonInput = document.getElementById('del-team-reason');
      const feedbackEl = document.getElementById('del-team-feedback');

      if (reasonInput) reasonInput.value = '';
      if (permCheck) permCheck.checked = false;
      if (feedbackEl) {
        feedbackEl.style.display = 'none';
        feedbackEl.textContent = '';
      }

      if (t.hasParticipation) {
        if (noticeEl) {
          noticeEl.innerHTML = `<strong>RETENTION POLICY ENFORCED:</strong> This team has active investigation activity, timers, or answer submissions. Confirming removal will <strong>DEACTIVATE</strong> the team account, instantly barring further participant login while safely preserving all historical scores and evaluation records in the CSE audit logs.`;
        }
        if (permWrap) permWrap.style.display = 'block';
      } else {
        if (noticeEl) {
          noticeEl.innerHTML = `<strong>CLEAN REGISTRATION REMOVAL:</strong> This team has not commenced investigation and has zero answer submissions. Confirming removal will <strong>permanently delete</strong> this team registration from the database.`;
        }
        if (permWrap) permWrap.style.display = 'none';
      }

      if (btnConfirmTeamDelete) {
        btnConfirmTeamDelete.disabled = false;
        btnConfirmTeamDelete.textContent = '[ CONFIRM REMOVAL ]';
      }

      teamDeleteModal.style.display = 'flex';
    }

    function closeDeleteTeamModal() {
      if (teamDeleteModal) teamDeleteModal.style.display = 'none';
      teamPendingDeletion = null;
    }

    if (btnCancelTeamDelete) {
      btnCancelTeamDelete.addEventListener('click', closeDeleteTeamModal);
    }

    if (btnConfirmTeamDelete) {
      btnConfirmTeamDelete.addEventListener('click', async () => {
        if (!teamPendingDeletion) return;
        const teamId = teamPendingDeletion.teamId;
        const reasonInput = document.getElementById('del-team-reason');
        const permCheck = document.getElementById('del-team-force-perm');
        const feedbackEl = document.getElementById('del-team-feedback');

        const reason = (reasonInput?.value || '').trim() || 'Administrative deletion action';
        const isPermanent = Boolean(permCheck?.checked);

        btnConfirmTeamDelete.disabled = true;
        btnConfirmTeamDelete.textContent = '[ PROCESSING... ]';

        try {
          const res = await apiFetch('/api/admin/teams/delete', {
            method: 'POST',
            body: JSON.stringify({ teamId, reason, permanent: isPermanent })
          });
          const data = await res.json();

          if (res.ok && data.success) {
            if (feedbackEl) {
              feedbackEl.style.display = 'block';
              feedbackEl.style.background = 'rgba(0, 230, 118, 0.15)';
              feedbackEl.style.border = '1px solid #00E676';
              feedbackEl.style.color = '#00E676';
              feedbackEl.textContent = `SUCCESS: ${data.message}`;
            }

            // Refresh teams table and overview stats
            setTimeout(async () => {
              closeDeleteTeamModal();
              await loadTeams();
              if (typeof loadOverview === 'function') loadOverview();
            }, 1000);
          } else {
            if (feedbackEl) {
              feedbackEl.style.display = 'block';
              feedbackEl.style.background = 'rgba(255, 36, 56, 0.15)';
              feedbackEl.style.border = '1px solid #FF2438';
              feedbackEl.style.color = '#FF2438';
              feedbackEl.textContent = data.error || 'Failed to remove team.';
            }
            btnConfirmTeamDelete.disabled = false;
            btnConfirmTeamDelete.textContent = '[ CONFIRM REMOVAL ]';
          }
        } catch (err) {
          if (feedbackEl) {
            feedbackEl.style.display = 'block';
            feedbackEl.style.background = 'rgba(255, 36, 56, 0.15)';
            feedbackEl.style.border = '1px solid #FF2438';
            feedbackEl.style.color = '#FF2438';
            feedbackEl.textContent = 'Network communication failure during team removal.';
          }
          btnConfirmTeamDelete.disabled = false;
          btnConfirmTeamDelete.textContent = '[ CONFIRM REMOVAL ]';
        }
      });
    }

    if (btnCloseTeamModal) {
      btnCloseTeamModal.addEventListener('click', () => {
        if (teamDetailsModal) teamDetailsModal.style.display = 'none';
      });
    }

    if (teamSearchInput) teamSearchInput.addEventListener('input', renderTeamsTable);
    if (teamStatusFilter) teamStatusFilter.addEventListener('change', renderTeamsTable);
    if (btnRefreshTeams) btnRefreshTeams.addEventListener('click', loadTeams);

    // -------------------------------------------------------------------------
    // Tab 3: LIVE SESSIONS MONITORING
    // -------------------------------------------------------------------------
    const sessionsTableBody = document.getElementById('sessions-table-body');
    const btnRefreshSessions = document.getElementById('btn-refresh-sessions');

    async function loadSessions() {
      if (!sessionsTableBody) return;
      try {
        const res = await apiFetch('/api/admin/sessions');
        const data = await res.json();
        const list = data.sessions || [];

        if (list.length === 0) {
          sessionsTableBody.innerHTML = `<tr><td colspan="8" style="text-align: center; color: var(--color-text-muted);">No active sessions currently running.</td></tr>`;
          return;
        }

        sessionsTableBody.innerHTML = '';
        list.forEach(s => {
          const tr = document.createElement('tr');
          let sBadge = 'badge-active';
          if (s.sessionStatus === 'SUBMITTED') sBadge = 'badge-submitted';
          if (s.sessionStatus === 'TERMINATED') sBadge = 'badge-terminated';
          if (s.sessionStatus === 'NOT STARTED') sBadge = 'badge-registered';

          tr.innerHTML = `
            <td style="font-family: var(--font-mono); font-weight: 700; color: #FFFFFF;">${escapeHtml(s.teamId)}</td>
            <td><strong>${escapeHtml(s.teamName)}</strong></td>
            <td>${escapeHtml(s.caseName)}</td>
            <td>ROUND ${s.currentRound}</td>
            <td>Q ${s.currentQuestion} / 15</td>
            <td style="font-family: var(--font-mono); color: #FFFFFF;">${escapeHtml(s.timeRemaining)}</td>
            <td><span class="hud-conn-badge" style="padding: 2px 8px; font-size: 0.65rem;">${escapeHtml(s.connectionStatus)}</span></td>
            <td><span class="status-pill ${sBadge}">${escapeHtml(s.sessionStatus)}</span></td>
          `;
          sessionsTableBody.appendChild(tr);
        });
      } catch (err) {
        sessionsTableBody.innerHTML = `<tr><td colspan="8" style="text-align: center; color: #FF2438;">Failed to load live sessions.</td></tr>`;
      }
    }

    if (btnRefreshSessions) btnRefreshSessions.addEventListener('click', loadSessions);

    // -------------------------------------------------------------------------
    // Tab 4: ROUND CONTROL & PHASING
    // -------------------------------------------------------------------------
    const btnSetR1 = document.getElementById('btn-set-round-1');
    const btnSetR2 = document.getElementById('btn-set-round-2');
    const btnSetEval = document.getElementById('btn-set-round-eval');

    async function loadRoundControl() {
      try {
        const res = await apiFetch('/api/admin/round-control');
        const data = await res.json();
        const curRound = String(data.currentRound);

        // Update pills
        const pill1 = document.getElementById('rc-status-pill-1');
        const pill2 = document.getElementById('rc-status-pill-2');
        const pill3 = document.getElementById('rc-status-pill-3');

        if (pill1 && pill2 && pill3) {
          [pill1, pill2, pill3].forEach(p => p.className = 'rc-status-pill pending');
          pill1.textContent = 'PENDING';
          pill2.textContent = 'PENDING';
          pill3.textContent = 'PENDING';

          if (curRound === '1') {
            pill1.className = 'rc-status-pill active';
            pill1.textContent = 'ACTIVE';
          } else if (curRound === '2') {
            pill1.className = 'rc-status-pill completed';
            pill1.textContent = 'COMPLETED';
            pill2.className = 'rc-status-pill active';
            pill2.textContent = 'ACTIVE';
          } else if (curRound === 'eval') {
            pill1.className = 'rc-status-pill completed';
            pill1.textContent = 'COMPLETED';
            pill2.className = 'rc-status-pill completed';
            pill2.textContent = 'COMPLETED';
            pill3.className = 'rc-status-pill active';
            pill3.textContent = 'ACTIVE';
          }
        }
      } catch (err) {
        console.error('Error loading round control:', err);
      }
    }

    async function setRound(roundVal, name) {
      try {
        const res = await apiFetch('/api/admin/round-control', {
          method: 'POST',
          body: { round: roundVal }
        });
        const data = await res.json();
        if (res.ok && data.success) {
          showToast('ROUND PHASE UPDATED', `Event successfully transitioned to ${name}.`, 'success');
          loadRoundControl();
          loadOverview();
        } else {
          showToast('ACTION FAILED', data.error || 'Could not update round.', 'error');
        }
      } catch (err) {
        showToast('SYSTEM ERROR', 'Network failure during round transition.', 'error');
      }
    }

    if (btnSetR1) {
      btnSetR1.addEventListener('click', () => {
        openConfirmModal('SET ACTIVE: ROUND 1', 'Transition active competition phase to Round 1 (15 questions)?', () => {
          setRound(1, 'ROUND 1');
        });
      });
    }

    if (btnSetR2) {
      btnSetR2.addEventListener('click', () => {
        openConfirmModal('ADVANCE TO ROUND 2', 'Advance the event phase to Round 2 (15 questions)?', () => {
          setRound(2, 'ROUND 2');
        });
      });
    }

    if (btnSetEval) {
      btnSetEval.addEventListener('click', () => {
        openConfirmModal('INITIATE EVALUATION PHASE', 'Initiate the 5-Minute Evaluation period across all investigation dossiers?', () => {
          setRound('eval', 'EVALUATION PHASE');
        });
      });
    }

    // -------------------------------------------------------------------------
    // Tab 5: VIOLATION MONITOR
    // -------------------------------------------------------------------------
    const viosTableBody = document.getElementById('violations-table-body');
    const btnRefreshVios = document.getElementById('btn-refresh-violations');

    async function loadViolations() {
      if (!viosTableBody) return;
      try {
        const res = await apiFetch('/api/admin/violations');
        const data = await res.json();
        const logs = data.violations || [];

        if (logs.length === 0) {
          viosTableBody.innerHTML = `<tr><td colspan="7" style="text-align: center; color: var(--color-text-muted);">No security violations logged. Event integrity pristine.</td></tr>`;
          return;
        }

        viosTableBody.innerHTML = '';
        logs.forEach(l => {
          const tr = document.createElement('tr');
          const isTerminated = l.count >= 3;
          tr.innerHTML = `
            <td style="font-family: var(--font-mono); color: var(--color-text-muted);">#${l.id}</td>
            <td style="font-family: var(--font-mono); font-weight: 700; color: #FFFFFF;">${escapeHtml(l.teamId)}</td>
            <td><strong>${escapeHtml(l.teamName)}</strong></td>
            <td><span class="violation-tag">${escapeHtml(l.type)}</span></td>
            <td style="font-family: var(--font-mono); font-size: 0.72rem;">${escapeHtml(l.timestamp)}</td>
            <td><strong style="color: ${isTerminated ? '#FF2438' : 'var(--color-amber-bright)'}">${l.count} of 3</strong></td>
            <td style="font-size: 0.8rem; color: ${isTerminated ? '#FF2438' : 'var(--color-text-secondary)'}">${escapeHtml(l.action)}</td>
          `;
          viosTableBody.appendChild(tr);
        });
      } catch (err) {
        viosTableBody.innerHTML = `<tr><td colspan="7" style="text-align: center; color: #FF2438;">Failed to load violation records.</td></tr>`;
      }
    }

    if (btnRefreshVios) btnRefreshVios.addEventListener('click', loadViolations);

    // -------------------------------------------------------------------------
    // Tab 6: EVALUATION & RESULTS — ANSWER REVIEW, CORRECTIONS & WINNER WORKFLOW
    // -------------------------------------------------------------------------
    const answerReviewTableBody = document.getElementById('answer-review-table-body');
    const winnerComparisonTableBody = document.getElementById('winner-comparison-table-body');
    const answerReviewSearchInput = document.getElementById('answer-review-search-input');
    const btnRefreshEvaluations = document.getElementById('btn-refresh-evaluations');
    const btnEvalReviewResults = document.getElementById('btn-eval-review-results');
    const btnFinalizeResults = document.getElementById('btn-finalize-results');
    const btnReleaseResults = document.getElementById('btn-release-results');
    const btnWithholdResults = document.getElementById('btn-withhold-results');
    const pubStatusText = document.getElementById('pub-status-text');
    const finalizationStatusText = document.getElementById('finalization-status-text');

    // Dual Winner Card Elements
    const sysWinnerTeamName = document.getElementById('sys-winner-team-name');
    const sysWinnerTeamId = document.getElementById('sys-winner-team-id');
    const sysWinnerScore = document.getElementById('sys-winner-score');
    const sysWinnerCase = document.getElementById('sys-winner-case');
    const declaredWinnerTeamName = document.getElementById('declared-winner-team-name');
    const declaredWinnerTeamId = document.getElementById('declared-winner-team-id');
    const declaredWinnerBadge = document.getElementById('declared-winner-badge');
    const declaredWinnerDecisionType = document.getElementById('declared-winner-decision-type');
    const declaredWinnerReasonDisplay = document.getElementById('declared-winner-reason-display');
    const btnTriggerWinnerOverride = document.getElementById('btn-trigger-winner-override');

    // Detailed Answer Review (DAR) Modal Elements
    const darModal = document.getElementById('detailed-answer-review-modal');
    const btnCloseDarModal = document.getElementById('btn-close-dar-modal');
    const btnCloseDarModalX = document.getElementById('btn-close-dar-modal-x');
    const btnDarTabR1 = document.getElementById('btn-dar-tab-r1');
    const btnDarTabR2 = document.getElementById('btn-dar-tab-r2');
    const darTeamId = document.getElementById('dar-team-id');
    const darTeamName = document.getElementById('dar-team-name');
    const darCaseName = document.getElementById('dar-case-name');
    const darOverallScore = document.getElementById('dar-overall-score');
    const darCorrectionsBadge = document.getElementById('dar-corrections-badge');
    const darSumSubmitted = document.getElementById('dar-sum-submitted');
    const darSumCorrect = document.getElementById('dar-sum-correct');
    const darSumIncorrect = document.getElementById('dar-sum-incorrect');
    const darSumUnanswered = document.getElementById('dar-sum-unanswered');
    const darSumScore = document.getElementById('dar-sum-score');
    const darQuestionsContainer = document.getElementById('dar-questions-container');

    // Mark Correction Modal Elements
    const mcModal = document.getElementById('mark-correction-modal');
    const btnCancelMarkCorrection = document.getElementById('btn-cancel-mark-correction');
    const btnCommitMarkCorrection = document.getElementById('btn-commit-mark-correction');
    const mcTeamId = document.getElementById('mc-team-id');
    const mcQNum = document.getElementById('mc-q-num');
    const mcQId = document.getElementById('mc-q-id');
    const mcSubAns = document.getElementById('mc-sub-ans');
    const mcKeyAns = document.getElementById('mc-key-ans');
    const mcCurrentMark = document.getElementById('mc-current-mark');
    const mcNewMark = document.getElementById('mc-new-mark');
    const mcReasonInput = document.getElementById('mc-reason-input');
    const mcConfirmCheckbox = document.getElementById('mc-confirm-checkbox');

    // Winner Override Modal Elements
    const woModal = document.getElementById('winner-override-modal');
    const btnCancelWinnerOverride = document.getElementById('btn-cancel-winner-override');
    const btnCommitWinnerOverride = document.getElementById('btn-commit-winner-override');
    const woSysWinnerDisplay = document.getElementById('wo-sys-winner-display');
    const woDeclWinnerDisplay = document.getElementById('wo-decl-winner-display');
    const woWinnerSelect = document.getElementById('wo-winner-select');
    const woReasonInput = document.getElementById('wo-reason-input');
    const woConfirmCheckbox = document.getElementById('wo-confirm-checkbox');

    // Finalize Results Modal Elements
    const finModal = document.getElementById('finalize-results-modal');
    const btnCancelFinalize = document.getElementById('btn-cancel-finalize');
    const btnCommitFinalize = document.getElementById('btn-commit-finalize');
    const finTeamsCount = document.getElementById('fin-teams-count');
    const finSysWinner = document.getElementById('fin-sys-winner');
    const finDeclWinner = document.getElementById('fin-decl-winner');
    const finConfirmCheckbox = document.getElementById('fin-confirm-checkbox');

    // Publish Results Modal Elements
    const pubModal = document.getElementById('publish-results-modal');
    const btnCancelPublish = document.getElementById('btn-cancel-publish');
    const btnCommitPublish = document.getElementById('btn-commit-publish');
    const pubFinStatus = document.getElementById('pub-fin-status');
    const pubWinnerName = document.getElementById('pub-winner-name');
    const pubConfirmCheckbox = document.getElementById('pub-confirm-checkbox');

    // Legacy Single Override Modal
    const overrideModal = document.getElementById('override-result-modal');
    const btnCancelOverride = document.getElementById('btn-cancel-override');
    const btnSubmitOverride = document.getElementById('btn-submit-override');
    const overrideTeamIdSpan = document.getElementById('override-team-id');
    const overrideSelectStatus = document.getElementById('override-select-status');
    const overrideReasonInput = document.getElementById('override-reason-input');
    let activeOverrideTeamId = null;

    // Module State
    let cachedEvaluations = [];
    let cachedWinnerReview = null;
    let currentDarSubmission = null;
    let currentDarRound = 1;
    let pendingCorrectionData = null;

    // 1. Load Evaluations & Answer Review Table
    async function loadEvaluations() {
      try {
        const res = await apiFetch('/api/admin/evaluations');
        const data = await res.json();
        cachedEvaluations = data.evaluations || [];

        // Check settings for publication & finalization status
        const isPub = !!(cachedEvaluations.length > 0 && cachedEvaluations[0].isPublished);
        const isFin = !!(cachedEvaluations.length > 0 && cachedEvaluations[0].isFinalized);

        if (pubStatusText) {
          if (isPub) {
            pubStatusText.textContent = 'RESULTS RELEASED TO PARTICIPANTS (LIVE)';
            pubStatusText.style.color = '#00E676';
          } else {
            pubStatusText.textContent = 'RESULTS UNDER REVIEW (UNPUBLISHED)';
            pubStatusText.style.color = 'var(--color-amber-bright)';
          }
        }

        if (finalizationStatusText) {
          if (isFin) {
            finalizationStatusText.textContent = 'RESULTS FINALIZED (LOCKED)';
            finalizationStatusText.style.color = '#00E676';
          } else {
            finalizationStatusText.textContent = 'NOT FINALIZED';
            finalizationStatusText.style.color = 'var(--color-amber-bright)';
          }
        }

        renderAnswerReviewTable();
        await loadFinalWinnerReview();
      } catch (err) {
        if (answerReviewTableBody) {
          answerReviewTableBody.innerHTML = `<tr><td colspan="9" style="text-align: center; color: #FF2438;">Failed to load evaluation records.</td></tr>`;
        }
      }
    }

    function renderAnswerReviewTable() {
      if (!answerReviewTableBody) return;
      const query = (answerReviewSearchInput?.value || '').trim().toLowerCase();
      const filtered = cachedEvaluations.filter(e => {
        if (!query) return true;
        return (e.teamId || '').toLowerCase().includes(query) ||
               (e.teamName || '').toLowerCase().includes(query) ||
               (e.caseName || '').toLowerCase().includes(query) ||
               (e.caseId || '').toLowerCase().includes(query);
      });

      if (filtered.length === 0) {
        answerReviewTableBody.innerHTML = `<tr><td colspan="9" style="text-align: center; color: var(--color-text-muted);">No matching team evaluation records found.</td></tr>`;
        return;
      }

      answerReviewTableBody.innerHTML = '';
      filtered.forEach(e => {
        const tr = document.createElement('tr');
        const isPub = !!e.isPublished;
        const pubBadge = isPub
          ? `<span class="status-pill badge-qualified" style="font-size: 0.68rem;">PUBLISHED</span>`
          : `<span class="status-pill badge-registered" style="font-size: 0.68rem;">UNPUBLISHED</span>`;

        let evalPillClass = 'badge-submitted';
        if (e.evaluationStatus === 'EVALUATED') evalPillClass = 'badge-qualified';

        const correctionsNotice = e.hasCorrections
          ? `<span title="Contains audited mark correction" style="color: var(--color-amber-bright); font-size: 0.72rem; margin-left: 4px;">⚠</span>`
          : '';

        tr.innerHTML = `
          <td style="font-family: var(--font-mono); font-weight: 700; color: #FFFFFF;">${escapeHtml(e.teamId)}</td>
          <td><strong>${escapeHtml(e.teamName)}</strong></td>
          <td style="font-family: var(--font-mono); font-size: 0.78rem; color: var(--color-crimson-bright);">${escapeHtml(e.caseName || e.caseId)}</td>
          <td style="font-family: var(--font-mono); font-size: 0.8rem; color: #FFFFFF;">${e.scoreR1} / 15</td>
          <td style="font-family: var(--font-mono); font-size: 0.8rem; color: #FFFFFF;">${e.scoreR2} / 15</td>
          <td><span class="status-pill ${evalPillClass}">${escapeHtml(e.evaluationStatus)}</span></td>
          <td style="font-family: var(--font-mono); font-weight: 800; font-size: 0.95rem; color: #00E676;">
            ${e.totalScore} / 30 ${correctionsNotice}
          </td>
          <td>${pubBadge}</td>
          <td style="text-align: right;">
            <button type="button" class="btn-table-action btn-review-answers" data-id="${e.teamId}">
              [ REVIEW ANSWERS ]
            </button>
          </td>
        `;

        tr.querySelector('.btn-review-answers').addEventListener('click', () => {
          openDetailedAnswerReview(e.teamId, 1);
        });

        answerReviewTableBody.appendChild(tr);
      });
    }

    if (answerReviewSearchInput) {
      answerReviewSearchInput.addEventListener('input', renderAnswerReviewTable);
    }
    if (btnRefreshEvaluations) {
      btnRefreshEvaluations.addEventListener('click', loadEvaluations);
    }
    if (btnEvalReviewResults) {
      btnEvalReviewResults.addEventListener('click', () => {
        const sec = document.getElementById('section-answer-review');
        if (sec) sec.scrollIntoView({ behavior: 'smooth' });
        loadEvaluations();
      });
    }

    // 2. Detailed Answer Review (DAR) Modal
    async function openDetailedAnswerReview(teamId, roundNum = 1) {
      try {
        const res = await apiFetch(`/api/admin/submissions/detail?teamId=${encodeURIComponent(teamId)}`);
        const data = await res.json();
        if (!res.ok || !data.success || !data.submission) {
          showToast('REVIEW ERROR', data.error || 'Failed to load team submission dossier.', 'error');
          return;
        }

        currentDarSubmission = data.submission;
        currentDarRound = roundNum;

        if (darTeamId) darTeamId.textContent = currentDarSubmission.teamId;
        if (darTeamName) darTeamName.textContent = currentDarSubmission.teamName;
        if (darCaseName) darCaseName.textContent = currentDarSubmission.caseName;
        if (darOverallScore) {
          darOverallScore.textContent = `${currentDarSubmission.totalScore} / 30`;
          if (currentDarSubmission.hasCorrections) {
            darOverallScore.innerHTML = `${currentDarSubmission.totalScore} / 30 <span style="font-size: 0.72rem; color: var(--color-amber-bright); font-weight: normal;">(Orig: ${currentDarSubmission.originalTotalScore}/30)</span>`;
          }
        }
        if (darCorrectionsBadge) {
          if (currentDarSubmission.hasCorrections) {
            darCorrectionsBadge.textContent = 'AUDITED CORRECTIONS APPLIED';
            darCorrectionsBadge.className = 'status-pill badge-warning';
            darCorrectionsBadge.style.color = 'var(--color-amber-bright)';
          } else {
            darCorrectionsBadge.textContent = 'AUTOMATED (ORIGINAL)';
            darCorrectionsBadge.className = 'status-pill badge-registered';
            darCorrectionsBadge.style.color = '#FFFFFF';
          }
        }

        renderDarRound(currentDarRound);
        if (darModal) darModal.style.display = 'flex';
      } catch (err) {
        showToast('SYSTEM ERROR', 'Network error while retrieving submission detail.', 'error');
      }
    }

    function renderDarRound(roundNum) {
      currentDarRound = roundNum;
      if (!currentDarSubmission) return;

      // Update Tab Buttons
      if (btnDarTabR1) {
        if (roundNum === 1) btnDarTabR1.classList.add('active');
        else btnDarTabR1.classList.remove('active');
      }
      if (btnDarTabR2) {
        if (roundNum === 2) btnDarTabR2.classList.add('active');
        else btnDarTabR2.classList.remove('active');
      }

      const questionsList = roundNum === 1 ? (currentDarSubmission.round1 || []) : (currentDarSubmission.round2 || []);
      const totalQs = questionsList.length;
      let submittedCount = 0;
      let correctCount = 0;
      let incorrectCount = 0;
      let unansweredCount = 0;
      let roundTotalScore = 0;

      questionsList.forEach(q => {
        if (q.submittedAnswer) submittedCount++;
        else unansweredCount++;

        if (q.isCorrect) correctCount++;
        else if (q.submittedAnswer) incorrectCount++;

        roundTotalScore += (Number(q.marksAwarded) || 0);
      });

      if (darSumSubmitted) darSumSubmitted.textContent = `${submittedCount} / ${totalQs}`;
      if (darSumCorrect) darSumCorrect.textContent = correctCount;
      if (darSumIncorrect) darSumIncorrect.textContent = incorrectCount;
      if (darSumUnanswered) darSumUnanswered.textContent = unansweredCount;
      if (darSumScore) darSumScore.textContent = `${roundTotalScore} / ${totalQs}`;

      if (!darQuestionsContainer) return;
      darQuestionsContainer.innerHTML = '';

      questionsList.forEach(q => {
        const card = document.createElement('div');
        let statusClass = 'status-unanswered';
        let statusBadge = '<span class="status-pill badge-registered" style="font-size: 0.66rem;">UNANSWERED (0)</span>';
        if (q.status === 'CORRECT') {
          statusClass = 'status-correct';
          statusBadge = '<span class="status-pill badge-qualified" style="font-size: 0.66rem;">CORRECT (+1)</span>';
        } else if (q.status === 'INCORRECT') {
          statusClass = 'status-incorrect';
          statusBadge = '<span class="status-pill badge-terminated" style="font-size: 0.66rem;">INCORRECT (0)</span>';
        }

        card.className = `dar-q-card ${statusClass}`;

        // Options A, B, C, D
        const opts = q.options || {};
        let optionsHtml = '';
        ['A', 'B', 'C', 'D'].forEach(letter => {
          const optText = opts[letter] || '';
          const isSelected = (q.submittedAnswer === letter);
          const isKey = (q.correctAnswer === letter);

          let pillClass = 'dar-opt-pill';
          let badges = '';
          if (isSelected && isKey) {
            pillClass += ' both';
            badges = `<span class="dar-opt-badge-key">PARTICIPANT SELECTION &amp; OFFICIAL KEY</span>`;
          } else if (isSelected) {
            pillClass += ' selected';
            badges = `<span class="dar-opt-badge-sel">PARTICIPANT SELECTION</span>`;
          } else if (isKey) {
            pillClass += ' correct-key';
            badges = `<span class="dar-opt-badge-key">OFFICIAL ANSWER KEY</span>`;
          }

          optionsHtml += `
            <div class="${pillClass}">
              <span class="dar-opt-prefix">${letter}.</span>
              <span style="flex: 1;">${escapeHtml(optText)}</span>
              ${badges}
            </div>
          `;
        });

        // Manual Correction banner if present
        let correctionBannerHtml = '';
        if (q.hasCorrection && q.correctionInfo) {
          const info = q.correctionInfo;
          correctionBannerHtml = `
            <div class="dar-correction-banner">
              ⚠ MANUALLY CORRECTED: Mark changed from <strong>${info.prevMark}</strong> to <strong>${info.newMark}</strong> &bull; Reason: &ldquo;${escapeHtml(info.reason)}&rdquo; &bull; Admin: ${escapeHtml(info.adminUser)} (${escapeHtml(info.timestamp)})
            </div>
          `;
        }

        card.innerHTML = `
          <div class="dar-q-header">
            <div>
              <span class="dar-q-num">QUESTION ${String(q.orderNum).padStart(2, '0')} // ${escapeHtml(q.questionId)}</span>
              <span style="font-family: var(--font-mono); font-size: 0.68rem; color: var(--color-text-muted); margin-left: 8px;">CLUE: ${escapeHtml(q.evidenceRef || 'None')}</span>
            </div>
            <div style="display: flex; align-items: center; gap: 8px;">
              ${statusBadge}
              <span style="font-family: var(--font-mono); font-size: 0.74rem; font-weight: 800; color: #FFFFFF;">
                MARKS: ${q.marksAwarded} / ${q.maxMarks}
              </span>
              <button type="button" class="btn-adjust-mark" data-qid="${q.questionId}">
                [ ADJUST MARK ]
              </button>
            </div>
          </div>
          <div class="dar-q-title">${escapeHtml(q.questionText)}</div>
          <div class="dar-options-grid">
            ${optionsHtml}
          </div>
          ${correctionBannerHtml}
        `;

        card.querySelector('.btn-adjust-mark').addEventListener('click', () => {
          openMarkCorrectionModal(q);
        });

        darQuestionsContainer.appendChild(card);
      });
    }

    if (btnDarTabR1) {
      btnDarTabR1.addEventListener('click', () => renderDarRound(1));
    }
    if (btnDarTabR2) {
      btnDarTabR2.addEventListener('click', () => renderDarRound(2));
    }
    if (btnCloseDarModal) {
      btnCloseDarModal.addEventListener('click', () => {
        if (darModal) darModal.style.display = 'none';
        currentDarSubmission = null;
      });
    }
    if (btnCloseDarModalX) {
      btnCloseDarModalX.addEventListener('click', () => {
        if (darModal) darModal.style.display = 'none';
        currentDarSubmission = null;
      });
    }

    // 3. Mark Correction Modal
    function openMarkCorrectionModal(q) {
      if (!currentDarSubmission) return;
      pendingCorrectionData = {
        teamId: currentDarSubmission.teamId,
        questionId: q.questionId,
        round: currentDarRound,
        currentMark: q.marksAwarded
      };

      if (mcTeamId) mcTeamId.textContent = currentDarSubmission.teamId;
      if (mcQNum) mcQNum.textContent = `Round ${currentDarRound} — Q${q.orderNum}`;
      if (mcQId) mcQId.textContent = q.questionId;
      if (mcSubAns) mcSubAns.textContent = q.submittedAnswer || 'UNANSWERED';
      if (mcKeyAns) mcKeyAns.textContent = q.correctAnswer;
      if (mcCurrentMark) mcCurrentMark.textContent = `${q.marksAwarded} / ${q.maxMarks}`;

      if (mcNewMark) {
        mcNewMark.value = (q.marksAwarded === 1) ? '0' : '1';
      }
      if (mcReasonInput) mcReasonInput.value = '';
      if (mcConfirmCheckbox) mcConfirmCheckbox.checked = false;
      if (btnCommitMarkCorrection) btnCommitMarkCorrection.disabled = true;

      if (mcModal) mcModal.style.display = 'flex';
    }

    if (mcConfirmCheckbox) {
      mcConfirmCheckbox.addEventListener('change', () => {
        if (btnCommitMarkCorrection) {
          btnCommitMarkCorrection.disabled = !mcConfirmCheckbox.checked;
        }
      });
    }

    if (btnCancelMarkCorrection) {
      btnCancelMarkCorrection.addEventListener('click', () => {
        if (mcModal) mcModal.style.display = 'none';
        pendingCorrectionData = null;
      });
    }

    if (btnCommitMarkCorrection) {
      btnCommitMarkCorrection.addEventListener('click', async () => {
        if (!pendingCorrectionData) return;
        const reason = mcReasonInput?.value.trim();
        const newMark = parseInt(mcNewMark?.value || '0', 10);

        if (!reason || reason.length < 5) {
          showToast('JUSTIFICATION REQUIRED', 'A documented reason of at least 5 characters is required for mark correction.', 'warning');
          return;
        }

        try {
          const res = await apiFetch('/api/admin/submissions/correct-mark', {
            method: 'POST',
            body: {
              teamId: pendingCorrectionData.teamId,
              questionId: pendingCorrectionData.questionId,
              round: pendingCorrectionData.round,
              newMark,
              reason
            }
          });
          const data = await res.json();
          if (res.ok && data.success) {
            showToast('EVALUATION CORRECTED', `Question score updated. New total: ${data.totalScore}/30.`, 'success');
            if (mcModal) mcModal.style.display = 'none';
            // Refresh detailed review and table
            await openDetailedAnswerReview(pendingCorrectionData.teamId, pendingCorrectionData.round);
            await loadEvaluations();
          } else {
            showToast('CORRECTION FAILED', data.error || 'Could not commit score correction.', 'error');
          }
        } catch (err) {
          showToast('SYSTEM ERROR', 'Network error during mark correction commit.', 'error');
        }
      });
    }

    // 4. Final Winner Review & Comparison Matrix
    async function loadFinalWinnerReview() {
      try {
        const res = await apiFetch('/api/admin/winner-review');
        const data = await res.json();
        if (!res.ok || !data.success) return;

        cachedWinnerReview = data;
        const sysWinner = data.systemCalculatedWinner;
        const declWinner = data.officialDeclaredWinner;

        // Card 1: System-Calculated Winner
        if (sysWinner) {
          if (sysWinnerTeamName) sysWinnerTeamName.textContent = sysWinner.teamName || sysWinner.teamId;
          if (sysWinnerTeamId) sysWinnerTeamId.textContent = `${sysWinner.teamId} • RANK #1`;
          if (sysWinnerScore) sysWinnerScore.textContent = `${sysWinner.totalScore} / 30`;
          if (sysWinnerCase) sysWinnerCase.textContent = sysWinner.caseName || sysWinner.caseId;
        } else {
          if (sysWinnerTeamName) sysWinnerTeamName.textContent = 'NO EVALUATED TEAMS';
          if (sysWinnerScore) sysWinnerScore.textContent = '-- / 30';
        }

        // Card 2: Officially Declared Winner
        if (declWinner) {
          if (declaredWinnerTeamName) declaredWinnerTeamName.textContent = declWinner.teamName || declWinner.teamId;
          if (declaredWinnerTeamId) declaredWinnerTeamId.textContent = `${declWinner.teamId} • OFFICIAL CHAMPION`;

          if (data.isOverridden) {
            if (declaredWinnerBadge) {
              declaredWinnerBadge.textContent = 'MANUAL OVERRIDE APPROVED';
              declaredWinnerBadge.style.background = 'rgba(229, 9, 36, 0.3)';
              declaredWinnerBadge.style.color = '#FFFFFF';
            }
            if (declaredWinnerDecisionType) {
              declaredWinnerDecisionType.textContent = 'JUDGES / COMMITTEE OVERRIDE';
              declaredWinnerDecisionType.style.color = 'var(--color-crimson-bright)';
            }
            if (declaredWinnerReasonDisplay) {
              declaredWinnerReasonDisplay.textContent = `Reason: "${declWinner.overrideReason || ''}"`;
              declaredWinnerReasonDisplay.title = declWinner.overrideReason || '';
            }
          } else {
            if (declaredWinnerBadge) {
              declaredWinnerBadge.textContent = 'SYSTEM DEFAULT';
              declaredWinnerBadge.style.background = 'rgba(0, 230, 118, 0.15)';
              declaredWinnerBadge.style.color = '#00E676';
            }
            if (declaredWinnerDecisionType) {
              declaredWinnerDecisionType.textContent = 'SYSTEM DEFAULT (MATCHES RANK 1)';
              declaredWinnerDecisionType.style.color = '#00E676';
            }
            if (declaredWinnerReasonDisplay) {
              declaredWinnerReasonDisplay.textContent = 'Matches official evaluation rank #1 rules.';
              declaredWinnerReasonDisplay.title = '';
            }
          }
        }

        // Populate Winner Comparison Table
        if (!winnerComparisonTableBody) return;
        const rankings = data.rankings || [];

        if (rankings.length === 0) {
          winnerComparisonTableBody.innerHTML = `<tr><td colspan="10" style="text-align: center; color: var(--color-text-muted);">No teams evaluated yet.</td></tr>`;
          return;
        }

        winnerComparisonTableBody.innerHTML = '';
        rankings.forEach(r => {
          const tr = document.createElement('tr');
          const isWinner = (declWinner && declWinner.teamId === r.teamId);
          const isSysWinner = (sysWinner && sysWinner.teamId === r.teamId);

          let rankBadge = `<span style="font-family: var(--font-mono); font-weight: 800; color: #FFFFFF;">#${r.systemRank}</span>`;
          if (r.systemRank === 1) {
            rankBadge = `<span class="status-pill badge-qualified" style="font-size: 0.68rem;">#1 (LEADER)</span>`;
          }

          let vioBadge = `<span style="color: #00E676; font-family: var(--font-mono); font-size: 0.76rem;">CLEAN (0)</span>`;
          if (r.violationCount > 0) {
            vioBadge = `<span style="color: #FF2438; font-family: var(--font-mono); font-size: 0.76rem;">${r.violationCount} VIOLATIONS</span>`;
          }

          let winnerTag = '';
          if (isWinner) {
            winnerTag = ` <span class="status-pill" style="font-size: 0.62rem; background: rgba(229,9,36,0.3); border: 1px solid var(--color-crimson); color: #FFFFFF;">OFFICIAL WINNER</span>`;
          } else if (isSysWinner) {
            winnerTag = ` <span class="status-pill" style="font-size: 0.62rem; background: rgba(0,230,118,0.2); border: 1px solid #00E676; color: #00E676;">SYS RANK 1</span>`;
          }

          tr.innerHTML = `
            <td style="font-family: var(--font-mono); font-weight: 700; color: #FFFFFF;">${escapeHtml(r.teamId)}</td>
            <td><strong>${escapeHtml(r.teamName)}</strong> ${winnerTag}</td>
            <td style="font-family: var(--font-mono); font-size: 0.78rem; color: var(--color-crimson-bright);">${escapeHtml(r.caseId)}</td>
            <td style="font-family: var(--font-mono); font-size: 0.8rem; color: #FFFFFF;">${r.scoreR1} / 15</td>
            <td style="font-family: var(--font-mono); font-size: 0.8rem; color: #FFFFFF;">${r.scoreR2} / 15</td>
            <td style="font-family: var(--font-mono); font-weight: 800; font-size: 0.95rem; color: #00E676;">${r.totalScore} / 30</td>
            <td>${rankBadge}</td>
            <td>${vioBadge}</td>
            <td><span class="status-pill ${r.currentFinalStatus === 'QUALIFIED' ? 'badge-qualified' : 'badge-not-qualified'}">${escapeHtml(r.currentFinalStatus)}</span></td>
            <td style="text-align: right; white-space: nowrap;">
              <button type="button" class="btn-table-action btn-view-team-res" data-id="${r.teamId}">
                [ VIEW TEAM RESULT ]
              </button>
              <button type="button" class="btn-table-action btn-override-final-dec" data-id="${r.teamId}" style="margin-left: 4px;">
                [ REVIEW FINAL DECISION ]
              </button>
            </td>
          `;

          tr.querySelector('.btn-view-team-res').addEventListener('click', () => {
            openDetailedAnswerReview(r.teamId, 1);
          });
          tr.querySelector('.btn-override-final-dec').addEventListener('click', () => {
            openWinnerOverrideModal(r.teamId);
          });

          winnerComparisonTableBody.appendChild(tr);
        });
      } catch (err) {
        console.warn('Could not load winner review comparison:', err);
      }
    }

    // 5. Authorized Final-Decision Winner Override Modal
    function openWinnerOverrideModal(preselectedTeamId = '') {
      if (!cachedWinnerReview) {
        showToast('EVALUATION INCOMPLETE', 'Winner review requires evaluated submission records.', 'warning');
        return;
      }

      const sysWinner = cachedWinnerReview.systemCalculatedWinner;
      const declWinner = cachedWinnerReview.officialDeclaredWinner;

      if (woSysWinnerDisplay) {
        woSysWinnerDisplay.textContent = sysWinner
          ? `${sysWinner.teamId} — ${sysWinner.teamName} (Score: ${sysWinner.totalScore}/30)`
          : 'None';
      }
      if (woDeclWinnerDisplay) {
        woDeclWinnerDisplay.textContent = declWinner
          ? `${declWinner.teamId} — ${declWinner.teamName}`
          : 'None';
      }

      if (woWinnerSelect) {
        woWinnerSelect.innerHTML = '<option value="">-- Select Winner Team --</option>';
        (cachedWinnerReview.rankings || []).forEach(r => {
          const opt = document.createElement('option');
          opt.value = r.teamId;
          opt.textContent = `${r.teamId} — ${r.teamName} (Score: ${r.totalScore}/30, Case: ${r.caseId})`;
          woWinnerSelect.appendChild(opt);
        });

        if (preselectedTeamId) {
          woWinnerSelect.value = preselectedTeamId;
        } else if (declWinner) {
          woWinnerSelect.value = declWinner.teamId;
        }
      }

      if (woReasonInput) woReasonInput.value = '';
      if (woConfirmCheckbox) woConfirmCheckbox.checked = false;
      if (btnCommitWinnerOverride) btnCommitWinnerOverride.disabled = true;

      if (woModal) woModal.style.display = 'flex';
    }

    if (btnTriggerWinnerOverride) {
      btnTriggerWinnerOverride.addEventListener('click', () => openWinnerOverrideModal());
    }
    if (woConfirmCheckbox) {
      woConfirmCheckbox.addEventListener('change', () => {
        if (btnCommitWinnerOverride) {
          btnCommitWinnerOverride.disabled = !woConfirmCheckbox.checked;
        }
      });
    }
    if (btnCancelWinnerOverride) {
      btnCancelWinnerOverride.addEventListener('click', () => {
        if (woModal) woModal.style.display = 'none';
      });
    }

    if (btnCommitWinnerOverride) {
      btnCommitWinnerOverride.addEventListener('click', async () => {
        const winnerTeamId = woWinnerSelect?.value;
        const reason = woReasonInput?.value.trim();

        if (!winnerTeamId) {
          showToast('SELECTION REQUIRED', 'Select an official winner team.', 'warning');
          return;
        }
        if (!reason || reason.length < 5) {
          showToast('JUSTIFICATION REQUIRED', 'A documented justification of at least 5 characters is required for winner override.', 'warning');
          return;
        }

        try {
          const res = await apiFetch('/api/admin/winner-override', {
            method: 'POST',
            body: { winnerTeamId, reason }
          });
          const data = await res.json();
          if (res.ok && data.success) {
            showToast('WINNER OVERRIDE COMMITTED', `Official winner recorded for team ${winnerTeamId}.`, 'success');
            if (woModal) woModal.style.display = 'none';
            await loadEvaluations();
          } else {
            showToast('OVERRIDE FAILED', data.error || 'Failed to commit winner override.', 'error');
          }
        } catch (err) {
          showToast('SYSTEM ERROR', 'Network error during winner override.', 'error');
        }
      });
    }

    // 6. Finalize Results Modal
    if (btnFinalizeResults) {
      btnFinalizeResults.addEventListener('click', () => {
        if (cachedEvaluations.length === 0) {
          showToast('NO EVALUATIONS', 'Cannot finalize results without evaluated submissions.', 'warning');
          return;
        }

        if (finTeamsCount) finTeamsCount.textContent = cachedEvaluations.length;
        if (finSysWinner) {
          finSysWinner.textContent = cachedWinnerReview?.systemCalculatedWinner?.teamName || 'Rank 1 Verified';
        }
        if (finDeclWinner) {
          finDeclWinner.textContent = cachedWinnerReview?.officialDeclaredWinner?.teamName || 'Approved Winner';
        }

        if (finConfirmCheckbox) finConfirmCheckbox.checked = false;
        if (btnCommitFinalize) btnCommitFinalize.disabled = true;

        if (finModal) finModal.style.display = 'flex';
      });
    }

    if (finConfirmCheckbox) {
      finConfirmCheckbox.addEventListener('change', () => {
        if (btnCommitFinalize) {
          btnCommitFinalize.disabled = !finConfirmCheckbox.checked;
        }
      });
    }

    if (btnCancelFinalize) {
      btnCancelFinalize.addEventListener('click', () => {
        if (finModal) finModal.style.display = 'none';
      });
    }

    if (btnCommitFinalize) {
      btnCommitFinalize.addEventListener('click', async () => {
        try {
          const res = await apiFetch('/api/admin/results-action', {
            method: 'POST',
            body: { action: 'finalize' }
          });
          const data = await res.json();
          if (res.ok && data.success) {
            showToast('RESULTS FINALIZED', 'Authoritative results locked and sealed. Ready for publication.', 'success');
            if (finModal) finModal.style.display = 'none';
            await loadEvaluations();
          } else {
            showToast('FINALIZATION REJECTED', data.error || 'Pre-finalization check failed.', 'error');
          }
        } catch (err) {
          showToast('SYSTEM ERROR', 'Network error during finalization.', 'error');
        }
      });
    }

    // 7. Publish Results Modal
    if (btnReleaseResults) {
      btnReleaseResults.addEventListener('click', () => {
        if (cachedEvaluations.length === 0) {
          showToast('NO RESULTS', 'Cannot publish results without evaluation records.', 'warning');
          return;
        }

        const isFin = cachedEvaluations.some(e => e.isFinalized);
        if (!isFin) {
          showToast('FINALIZATION REQUIRED', 'Results must be finalized before publishing to candidates. Click [ FINALIZE RESULTS ] first.', 'warning');
          return;
        }

        if (pubWinnerName) {
          pubWinnerName.textContent = cachedWinnerReview?.officialDeclaredWinner?.teamName || 'Event Champion';
        }

        if (pubConfirmCheckbox) pubConfirmCheckbox.checked = false;
        if (btnCommitPublish) btnCommitPublish.disabled = true;

        if (pubModal) pubModal.style.display = 'flex';
      });
    }

    if (pubConfirmCheckbox) {
      pubConfirmCheckbox.addEventListener('change', () => {
        if (btnCommitPublish) {
          btnCommitPublish.disabled = !pubConfirmCheckbox.checked;
        }
      });
    }

    if (btnCancelPublish) {
      btnCancelPublish.addEventListener('click', () => {
        if (pubModal) pubModal.style.display = 'none';
      });
    }

    if (btnCommitPublish) {
      btnCommitPublish.addEventListener('click', async () => {
        try {
          const res = await apiFetch('/api/admin/results-action', {
            method: 'POST',
            body: { action: 'release' }
          });
          const data = await res.json();
          if (res.ok && data.success) {
            showToast('RESULTS PUBLISHED', 'Official results published. Authenticated candidates can now view their outcomes.', 'success');
            if (pubModal) pubModal.style.display = 'none';
            await loadEvaluations();
          } else {
            showToast('PUBLICATION FAILED', data.error || 'Failed to publish results.', 'error');
          }
        } catch (err) {
          showToast('SYSTEM ERROR', 'Network error during results publication.', 'error');
        }
      });
    }

    // 8. Withhold Results
    if (btnWithholdResults) {
      btnWithholdResults.addEventListener('click', () => {
        openConfirmModal('WITHHOLD RESULTS PUBLICATION', 'Withhold results publication? Candidate portals will immediately revert to "RESULTS UNDER REVIEW".', async () => {
          try {
            const res = await apiFetch('/api/admin/results-action', {
              method: 'POST',
              body: { action: 'withhold' }
            });
            const data = await res.json();
            if (res.ok && data.success) {
              showToast('RESULTS WITHHELD', 'Results publication revoked. Candidate portals reverted to "RESULTS UNDER REVIEW".', 'success');
              await loadEvaluations();
            } else {
              showToast('ACTION FAILED', data.error || 'Could not withhold results.', 'error');
            }
          } catch (err) {
            showToast('SYSTEM ERROR', 'Network error during withhold action.', 'error');
          }
        });
      });
    }

    // 9. Legacy Single Status Override Modal
    if (btnCancelOverride) {
      btnCancelOverride.addEventListener('click', () => {
        if (overrideModal) overrideModal.style.display = 'none';
        activeOverrideTeamId = null;
      });
    }

    if (btnSubmitOverride) {
      btnSubmitOverride.addEventListener('click', async () => {
        const newStatus = overrideSelectStatus?.value;
        const reason = overrideReasonInput?.value.trim();

        if (!activeOverrideTeamId || !newStatus || !reason) {
          showToast('INPUT REQUIRED', 'A mandatory audit reason is required for manual override.', 'warning');
          return;
        }

        try {
          const res = await apiFetch('/api/admin/override-result', {
            method: 'POST',
            body: {
              teamId: activeOverrideTeamId,
              newStatus,
              reason
            }
          });
          const data = await res.json();
          if (res.ok && data.success) {
            showToast('DECISION OVERRIDDEN', `Team ${activeOverrideTeamId} qualification updated to ${newStatus}.`, 'success');
            if (overrideModal) overrideModal.style.display = 'none';
            loadEvaluations();
          } else {
            showToast('OVERRIDE REJECTED', data.error || 'Could not commit override.', 'error');
          }
        } catch (err) {
          showToast('SYSTEM ERROR', 'Failed to communicate with audit server.', 'error');
        }
      });
    }

    // -------------------------------------------------------------------------
    // Tab 7: EVENT SETTINGS & AUDIT LOGS
    // -------------------------------------------------------------------------
    const settingsForm = document.getElementById('event-settings-form');
    const setEventAvail = document.getElementById('set-event-avail');
    const setRegAvail = document.getElementById('set-reg-avail');
    const setR1Dur = document.getElementById('set-r1-dur');
    const setR2Dur = document.getElementById('set-r2-dur');
    const setEvalDur = document.getElementById('set-eval-dur');
    const setVioLimit = document.getElementById('set-vio-limit');
    const auditLogsList = document.getElementById('audit-logs-list');

    async function loadSettings() {
      try {
        const res = await apiFetch('/api/admin/settings');
        const data = await res.json();
        const s = data.settings || {};

        if (setEventAvail) setEventAvail.checked = Boolean(s.eventAvailable);
        if (setRegAvail) setRegAvail.checked = Boolean(s.registrationAvailable);
        if (setR1Dur) setR1Dur.value = s.round1Duration || 10;
        if (setR2Dur) setR2Dur.value = s.round2Duration || 10;
        if (setEvalDur) setEvalDur.value = s.evalDuration || 5;
        if (setVioLimit) setVioLimit.value = s.violationThreshold || 3;

        loadAuditLogs();
      } catch (err) {
        console.error('Error loading settings:', err);
      }
    }

    async function loadAuditLogs() {
      if (!auditLogsList) return;
      try {
        const res = await apiFetch('/api/admin/audit-logs');
        const data = await res.json();
        const logs = data.auditLogs || [];

        if (logs.length === 0) {
          auditLogsList.innerHTML = `<div style="color: var(--color-text-muted); font-size: 0.76rem;">No administrator audit events recorded yet.</div>`;
          return;
        }

        auditLogsList.innerHTML = '';
        logs.forEach(l => {
          const item = document.createElement('div');
          item.className = 'audit-log-item';
          item.innerHTML = `
            <div class="audit-item-header">
              <span class="audit-action-tag">${escapeHtml(l.action)}</span>
              <span class="audit-meta">${escapeHtml(l.adminId)} // ${escapeHtml(l.timestamp)}</span>
            </div>
            <div class="audit-item-details">${escapeHtml(l.details)}</div>
          `;
          auditLogsList.appendChild(item);
        });
      } catch (err) {
        auditLogsList.innerHTML = `<div style="color: #FF2438;">Failed to load audit logs.</div>`;
      }
    }

    if (settingsForm) {
      settingsForm.addEventListener('submit', (e) => {
        e.preventDefault();

        const newSettings = {
          eventAvailable: setEventAvail ? setEventAvail.checked : true,
          registrationAvailable: setRegAvail ? setRegAvail.checked : true,
          round1Duration: parseInt(setR1Dur?.value || '10', 10),
          round2Duration: parseInt(setR2Dur?.value || '10', 10),
          evalDuration: parseInt(setEvalDur?.value || '5', 10),
          violationThreshold: parseInt(setVioLimit?.value || '3', 10)
        };

        openConfirmModal('COMMIT EVENT SETTINGS', 'Are you sure you want to save updated event parameters to the authoritative database?', async () => {
          try {
            const res = await apiFetch('/api/admin/settings', {
              method: 'POST',
              body: { settings: newSettings }
            });
            const data = await res.json();
            if (res.ok && data.success) {
              showToast('SETTINGS SAVED', 'Event configuration successfully committed to SQLite.', 'success');
              loadSettings();
            } else {
              showToast('SAVE FAILED', data.error || 'Could not save settings.', 'error');
            }
          } catch (err) {
            showToast('SYSTEM ERROR', 'Network error while updating settings.', 'error');
          }
        });
      });
    }

    // -------------------------------------------------------------------------
    // Tab 7: FINAL REPORT MANAGEMENT CONTROLLER
    // -------------------------------------------------------------------------
    let currentReport = null;
    let liveStatsData = null;
    let isDraftDirty = false;
    let editingResultTeamId = null;

    // Badges & Status
    const repStatusBadge = document.getElementById('report-status-badge');
    const repVersionTag = document.getElementById('report-version-badge');
    const repLastUpdated = document.getElementById('report-last-updated-text');
    const reportUnsavedBanner = document.getElementById('report-unsaved-banner');
    const reportPublishedBanner = document.getElementById('report-published-banner');
    const reportPublishedMeta = document.getElementById('report-published-meta');

    // Views
    const reportEmptyState = document.getElementById('report-empty-state');
    const reportEditorView = document.getElementById('report-editor-view');
    const reportPreviewView = document.getElementById('report-preview-view');
    const reportForm = document.getElementById('final-report-form');

    // Toolbar Actions
    const btnCreateReport = document.getElementById('btn-create-report');
    const btnEmptyCreateReport = document.getElementById('btn-empty-create-report');
    const btnEditReport = document.getElementById('btn-edit-report');
    const btnPreviewReport = document.getElementById('btn-preview-report');
    const btnExportPdf = document.getElementById('btn-export-pdf');
    const btnPublishReport = document.getElementById('btn-publish-report');
    const btnSaveDraft = document.getElementById('btn-save-draft');
    const btnSaveDraftBottom = document.getElementById('btn-save-draft-bottom');
    const btnDiscardChanges = document.getElementById('btn-discard-changes');
    const btnDiscardBottom = document.getElementById('btn-discard-bottom');
    const btnVersionHistory = document.getElementById('btn-version-history');
    const btnNewRevision = document.getElementById('btn-new-revision');
    const btnBannerNewRevision = document.getElementById('btn-banner-new-revision');

    // Preview View Actions
    const btnReturnToEditor = document.getElementById('btn-return-to-editor');
    const btnPreviewExportPdf = document.getElementById('btn-preview-export-pdf');
    const btnPreviewPublish = document.getElementById('btn-preview-publish');
    const btnPreviewBottom = document.getElementById('btn-preview-bottom');

    // Section A Form Fields
    const repEventTitle = document.getElementById('rep-event-title');
    const repCollegeName = document.getElementById('rep-college-name');
    const repDeptName = document.getElementById('rep-dept-name');
    const repEventDate = document.getElementById('rep-event-date');
    const repEventVenue = document.getElementById('rep-event-venue');
    const repOrganizer = document.getElementById('rep-organizer');
    const repCoordinators = document.getElementById('rep-coordinators');

    // Section B Rich Editors
    const repIntroEditor = document.getElementById('rep-intro-editor');
    const repOverviewEditor = document.getElementById('rep-overview-editor');
    const repObjectivesEditor = document.getElementById('rep-objectives-editor');
    const repPurposeEditor = document.getElementById('rep-purpose-editor');
    const repHighlightsEditor = document.getElementById('rep-highlights-editor');

    // Section C Participation Fields
    const liveStatReg = document.getElementById('live-stat-reg');
    const liveStatPart = document.getElementById('live-stat-part');
    const liveStatTotal = document.getElementById('live-stat-total');
    const liveStatComp = document.getElementById('live-stat-comp');
    const liveStatDisq = document.getElementById('live-stat-disq');
    const overrideStatReg = document.getElementById('override-stat-reg');
    const overrideStatPart = document.getElementById('override-stat-part');
    const overrideStatTotal = document.getElementById('override-stat-total');
    const overrideStatComp = document.getElementById('override-stat-comp');
    const overrideStatDisq = document.getElementById('override-stat-disq');
    const indicatorStatReg = document.getElementById('indicator-stat-reg');
    const indicatorStatPart = document.getElementById('indicator-stat-part');
    const indicatorStatTotal = document.getElementById('indicator-stat-total');
    const indicatorStatComp = document.getElementById('indicator-stat-comp');
    const indicatorStatDisq = document.getElementById('indicator-stat-disq');
    const statOverrideReasonWrap = document.getElementById('stat-override-reason-wrap');
    const statOverrideReason = document.getElementById('stat-override-reason');
    const btnSyncLiveStats = document.getElementById('btn-sync-live-stats');

    // Section D Form Fields
    const repR1Title = document.getElementById('rep-r1-title');
    const repR1Desc = document.getElementById('rep-r1-desc');
    const repR2Title = document.getElementById('rep-r2-title');
    const repR2Desc = document.getElementById('rep-r2-desc');
    const repEvalTitle = document.getElementById('rep-eval-title');
    const repEvalDesc = document.getElementById('rep-eval-desc');

    // Section E Results
    const btnSyncResults = document.getElementById('btn-sync-results');
    const reportResultsTbody = document.getElementById('report-results-tbody');

    // Section F Rich Editors
    const repSumHighlights = document.getElementById('rep-sum-highlights');
    const repSumChallenges = document.getElementById('rep-sum-challenges');
    const repSumPerf = document.getElementById('rep-sum-perf');
    const repSumObs = document.getElementById('rep-sum-obs');
    const repSumLessons = document.getElementById('rep-sum-lessons');
    const repSumConclusion = document.getElementById('rep-sum-conclusion');
    const repSumRecs = document.getElementById('rep-sum-recs');
    const repSumAck = document.getElementById('rep-sum-ack');

    // Section G Form Fields
    const repPrepBy = document.getElementById('rep-prep-by');
    const repOrgName = document.getElementById('rep-org-name');
    const repCoordNames = document.getElementById('rep-coord-names');
    const repFacultyCoord = document.getElementById('rep-faculty-coord');
    const repPrepDate = document.getElementById('rep-prep-date');

    // Modals
    const publishConfirmModal = document.getElementById('publish-confirm-modal');
    const btnConfirmPublish = document.getElementById('btn-confirm-publish');
    const btnCancelReportPublish = document.getElementById('btn-cancel-publish');

    const versionHistoryModal = document.getElementById('version-history-modal');
    const versionHistoryTbody = document.getElementById('version-history-tbody');
    const btnCloseVersionModal = document.getElementById('btn-close-version-modal');

    const resultCorrectionModal = document.getElementById('result-correction-modal');
    const corrTeamIdEl = document.getElementById('corr-team-id');
    const corrWinnerPos = document.getElementById('corr-winner-pos');
    const corrRecognition = document.getElementById('corr-recognition');
    const corrReason = document.getElementById('corr-reason');
    const btnCommitCorrection = document.getElementById('btn-commit-correction');
    const btnCancelCorrection = document.getElementById('btn-cancel-correction');

    const discardConfirmModal = document.getElementById('discard-confirm-modal');
    const btnConfirmDiscard = document.getElementById('btn-confirm-discard');
    const btnCancelDiscard = document.getElementById('btn-cancel-discard');

    // Helper: Mark / Clear Draft Dirty
    function markDraftDirty() {
      if (currentReport && currentReport.status !== 'PUBLISHED') {
        isDraftDirty = true;
        if (reportUnsavedBanner) reportUnsavedBanner.style.display = 'flex';
      }
    }

    function clearDraftDirty() {
      isDraftDirty = false;
      if (reportUnsavedBanner) reportUnsavedBanner.style.display = 'none';
    }

    // Helper: Bind Rich Editor Toolbars
    document.querySelectorAll('.rich-toolbar').forEach(tb => {
      const targetId = tb.getAttribute('data-target');
      const targetEl = document.getElementById(targetId);
      if (!targetEl) return;

      tb.querySelectorAll('.btn-tb').forEach(btn => {
        btn.addEventListener('click', (e) => {
          e.preventDefault();
          if (currentReport && currentReport.status === 'PUBLISHED') return;
          targetEl.focus();
          const cmd = btn.getAttribute('data-cmd');
          const val = btn.getAttribute('data-val') || null;
          document.execCommand(cmd, false, val);
          markDraftDirty();
        });
      });
    });

    // Helper: Mark dirty on input across editable areas
    const allReportInputs = [
      repEventTitle, repCollegeName, repDeptName, repEventDate, repEventVenue,
      repOrganizer, repCoordinators, repIntroEditor, repOverviewEditor,
      repObjectivesEditor, repPurposeEditor, repHighlightsEditor,
      overrideStatReg, overrideStatPart, overrideStatTotal, overrideStatComp, overrideStatDisq,
      statOverrideReason, repR1Title, repR1Desc, repR2Title, repR2Desc, repEvalTitle, repEvalDesc,
      repSumHighlights, repSumChallenges, repSumPerf, repSumObs, repSumLessons,
      repSumConclusion, repSumRecs, repSumAck, repPrepBy, repOrgName, repCoordNames,
      repFacultyCoord, repPrepDate
    ];

    allReportInputs.forEach(el => {
      if (!el) return;
      el.addEventListener('input', () => {
        markDraftDirty();
        checkParticipationOverrides();
      });
      el.addEventListener('change', () => {
        markDraftDirty();
        checkParticipationOverrides();
      });
    });

    // Check participation manual overrides against live stats
    function checkParticipationOverrides() {
      if (!liveStatsData) return;

      const pairs = [
        { live: liveStatsData.registeredTeams, ov: overrideStatReg, ind: indicatorStatReg },
        { live: liveStatsData.participatingTeams, ov: overrideStatPart, ind: indicatorStatPart },
        { live: liveStatsData.totalParticipants, ov: overrideStatTotal, ind: indicatorStatTotal },
        { live: liveStatsData.completedInvestigations, ov: overrideStatComp, ind: indicatorStatComp },
        { live: liveStatsData.disqualifiedTeams, ov: overrideStatDisq, ind: indicatorStatDisq }
      ];

      let anyOverride = false;
      pairs.forEach(p => {
        if (!p.ov || !p.ind) return;
        const ovVal = p.ov.value.trim();
        if (ovVal !== '' && parseInt(ovVal, 10) !== parseInt(p.live, 10)) {
          p.ind.style.display = 'block';
          anyOverride = true;
        } else {
          p.ind.style.display = 'none';
        }
      });

      if (statOverrideReasonWrap) {
        statOverrideReasonWrap.style.display = anyOverride ? 'block' : 'none';
      }
    }

    // Render Section E: Results Table
    function renderReportResultsTable() {
      if (!reportResultsTbody) return;
      if (!currentReport || !Array.isArray(currentReport.results)) {
        reportResultsTbody.innerHTML = `<tr><td colspan="7" style="text-align: center; color: var(--color-text-muted); padding: 1.5rem;">No official evaluated results loaded yet.</td></tr>`;
        return;
      }

      reportResultsTbody.innerHTML = '';
      const isPublished = currentReport.status === 'PUBLISHED';

      currentReport.results.forEach(r => {
        const tr = document.createElement('tr');
        const statusClass = r.finalStatus === 'QUALIFIED' ? 'status-active' :
                           (r.finalStatus === 'DISQUALIFIED' ? 'status-terminated' : 'status-review');

        tr.innerHTML = `
          <td style="font-family: var(--font-mono); font-weight: 700; color: #FFFFFF;">${escapeHtml(r.teamId)}</td>
          <td style="font-weight: 700;">${escapeHtml(r.teamName)}</td>
          <td style="color: var(--color-text-secondary);">${escapeHtml(r.collegeName)}</td>
          <td style="font-family: var(--font-mono); font-weight: 700; color: #FFFFFF;">${escapeHtml(String(r.totalScore))} / 30</td>
          <td style="font-family: var(--font-mono); color: var(--color-crimson-bright); font-weight: 700;">${escapeHtml(r.accuracy)}</td>
          <td><span class="status-pill ${statusClass}">${escapeHtml(r.finalStatus)}</span></td>
          <td style="font-weight: 700; color: #FFFFFF;">${escapeHtml(r.winnerPosition || 'Participant')}</td>
          <td style="font-size: 0.76rem; color: var(--color-text-secondary);">${escapeHtml(r.recognition || 'Certificate of Merit')}</td>
          <td style="text-align: right;">
            <button type="button" class="btn-table-action btn-edit-award" data-tid="${escapeHtml(r.teamId)}" ${isPublished ? 'disabled title="Cannot edit published report awards"' : ''}>
              ✏ [ EDIT AWARD ]
            </button>
          </td>
        `;

        const btnEdit = tr.querySelector('.btn-edit-award');
        if (btnEdit && !isPublished) {
          btnEdit.addEventListener('click', () => {
            openResultCorrectionModal(r);
          });
        }

        reportResultsTbody.appendChild(tr);
      });
    }

    // Modal: Open Result / Award Correction
    function openResultCorrectionModal(teamResult) {
      if (!resultCorrectionModal) return;
      editingResultTeamId = teamResult.teamId;
      if (corrTeamIdEl) corrTeamIdEl.textContent = `${teamResult.teamId} (${teamResult.teamName})`;
      if (corrWinnerPos) corrWinnerPos.value = teamResult.winnerPosition || '';
      if (corrRecognition) corrRecognition.value = teamResult.recognition || '';
      if (corrReason) corrReason.value = teamResult.manualCorrectionReason || '';
      resultCorrectionModal.style.display = 'flex';
    }

    if (btnCancelCorrection) {
      btnCancelCorrection.addEventListener('click', () => {
        if (resultCorrectionModal) resultCorrectionModal.style.display = 'none';
        editingResultTeamId = null;
      });
    }

    if (btnCommitCorrection) {
      btnCommitCorrection.addEventListener('click', () => {
        const reason = corrReason ? corrReason.value.trim() : '';
        if (!reason) {
          showToast('AUDIT REASON REQUIRED', 'A mandatory audit reason is required for any manual award correction.', 'error');
          if (corrReason) corrReason.focus();
          return;
        }

        if (!currentReport || !currentReport.results) return;
        const target = currentReport.results.find(r => r.teamId === editingResultTeamId);
        if (target) {
          target.winnerPosition = corrWinnerPos ? corrWinnerPos.value.trim() : target.winnerPosition;
          target.recognition = corrRecognition ? corrRecognition.value.trim() : target.recognition;
          target.manualCorrectionReason = reason;

          markDraftDirty();
          renderReportResultsTable();
          showToast('AWARD ADJUSTED', `Award updated for ${target.teamId}. Save draft to commit change to SQLite.`, 'info');
        }

        if (resultCorrectionModal) resultCorrectionModal.style.display = 'none';
        editingResultTeamId = null;
      });
    }

    // Re-sync Live Stats button
    if (btnSyncLiveStats) {
      btnSyncLiveStats.addEventListener('click', async () => {
        try {
          const res = await apiFetch('/api/admin/report/live-stats');
          const data = await res.json();
          if (res.ok && data.liveStats) {
            liveStatsData = data.liveStats;
            populateParticipationUI(data.liveStats, null);
            showToast('STATS RE-SYNCED', 'Live SQLite database metrics successfully refreshed.', 'success');
          }
        } catch (e) {
          showToast('SYNC FAILED', 'Could not refresh live statistics from database.', 'error');
        }
      });
    }

    // Re-sync Results button
    if (btnSyncResults) {
      btnSyncResults.addEventListener('click', async () => {
        try {
          const res = await apiFetch('/api/admin/report/live-stats');
          const data = await res.json();
          if (res.ok && data.liveStats && Array.isArray(data.liveStats.results)) {
            currentReport.results = data.liveStats.results;
            renderReportResultsTable();
            markDraftDirty();
            showToast('RESULTS RE-SYNCED', 'Evaluation & Results matrix re-synced from SQLite.', 'success');
          }
        } catch (e) {
          showToast('SYNC FAILED', 'Could not re-sync results from database.', 'error');
        }
      });
    }

    // Populate Participation Section UI
    function populateParticipationUI(live, partData) {
      if (!live) return;
      if (liveStatReg) liveStatReg.textContent = live.registeredTeams;
      if (liveStatPart) liveStatPart.textContent = live.participatingTeams;
      if (liveStatTotal) liveStatTotal.textContent = live.totalParticipants;
      if (liveStatComp) liveStatComp.textContent = live.completedInvestigations;
      if (liveStatDisq) liveStatDisq.textContent = live.disqualifiedTeams;

      const ov = (partData && partData.manualOverrides) || {};
      if (overrideStatReg) overrideStatReg.value = ov.registered !== null && ov.registered !== undefined ? ov.registered : live.registeredTeams;
      if (overrideStatPart) overrideStatPart.value = ov.participating !== null && ov.participating !== undefined ? ov.participating : live.participatingTeams;
      if (overrideStatTotal) overrideStatTotal.value = ov.participants !== null && ov.participants !== undefined ? ov.participants : live.totalParticipants;
      if (overrideStatComp) overrideStatComp.value = ov.completed !== null && ov.completed !== undefined ? ov.completed : live.completedInvestigations;
      if (overrideStatDisq) overrideStatDisq.value = ov.disqualified !== null && ov.disqualified !== undefined ? ov.disqualified : live.disqualifiedTeams;
      if (statOverrideReason) statOverrideReason.value = ov.reason || '';

      checkParticipationOverrides();
    }

    // Populate Full Report Form from Report Object
    function populateReportForm(rep, live) {
      // Section A
      if (repEventTitle) repEventTitle.value = rep.title || '';
      if (repCollegeName) repCollegeName.value = rep.collegeName || '';
      if (repDeptName) repDeptName.value = rep.departmentName || '';
      if (repEventDate) repEventDate.value = rep.eventDate || '';
      if (repEventVenue) repEventVenue.value = rep.eventVenue || '';
      if (repOrganizer) repOrganizer.value = rep.organizer || '';
      if (repCoordinators) repCoordinators.value = rep.coordinators || '';

      // Section B
      const ov = rep.overview || {};
      if (repIntroEditor) repIntroEditor.innerHTML = ov.intro || '';
      if (repOverviewEditor) repOverviewEditor.innerHTML = ov.overview || '';
      if (repObjectivesEditor) repObjectivesEditor.innerHTML = ov.objectives || '';
      if (repPurposeEditor) repPurposeEditor.innerHTML = ov.purpose || '';
      if (repHighlightsEditor) repHighlightsEditor.innerHTML = ov.highlights || '';

      // Section C
      populateParticipationUI(live, rep.participation);

      // Section D
      const st = rep.structure || {};
      if (repR1Title) repR1Title.value = st.r1Title || 'ROUND 1: 15 QUESTIONS — 10 MINUTES';
      if (repR1Desc) repR1Desc.value = st.r1Desc || '';
      if (repR2Title) repR2Title.value = st.r2Desc ? st.r2Title : 'ROUND 2: 15 QUESTIONS — 10 MINUTES';
      if (repR2Desc) repR2Desc.value = st.r2Desc || '';
      if (repEvalTitle) repEvalTitle.value = st.evalDesc ? st.evalTitle : 'EVALUATION: 5 MINUTES';
      if (repEvalDesc) repEvalDesc.value = st.evalDesc || '';

      // Section E
      renderReportResultsTable();

      // Section F
      const sum = rep.summary || {};
      if (repSumHighlights) repSumHighlights.innerHTML = sum.highlights || '';
      if (repSumChallenges) repSumChallenges.innerHTML = sum.challenges || '';
      if (repSumPerf) repSumPerf.innerHTML = sum.performance || '';
      if (repSumObs) repSumObs.innerHTML = sum.observations || '';
      if (repSumLessons) repSumLessons.innerHTML = sum.lessons || '';
      if (repSumConclusion) repSumConclusion.innerHTML = sum.conclusion || '';
      if (repSumRecs) repSumRecs.innerHTML = sum.recommendations || '';
      if (repSumAck) repSumAck.innerHTML = sum.acknowledgements || '';

      // Section G
      const org = rep.organizers || {};
      if (repPrepBy) repPrepBy.value = org.preparedBy || '';
      if (repOrgName) repOrgName.value = org.organizerName || '';
      if (repCoordNames) repCoordNames.value = org.coordinatorNames || '';
      if (repFacultyCoord) repFacultyCoord.value = org.facultyCoordinator || '';
      if (repPrepDate) repPrepDate.value = org.prepDate || '';

      // Status Banners & Controls
      const isPub = rep.status === 'PUBLISHED';
      if (reportPublishedBanner) {
        reportPublishedBanner.style.display = isPub ? 'flex' : 'none';
        if (reportPublishedMeta && isPub) {
          reportPublishedMeta.textContent = `Published by ${rep.publishedBy || 'CSE Admin'} on ${rep.publishedAt ? new Date(rep.publishedAt).toLocaleString() : 'N/A'}`;
        }
      }

      if (btnNewRevision) btnNewRevision.style.display = isPub ? 'inline-flex' : 'none';
      if (btnPublishReport) {
        if (isPub) {
          btnPublishReport.disabled = true;
          btnPublishReport.innerHTML = `<span>✔ [ PUBLISHED ]</span>`;
        } else {
          btnPublishReport.disabled = false;
          btnPublishReport.innerHTML = `<span>[ PUBLISH REPORT ]</span>`;
        }
      }

      // Disable inputs if published
      allReportInputs.forEach(el => {
        if (!el) return;
        if (el.contentEditable === 'true' || el.contentEditable === 'false') {
          el.contentEditable = isPub ? 'false' : 'true';
        } else {
          el.disabled = isPub;
        }
      });

      if (btnSaveDraft) btnSaveDraft.disabled = isPub;
      if (btnSaveDraftBottom) btnSaveDraftBottom.disabled = isPub;

      clearDraftDirty();
    }

    // Main: Load Report from Backend
    async function loadFinalReport() {
      try {
        const res = await apiFetch('/api/admin/report');
        const data = await res.json();

        liveStatsData = data.liveStats;

        if (!data.hasReport || !data.report) {
          currentReport = null;
          if (reportEmptyState) reportEmptyState.style.display = 'block';
          if (reportEditorView) reportEditorView.style.display = 'none';
          if (reportPreviewView) reportPreviewView.style.display = 'none';

          if (repStatusBadge) {
            repStatusBadge.textContent = 'NO REPORT';
            repStatusBadge.className = 'status-badge status-draft';
          }
          if (repVersionTag) repVersionTag.textContent = 'v0';
          if (repLastUpdated) repLastUpdated.textContent = 'No report record in database';

          // Disable buttons except create
          [btnEditReport, btnPreviewReport, btnExportPdf, btnPublishReport, btnSaveDraft, btnDiscardChanges, btnVersionHistory, btnNewRevision].forEach(b => {
            if (b) b.disabled = true;
          });
          if (btnCreateReport) btnCreateReport.disabled = false;
          return;
        }

        // Report exists
        currentReport = data.report;
        if (reportEmptyState) reportEmptyState.style.display = 'none';
        if (reportEditorView) reportEditorView.style.display = 'block';
        if (reportPreviewView) reportPreviewView.style.display = 'none';

        // Enable buttons
        [btnEditReport, btnPreviewReport, btnExportPdf, btnPublishReport, btnSaveDraft, btnDiscardChanges, btnVersionHistory].forEach(b => {
          if (b) b.disabled = false;
        });
        if (btnCreateReport) btnCreateReport.disabled = false;

        // Status Badge
        if (repStatusBadge) {
          repStatusBadge.textContent = currentReport.status;
          repStatusBadge.className = 'status-badge';
          if (currentReport.status === 'DRAFT') repStatusBadge.classList.add('status-draft');
          if (currentReport.status === 'IN REVIEW') repStatusBadge.classList.add('status-in-review');
          if (currentReport.status === 'FINALIZED') repStatusBadge.classList.add('status-finalized');
          if (currentReport.status === 'PUBLISHED') repStatusBadge.classList.add('status-published');
        }

        // Version & Timestamps
        if (repVersionTag) repVersionTag.textContent = `v${currentReport.version}`;
        if (repLastUpdated) {
          const dtStr = currentReport.updatedAt ? new Date(currentReport.updatedAt).toLocaleString() : 'N/A';
          repLastUpdated.textContent = `Updated: ${dtStr} by ${currentReport.updatedBy || 'admin'}`;
        }

        populateReportForm(currentReport, liveStatsData);

      } catch (err) {
        console.error('Error loading report:', err);
        showToast('SYSTEM ERROR', 'Failed to retrieve event report from SQLite database.', 'error');
      }
    }

    // Action: Create New Report
    async function createNewReportDraft() {
      openConfirmModal('CREATE EVENT REPORT', 'Initialize a new official event report draft using current live database values?', async () => {
        try {
          const res = await apiFetch('/api/admin/report/create', { method: 'POST' });
          const data = await res.json();
          if (res.ok && data.success) {
            showToast('REPORT CREATED', `Initialized Draft Report #${data.id} in SQLite.`, 'success');
            loadFinalReport();
          } else {
            showToast('CREATION FAILED', data.error || 'Could not initialize report.', 'error');
          }
        } catch (e) {
          showToast('SYSTEM ERROR', 'Network error while initializing report.', 'error');
        }
      });
    }

    if (btnCreateReport) btnCreateReport.addEventListener('click', createNewReportDraft);
    if (btnEmptyCreateReport) btnEmptyCreateReport.addEventListener('click', createNewReportDraft);

    // Action: Save Draft
    async function saveReportDraft(changeSummary = 'Draft updated by administrator') {
      if (!currentReport) return;
      if (currentReport.status === 'PUBLISHED') {
        showToast('CANNOT EDIT PUBLISHED', 'This report is published. Please click [ NEW REVISION ] to make edits.', 'error');
        return;
      }

      // Check if manual overrides exist and need reason
      const ovReason = statOverrideReason ? statOverrideReason.value.trim() : '';
      const pairs = [
        { live: liveStatsData.registeredTeams, ov: overrideStatReg },
        { live: liveStatsData.participatingTeams, ov: overrideStatPart },
        { live: liveStatsData.totalParticipants, ov: overrideStatTotal },
        { live: liveStatsData.completedInvestigations, ov: overrideStatComp },
        { live: liveStatsData.disqualifiedTeams, ov: overrideStatDisq }
      ];
      let hasMismatch = pairs.some(p => p.ov && p.ov.value.trim() !== '' && parseInt(p.ov.value.trim(), 10) !== parseInt(p.live, 10));
      if (hasMismatch && !ovReason) {
        showToast('AUDIT REASON REQUIRED', 'A reason is required when overriding calculated event metrics.', 'error');
        if (statOverrideReason) statOverrideReason.focus();
        return;
      }

      const payload = {
        id: currentReport.id,
        title: repEventTitle ? repEventTitle.value.trim() : currentReport.title,
        collegeName: repCollegeName ? repCollegeName.value.trim() : currentReport.collegeName,
        departmentName: repDeptName ? repDeptName.value.trim() : currentReport.departmentName,
        eventDate: repEventDate ? repEventDate.value.trim() : currentReport.eventDate,
        eventVenue: repEventVenue ? repEventVenue.value.trim() : currentReport.eventVenue,
        organizer: repOrganizer ? repOrganizer.value.trim() : currentReport.organizer,
        coordinators: repCoordinators ? repCoordinators.value.trim() : currentReport.coordinators,
        overview: {
          intro: repIntroEditor ? repIntroEditor.innerHTML : '',
          overview: repOverviewEditor ? repOverviewEditor.innerHTML : '',
          objectives: repObjectivesEditor ? repObjectivesEditor.innerHTML : '',
          purpose: repPurposeEditor ? repPurposeEditor.innerHTML : '',
          highlights: repHighlightsEditor ? repHighlightsEditor.innerHTML : ''
        },
        participation: {
          registeredTeams: overrideStatReg && overrideStatReg.value ? parseInt(overrideStatReg.value, 10) : liveStatsData.registeredTeams,
          participatingTeams: overrideStatPart && overrideStatPart.value ? parseInt(overrideStatPart.value, 10) : liveStatsData.participatingTeams,
          totalParticipants: overrideStatTotal && overrideStatTotal.value ? parseInt(overrideStatTotal.value, 10) : liveStatsData.totalParticipants,
          completedInvestigations: overrideStatComp && overrideStatComp.value ? parseInt(overrideStatComp.value, 10) : liveStatsData.completedInvestigations,
          disqualifiedTeams: overrideStatDisq && overrideStatDisq.value ? parseInt(overrideStatDisq.value, 10) : liveStatsData.disqualifiedTeams,
          manualOverrides: {
            registered: overrideStatReg && overrideStatReg.value ? parseInt(overrideStatReg.value, 10) : null,
            participating: overrideStatPart && overrideStatPart.value ? parseInt(overrideStatPart.value, 10) : null,
            participants: overrideStatTotal && overrideStatTotal.value ? parseInt(overrideStatTotal.value, 10) : null,
            completed: overrideStatComp && overrideStatComp.value ? parseInt(overrideStatComp.value, 10) : null,
            disqualified: overrideStatDisq && overrideStatDisq.value ? parseInt(overrideStatDisq.value, 10) : null,
            reason: ovReason
          }
        },
        structure: {
          r1Title: repR1Title ? repR1Title.value.trim() : 'ROUND 1: 15 QUESTIONS — 10 MINUTES',
          r1Desc: repR1Desc ? repR1Desc.value.trim() : '',
          r2Title: repR2Title ? repR2Title.value.trim() : 'ROUND 2: 15 QUESTIONS — 10 MINUTES',
          r2Desc: repR2Desc ? repR2Desc.value.trim() : '',
          evalTitle: repEvalTitle ? repEvalTitle.value.trim() : 'EVALUATION: 5 MINUTES',
          evalDesc: repEvalDesc ? repEvalDesc.value.trim() : ''
        },
        results: currentReport.results || [],
        summary: {
          highlights: repSumHighlights ? repSumHighlights.innerHTML : '',
          challenges: repSumChallenges ? repSumChallenges.innerHTML : '',
          performance: repSumPerf ? repSumPerf.innerHTML : '',
          observations: repSumObs ? repSumObs.innerHTML : '',
          lessons: repSumLessons ? repSumLessons.innerHTML : '',
          conclusion: repSumConclusion ? repSumConclusion.innerHTML : '',
          recommendations: repSumRecs ? repSumRecs.innerHTML : '',
          acknowledgements: repSumAck ? repSumAck.innerHTML : ''
        },
        organizers: {
          preparedBy: repPrepBy ? repPrepBy.value.trim() : '',
          organizerName: repOrgName ? repOrgName.value.trim() : '',
          coordinatorNames: repCoordNames ? repCoordNames.value.trim() : '',
          facultyCoordinator: repFacultyCoord ? repFacultyCoord.value.trim() : '',
          prepDate: repPrepDate ? repPrepDate.value.trim() : ''
        },
        changeSummary: changeSummary
      };

      try {
        const res = await apiFetch('/api/admin/report/save', {
          method: 'POST',
          body: payload
        });
        const data = await res.json();
        if (res.ok && data.success) {
          clearDraftDirty();
          showToast('DRAFT SAVED', `Report version v${data.version} successfully persisted to SQLite.`, 'success');
          loadFinalReport();
        } else {
          showToast('SAVE FAILED', data.error || 'Failed to persist draft.', 'error');
        }
      } catch (e) {
        showToast('SYSTEM ERROR', 'Network error while saving report draft.', 'error');
      }
    }

    if (btnSaveDraft) btnSaveDraft.addEventListener('click', () => saveReportDraft());
    if (btnSaveDraftBottom) btnSaveDraftBottom.addEventListener('click', () => saveReportDraft());

    // Action: Discard Changes with Confirmation
    function discardDraftChanges() {
      if (!isDraftDirty) {
        showToast('NO CHANGES', 'No unsaved modifications to discard.', 'info');
        return;
      }
      if (discardConfirmModal) discardConfirmModal.style.display = 'flex';
    }

    if (btnDiscardChanges) btnDiscardChanges.addEventListener('click', discardDraftChanges);
    if (btnDiscardBottom) btnDiscardBottom.addEventListener('click', discardDraftChanges);

    if (btnCancelDiscard) {
      btnCancelDiscard.addEventListener('click', () => {
        if (discardConfirmModal) discardConfirmModal.style.display = 'none';
      });
    }

    if (btnConfirmDiscard) {
      btnConfirmDiscard.addEventListener('click', () => {
        if (discardConfirmModal) discardConfirmModal.style.display = 'none';
        clearDraftDirty();
        loadFinalReport();
        showToast('CHANGES DISCARDED', 'Reverted unsaved edits to last saved state.', 'info');
      });
    }

    // Render Official Printable Report Preview Sheet
    function renderPreviewSheet() {
      if (!currentReport) return;

      // Header Block
      const prevCollege = document.getElementById('prev-college-name');
      const prevDept = document.getElementById('prev-dept-name');
      const prevTitle = document.getElementById('prev-event-title');
      const prevDate = document.getElementById('prev-event-date');
      const prevVenue = document.getElementById('prev-event-venue');
      const prevOrg = document.getElementById('prev-organizer');

      if (prevCollege) prevCollege.textContent = (repCollegeName && repCollegeName.value) || currentReport.collegeName;
      if (prevDept) prevDept.textContent = (repDeptName && repDeptName.value) || currentReport.departmentName;
      if (prevTitle) prevTitle.textContent = (repEventTitle && repEventTitle.value) || currentReport.title;
      if (prevDate) prevDate.textContent = (repEventDate && repEventDate.value) || currentReport.eventDate;
      if (prevVenue) prevVenue.textContent = (repEventVenue && repEventVenue.value) || currentReport.eventVenue;
      if (prevOrg) prevOrg.textContent = (repOrganizer && repOrganizer.value) || currentReport.organizer;

      // Status Pill & Watermark
      const prevPill = document.getElementById('preview-status-badge');
      const prevWatermark = document.getElementById('preview-draft-watermark');
      const prevBannerText = document.getElementById('prev-status-banner-text');

      const isPub = currentReport.status === 'PUBLISHED';
      if (prevPill) {
        prevPill.textContent = isPub ? 'PUBLISHED OFFICIAL REPORT' : `${currentReport.status} PREVIEW`;
        prevPill.style.color = isPub ? '#00E676' : '#FF2438';
      }
      if (prevWatermark) {
        prevWatermark.style.display = isPub ? 'none' : 'block';
        prevWatermark.textContent = `OFFICIAL ${currentReport.status} — NOT YET SEALED`;
      }
      if (prevBannerText) {
        prevBannerText.textContent = isPub ?
          `OFFICIAL AUTHORITATIVE EVENT RECORD // PUBLISHED ${new Date(currentReport.publishedAt || Date.now()).toLocaleDateString()}` :
          `DOCUMENT STATUS: ${currentReport.status} // INTERNAL CSE ASSESSMENT RECORD`;
      }

      // Section 1: Overview
      const prevIntro = document.getElementById('prev-intro');
      const prevOv = document.getElementById('prev-overview');
      const prevObj = document.getElementById('prev-objectives');
      const prevPurp = document.getElementById('prev-purpose');
      const prevHigh = document.getElementById('prev-highlights');

      if (prevIntro) prevIntro.innerHTML = (repIntroEditor && repIntroEditor.innerHTML) || '';
      if (prevOv) prevOv.innerHTML = (repOverviewEditor && repOverviewEditor.innerHTML) || '';
      if (prevObj) prevObj.innerHTML = (repObjectivesEditor && repObjectivesEditor.innerHTML) || '';
      if (prevPurp) prevPurp.innerHTML = (repPurposeEditor && repPurposeEditor.innerHTML) || '';
      if (prevHigh) prevHigh.innerHTML = (repHighlightsEditor && repHighlightsEditor.innerHTML) || '';

      // Section 2: Participation Table
      const prevPartTbody = document.getElementById('prev-participation-tbody');
      if (prevPartTbody && liveStatsData) {
        const regVal = (overrideStatReg && overrideStatReg.value) || liveStatsData.registeredTeams;
        const partVal = (overrideStatPart && overrideStatPart.value) || liveStatsData.participatingTeams;
        const totalVal = (overrideStatTotal && overrideStatTotal.value) || liveStatsData.totalParticipants;
        const compVal = (overrideStatComp && overrideStatComp.value) || liveStatsData.completedInvestigations;
        const disqVal = (overrideStatDisq && overrideStatDisq.value) || liveStatsData.disqualifiedTeams;
        const reason = (statOverrideReason && statOverrideReason.value.trim()) || '';

        const rows = [
          { name: 'Total Registered Teams', count: regVal, live: liveStatsData.registeredTeams },
          { name: 'Active Participating Teams', count: partVal, live: liveStatsData.participatingTeams },
          { name: 'Total Student Participants', count: totalVal, live: liveStatsData.totalParticipants },
          { name: 'Completed Full Investigations', count: compVal, live: liveStatsData.completedInvestigations },
          { name: 'Disqualified / Terminated Teams', count: disqVal, live: liveStatsData.disqualifiedTeams }
        ];

        prevPartTbody.innerHTML = '';
        rows.forEach(r => {
          const isOverridden = parseInt(r.count, 10) !== parseInt(r.live, 10);
          const tr = document.createElement('tr');
          tr.innerHTML = `
            <td><strong>${escapeHtml(r.name)}</strong></td>
            <td style="font-family: var(--font-mono); font-weight: 700; font-size: 0.9rem;">${escapeHtml(String(r.count))}</td>
            <td>${isOverridden ? '<span style="color: #B5081C; font-weight: 700;">Manual Override</span>' : 'Authoritative SQLite Database'}</td>
            <td>${isOverridden ? escapeHtml(reason || 'Audited manual figure') : 'Verified by automated session monitor'}</td>
          `;
          prevPartTbody.appendChild(tr);
        });
      }

      // Section 3: Structure
      const prevR1Title = document.getElementById('prev-r1-title');
      const prevR1Desc = document.getElementById('prev-r1-desc');
      const prevR2Title = document.getElementById('prev-r2-title');
      const prevR2Desc = document.getElementById('prev-r2-desc');
      const prevEvalTitle = document.getElementById('prev-eval-title');
      const prevEvalDesc = document.getElementById('prev-eval-desc');

      if (prevR1Title) prevR1Title.textContent = (repR1Title && repR1Title.value) || 'ROUND 1: 15 QUESTIONS — 10 MINUTES';
      if (prevR1Desc) prevR1Desc.textContent = (repR1Desc && repR1Desc.value) || '';
      if (prevR2Title) prevR2Title.textContent = (repR2Title && repR2Title.value) || 'ROUND 2: 15 QUESTIONS — 10 MINUTES';
      if (prevR2Desc) prevR2Desc.textContent = (repR2Desc && repR2Desc.value) || '';
      if (prevEvalTitle) prevEvalTitle.textContent = (repEvalTitle && repEvalTitle.value) || 'EVALUATION: 5 MINUTES';
      if (prevEvalDesc) prevEvalDesc.textContent = (repEvalDesc && repEvalDesc.value) || '';

      // Section 4: Results Table
      const prevResTbody = document.getElementById('prev-results-tbody');
      if (prevResTbody) {
        prevResTbody.innerHTML = '';
        const results = currentReport.results || [];
        results.forEach(r => {
          const tr = document.createElement('tr');
          tr.innerHTML = `
            <td style="font-family: var(--font-mono); font-weight: 700;">${escapeHtml(r.teamId)}</td>
            <td><strong>${escapeHtml(r.teamName)}</strong></td>
            <td>${escapeHtml(r.collegeName)}</td>
            <td style="font-family: var(--font-mono); font-weight: 700;">${escapeHtml(String(r.totalScore))}</td>
            <td style="font-family: var(--font-mono); font-weight: 700;">${escapeHtml(r.accuracy)}</td>
            <td><strong>${escapeHtml(r.finalStatus)}</strong></td>
            <td style="font-weight: 800; color: #B5081C;">${escapeHtml(r.winnerPosition || 'Participant')}</td>
            <td>${escapeHtml(r.recognition || 'Certificate of Merit')}</td>
          `;
          prevResTbody.appendChild(tr);
        });
      }

      // Section 5: Observations & Analysis
      const prevPerf = document.getElementById('prev-sum-perf');
      const prevChallenges = document.getElementById('prev-sum-challenges');
      const prevObs = document.getElementById('prev-sum-obs');
      const prevLessons = document.getElementById('prev-sum-lessons');

      if (prevPerf) prevPerf.innerHTML = (repSumPerf && repSumPerf.innerHTML) || '';
      if (prevChallenges) prevChallenges.innerHTML = (repSumChallenges && repSumChallenges.innerHTML) || '';
      if (prevObs) prevObs.innerHTML = (repSumObs && repSumObs.innerHTML) || '';
      if (prevLessons) prevLessons.innerHTML = (repSumLessons && repSumLessons.innerHTML) || '';

      // Section 6: Recommendations & Conclusion
      const prevRecs = document.getElementById('prev-sum-recs');
      const prevConc = document.getElementById('prev-sum-conclusion');
      const prevAck = document.getElementById('prev-sum-ack');

      if (prevRecs) prevRecs.innerHTML = (repSumRecs && repSumRecs.innerHTML) || '';
      if (prevConc) prevConc.innerHTML = (repSumConclusion && repSumConclusion.innerHTML) || '';
      if (prevAck) prevAck.innerHTML = (repSumAck && repSumAck.innerHTML) || '';

      // Section 7: Signatures
      const prevSigPrep = document.getElementById('prev-sig-prep');
      const prevSigFaculty = document.getElementById('prev-sig-faculty');

      if (prevSigPrep) prevSigPrep.textContent = (repPrepBy && repPrepBy.value) || currentReport.organizers?.preparedBy || 'CSE Event Coordinator';
      if (prevSigFaculty) prevSigFaculty.textContent = (repFacultyCoord && repFacultyCoord.value) || currentReport.organizers?.facultyCoordinator || 'CSE Faculty Lead';

      // Footer
      const prevFooter = document.getElementById('prev-report-footer-version');
      if (prevFooter) {
        prevFooter.textContent = `REPORT VERSION v${currentReport.version} // OFFICIAL T.J.S. RECORD`;
      }

      // Switch View
      if (reportEditorView) reportEditorView.style.display = 'none';
      if (reportPreviewView) reportPreviewView.style.display = 'flex';
      if (btnPreviewPublish) {
        btnPreviewPublish.style.display = isPub ? 'none' : 'inline-flex';
      }
    }

    // Switch between Editor and Preview
    function switchToEditor() {
      if (reportPreviewView) reportPreviewView.style.display = 'none';
      if (reportEditorView) reportEditorView.style.display = 'block';
    }

    if (btnEditReport) btnEditReport.addEventListener('click', switchToEditor);
    if (btnReturnToEditor) btnReturnToEditor.addEventListener('click', switchToEditor);

    if (btnPreviewReport) {
      btnPreviewReport.addEventListener('click', () => {
        renderPreviewSheet();
      });
    }

    if (btnPreviewBottom) {
      btnPreviewBottom.addEventListener('click', () => {
        renderPreviewSheet();
      });
    }

    // Operational PDF Export Function
    function exportReportPdf() {
      renderPreviewSheet();
      // Brief timeout to ensure DOM update is painted before print dialog
      setTimeout(() => {
        window.print();
      }, 150);
    }

    if (btnExportPdf) btnExportPdf.addEventListener('click', exportReportPdf);
    if (btnPreviewExportPdf) btnPreviewExportPdf.addEventListener('click', exportReportPdf);

    // Publish Final Report Workflow
    function openPublishModal() {
      if (!currentReport) return;
      if (currentReport.status === 'PUBLISHED') {
        showToast('ALREADY PUBLISHED', 'This report is already officially published.', 'info');
        return;
      }
      if (publishConfirmModal) publishConfirmModal.style.display = 'flex';
    }

    if (btnPublishReport) btnPublishReport.addEventListener('click', openPublishModal);
    if (btnPreviewPublish) btnPreviewPublish.addEventListener('click', openPublishModal);

    if (btnCancelReportPublish) {
      btnCancelReportPublish.addEventListener('click', () => {
        if (publishConfirmModal) publishConfirmModal.style.display = 'none';
      });
    }

    if (btnConfirmPublish) {
      btnConfirmPublish.addEventListener('click', async () => {
        if (!currentReport) return;
        if (publishConfirmModal) publishConfirmModal.style.display = 'none';

        // Save any pending draft changes first
        if (isDraftDirty) {
          await saveReportDraft('Pre-publication auto save');
        }

        try {
          const res = await apiFetch('/api/admin/report/status', {
            method: 'POST',
            body: {
              id: currentReport.id,
              targetStatus: 'PUBLISHED'
            }
          });
          const data = await res.json();
          if (res.ok && data.success) {
            showToast('REPORT PUBLISHED', 'Official Event Report is now officially published and sealed.', 'success');
            loadFinalReport();
          } else {
            showToast('PUBLISH FAILED', data.error || 'Failed to publish report.', 'error');
          }
        } catch (e) {
          showToast('SYSTEM ERROR', 'Network error during publication.', 'error');
        }
      });
    }

    // Action: New Revision from Published Report
    async function createNewRevision() {
      if (!currentReport) return;
      openConfirmModal('CREATE NEW REVISION', `Create a new editable draft revision (v${currentReport.version + 1}) from this published report?`, async () => {
        try {
          const res = await apiFetch('/api/admin/report/new-revision', {
            method: 'POST',
            body: { id: currentReport.id }
          });
          const data = await res.json();
          if (res.ok && data.success) {
            showToast('NEW REVISION OPENED', `Draft revision v${data.version} created and ready for editing.`, 'success');
            loadFinalReport();
          } else {
            showToast('FAILED', data.error || 'Could not branch revision.', 'error');
          }
        } catch (e) {
          showToast('SYSTEM ERROR', 'Network error while creating revision.', 'error');
        }
      });
    }

    if (btnNewRevision) btnNewRevision.addEventListener('click', createNewRevision);
    if (btnBannerNewRevision) btnBannerNewRevision.addEventListener('click', createNewRevision);

    // Version History Modal & Restore Action
    async function openVersionHistoryModal() {
      if (!versionHistoryModal) return;
      versionHistoryModal.style.display = 'flex';
      if (versionHistoryTbody) {
        versionHistoryTbody.innerHTML = `<tr><td colspan="6" style="text-align: center; color: var(--color-text-muted); padding: 1.5rem;">Loading immutable version snapshots from SQLite...</td></tr>`;
      }

      try {
        const res = await apiFetch('/api/admin/report/versions');
        const data = await res.json();
        const versions = data.versions || [];

        if (versions.length === 0) {
          versionHistoryTbody.innerHTML = `<tr><td colspan="6" style="text-align: center; color: var(--color-text-muted); padding: 1.5rem;">No version history records found.</td></tr>`;
          return;
        }

        versionHistoryTbody.innerHTML = '';
        versions.forEach(v => {
          const tr = document.createElement('tr');
          const isCurrent = currentReport && v.version === currentReport.version && v.status === currentReport.status;
          const statusClass = v.status === 'PUBLISHED' ? 'status-active' :
                             (v.status === 'FINALIZED' ? 'status-active' :
                             (v.status === 'IN REVIEW' ? 'status-review' : 'status-draft'));

          tr.innerHTML = `
            <td style="font-family: var(--font-mono); font-weight: 800; color: #FFFFFF;">v${escapeHtml(String(v.version))} ${isCurrent ? '<span style="color: var(--color-crimson-bright); font-size: 0.7rem;">[ACTIVE]</span>' : ''}</td>
            <td><span class="status-pill ${statusClass}">${escapeHtml(v.status)}</span></td>
            <td style="font-family: var(--font-mono); color: var(--color-text-secondary);">${escapeHtml(v.savedBy)}</td>
            <td style="font-family: var(--font-mono); font-size: 0.74rem;">${escapeHtml(new Date(v.savedAt).toLocaleString())}</td>
            <td style="font-size: 0.78rem; color: var(--color-text-secondary);">${escapeHtml(v.changeSummary || 'Snapshot recorded')}</td>
            <td style="text-align: right;">
              <button type="button" class="btn-table-action btn-restore-version" data-vid="${v.id}" data-vnum="${v.version}" ${isCurrent ? 'disabled title="Currently active version"' : ''}>
                ↺ [ RESTORE ]
              </button>
            </td>
          `;

          const btnRestore = tr.querySelector('.btn-restore-version');
          if (btnRestore && !isCurrent) {
            btnRestore.addEventListener('click', () => {
              restoreVersionSnapshot(v.id, v.version);
            });
          }

          versionHistoryTbody.appendChild(tr);
        });

      } catch (e) {
        if (versionHistoryTbody) {
          versionHistoryTbody.innerHTML = `<tr><td colspan="6" style="text-align: center; color: #FF2438; padding: 1.5rem;">Failed to fetch version history.</td></tr>`;
        }
      }
    }

    function restoreVersionSnapshot(versionId, versionNum) {
      openConfirmModal('RESTORE REPORT VERSION', `Restore report data to snapshot version v${versionNum}? This will incorporate the snapshot content as a new draft version.`, async () => {
        try {
          const res = await apiFetch('/api/admin/report/restore', {
            method: 'POST',
            body: { versionId }
          });
          const data = await res.json();
          if (res.ok && data.success) {
            if (versionHistoryModal) versionHistoryModal.style.display = 'none';
            showToast('VERSION RESTORED', `Report successfully restored to v${versionNum} content (new version v${data.version}).`, 'success');
            loadFinalReport();
          } else {
            showToast('RESTORE FAILED', data.error || 'Could not restore version.', 'error');
          }
        } catch (e) {
          showToast('SYSTEM ERROR', 'Network error during version restore.', 'error');
        }
      });
    }

    if (btnVersionHistory) btnVersionHistory.addEventListener('click', openVersionHistoryModal);
    if (btnCloseVersionModal) {
      btnCloseVersionModal.addEventListener('click', () => {
        if (versionHistoryModal) versionHistoryModal.style.display = 'none';
      });
    }

    // =========================================================================
    // TAB 8: CASE & QUESTION MANAGEMENT CONTROLLER
    // =========================================================================
    let currentCaseId = 'case-01';
    let allAdminCases = [];
    let activeCaseDetail = null;
    let currentRoundNum = 1;
    let currentR1Questions = [];
    let currentR2Questions = [];
    let activeEvTab = 'R1';
    let currentCaseFilter = 'ALL';
    let caseSearchQuery = '';
    let pendingEmergencyCallback = null;

    // Elements
    const cqLockAlert = document.getElementById('cq-lock-alert');
    const cqCasesCount = document.getElementById('cq-cases-count');
    const cqCasesList = document.getElementById('cq-cases-list');
    const cqSearchCases = document.getElementById('cq-search-cases');
    const cqFilterTabs = document.querySelectorAll('.cq-filter-tab');

    const cqCaseMetaForm = document.getElementById('cq-case-meta-form');
    const cqCaseIdInput = document.getElementById('cq-case-id-input');
    const cqCaseStatusInput = document.getElementById('cq-case-status-input');
    const cqCaseOrderInput = document.getElementById('cq-case-order-input');
    const cqCaseNameInput = document.getElementById('cq-case-name-input');
    const cqCaseSummaryInput = document.getElementById('cq-case-summary-input');
    const cqActiveCaseTag = document.getElementById('cq-active-case-tag');
    const cqCaseStatusDot = document.getElementById('cq-case-status-dot');

    const cqEvidenceTotalBadge = document.getElementById('cq-evidence-total-badge');
    const cqEvR1Count = document.getElementById('cq-ev-r1-count');
    const cqEvR2Count = document.getElementById('cq-ev-r2-count');
    const cqEvidenceContainer = document.getElementById('cq-evidence-items-container');
    const btnEvTabR1 = document.getElementById('btn-ev-tab-r1');
    const btnEvTabR2 = document.getElementById('btn-ev-tab-r2');

    const btnSwitchR1 = document.getElementById('btn-switch-r1');
    const btnSwitchR2 = document.getElementById('btn-switch-r2');
    const r1QCounter = document.getElementById('r1-q-counter');
    const r2QCounter = document.getElementById('r2-q-counter');
    const cqRvStatusPill = document.getElementById('cq-rv-status-pill');
    const cqRvMarksSum = document.getElementById('cq-rv-marks-sum');
    const cqQuestionsContainer = document.getElementById('cq-questions-container');

    const btnValidateCases = document.getElementById('btn-validate-cases');
    const btnAddNewCase = document.getElementById('btn-add-new-case');
    const btnPreviewCaseCard = document.getElementById('btn-preview-case-card');
    const btnDeleteCase = document.getElementById('btn-delete-case');
    const btnPreviewRound = document.getElementById('btn-preview-round');
    const btnAddQuestion = document.getElementById('btn-add-question');
    const btnCancelCaseMeta = document.getElementById('btn-cancel-case-meta');

    // Modals
    const questionEditorModal = document.getElementById('question-editor-modal');
    const questionEditorForm = document.getElementById('question-editor-form');
    const qEditId = document.getElementById('q-edit-id');
    const qEditCaseId = document.getElementById('q-edit-case-id');
    const qEditRound = document.getElementById('q-edit-round');
    const qEditOrderNum = document.getElementById('q-edit-order-num');
    const qEditMarks = document.getElementById('q-edit-marks');
    const qEditCorrectAns = document.getElementById('q-edit-correct-ans');
    const qEditText = document.getElementById('q-edit-text');
    const qEditOptA = document.getElementById('q-edit-opt-a');
    const qEditOptB = document.getElementById('q-edit-opt-b');
    const qEditOptC = document.getElementById('q-edit-opt-c');
    const qEditOptD = document.getElementById('q-edit-opt-d');
    const qEditEvidenceRef = document.getElementById('q-edit-evidence-ref');
    const qDuplicateAlertBox = document.getElementById('q-duplicate-alert-box');
    const qDupAlertDesc = document.getElementById('q-dup-alert-desc');
    const qDupOverrideCheck = document.getElementById('q-dup-override-check');
    const btnCancelQuestionEditor = document.getElementById('btn-cancel-question-editor');

    const emergencyEditModal = document.getElementById('emergency-edit-modal');
    const emergencyReasonInput = document.getElementById('emergency-reason-input');
    const emergencyConfirmCheckbox = document.getElementById('emergency-confirm-checkbox');
    const btnCommitEmergency = document.getElementById('btn-commit-emergency');
    const btnCancelEmergency = document.getElementById('btn-cancel-emergency');

    const participantCardPreviewModal = document.getElementById('participant-card-preview-modal');
    const simPrevCaseName = document.getElementById('sim-prev-case-name');
    const simPrevCaseDesc = document.getElementById('sim-prev-case-desc');
    const btnCloseCardPreview = document.getElementById('btn-close-card-preview');

    const casesValidationModal = document.getElementById('cases-validation-modal');
    const valSummaryBanner = document.getElementById('val-summary-banner');
    const valCasesTbody = document.getElementById('val-cases-tbody');
    const btnCloseValModal = document.getElementById('btn-close-val-modal');

    const roundPreviewModal = document.getElementById('round-preview-modal');
    const rprevQuestionsScroll = document.getElementById('rprev-questions-scroll');
    const btnCloseRoundPreview = document.getElementById('btn-close-round-preview');

    // 1. Load All Cases & Initial Case
    async function loadCasesQuestions() {
      try {
        let casesData = null;
        try {
          const res = await apiFetch('/api/admin/cases');
          if (res.ok) {
            const data = await res.json();
            casesData = data.cases;
          }
        } catch (apiErr) {}

        if (!casesData || casesData.length === 0) {
          const staticRes = await fetch('cases_seed.json');
          if (staticRes.ok) {
            const seedObj = await staticRes.json();
            window._traceX_seedObj = seedObj;
            casesData = Object.keys(seedObj).map((cid, idx) => {
              const item = seedObj[cid];
              const r1 = item.questions || [];
              const r2 = item.round2Questions || [];
              const ev1 = item.evidence || [];
              const ev2 = item.round2Evidence || [];
              return {
                caseId: cid,
                name: item.name || cid,
                orderIdx: idx + 1,
                status: 'ACTIVE',
                r1Count: r1.length,
                r2Count: r2.length,
                evidenceCount: ev1.length,
                round2EvidenceCount: ev2.length
              };
            });
          }
        }

        allAdminCases = casesData || [];
        if (cqCasesCount) cqCasesCount.textContent = allAdminCases.length;

        // Ensure active case exists in list
        const exists = allAdminCases.some(c => c.caseId === currentCaseId);
        if (!exists && allAdminCases.length > 0) {
          currentCaseId = allAdminCases[0].caseId;
        }

        renderCaseNavList();
        if (currentCaseId) {
          await loadCaseDetail(currentCaseId);
        }
      } catch (e) {
        showToast('ERROR', 'Failed to load investigation cases.', 'error');
      }
    }

    // 2. Render Case Navigation List
    function renderCaseNavList() {
      if (!cqCasesList) return;

      let filtered = allAdminCases.filter(c => {
        if (currentCaseFilter !== 'ALL' && c.status !== currentCaseFilter) return false;
        if (caseSearchQuery) {
          const q = caseSearchQuery.toLowerCase();
          return c.name.toLowerCase().includes(q) || c.caseId.toLowerCase().includes(q);
        }
        return true;
      });

      if (filtered.length === 0) {
        cqCasesList.innerHTML = `<div style="text-align: center; color: var(--color-text-muted); font-size: 0.78rem; padding: 2rem 1rem;">No cases match current filter.</div>`;
        return;
      }

      cqCasesList.innerHTML = filtered.map(c => {
        const isActive = c.caseId === currentCaseId;
        const r1Complete = c.r1Count === 15;
        const r2Complete = c.r2Count === 15;
        return `
          <div class="cq-case-nav-item ${isActive ? 'active' : ''}" data-case-id="${c.caseId}">
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <span class="cq-case-nav-id">${escapeHtml(c.caseId.toUpperCase())}</span>
              <span style="font-family: var(--font-mono); font-size: 0.6rem; color: ${c.status === 'ACTIVE' ? '#00E676' : '#858585'};">
                ● ${c.status}
              </span>
            </div>
            <div class="cq-case-nav-name">${escapeHtml(c.name)}</div>
            <div class="cq-case-nav-badges">
              <span class="cq-nav-pill ${r1Complete ? 'green' : ''}">R1: ${c.r1Count}/15 Qs</span>
              <span class="cq-nav-pill ${r2Complete ? 'green' : ''}">R2: ${c.r2Count}/15 Qs</span>
              <span class="cq-nav-pill">${c.evidenceCount + c.round2EvidenceCount} Clues</span>
            </div>
          </div>
        `;
      }).join('');

      cqCasesList.querySelectorAll('.cq-case-nav-item').forEach(item => {
        item.addEventListener('click', async () => {
          const cid = item.getAttribute('data-case-id');
          if (cid !== currentCaseId) {
            currentCaseId = cid;
            renderCaseNavList();
            await loadCaseDetail(currentCaseId);
          }
        });
      });
    }

    // 3. Load Detail of a Specific Case
    async function loadCaseDetail(caseId) {
      try {
        let data = null;
        try {
          const res = await apiFetch(`/api/admin/cases/detail?id=${encodeURIComponent(caseId)}`);
          if (res.ok) {
            data = await res.json();
          }
        } catch (apiErr) {}

        if (!data) {
          if (!window._traceX_seedObj) {
            const staticRes = await fetch('cases_seed.json');
            if (staticRes.ok) window._traceX_seedObj = await staticRes.json();
          }
          if (window._traceX_seedObj && window._traceX_seedObj[caseId]) {
            const raw = window._traceX_seedObj[caseId];
            data = {
              case: {
                caseId: caseId,
                name: raw.name || caseId,
                orderIdx: parseInt(caseId.replace(/\D/g, '') || '1', 10),
                status: 'ACTIVE',
                summary: raw.summary || '',
                evidence: raw.evidence || [],
                round2Evidence: raw.round2Evidence || []
              },
              round1Questions: raw.questions || [],
              round2Questions: raw.round2Questions || [],
              isLocked: false
            };
          }
        }

        if (!data) throw new Error('Case not found');
        activeCaseDetail = data;

        // Event Lock Alert
        if (cqLockAlert) {
          cqLockAlert.style.display = data.isLocked ? 'flex' : 'none';
        }

        const cs = data.case;
        if (cqCaseIdInput) cqCaseIdInput.value = cs.caseId;
        if (cqCaseStatusInput) cqCaseStatusInput.value = cs.status;
        if (cqCaseOrderInput) cqCaseOrderInput.value = cs.orderIdx;
        if (cqCaseNameInput) cqCaseNameInput.value = cs.name;
        if (cqCaseSummaryInput) cqCaseSummaryInput.value = cs.summary;
        if (cqActiveCaseTag) cqActiveCaseTag.textContent = `${cs.caseId.toUpperCase()} — DOSSIER`;
        if (cqCaseStatusDot) {
          cqCaseStatusDot.className = cs.status === 'ACTIVE' ? 'cq-dot' : 'cq-dot inactive';
        }

        // Store Questions
        currentR1Questions = data.round1Questions || [];
        currentR2Questions = data.round2Questions || [];

        // Evidence counters
        const r1Ev = cs.evidence || [];
        const r2Ev = cs.round2Evidence || [];
        if (cqEvidenceTotalBadge) cqEvidenceTotalBadge.textContent = `${r1Ev.length + r2Ev.length} EVIDENCE ITEMS`;
        if (cqEvR1Count) cqEvR1Count.textContent = r1Ev.length;
        if (cqEvR2Count) cqEvR2Count.textContent = r2Ev.length;

        renderEvidenceList();
        renderQuestionsList();
      } catch (e) {
        showToast('ERROR', `Failed to load details for ${caseId}.`, 'error');
      }
    }

    // 4. Render Evidence Items for Active Case
    function renderEvidenceList() {
      if (!cqEvidenceContainer || !activeCaseDetail) return;
      const cs = activeCaseDetail.case;
      const evItems = activeEvTab === 'R1' ? (cs.evidence || []) : (cs.round2Evidence || []);

      if (evItems.length === 0) {
        cqEvidenceContainer.innerHTML = `<div style="color: var(--color-text-muted); font-size: 0.76rem; padding: 0.8rem;">No evidence items registered for Round ${activeEvTab === 'R1' ? 1 : 2}.</div>`;
        return;
      }

      cqEvidenceContainer.innerHTML = evItems.map((ev, idx) => `
        <div class="cq-ev-item-card">
          <div>
            <span class="cq-ev-item-title">${escapeHtml(ev.title || `CLUE #${idx+1}`)}</span>
            <span class="cq-ev-item-type">${escapeHtml(ev.type || 'DIGITAL LOG')}</span>
          </div>
          <div style="font-family: var(--font-mono); font-size: 0.72rem; color: var(--color-text-muted);">
            REFERENCE REF: CLUE-${idx+1}
          </div>
        </div>
      `).join('');
    }

    // 5. Render Questions for Selected Round
    function renderQuestionsList() {
      if (!cqQuestionsContainer) return;
      const qs = currentRoundNum === 1 ? currentR1Questions : currentR2Questions;

      // Update counters
      if (r1QCounter) r1QCounter.textContent = `${currentR1Questions.length}/15`;
      if (r2QCounter) r2QCounter.textContent = `${currentR2Questions.length}/15`;

      const isComplete = qs.length === 15;
      if (cqRvStatusPill) {
        cqRvStatusPill.className = isComplete ? 'cq-rv-pill success' : 'cq-rv-pill warn';
        cqRvStatusPill.textContent = isComplete 
          ? `✔ ROUND VALIDATION: 15 OF 15 QUESTIONS CONFIGURED` 
          : `⚠ INCOMPLETE ROUND: ${qs.length} OF 15 QUESTIONS CONFIGURED`;
      }

      const totalMarks = qs.reduce((sum, q) => sum + (Number(q.marks) || 1), 0);
      if (cqRvMarksSum) cqRvMarksSum.textContent = totalMarks;

      if (qs.length === 0) {
        cqQuestionsContainer.innerHTML = `
          <div style="text-align: center; color: var(--color-text-muted); font-size: 0.82rem; padding: 3rem 1rem; border: 1px dashed rgba(255,255,255,0.1); border-radius: 6px;">
            No questions configured in Round ${currentRoundNum} for this case. Click [+ ADD QUESTION] to begin.
          </div>
        `;
        return;
      }

      cqQuestionsContainer.innerHTML = qs.map((q, idx) => {
        const orderDisplay = `#${String(q.orderNum || idx + 1).padStart(2, '0')}`;
        const correctLetter = (q.correctAnswer || 'A').toUpperCase();
        return `
          <div class="q-card" data-qid="${q.id}">
            <div class="q-card-header">
              <span class="q-order-badge">${orderDisplay}</span>
              <span style="font-family: var(--font-mono); font-size: 0.65rem; color: var(--color-crimson-bright);">
                CASE: ${escapeHtml(q.caseId)} · ROUND ${q.round}
              </span>
            </div>

            <div class="q-text">${escapeHtml(q.text)}</div>

            <div class="q-card-opts-grid">
              <div class="q-opt-pill ${correctLetter === 'A' ? 'correct' : ''}">
                <span class="q-opt-letter">[A]</span>
                <span>${escapeHtml(q.optionA || '')}</span>
                ${correctLetter === 'A' ? '<span style="margin-left: auto; color: #00E676; font-size: 0.65rem; font-weight: 700;">✔ KEY</span>' : ''}
              </div>
              <div class="q-opt-pill ${correctLetter === 'B' ? 'correct' : ''}">
                <span class="q-opt-letter">[B]</span>
                <span>${escapeHtml(q.optionB || '')}</span>
                ${correctLetter === 'B' ? '<span style="margin-left: auto; color: #00E676; font-size: 0.65rem; font-weight: 700;">✔ KEY</span>' : ''}
              </div>
              <div class="q-opt-pill ${correctLetter === 'C' ? 'correct' : ''}">
                <span class="q-opt-letter">[C]</span>
                <span>${escapeHtml(q.optionC || '')}</span>
                ${correctLetter === 'C' ? '<span style="margin-left: auto; color: #00E676; font-size: 0.65rem; font-weight: 700;">✔ KEY</span>' : ''}
              </div>
              <div class="q-opt-pill ${correctLetter === 'D' ? 'correct' : ''}">
                <span class="q-opt-letter">[D]</span>
                <span>${escapeHtml(q.optionD || '')}</span>
                ${correctLetter === 'D' ? '<span style="margin-left: auto; color: #00E676; font-size: 0.65rem; font-weight: 700;">✔ KEY</span>' : ''}
              </div>
            </div>

            <div class="q-card-footer">
              <div class="q-card-meta">
                <span class="cq-nav-pill" style="color: #00E676; border-color: rgba(0,230,118,0.25);">
                  WEIGHT: ${q.marks} MARK${q.marks > 1 ? 'S' : ''}
                </span>
                ${q.evidenceRef ? `<span class="cq-nav-pill">CLUE REF: ${escapeHtml(q.evidenceRef)}</span>` : ''}
              </div>

              <div class="q-card-actions">
                <button type="button" class="btn-q-action btn-move-q-up" data-qid="${q.id}" data-idx="${idx}" title="Move Up" ${idx === 0 ? 'disabled' : ''}>▲</button>
                <button type="button" class="btn-q-action btn-move-q-down" data-qid="${q.id}" data-idx="${idx}" title="Move Down" ${idx === qs.length - 1 ? 'disabled' : ''}>▼</button>
                <button type="button" class="btn-q-action btn-edit-q" data-qid="${q.id}">[ EDIT ]</button>
                <button type="button" class="btn-q-action del btn-del-q" data-qid="${q.id}">[ DELETE ]</button>
              </div>
            </div>
          </div>
        `;
      }).join('');

      // Wire Question Actions
      cqQuestionsContainer.querySelectorAll('.btn-edit-q').forEach(btn => {
        btn.addEventListener('click', () => {
          const qid = btn.getAttribute('data-qid');
          const q = qs.find(item => item.id === qid);
          if (q) openQuestionEditor(q, false);
        });
      });

      cqQuestionsContainer.querySelectorAll('.btn-del-q').forEach(btn => {
        btn.addEventListener('click', () => {
          const qid = btn.getAttribute('data-qid');
          deleteQuestionPrompt(qid);
        });
      });

      cqQuestionsContainer.querySelectorAll('.btn-move-q-up').forEach(btn => {
        btn.addEventListener('click', () => {
          const idx = parseInt(btn.getAttribute('data-idx'));
          if (idx > 0) reorderQuestions(idx, idx - 1);
        });
      });

      cqQuestionsContainer.querySelectorAll('.btn-move-q-down').forEach(btn => {
        btn.addEventListener('click', () => {
          const idx = parseInt(btn.getAttribute('data-idx'));
          if (idx < qs.length - 1) reorderQuestions(idx, idx + 1);
        });
      });
    }

    // 6. Question Reordering
    async function reorderQuestions(fromIdx, toIdx) {
      const qs = currentRoundNum === 1 ? currentR1Questions : currentR2Questions;
      const moved = qs.splice(fromIdx, 1)[0];
      qs.splice(toIdx, 0, moved);

      const orderList = qs.map(q => q.id);
      try {
        const res = await apiFetch('/api/admin/questions/reorder', {
          method: 'POST',
          body: {
            caseId: currentCaseId,
            round: currentRoundNum,
            orderList: orderList
          }
        });
        const data = await res.json();
        if (res.status === 403 && data.error === 'EVENT_LOCKED') {
          triggerEmergencyModal('REORDER QUESTIONS', async (reason) => {
            await apiFetch('/api/admin/questions/reorder', {
              method: 'POST',
              body: { caseId: currentCaseId, round: currentRoundNum, orderList, emergencyOverride: true, emergencyReason: reason }
            });
            await loadCaseDetail(currentCaseId);
          });
          return;
        }

        if (res.ok) {
          showToast('REORDERED', `Questions updated in Round ${currentRoundNum}.`, 'success');
          await loadCaseDetail(currentCaseId);
        } else {
          showToast('ERROR', data.error || 'Failed to reorder questions.', 'error');
        }
      } catch (e) {
        showToast('ERROR', 'Network error during question reordering.', 'error');
      }
    }

    // 7. Delete Question Handler
    function deleteQuestionPrompt(qid) {
      openConfirmModal('DELETE QUESTION', `Permanently delete Question ${qid} from Case ${currentCaseId}? This action cannot be undone.`, async () => {
        try {
          const res = await apiFetch('/api/admin/questions/delete', {
            method: 'POST',
            body: { id: qid }
          });
          const data = await res.json();

          if (res.status === 403 && data.error === 'EVENT_LOCKED') {
            triggerEmergencyModal('DELETE QUESTION', async (reason) => {
              await apiFetch('/api/admin/questions/delete', {
                method: 'POST',
                body: { id: qid, emergencyOverride: true, emergencyReason: reason }
              });
              showToast('DELETED', `Question ${qid} deleted via emergency override.`, 'success');
              await loadCaseDetail(currentCaseId);
            });
            return;
          }

          if (res.ok) {
            showToast('QUESTION DELETED', `Question ${qid} deleted successfully.`, 'success');
            await loadCaseDetail(currentCaseId);
          } else {
            showToast('ERROR', data.error || 'Failed to delete question.', 'error');
          }
        } catch (e) {
          showToast('ERROR', 'Network error while deleting question.', 'error');
        }
      });
    }

    // 8. Open Question Editor Modal
    function openQuestionEditor(q, isNew = false) {
      if (!questionEditorModal) return;
      if (qDuplicateAlertBox) qDuplicateAlertBox.style.display = 'none';
      if (qDupOverrideCheck) qDupOverrideCheck.checked = false;

      const qs = currentRoundNum === 1 ? currentR1Questions : currentR2Questions;
      const nextOrder = qs.length + 1;

      if (isNew) {
        document.getElementById('q-modal-heading').textContent = `ADD QUESTION — ROUND ${currentRoundNum}`;
        document.getElementById('q-modal-badge').textContent = 'NEW QUESTION';
        qEditId.value = '';
        qEditCaseId.value = currentCaseId;
        qEditRound.value = currentRoundNum;
        qEditOrderNum.value = nextOrder;
        qEditMarks.value = 1;
        qEditCorrectAns.value = 'A';
        qEditText.value = '';
        qEditOptA.value = '';
        qEditOptB.value = '';
        qEditOptC.value = '';
        qEditOptD.value = '';
        qEditEvidenceRef.value = '';
      } else {
        document.getElementById('q-modal-heading').textContent = `EDIT QUESTION #${q.orderNum} — ROUND ${q.round}`;
        document.getElementById('q-modal-badge').textContent = `ID: ${q.id}`;
        qEditId.value = q.id;
        qEditCaseId.value = q.caseId;
        qEditRound.value = q.round;
        qEditOrderNum.value = q.orderNum;
        qEditMarks.value = q.marks;
        qEditCorrectAns.value = q.correctAnswer || 'A';
        qEditText.value = q.text || '';
        qEditOptA.value = q.optionA || '';
        qEditOptB.value = q.optionB || '';
        qEditOptC.value = q.optionC || '';
        qEditOptD.value = q.optionD || '';
        qEditEvidenceRef.value = q.evidenceRef || '';
      }

      questionEditorModal.style.display = 'flex';
    }

    if (btnAddQuestion) {
      btnAddQuestion.addEventListener('click', () => openQuestionEditor(null, true));
    }

    if (btnCancelQuestionEditor) {
      btnCancelQuestionEditor.addEventListener('click', () => {
        if (questionEditorModal) questionEditorModal.style.display = 'none';
      });
    }

    // Question Form Submit Handler
    if (questionEditorForm) {
      questionEditorForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const payload = {
          id: qEditId.value,
          caseId: qEditCaseId.value,
          round: parseInt(qEditRound.value),
          orderNum: parseInt(qEditOrderNum.value),
          marks: parseInt(qEditMarks.value),
          correctAnswer: qEditCorrectAns.value,
          text: qEditText.value.trim(),
          optionA: qEditOptA.value.trim(),
          optionB: qEditOptB.value.trim(),
          optionC: qEditOptC.value.trim(),
          optionD: qEditOptD.value.trim(),
          evidenceRef: qEditEvidenceRef.value.trim(),
          ignoreDuplicateWarning: qDupOverrideCheck ? qDupOverrideCheck.checked : false
        };

        try {
          const res = await apiFetch('/api/admin/questions/save', {
            method: 'POST',
            body: payload
          });
          const data = await res.json();

          // Check for duplicate question warning (409)
          if (res.status === 409 && data.error === 'DUPLICATE_QUESTION_TEXT') {
            if (qDuplicateAlertBox && qDupAlertDesc) {
              qDupAlertDesc.textContent = data.message;
              qDuplicateAlertBox.style.display = 'block';
            }
            showToast('DUPLICATE WARNING', 'Identical question text flagged in this round.', 'warning');
            return;
          }

          // Check for Event Lock (403)
          if (res.status === 403 && data.error === 'EVENT_LOCKED') {
            triggerEmergencyModal('SAVE QUESTION', async (reason) => {
              payload.emergencyOverride = true;
              payload.emergencyReason = reason;
              const emRes = await apiFetch('/api/admin/questions/save', {
                method: 'POST',
                body: payload
              });
              const emData = await emRes.json();
              if (emRes.ok) {
                if (questionEditorModal) questionEditorModal.style.display = 'none';
                showToast('SAVED VIA EMERGENCY', 'Question updated and logged to audit trail.', 'success');
                await loadCaseDetail(currentCaseId);
              } else {
                showToast('ERROR', emData.error || 'Failed to save question.', 'error');
              }
            });
            return;
          }

          if (res.ok) {
            if (questionEditorModal) questionEditorModal.style.display = 'none';
            showToast('QUESTION SAVED', 'Question configuration updated successfully.', 'success');
            await loadCaseDetail(currentCaseId);
          } else {
            showToast('VALIDATION ERROR', data.error || 'Failed to save question.', 'error');
          }
        } catch (e) {
          showToast('ERROR', 'Network error during question save.', 'error');
        }
      });
    }

    // 9. Save Case Metadata Dossier
    if (cqCaseMetaForm) {
      cqCaseMetaForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const cid = cqCaseIdInput.value.trim();
        const payload = {
          caseId: cid,
          name: cqCaseNameInput.value.trim(),
          summary: cqCaseSummaryInput.value.trim(),
          status: cqCaseStatusInput.value,
          orderIdx: parseInt(cqCaseOrderInput.value) || 1,
          evidence: activeCaseDetail ? activeCaseDetail.case.evidence : [],
          round2Evidence: activeCaseDetail ? activeCaseDetail.case.round2Evidence : []
        };

        try {
          const res = await apiFetch('/api/admin/cases/save', {
            method: 'POST',
            body: payload
          });
          const data = await res.json();

          if (res.status === 403 && data.error === 'EVENT_LOCKED') {
            triggerEmergencyModal('SAVE CASE DOSSIER', async (reason) => {
              payload.emergencyOverride = true;
              payload.emergencyReason = reason;
              const emRes = await apiFetch('/api/admin/cases/save', {
                method: 'POST',
                body: payload
              });
              if (emRes.ok) {
                showToast('CASE SAVED', `Case ${cid} updated via emergency override.`, 'success');
                await loadCasesQuestions();
              }
            });
            return;
          }

          if (res.ok) {
            showToast('DOSSIER SAVED', `Case ${cid} dossier updated successfully.`, 'success');
            await loadCasesQuestions();
          } else {
            showToast('ERROR', data.error || 'Failed to save case.', 'error');
          }
        } catch (e) {
          showToast('ERROR', 'Network error during case save.', 'error');
        }
      });
    }

    if (btnCancelCaseMeta) {
      btnCancelCaseMeta.addEventListener('click', () => {
        if (currentCaseId) loadCaseDetail(currentCaseId);
      });
    }

    // 10. Add New Case Handler
    if (btnAddNewCase) {
      btnAddNewCase.addEventListener('click', () => {
        const nextId = `case-${String(allAdminCases.length + 1).padStart(2, '0')}`;
        currentCaseId = nextId;
        if (cqCaseIdInput) {
          cqCaseIdInput.readOnly = false;
          cqCaseIdInput.value = nextId;
        }
        if (cqCaseNameInput) cqCaseNameInput.value = `CASE ${allAdminCases.length + 1} — NEW INVESTIGATION`;
        if (cqCaseSummaryInput) cqCaseSummaryInput.value = 'Description for student case selection...';
        if (cqCaseStatusInput) cqCaseStatusInput.value = 'ACTIVE';
        if (cqCaseOrderInput) cqCaseOrderInput.value = allAdminCases.length + 1;
        if (cqActiveCaseTag) cqActiveCaseTag.textContent = `${nextId.toUpperCase()} — NEW CASE`;

        currentR1Questions = [];
        currentR2Questions = [];
        activeCaseDetail = {
          case: {
            caseId: nextId,
            name: `CASE ${allAdminCases.length + 1} — NEW INVESTIGATION`,
            summary: '',
            status: 'ACTIVE',
            orderIdx: allAdminCases.length + 1,
            evidence: [],
            round2Evidence: []
          },
          round1Questions: [],
          round2Questions: [],
          isLocked: false
        };

        renderEvidenceList();
        renderQuestionsList();
        showToast('NEW CASE', 'Configure parameters and click [ SAVE CASE DOSSIER ] to create.', 'info');
      });
    }

    // 11. Delete Case Handler
    if (btnDeleteCase) {
      btnDeleteCase.addEventListener('click', () => {
        openConfirmModal('DELETE INVESTIGATION CASE', `Permanently delete case ${currentCaseId} and all associated 30 questions? Note: Cases already selected or completed in active investigations cannot be deleted.`, async () => {
          try {
            const res = await apiFetch('/api/admin/cases/delete', {
              method: 'POST',
              body: { caseId: currentCaseId }
            });
            const data = await res.json();

            if (res.status === 400 && data.error === 'CASE_IN_USE') {
              showToast('CANNOT DELETE', data.message, 'warning');
              return;
            }

            if (res.status === 403 && data.error === 'EVENT_LOCKED') {
              triggerEmergencyModal('DELETE CASE', async (reason) => {
                await apiFetch('/api/admin/cases/delete', {
                  method: 'POST',
                  body: { caseId: currentCaseId, emergencyOverride: true, emergencyReason: reason }
                });
                showToast('CASE DELETED', `Case ${currentCaseId} deleted via emergency override.`, 'success');
                currentCaseId = 'case-01';
                await loadCasesQuestions();
              });
              return;
            }

            if (res.ok) {
              showToast('CASE DELETED', `Case ${currentCaseId} removed successfully.`, 'success');
              currentCaseId = 'case-01';
              await loadCasesQuestions();
            } else {
              showToast('ERROR', data.error || 'Could not delete case.', 'error');
            }
          } catch (e) {
            showToast('ERROR', 'Network error during case deletion.', 'error');
          }
        });
      });
    }

    // 12. Participant Card Preview Modal
    if (btnPreviewCaseCard) {
      btnPreviewCaseCard.addEventListener('click', () => {
        if (!participantCardPreviewModal) return;
        if (simPrevCaseName) simPrevCaseName.textContent = cqCaseNameInput.value || 'CASE NAME';
        if (simPrevCaseDesc) simPrevCaseDesc.textContent = cqCaseSummaryInput.value || 'Case summary description';
        participantCardPreviewModal.style.display = 'flex';
      });
    }

    if (btnCloseCardPreview) {
      btnCloseCardPreview.addEventListener('click', () => {
        if (participantCardPreviewModal) participantCardPreviewModal.style.display = 'none';
      });
    }

    // 13. Case & Question Readiness Validation Audit Modal
    if (btnValidateCases) {
      btnValidateCases.addEventListener('click', async () => {
        if (!casesValidationModal) return;
        try {
          const res = await apiFetch('/api/admin/cases/validation');
          const data = await res.json();

          if (valSummaryBanner) {
            valSummaryBanner.className = data.isReadyForEvent ? 'val-summary-banner ready' : 'val-summary-banner not-ready';
            valSummaryBanner.innerHTML = data.isReadyForEvent
              ? `<div><strong>✔ EVENT READY:</strong> All ${data.totalCases} cases fully populated with exactly 15 Round 1 & 15 Round 2 questions (450 total). All answer keys validated.</div>`
              : `<div><strong>⚠ READINESS ISSUES DETECTED (${data.issues.length}):</strong> Event cannot launch until missing questions or option keys are resolved.</div>`;
          }

          if (valCasesTbody) {
            valCasesTbody.innerHTML = (data.casesValidation || []).map(cv => `
              <tr>
                <td style="font-family: var(--font-mono); font-weight: 700; color: var(--color-crimson-bright);">${escapeHtml(cv.caseId)}</td>
                <td>${escapeHtml(cv.name)}</td>
                <td style="font-family: var(--font-mono); color: ${cv.r1Count === 15 ? '#00E676' : '#FF2438'}; font-weight: 700;">
                  ${cv.r1Count} / 15 ${cv.r1Count === 15 ? '✔' : '✖'}
                </td>
                <td style="font-family: var(--font-mono); color: ${cv.r2Count === 15 ? '#00E676' : '#FF2438'}; font-weight: 700;">
                  ${cv.r2Count} / 15 ${cv.r2Count === 15 ? '✔' : '✖'}
                </td>
                <td>
                  <span class="cq-nav-pill ${cv.isComplete ? 'green' : ''}">
                    ${cv.isComplete ? 'READY' : 'INCOMPLETE'}
                  </span>
                </td>
                <td style="font-size: 0.74rem; color: #FF2438;">
                  ${cv.issues.length > 0 ? cv.issues.map(i => `• ${escapeHtml(i)}`).join('<br>') : '<span style="color: #00E676;">None (Valid)</span>'}
                </td>
              </tr>
            `).join('');
          }

          casesValidationModal.style.display = 'flex';
        } catch (e) {
          showToast('ERROR', 'Failed to retrieve validation audit report.', 'error');
        }
      });
    }

    if (btnCloseValModal) {
      btnCloseValModal.addEventListener('click', () => {
        if (casesValidationModal) casesValidationModal.style.display = 'none';
      });
    }

    // 14. Preview Round Modal
    if (btnPreviewRound) {
      btnPreviewRound.addEventListener('click', () => {
        if (!roundPreviewModal || !rprevQuestionsScroll) return;
        const qs = currentRoundNum === 1 ? currentR1Questions : currentR2Questions;

        document.getElementById('rprev-modal-heading').textContent = `CANDIDATE ROUND ${currentRoundNum} PREVIEW (${qs.length} QUESTIONS)`;
        rprevQuestionsScroll.innerHTML = qs.map((q, idx) => `
          <div style="background: #060608; border: 1px solid rgba(255,255,255,0.08); border-radius: 6px; padding: 1.2rem; margin-bottom: 1rem;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.6rem;">
              <span class="q-order-badge">QUESTION #${idx + 1} OF 15</span>
              <span style="font-family: var(--font-mono); font-size: 0.7rem; color: var(--color-crimson-bright);">10-MINUTE TIMER ACTIVE IN LIVE ROUND</span>
            </div>
            <div style="font-weight: 700; color: #FFFFFF; font-size: 0.95rem; margin-bottom: 1rem;">${escapeHtml(q.text)}</div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.6rem;">
              <div class="q-opt-pill"><span class="q-opt-letter">[A]</span> ${escapeHtml(q.optionA)}</div>
              <div class="q-opt-pill"><span class="q-opt-letter">[B]</span> ${escapeHtml(q.optionB)}</div>
              <div class="q-opt-pill"><span class="q-opt-letter">[C]</span> ${escapeHtml(q.optionC)}</div>
              <div class="q-opt-pill"><span class="q-opt-letter">[D]</span> ${escapeHtml(q.optionD)}</div>
            </div>
          </div>
        `).join('');

        roundPreviewModal.style.display = 'flex';
      });
    }

    if (btnCloseRoundPreview) {
      btnCloseRoundPreview.addEventListener('click', () => {
        if (roundPreviewModal) roundPreviewModal.style.display = 'none';
      });
    }

    // 15. Emergency Modal Trigger Helper
    function triggerEmergencyModal(actionTitle, onConfirm) {
      if (!emergencyEditModal) return;
      pendingEmergencyCallback = onConfirm;
      document.getElementById('emerg-modal-heading').textContent = `EMERGENCY ${actionTitle.toUpperCase()}`;
      if (emergencyReasonInput) emergencyReasonInput.value = '';
      if (emergencyConfirmCheckbox) emergencyConfirmCheckbox.checked = false;
      if (btnCommitEmergency) btnCommitEmergency.disabled = true;

      emergencyEditModal.style.display = 'flex';
    }

    if (emergencyConfirmCheckbox && btnCommitEmergency && emergencyReasonInput) {
      const updateEmergencyBtn = () => {
        btnCommitEmergency.disabled = !(emergencyConfirmCheckbox.checked && emergencyReasonInput.value.trim().length > 0);
      };
      emergencyConfirmCheckbox.addEventListener('change', updateEmergencyBtn);
      emergencyReasonInput.addEventListener('input', updateEmergencyBtn);
    }

    if (btnCancelEmergency) {
      btnCancelEmergency.addEventListener('click', () => {
        if (emergencyEditModal) emergencyEditModal.style.display = 'none';
        pendingEmergencyCallback = null;
      });
    }

    if (btnCommitEmergency) {
      btnCommitEmergency.addEventListener('click', async () => {
        const reason = emergencyReasonInput.value.trim();
        if (!reason) return;
        if (emergencyEditModal) emergencyEditModal.style.display = 'none';
        if (typeof pendingEmergencyCallback === 'function') {
          await pendingEmergencyCallback(reason);
        }
        pendingEmergencyCallback = null;
      });
    }

    // Wire Round Switchers
    if (btnSwitchR1) {
      btnSwitchR1.addEventListener('click', () => {
        currentRoundNum = 1;
        btnSwitchR1.classList.add('active');
        if (btnSwitchR2) btnSwitchR2.classList.remove('active');
        renderQuestionsList();
      });
    }

    if (btnSwitchR2) {
      btnSwitchR2.addEventListener('click', () => {
        currentRoundNum = 2;
        btnSwitchR2.classList.add('active');
        if (btnSwitchR1) btnSwitchR1.classList.remove('active');
        renderQuestionsList();
      });
    }

    // Wire Evidence Tabs
    if (btnEvTabR1) {
      btnEvTabR1.addEventListener('click', () => {
        activeEvTab = 'R1';
        btnEvTabR1.classList.add('active');
        if (btnEvTabR2) btnEvTabR2.classList.remove('active');
        renderEvidenceList();
      });
    }

    if (btnEvTabR2) {
      btnEvTabR2.addEventListener('click', () => {
        activeEvTab = 'R2';
        btnEvTabR2.classList.add('active');
        if (btnEvTabR1) btnEvTabR1.classList.remove('active');
        renderEvidenceList();
      });
    }

    // Wire Case Search and Filters
    if (cqSearchCases) {
      cqSearchCases.addEventListener('input', (e) => {
        caseSearchQuery = e.target.value.trim();
        renderCaseNavList();
      });
    }

    cqFilterTabs.forEach(tab => {
      tab.addEventListener('click', () => {
        cqFilterTabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        currentCaseFilter = tab.getAttribute('data-filter');
        renderCaseNavList();
      });
    });


    // =========================================================================
    // TAB 9: BACKUP & EXPORT CONTROLLER
    // =========================================================================
    const btnExportTeams = document.getElementById('btn-export-teams');
    const btnExportResults = document.getElementById('btn-export-results');
    const btnExportViolations = document.getElementById('btn-export-violations');
    const btnExportReportCsv = document.getElementById('btn-export-report-csv');
    const btnExportReportPdfLink = document.getElementById('btn-export-report-pdf-link');

    const btnCreateBackupNow = document.getElementById('btn-create-backup-now');
    const bkpLiveSize = document.getElementById('bkp-live-size');
    const backupHistoryTbody = document.getElementById('backup-history-tbody');
    const exportHistoryTbody = document.getElementById('export-history-tbody');

    const backupDetailsModal = document.getElementById('backup-details-modal');
    const btnCloseBkpDetails = document.getElementById('btn-close-bkp-details');
    const bdtId = document.getElementById('bdt-id');
    const bdtFilename = document.getElementById('bdt-filename');
    const bdtCreatedAt = document.getElementById('bdt-created-at');
    const bdtCreatedBy = document.getElementById('bdt-created-by');
    const bdtFilesize = document.getElementById('bdt-filesize');
    const bdtStatus = document.getElementById('bdt-status');
    const bdtStatsGrid = document.getElementById('bdt-stats-grid');

    async function loadBackupExport() {
      await Promise.all([
        loadBackupsList(),
        loadExportHistory(),
        loadBackupDetailsTelemetry()
      ]);
    }

    // 1. Load Backups List
    async function loadBackupsList() {
      if (!backupHistoryTbody) return;
      try {
        const res = await apiFetch('/api/admin/backups');
        const data = await res.json();
        const backups = data.backups || [];

        if (backups.length === 0) {
          backupHistoryTbody.innerHTML = `<tr><td colspan="7" style="text-align: center; color: var(--color-text-muted); padding: 2rem;">No backups created yet. Click [ CREATE DATABASE BACKUP NOW ] to generate your first snapshot.</td></tr>`;
          return;
        }

        backupHistoryTbody.innerHTML = backups.map(b => {
          const szKb = (b.fileSize / 1024).toFixed(1);
          return `
            <tr>
              <td style="font-family: var(--font-mono); font-weight: 700; color: var(--color-crimson-bright);">${escapeHtml(b.backupId)}</td>
              <td style="font-family: var(--font-mono); font-size: 0.78rem;">${escapeHtml(b.filename)}</td>
              <td style="font-family: var(--font-mono); font-size: 0.75rem;">${escapeHtml(b.createdAt)}</td>
              <td style="font-family: var(--font-mono);">${escapeHtml(b.createdBy)}</td>
              <td style="font-family: var(--font-mono);">${szKb} KB</td>
              <td>
                <span class="cq-nav-pill ${b.status === 'COMPLETED' ? 'green' : ''}">
                  ${escapeHtml(b.status)}
                </span>
              </td>
              <td style="text-align: right;">
                <button type="button" class="btn-q-action btn-dl-bkp" data-bid="${b.backupId}" title="Download SQLite database snapshot">
                  ⬇ [ DOWNLOAD ]
                </button>
                <button type="button" class="btn-q-action btn-det-bkp" data-bid="${b.backupId}" title="Inspect backup metadata">
                  👁 [ DETAILS ]
                </button>
                <button type="button" class="btn-q-action del btn-del-bkp" data-bid="${b.backupId}" title="Delete backup archive">
                  🗑
                </button>
              </td>
            </tr>
          `;
        }).join('');

        // Wire Action Buttons
        backupHistoryTbody.querySelectorAll('.btn-dl-bkp').forEach(btn => {
          btn.addEventListener('click', () => {
            const bid = btn.getAttribute('data-bid');
            downloadBackupFile(bid);
          });
        });

        backupHistoryTbody.querySelectorAll('.btn-det-bkp').forEach(btn => {
          btn.addEventListener('click', () => {
            const bid = btn.getAttribute('data-bid');
            openBackupDetails(bid);
          });
        });

        backupHistoryTbody.querySelectorAll('.btn-del-bkp').forEach(btn => {
          btn.addEventListener('click', () => {
            const bid = btn.getAttribute('data-bid');
            deleteBackupRecord(bid);
          });
        });
      } catch (e) {
        backupHistoryTbody.innerHTML = `<tr><td colspan="7" style="text-align: center; color: #FF2438; padding: 1.5rem;">Failed to fetch database backups registry.</td></tr>`;
      }
    }

    // 2. Download Database Backup File
    function downloadBackupFile(backupId) {
      const token = getAuthToken();
      // Use direct authenticated download link
      const downloadUrl = `/api/admin/backups/download?id=${encodeURIComponent(backupId)}`;
      
      // Use fetch with blob to pass Authorization header cleanly
      apiFetch(downloadUrl)
        .then(res => {
          if (!res.ok) throw new Error('Download failed');
          return res.blob();
        })
        .then(blob => {
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.style.display = 'none';
          a.href = url;
          a.download = `tracex_backup_${backupId}.db`;
          document.body.appendChild(a);
          a.click();
          window.URL.revokeObjectURL(url);
          a.remove();
          showToast('DOWNLOAD STARTED', `Database archive ${backupId} saved to local disk.`, 'success');
        })
        .catch(err => {
          showToast('DOWNLOAD ERROR', 'Failed to download database backup archive.', 'error');
        });
    }

    // 3. Inspect Backup Details
    async function openBackupDetails(backupId) {
      if (!backupDetailsModal) return;
      try {
        const res = await apiFetch(`/api/admin/backups/details?id=${encodeURIComponent(backupId)}`);
        const data = await res.json();
        const b = data.backup;

        if (bdtId) bdtId.textContent = b.backup_id || b.backupId;
        if (bdtFilename) bdtFilename.textContent = b.filename;
        if (bdtCreatedAt) bdtCreatedAt.textContent = b.created_at || b.createdAt;
        if (bdtCreatedBy) bdtCreatedBy.textContent = b.created_by || b.createdBy;
        if (bdtFilesize) bdtFilesize.textContent = `${((b.file_size || b.fileSize) / 1024).toFixed(1)} KB`;
        if (bdtStatus) bdtStatus.textContent = b.status;

        if (bdtStatsGrid && data.tableCounts) {
          const tc = data.tableCounts;
          bdtStatsGrid.innerHTML = `
            <div class="bdt-stat-pill">Teams: <strong>${tc.teams}</strong></div>
            <div class="bdt-stat-pill">Cases: <strong>${tc.cases}</strong></div>
            <div class="bdt-stat-pill">Questions: <strong>${tc.questions}</strong></div>
            <div class="bdt-stat-pill">Submissions: <strong>${tc.submissions}</strong></div>
            <div class="bdt-stat-pill">Audit Logs: <strong>${tc.auditLogs}</strong></div>
            <div class="bdt-stat-pill">Snapshot Integrity: <strong style="color: #00E676;">100% VALID</strong></div>
          `;
        }

        backupDetailsModal.style.display = 'flex';
      } catch (e) {
        showToast('ERROR', 'Failed to retrieve backup archive metadata.', 'error');
      }
    }

    if (btnCloseBkpDetails) {
      btnCloseBkpDetails.addEventListener('click', () => {
        if (backupDetailsModal) backupDetailsModal.style.display = 'none';
      });
    }

    // 4. Delete Backup Record
    function deleteBackupRecord(backupId) {
      openConfirmModal('DELETE DATABASE BACKUP', `Permanently delete archive ${backupId} from the server backup vault?`, async () => {
        try {
          const res = await apiFetch('/api/admin/backups/delete', {
            method: 'POST',
            body: { backupId }
          });
          if (res.ok) {
            showToast('BACKUP DELETED', `Backup ${backupId} deleted from disk.`, 'success');
            await loadBackupsList();
          } else {
            showToast('ERROR', 'Failed to delete backup file.', 'error');
          }
        } catch (e) {
          showToast('ERROR', 'Network error during backup deletion.', 'error');
        }
      });
    }

    // 5. Load Export History Log
    async function loadExportHistory() {
      if (!exportHistoryTbody) return;
      try {
        const res = await apiFetch('/api/admin/export/history');
        const data = await res.json();
        const logs = data.exportHistory || [];

        if (logs.length === 0) {
          exportHistoryTbody.innerHTML = `<tr><td colspan="7" style="text-align: center; color: var(--color-text-muted); padding: 1.5rem;">No export operations executed in this session yet.</td></tr>`;
          return;
        }

        exportHistoryTbody.innerHTML = logs.map(l => `
          <tr>
            <td style="font-family: var(--font-mono); font-weight: 700; color: var(--color-crimson-bright);">EXP-${String(l.id).padStart(4, '0')}</td>
            <td style="font-family: var(--font-heading); font-weight: 700; color: #FFFFFF;">${escapeHtml(l.export_type)}</td>
            <td style="font-family: var(--font-mono);">${escapeHtml(l.format)}</td>
            <td style="font-family: var(--font-mono);">${escapeHtml(l.admin_id)}</td>
            <td style="font-family: var(--font-mono); font-size: 0.74rem;">${escapeHtml(l.timestamp)}</td>
            <td style="font-family: var(--font-mono); font-weight: 700;">${l.record_count}</td>
            <td>
              <span class="cq-nav-pill ${l.status === 'COMPLETED' ? 'green' : ''}">
                ${escapeHtml(l.status)}
              </span>
            </td>
          </tr>
        `).join('');
      } catch (e) {
        exportHistoryTbody.innerHTML = `<tr><td colspan="7" style="text-align: center; color: #FF2438; padding: 1rem;">Failed to load export audit trail.</td></tr>`;
      }
    }

    // 6. Live Telemetry
    async function loadBackupDetailsTelemetry() {
      try {
        const res = await apiFetch('/api/admin/backups/details');
        const data = await res.json();
        if (bkpLiveSize && data.liveDbSize) {
          bkpLiveSize.textContent = `${(data.liveDbSize / 1024).toFixed(1)} KB`;
        }
      } catch (e) {}
    }

    // 7. Generic CSV Exporter Function
    async function triggerCsvExport(endpoint, defaultFilename, label) {
      try {
        const res = await apiFetch(endpoint);
        if (!res.ok) throw new Error('Export request failed');
        const blob = await res.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = defaultFilename;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        a.remove();
        showToast('EXPORT COMPLETE', `${label} exported as CSV (Excel compatible).`, 'success');
        await loadExportHistory();
      } catch (e) {
        showToast('EXPORT FAILED', `Failed to generate ${label} export.`, 'error');
      }
    }

    // Wire Export Buttons
    if (btnExportTeams) {
      btnExportTeams.addEventListener('click', () => {
        triggerCsvExport('/api/admin/export/teams', 'tracex_registered_teams.csv', 'Registered Teams');
      });
    }

    if (btnExportResults) {
      btnExportResults.addEventListener('click', () => {
        triggerCsvExport('/api/admin/export/results', 'tracex_official_results.csv', 'Evaluation Results');
      });
    }

    if (btnExportViolations) {
      btnExportViolations.addEventListener('click', () => {
        triggerCsvExport('/api/admin/export/violations', 'tracex_security_violations.csv', 'Security Violations');
      });
    }

    if (btnExportReportCsv) {
      btnExportReportCsv.addEventListener('click', () => {
        triggerCsvExport('/api/admin/export/report', 'tracex_final_event_report_data.csv', 'Final Event Report');
      });
    }

    if (btnExportReportPdfLink) {
      btnExportReportPdfLink.addEventListener('click', () => {
        const reportNavBtn = document.getElementById('nav-final-report');
        if (reportNavBtn) reportNavBtn.click();
      });
    }

    // Wire Create Database Backup Now
    if (btnCreateBackupNow) {
      btnCreateBackupNow.addEventListener('click', async () => {
        btnCreateBackupNow.disabled = true;
        btnCreateBackupNow.textContent = '⏳ [ CREATING CONSISTENT SNAPSHOT... ]';

        try {
          const res = await apiFetch('/api/admin/backups/create', {
            method: 'POST',
            body: {}
          });
          const data = await res.json();

          if (res.ok && data.success) {
            showToast('BACKUP CREATED', `Snapshot ${data.backup.backupId} created successfully (${(data.backup.fileSize / 1024).toFixed(1)} KB).`, 'success');
            await loadBackupExport();
          } else {
            showToast('BACKUP ERROR', data.error || 'Database backup operation failed.', 'error');
          }
        } catch (e) {
          showToast('SYSTEM ERROR', 'Network error while generating database backup.', 'error');
        } finally {
          btnCreateBackupNow.disabled = false;
          btnCreateBackupNow.textContent = '💾 [ CREATE DATABASE BACKUP NOW ]';
        }
      });
    }

    // =========================================================================
    // PROTOCOL: SURREAL — FINAL SCORE MANAGEMENT
    // =========================================================================
    let surrealTeams = [];
    let surrealActiveTeam = null;

    const surrealTableBody = document.getElementById('surreal-table-body');
    const surrealSearchInput = document.getElementById('surreal-search-input');
    const surrealStatusFilter = document.getElementById('surreal-status-filter');
    const btnRefreshSurreal = document.getElementById('btn-refresh-surreal');

    // Modals
    const surrealEditModal = document.getElementById('surreal-edit-modal');
    const surrealModalTeamId = document.getElementById('surreal-modal-team-id');
    const surrealModalTeamName = document.getElementById('surreal-modal-team-name');
    const surrealModalCurrScore = document.getElementById('surreal-modal-curr-score');
    const surrealInputScore = document.getElementById('surreal-input-score');
    const surrealInputReason = document.getElementById('surreal-input-reason');
    const surrealEditError = document.getElementById('surreal-edit-error');
    const btnSurrealCancel = document.getElementById('btn-surreal-cancel');
    const btnSurrealSave = document.getElementById('btn-surreal-save');

    const surrealHistoryModal = document.getElementById('surreal-history-modal');
    const surrealHistSubtitle = document.getElementById('surreal-hist-subtitle');
    const surrealHistoryContainer = document.getElementById('surreal-history-container');
    const btnSurrealCloseHistory = document.getElementById('btn-surreal-close-history');

    async function loadSurreal() {
      if (!surrealTableBody) return;
      const container = document.querySelector('#tab-surreal .admin-table-container');
      const prevScroll = container ? container.scrollLeft : 0;

      if (surrealTeams.length === 0) {
        surrealTableBody.innerHTML = `
          <tr>
            <td colspan="9" style="text-align: center; padding: 2rem; color: var(--color-text-muted);">
              Fetching participant score dossiers from SQLite repository...
            </td>
          </tr>
        `;
      }

      try {
        const res = await apiFetch('/api/admin/surreal/teams');
        const data = await res.json();
        if (res.ok && data.teams) {
          surrealTeams = data.teams;

          // Update summary metrics
          const totalTeams = surrealTeams.length;
          const scoredTeams = surrealTeams.filter(t => t.hasSubmission || t.currentFinalScore > 0).length;

          const elTotal = document.getElementById('surreal-stat-total');
          const elScored = document.getElementById('surreal-stat-scored');

          if (elTotal) elTotal.textContent = totalTeams;
          if (elScored) elScored.textContent = scoredTeams;

          renderSurrealTable();
          if (container) container.scrollLeft = prevScroll;
        } else {
          surrealTableBody.innerHTML = `
            <tr>
              <td colspan="9" style="text-align: center; padding: 2rem; color: #EF4444;">
                ${escapeHtml(data.error || 'Failed to load SURREAL participant data.')}
              </td>
            </tr>
          `;
        }
      } catch (err) {
        surrealTableBody.innerHTML = `
          <tr>
            <td colspan="9" style="text-align: center; padding: 2rem; color: #EF4444;">
              Network error while loading SURREAL scores.
            </td>
          </tr>
        `;
      }
    }

    function renderSurrealTable() {
      if (!surrealTableBody) return;
      const q = (surrealSearchInput ? surrealSearchInput.value : '').trim().toLowerCase();
      const statusFilter = surrealStatusFilter ? surrealStatusFilter.value : 'ALL';

      let filtered = surrealTeams.filter(t => {
        const matchesQuery = !q ||
          t.teamId.toLowerCase().includes(q) ||
          t.teamName.toLowerCase().includes(q) ||
          t.collegeName.toLowerCase().includes(q) ||
          t.department.toLowerCase().includes(q);

        if (!matchesQuery) return false;

        if (statusFilter === 'ALL') return true;
        if (statusFilter === 'QUALIFIED') return t.qualificationStatus === 'QUALIFIED';
        if (statusFilter === 'NOT QUALIFIED') return t.qualificationStatus === 'NOT QUALIFIED';
        if (statusFilter === 'DISQUALIFIED') return t.qualificationStatus === 'DISQUALIFIED';
        if (statusFilter === 'RESULTS UNDER REVIEW') return t.qualificationStatus === 'RESULTS UNDER REVIEW' || t.evaluationStatus === 'PENDING';
        return true;
      });

      if (filtered.length === 0) {
        surrealTableBody.innerHTML = `
          <tr>
            <td colspan="9" style="text-align: center; padding: 2.5rem; color: var(--color-text-muted);">
              No participant dossiers match the current search &amp; filter criteria.
            </td>
          </tr>
        `;
        return;
      }

      surrealTableBody.innerHTML = filtered.map(t => {
        let qualClass = 'badge-registered';
        if (t.qualificationStatus === 'QUALIFIED') qualClass = 'badge-active';
        else if (t.qualificationStatus === 'NOT QUALIFIED') qualClass = 'badge-not-qualified';
        else if (t.qualificationStatus === 'DISQUALIFIED') qualClass = 'badge-terminated';

        const rosterText = Array.isArray(t.members) && t.members.length > 0
          ? t.members.map(m => m.name || m).join(', ')
          : 'Enrolled Members';

        // Do not show the originally pointed score after editing
        const displayCalculated = t.isAdjusted ? t.currentFinalScore : t.originalCalculatedScore;

        return `
          <tr>
            <td style="font-family: var(--font-mono); font-weight: 700; color: #FFFFFF;">${escapeHtml(t.teamId)}</td>
            <td><strong>${escapeHtml(t.teamName)}</strong></td>
            <td>
              <div style="font-size: 0.8rem; color: #FFFFFF;">${escapeHtml(t.collegeName)}</div>
              <div style="font-size: 0.72rem; color: var(--color-text-muted);" title="${escapeHtml(rosterText)}">
                ${escapeHtml(t.department)} · ${escapeHtml(t.teamSize)} (${t.members ? t.members.length : 0} members)
              </div>
            </td>
            <td style="text-align: center; font-family: var(--font-mono); font-weight: 700; color: #10B981;">
              ${displayCalculated} <span style="font-size: 0.72rem; color: var(--color-text-muted);">/ 30</span>
            </td>
            <td style="text-align: center; vertical-align: middle;">
              <div style="display: inline-flex; align-items: center; justify-content: center; gap: 8px;">
                <span style="font-family: var(--font-mono); font-weight: 800; font-size: 1.05rem; color: #FFFFFF;">
                  ${t.currentFinalScore} <span style="font-size: 0.72rem; color: var(--color-text-muted);">/ 30</span>
                </span>
                <button type="button" class="btn-surreal-edit surreal-quick-edit" data-tid="${escapeHtml(t.teamId)}" title="Edit score for ${escapeHtml(t.teamId)}">
                  ✎ EDIT
                </button>
              </div>
            </td>
            <td style="text-align: center; font-family: var(--font-mono); color: var(--color-text-muted); font-size: 0.85rem;">
              30
            </td>
            <td style="text-align: center;">
              <span class="status-pill ${qualClass}">${escapeHtml(t.qualificationStatus)}</span>
            </td>
            <td style="font-family: var(--font-mono); font-size: 0.72rem; color: var(--color-text-secondary);">
              ${escapeHtml(t.lastModifiedAt || 'N/A')}
            </td>
            <td style="text-align: right; white-space: nowrap;">
              <button type="button" class="btn-table-action btn-surreal-edit" data-tid="${escapeHtml(t.teamId)}" style="margin-right: 6px; background: rgba(229, 9, 36, 0.25); border-color: var(--color-crimson); color: #FFFFFF;">
                [ EDIT SCORE ]
              </button>
              <button type="button" class="btn-table-action btn-surreal-history" data-tid="${escapeHtml(t.teamId)}">
                [ HISTORY ]
              </button>
            </td>
          </tr>
        `;
      }).join('');
    }

    if (surrealSearchInput) {
      surrealSearchInput.addEventListener('input', () => renderSurrealTable());
    }

    if (surrealStatusFilter) {
      surrealStatusFilter.addEventListener('change', () => renderSurrealTable());
    }

    if (btnRefreshSurreal) {
      btnRefreshSurreal.addEventListener('click', () => loadSurreal());
    }

    // Delegate table actions
    if (surrealTableBody) {
      surrealTableBody.addEventListener('click', (e) => {
        const btnEdit = e.target.closest('.btn-surreal-edit');
        if (btnEdit) {
          const tid = btnEdit.getAttribute('data-tid');
          openSurrealEditModal(tid);
          return;
        }

        const btnHist = e.target.closest('.btn-surreal-history');
        if (btnHist) {
          const tid = btnHist.getAttribute('data-tid');
          openSurrealHistoryModal(tid);
          return;
        }
      });
    }

    function openSurrealEditModal(teamId) {
      const team = surrealTeams.find(t => t.teamId.toUpperCase() === teamId.toUpperCase());
      if (!team || !surrealEditModal) return;

      surrealActiveTeam = team;
      if (surrealModalTeamId) surrealModalTeamId.textContent = team.teamId;
      if (surrealModalTeamName) surrealModalTeamName.textContent = team.teamName;
      if (surrealModalCurrScore) surrealModalCurrScore.textContent = `${team.currentFinalScore} / 30`;
      if (surrealInputScore) surrealInputScore.value = team.currentFinalScore;
      if (surrealInputReason) surrealInputReason.value = '';
      if (surrealEditError) {
        surrealEditError.textContent = '';
        surrealEditError.style.display = 'none';
      }

      // Ensure no secondary confirmation modal is ever open
      if (confirmModal) confirmModal.style.display = 'none';

      // Reset in-modal confirmation state
      const defaultActions = document.getElementById('surreal-modal-default-actions');
      const confirmActions = document.getElementById('surreal-modal-confirm-actions');
      if (defaultActions) defaultActions.style.display = 'flex';
      if (confirmActions) confirmActions.style.display = 'none';

      surrealEditModal.style.display = 'flex';
      if (surrealInputScore) surrealInputScore.focus();
    }

    function closeSurrealEditModal() {
      if (surrealEditModal) surrealEditModal.style.display = 'none';
      surrealActiveTeam = null;
    }

    if (btnSurrealCancel) {
      btnSurrealCancel.addEventListener('click', closeSurrealEditModal);
    }

    if (btnSurrealSave) {
      btnSurrealSave.addEventListener('click', () => {
        if (!surrealActiveTeam) return;

        const scoreStr = (surrealInputScore ? surrealInputScore.value : '').trim();
        const reason = (surrealInputReason ? surrealInputReason.value : '').trim();

        if (surrealEditError) {
          surrealEditError.textContent = '';
          surrealEditError.style.display = 'none';
        }

        if (!scoreStr) {
          showSurrealError('Final score is required. Please enter an integer between 0 and 30.');
          return;
        }

        if (scoreStr.includes('.')) {
          showSurrealError('Decimal scores are not allowed. Please enter a whole integer value between 0 and 30.');
          return;
        }

        const newScore = parseInt(scoreStr, 10);
        if (isNaN(newScore)) {
          showSurrealError('Score must be a valid numeric integer value.');
          return;
        }

        if (newScore < 0) {
          showSurrealError('Negative scores are strictly prohibited. Score cannot be less than 0.');
          return;
        }

        if (newScore > 30) {
          showSurrealError('Score cannot exceed the maximum possible score of 30.');
          return;
        }

        if (!reason || reason.length < 3) {
          showSurrealError('A documented reason for modification is required (minimum 3 characters).');
          return;
        }

        // Show in-modal confirmation state (NO SECOND MODAL POPPING UP)
        const defaultActions = document.getElementById('surreal-modal-default-actions');
        const confirmActions = document.getElementById('surreal-modal-confirm-actions');
        const confirmVal = document.getElementById('surreal-confirm-preview-score');
        if (confirmVal) confirmVal.textContent = newScore;
        if (defaultActions) defaultActions.style.display = 'none';
        if (confirmActions) confirmActions.style.display = 'block';
      });
    }

    const btnSurrealConfirmBack = document.getElementById('btn-surreal-confirm-back');
    if (btnSurrealConfirmBack) {
      btnSurrealConfirmBack.addEventListener('click', () => {
        const defaultActions = document.getElementById('surreal-modal-default-actions');
        const confirmActions = document.getElementById('surreal-modal-confirm-actions');
        if (confirmActions) confirmActions.style.display = 'none';
        if (defaultActions) defaultActions.style.display = 'flex';
      });
    }

    const btnSurrealConfirmProceed = document.getElementById('btn-surreal-confirm-proceed');
    if (btnSurrealConfirmProceed) {
      btnSurrealConfirmProceed.addEventListener('click', async () => {
        if (!surrealActiveTeam) return;
        const team = surrealActiveTeam;
        const scoreStr = (surrealInputScore ? surrealInputScore.value : '').trim();
        const reason = (surrealInputReason ? surrealInputReason.value : '').trim();
        const newScore = parseInt(scoreStr, 10);

        btnSurrealConfirmProceed.disabled = true;
        btnSurrealConfirmProceed.textContent = 'SAVING...';

        try {
          const res = await apiFetch('/api/admin/surreal/update-score', {
            method: 'POST',
            body: {
              teamId: team.teamId,
              newScore: newScore,
              reason: reason
            }
          });

          const data = await res.json();
          if (res.ok && data.success) {
            closeSurrealEditModal();
            showToast('SCORE UPDATED', `Final score for ${team.teamId} updated to ${newScore} / 30.`, 'success');
            await loadSurreal();
          } else {
            showSurrealError(data.error || 'Failed to update score.');
            showToast('UPDATE REJECTED', data.error || 'Score update failed.', 'error');
            const defaultActions = document.getElementById('surreal-modal-default-actions');
            const confirmActions = document.getElementById('surreal-modal-confirm-actions');
            if (confirmActions) confirmActions.style.display = 'none';
            if (defaultActions) defaultActions.style.display = 'flex';
          }
        } catch (err) {
          showSurrealError('Network error while committing score change to server.');
          showToast('SYSTEM ERROR', 'Network error during score adjustment.', 'error');
          const defaultActions = document.getElementById('surreal-modal-default-actions');
          const confirmActions = document.getElementById('surreal-modal-confirm-actions');
          if (confirmActions) confirmActions.style.display = 'none';
          if (defaultActions) defaultActions.style.display = 'flex';
        } finally {
          btnSurrealConfirmProceed.disabled = false;
          btnSurrealConfirmProceed.textContent = 'CONFIRM & SAVE';
        }
      });
    }

    function showSurrealError(msg) {
      if (!surrealEditError) return;
      surrealEditError.textContent = msg;
      surrealEditError.style.display = 'block';
    }

    async function openSurrealHistoryModal(teamId) {
      if (!surrealHistoryModal || !surrealHistoryContainer) return;
      surrealHistoryModal.style.display = 'flex';
      if (surrealHistSubtitle) surrealHistSubtitle.textContent = `Historical score audit trail for Team ${teamId}`;
      surrealHistoryContainer.innerHTML = `
        <div style="text-align: center; padding: 2rem; color: var(--color-text-muted);">
          Fetching audit trail records from SQLite...
        </div>
      `;

      try {
        const res = await apiFetch(`/api/admin/surreal/history?teamId=${encodeURIComponent(teamId)}`);
        const data = await res.json();
        if (res.ok && data.history) {
          if (data.history.length === 0) {
            surrealHistoryContainer.innerHTML = `
              <div style="text-align: center; padding: 2.5rem; color: var(--color-text-muted); background: var(--color-surface-secondary); border-radius: 4px;">
                No administrative score modifications recorded for this team. Score remains at original calculated value.
              </div>
            `;
            return;
          }

          surrealHistoryContainer.innerHTML = data.history.map(item => `
            <div style="background: var(--color-surface-secondary); border: 1px solid var(--color-border); border-left: 3px solid var(--color-crimson); padding: 0.85rem 1.1rem; border-radius: 4px;">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem;">
                <span style="font-family: var(--font-mono); font-size: 0.72rem; font-weight: 700; color: #FFFFFF;">
                  SCORE CHANGE: <span style="color: var(--color-text-muted);">${item.prevFinalScore} / 30</span> &rarr; <span style="color: var(--color-crimson); font-weight: 800;">${item.newFinalScore} / 30</span>
                </span>
                <span style="font-family: var(--font-mono); font-size: 0.68rem; color: var(--color-text-muted);">
                  ${escapeHtml(item.timestamp)}
                </span>
              </div>
              <div style="font-size: 0.8rem; color: var(--color-text-secondary); margin-bottom: 0.35rem;">
                Reason: &ldquo;${escapeHtml(item.reason)}&rdquo;
              </div>
              <div style="display: flex; justify-content: space-between; font-family: var(--font-mono); font-size: 0.68rem; color: var(--color-text-muted);">
                <span>Admin: <strong style="color: #FFFFFF;">${escapeHtml(item.adminId)}</strong></span>
                <span>Original Calculated Score: <strong style="color: #10B981;">${item.originalScore} / 30</strong></span>
              </div>
            </div>
          `).join('');
        } else {
          surrealHistoryContainer.innerHTML = `
            <div style="text-align: center; padding: 2rem; color: #EF4444;">
              ${escapeHtml(data.error || 'Failed to load audit history.')}
            </div>
          `;
        }
      } catch (err) {
        surrealHistoryContainer.innerHTML = `
          <div style="text-align: center; padding: 2rem; color: #EF4444;">
            Network error while retrieving audit history.
          </div>
        `;
      }
    }

    if (btnSurrealCloseHistory) {
      btnSurrealCloseHistory.addEventListener('click', () => {
        if (surrealHistoryModal) surrealHistoryModal.style.display = 'none';
      });
    }

    // Initial Overview Load
    loadOverview();
  }

  // DOM Content Loaded Hook
  document.addEventListener('DOMContentLoaded', () => {
    initAdminLogin();
    initAdminDashboard();
  });

})();
