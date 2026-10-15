/**
 * TRACE × X — CYBER CRIME INVESTIGATION
 * Application Architecture & Core Logic
 * T.J.S. ENGINEERING COLLEGE | DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING
 * 
 * STEP 4: Homepage, Team Registration, and Participant Authentication Flow
 */

'use strict';

const TraceApp = (function () {
  // Shared Configuration Blueprint
  const config = {
    eventName: 'TRACE × X',
    institution: 'TJS ENGINEERING COLLEGE',
    department: 'DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING',
    tagline: 'THE TRUTH LEAVES A TRACE',
    version: '1.4.0-authentication',
    routes: {
      home: 'index.html',
      login: 'login.html',
      register: 'register.html',
      admin: 'admin.html',
      investigation: 'investigation.html'
    }
  };

  /**
   * Generates a unique, cryptographic-styled Team ID (Format: TX-YYYY-XXXX)
   */
  function generateTeamId() {
    const year = new Date().getFullYear();
    const randomHex = Math.floor(1000 + Math.random() * 9000);
    const suffixLetters = ['X', 'A', 'K', 'Z', 'F'];
    const suffix = suffixLetters[Math.floor(Math.random() * suffixLetters.length)];
    return `TX-${year}-${randomHex}${suffix}`;
  }

  /**
   * Converts camelCase to kebab-case
   */
  function toKebabCase(str) {
    return str.replace(/[A-Z]/g, letter => `-${letter.toLowerCase()}`);
  }

  /**
   * Escapes HTML entities to prevent XSS
   */
  function escapeHtml(str) {
    if (!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  /**
   * Helper to resolve active team ID for strict session data isolation
   */
  function getActiveTeamId() {
    try {
      const auth = JSON.parse(sessionStorage.getItem('traceX_auth_session') || '{}');
      if (auth && auth.teamId) return String(auth.teamId).trim().toUpperCase();
    } catch (e) {}
    try {
      const act = JSON.parse(sessionStorage.getItem('traceX_activeTeam') || '{}');
      if (act && act.teamId) return String(act.teamId).trim().toUpperCase();
    } catch (e) {}
    return 'TX-2026-TEAM';
  }

  /**
   * Client-Side View Navigation Manager
   * Handles seamless transitions between Homepage, Case Selection, and Fullscreen Investigation
   * without document reloads, preserving fullscreen state, active sessions, and timers.
   */
  const NavigationManager = (function () {
    let currentView = 'home';
    let isInternalNav = false;

    function getCurrentView() {
      return currentView;
    }

    function isInternalNavigating() {
      return isInternalNav;
    }

    function switchView(targetView, caseIdParam) {
      isInternalNav = true;

      const viewHome = document.getElementById('view-homepage');
      const viewCases = document.getElementById('view-case-selection');
      const viewInv = document.getElementById('view-investigation');
      const siteHeader = document.getElementById('site-header') || document.querySelector('.site-header');

      document.body.classList.remove('homepage-active', 'cases-active', 'investigation-active');

      if (targetView === 'cases') {
        currentView = 'cases';
        document.body.classList.add('cases-active');
        try {
          sessionStorage.setItem('traceX_nav_view', 'cases');
        } catch (e) {}

        if (viewHome) {
          viewHome.classList.remove('trace-view-active');
          viewHome.style.display = 'none';
        }
        if (viewInv) {
          viewInv.classList.remove('trace-view-active');
          viewInv.style.display = 'none';
        }
        if (viewCases) {
          viewCases.classList.add('trace-view-active');
          viewCases.style.display = 'block';
        }
        if (siteHeader) {
          siteHeader.style.display = '';
        }

        window.scrollTo(0, 0);

      } else if (targetView === 'investigation') {
        currentView = 'investigation';
        document.body.classList.add('investigation-active');
        try {
          sessionStorage.setItem('traceX_nav_view', 'investigation');
        } catch (e) {}

        if (viewHome) {
          viewHome.classList.remove('trace-view-active');
          viewHome.style.display = 'none';
        }
        if (viewCases) {
          viewCases.classList.remove('trace-view-active');
          viewCases.style.display = 'none';
        }
        if (siteHeader) {
          siteHeader.style.display = 'none';
        }
        if (viewInv) {
          viewInv.classList.add('trace-view-active');
          viewInv.style.display = 'flex';
        }

        window.scrollTo(0, 0);

        // Render and initialize the investigation workstation for the selected case
        initInvestigation(caseIdParam);

      } else {
        // Default: 'home'
        currentView = 'home';
        document.body.classList.add('homepage-active');
        try {
          sessionStorage.setItem('traceX_nav_view', 'home');
        } catch (e) {}

        if (viewCases) {
          viewCases.classList.remove('trace-view-active');
          viewCases.style.display = 'none';
        }
        if (viewInv) {
          viewInv.classList.remove('trace-view-active');
          viewInv.style.display = 'none';
        }
        if (viewHome) {
          viewHome.classList.add('trace-view-active');
          viewHome.style.display = 'block';
        }
        if (siteHeader) {
          siteHeader.style.display = '';
        }

        window.scrollTo(0, 0);
      }

      setTimeout(() => {
        isInternalNav = false;
      }, 600);
    }

    return {
      getCurrentView,
      isInternalNavigating,
      switchView
    };
  })();

  /**
   * Initializes the Team Registration Terminal
   */
  function initRegistration() {
    const form = document.getElementById('team-registration-form');
    if (!form) return; // Not on the registration page

    const membersContainer = document.getElementById('members-container');
    const sizeOptions = document.querySelectorAll('.size-card-option');
    const formContainer = document.getElementById('registration-form-container');
    const successContainer = document.getElementById('registration-success-container');
    const displayTeamId = document.getElementById('display-team-id');
    const displayTeamName = document.getElementById('display-team-name');
    const displayRegNum = document.getElementById('display-reg-num');
    const copyBtn = document.getElementById('btn-copy-team-id');
    const globalError = document.getElementById('form-global-error');

    // PIN toggle elements
    const pinInput1 = document.getElementById('input-security-pin');
    const pinInput2 = document.getElementById('input-confirm-pin');
    const togglePin1 = document.getElementById('toggle-pin-1');
    const togglePin2 = document.getElementById('toggle-pin-2');

    let currentSize = 1;
    const memberValues = ['', '', '', ''];

    /**
     * Renders member input fields based on selected team size
     */
    function renderMemberFields(size) {
      if (!membersContainer) return;

      // Save any currently typed values before re-rendering
      for (let i = 0; i < 4; i++) {
        const existingInput = document.getElementById(`input-member-${i + 1}`);
        if (existingInput) {
          memberValues[i] = existingInput.value;
        }
      }

      membersContainer.innerHTML = '';

      for (let i = 1; i <= size; i++) {
        const isLead = i === 1;
        const labelText = isLead ? 'MEMBER 01 — TEAM LEAD' : `MEMBER 0${i}`;
        const placeholderText = isLead 
          ? 'Enter Team Lead full name' 
          : `Enter full name of Member 0${i}`;

        const fieldGroup = document.createElement('div');
        fieldGroup.className = 'form-field-group';
        fieldGroup.id = `group-member-${i}`;

        fieldGroup.innerHTML = `
          <label for="input-member-${i}" class="field-label">
            <span>${labelText}</span>
            <span class="required-star">*</span>
          </label>
          <input 
            type="text" 
            id="input-member-${i}" 
            name="member_${i}" 
            class="text-input-field" 
            placeholder="${placeholderText}" 
            value="${escapeHtml(memberValues[i - 1])}" 
            required 
            autocomplete="name"
          >
          <span class="field-error-msg" id="error-member-${i}">Please enter ${labelText.toLowerCase()}.</span>
        `;

        // Live error clearing
        const inputElem = fieldGroup.querySelector('input');
        inputElem.addEventListener('input', function () {
          memberValues[i - 1] = this.value;
          if (this.value.trim().length > 0) {
            fieldGroup.classList.remove('has-error');
          }
        });

        membersContainer.appendChild(fieldGroup);
      }
    }

    // Set initial member fields (default: SOLO)
    renderMemberFields(currentSize);

    // Setup Team Size selector events
    sizeOptions.forEach(option => {
      function selectThisOption() {
        sizeOptions.forEach(opt => {
          opt.classList.remove('selected');
          opt.setAttribute('aria-checked', 'false');
        });

        option.classList.add('selected');
        option.setAttribute('aria-checked', 'true');

        const sizeVal = parseInt(option.getAttribute('data-size'), 10);
        if (!isNaN(sizeVal) && sizeVal >= 1 && sizeVal <= 4) {
          currentSize = sizeVal;
          renderMemberFields(currentSize);
        }
      }

      option.addEventListener('click', selectThisOption);
      option.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          selectThisOption();
        }
      });
    });

    // Setup Show/Hide PIN buttons
    function setupPinToggle(btn, input) {
      if (!btn || !input) return;
      btn.addEventListener('click', function () {
        const isPassword = input.type === 'password';
        input.type = isPassword ? 'text' : 'password';
        btn.textContent = isPassword ? 'HIDE' : 'SHOW';
      });
    }

    setupPinToggle(togglePin1, pinInput1);
    setupPinToggle(togglePin2, pinInput2);

    // Live error clearing on standard text fields
    const standardFields = ['teamName', 'collegeName', 'department', 'securityPin', 'confirmPin'];
    standardFields.forEach(fieldName => {
      const input = document.getElementById(`input-${toKebabCase(fieldName)}`);
      const group = document.getElementById(`group-${fieldName}`);
      if (input && group) {
        input.addEventListener('input', function () {
          if (this.value.trim().length > 0) {
            group.classList.remove('has-error');
          }
        });
      }
    });

    const agreementCheckbox = document.getElementById('input-agreement');
    const agreementGroup = document.getElementById('group-agreement');
    if (agreementCheckbox && agreementGroup) {
      agreementCheckbox.addEventListener('change', function () {
        if (this.checked) {
          agreementGroup.classList.remove('has-error');
        }
      });
    }

    /**
     * Form Submission Handler & Validation
     */
    form.addEventListener('submit', function (e) {
      e.preventDefault();

      let isValid = true;
      let firstInvalidElement = null;

      function setError(groupId, isError) {
        const group = document.getElementById(groupId);
        if (!group) return;
        if (isError) {
          group.classList.add('has-error');
          isValid = false;
          if (!firstInvalidElement) {
            firstInvalidElement = group.querySelector('input') || group;
          }
        } else {
          group.classList.remove('has-error');
        }
      }

      // 1. Team Name
      const teamNameVal = document.getElementById('input-team-name')?.value.trim();
      setError('group-teamName', !teamNameVal);

      // 2. College Name
      const collegeNameVal = document.getElementById('input-college-name')?.value.trim();
      setError('group-collegeName', !collegeNameVal);

      // 3. Department
      const deptVal = document.getElementById('input-department')?.value.trim();
      setError('group-department', !deptVal);

      // 4. Team Members (All visible members required)
      for (let i = 1; i <= currentSize; i++) {
        const memberInput = document.getElementById(`input-member-${i}`);
        const memberVal = memberInput ? memberInput.value.trim() : '';
        setError(`group-member-${i}`, !memberVal);
      }

      // 5. Security PIN (Required, min 4 characters)
      const pinVal = pinInput1?.value.trim();
      setError('group-securityPin', !pinVal || pinVal.length < 4);

      // 6. Confirm PIN (Must match)
      const confirmPinVal = pinInput2?.value.trim();
      const pinsMatch = Boolean(pinVal && confirmPinVal && pinVal === confirmPinVal);
      setError('group-confirmPin', !confirmPinVal || !pinsMatch);

      // 7. Agreement Checkbox
      const agreementChecked = Boolean(agreementCheckbox?.checked);
      setError('group-agreement', !agreementChecked);

      // If invalid, focus first error and show global notice
      if (!isValid) {
        if (globalError) globalError.style.display = 'block';
        if (firstInvalidElement && typeof firstInvalidElement.focus === 'function') {
          firstInvalidElement.focus();
        }
        return;
      }

      // Hide global error if valid
      if (globalError) globalError.style.display = 'none';

      // Disable submit button during credential generation
      const submitBtn = document.getElementById('btn-submit-reg');
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = `<span>[ GENERATING SYSTEM CREDENTIALS... ]</span>`;
      }

      // Collect team record for database registration (teamId assigned authoritatively by backend sequence)
      const teamData = {
        teamName: teamNameVal,
        collegeName: collegeNameVal,
        department: deptVal,
        teamSize: currentSize,
        members: memberValues.slice(0, currentSize),
        pinMasked: '••••••',
        pinRaw: pinVal,
        registeredAt: new Date().toISOString()
      };

      // Register team against authoritative backend API
      fetch('/api/teams/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(teamData)
      })
      .then(async res => {
        let data = {};
        try {
          data = await res.json();
        } catch (jsonErr) {
          data = { error: `Server communication failure (HTTP ${res.status}).` };
        }
        return { ok: res.ok, status: res.status, data };
      })
      .then(({ ok, status, data }) => {
        if (!ok || !data.success) {
          if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.innerHTML = `<span>[ SUBMIT TEAM REGISTRATION ]</span> <span aria-hidden="true">→</span>`;
          }
          if (globalError) {
            globalError.textContent = data.error || `Registration failed (HTTP ${status}). Please try again.`;
            globalError.style.display = 'block';
            globalError.scrollIntoView({ behavior: 'smooth' });
          }
          return;
        }

        const assignedTeamId = data.teamId || 'TX-2026-0001';
        teamData.teamId = assignedTeamId;
        teamData.registrationNumber = data.registrationNumber || 1;

        // Store in sessionStorage on confirmed database registration
        try {
          let registry = [];
          const existing = JSON.parse(sessionStorage.getItem('traceX_registeredTeams') || '[]');
          if (Array.isArray(existing)) registry = existing;
          registry.push(teamData);
          sessionStorage.setItem('traceX_registeredTeams', JSON.stringify(registry));
          sessionStorage.setItem('traceX_activeTeam', JSON.stringify(teamData));
        } catch (err) {
          console.warn('Session storage write error:', err);
        }

        // Transition to Success Screen ONLY on confirmed database write
        if (formContainer) formContainer.style.display = 'none';
        if (displayTeamId) displayTeamId.textContent = assignedTeamId;
        if (displayTeamName) displayTeamName.textContent = teamNameVal;
        if (displayRegNum && data && data.registrationNumber) {
          displayRegNum.textContent = `#${data.registrationNumber}`;
        }

        if (successContainer) {
          successContainer.style.display = 'block';
          successContainer.scrollIntoView({ behavior: 'smooth' });
        }
      })
      .catch(err => {
        console.error('Registration network error:', err);
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.innerHTML = `<span>[ SUBMIT TEAM REGISTRATION ]</span> <span aria-hidden="true">→</span>`;
        }
        if (globalError) {
          globalError.textContent = 'Network communication failure. Could not connect to registration server. Please verify your connection and try again.';
          globalError.style.display = 'block';
          globalError.scrollIntoView({ behavior: 'smooth' });
        }
      });
    });

    // Setup Copy Team ID button
    if (copyBtn && displayTeamId) {
      copyBtn.addEventListener('click', function () {
        const idText = displayTeamId.textContent.trim();
        if (!idText) return;

        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(idText).then(onCopySuccess).catch(fallbackCopy);
        } else {
          fallbackCopy();
        }

        function fallbackCopy() {
          const tempInput = document.createElement('input');
          tempInput.value = idText;
          document.body.appendChild(tempInput);
          tempInput.select();
          document.execCommand('copy');
          document.body.removeChild(tempInput);
          onCopySuccess();
        }

        function onCopySuccess() {
          const originalText = copyBtn.textContent;
          copyBtn.textContent = '✔ COPIED TO CLIPBOARD!';
          copyBtn.style.borderColor = 'var(--color-crimson-bright)';
          copyBtn.style.color = '#FFFFFF';

          setTimeout(() => {
            copyBtn.textContent = originalText;
            copyBtn.style.borderColor = '';
            copyBtn.style.color = '';
          }, 2500);
        }
      });
    }
  }

  /**
   * Initializes the Participant Login Terminal & Fullscreen Flow
   */
  function initLogin() {
    const form = document.getElementById('participant-login-form');
    if (!form) return; // Not on the login page

    const teamIdInput = document.getElementById('input-login-team-id');
    const pinInput = document.getElementById('input-login-pin');
    const togglePinBtn = document.getElementById('toggle-login-pin');
    const submitBtn = document.getElementById('btn-login-submit');
    const errorAlert = document.getElementById('login-error-alert');
    const fsModal = document.getElementById('fullscreen-activation-modal');
    const enterFsBtn = document.getElementById('btn-enter-fullscreen');

    // Show/Hide PIN control
    if (togglePinBtn && pinInput) {
      togglePinBtn.addEventListener('click', function () {
        const isPassword = pinInput.type === 'password';
        pinInput.type = isPassword ? 'text' : 'password';
        togglePinBtn.textContent = isPassword ? 'HIDE' : 'SHOW';
      });
    }

    // Live error clearing
    [teamIdInput, pinInput].forEach(input => {
      if (input) {
        input.addEventListener('input', function () {
          if (errorAlert) errorAlert.style.display = 'none';
          const group = this.closest('.form-field-group');
          if (group) group.classList.remove('has-error');
        });
      }
    });

    // Form submit validation & verification
    form.addEventListener('submit', function (e) {
      e.preventDefault();

      const teamIdVal = teamIdInput ? teamIdInput.value.trim() : '';
      const pinVal = pinInput ? pinInput.value.trim() : '';

      let hasFieldError = false;

      if (!teamIdVal) {
        document.getElementById('group-login-teamId')?.classList.add('has-error');
        hasFieldError = true;
      } else {
        document.getElementById('group-login-teamId')?.classList.remove('has-error');
      }

      if (!pinVal) {
        document.getElementById('group-login-pin')?.classList.add('has-error');
        hasFieldError = true;
      } else {
        document.getElementById('group-login-pin')?.classList.remove('has-error');
      }

      if (hasFieldError) return;

      // Disable button briefly during authentication check
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = `<span>[ AUTHENTICATING... ]</span>`;
      }

      // Verify credentials against authoritative backend API
      fetch('/api/teams/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ teamId: teamIdVal, pin: pinVal })
      })
      .then(res => res.json().then(data => ({ status: res.status, ok: res.ok, data })))
      .then(({ ok, data }) => {
        if (!ok || !data.success) {
          if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.innerHTML = `<span>[ ENTER INVESTIGATION ]</span> <span aria-hidden="true">→</span>`;
          }
          if (errorAlert) {
            errorAlert.style.display = 'block';
            const errorDesc = errorAlert.querySelector('.login-error-desc');
            if (errorDesc) errorDesc.textContent = data.error || 'Invalid Team ID or Security PIN.';
            errorAlert.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
          }
          return;
        }

        const authenticatedTeam = data.team;
        const progress = data.progress;

        // Store active authenticated session
        const sessionData = {
          authenticated: true,
          teamId: authenticatedTeam.teamId,
          teamName: authenticatedTeam.teamName,
          collegeName: authenticatedTeam.collegeName,
          department: authenticatedTeam.department,
          token: data.token || '',
          loginTime: new Date().toISOString()
        };
        sessionStorage.setItem('traceX_auth_session', JSON.stringify(sessionData));
        sessionStorage.setItem('traceX_activeTeam', JSON.stringify(authenticatedTeam));
        sessionStorage.setItem(`traceX_${authenticatedTeam.teamId}_auth_session`, JSON.stringify(sessionData));
        sessionStorage.setItem('traceX_intro_completed', 'true');
        sessionStorage.setItem('traceX_pending_fullscreen', 'true');

        // Clean up legacy unscoped keys to prevent any cross-team bleed
        sessionStorage.removeItem('traceX_selectedCase');

        // Route to the appropriate screen according to team's explicit server-persisted state
        const state = progress ? progress.logicalState : 'CASE_NOT_SELECTED';
        const assignedCase = (progress && progress.caseId) ? progress.caseId : null;

        if (state === 'ROUND_1_IN_PROGRESS' && assignedCase) {
          window.location.href = `${config.routes.home}#investigation?case=${encodeURIComponent(assignedCase)}&round=1`;
        } else if (state === 'ROUND_1_COMPLETED' && assignedCase) {
          window.location.href = `${config.routes.home}#investigation?case=${encodeURIComponent(assignedCase)}&round=1&completed=1`;
        } else if (state === 'ROUND_2_IN_PROGRESS' && assignedCase) {
          window.location.href = `${config.routes.home}#investigation?case=${encodeURIComponent(assignedCase)}&round=2`;
        } else if ((state === 'ROUND_2_COMPLETED' || state === 'EVALUATION_PENDING') && assignedCase) {
          window.location.href = `evaluation.html?case=${encodeURIComponent(assignedCase)}`;
        } else if (state === 'EVALUATION_COMPLETED' && assignedCase) {
          window.location.href = `results.html?case=${encodeURIComponent(assignedCase)}`;
        } else {
          // New team or CASE_NOT_SELECTED -> View available 15 cases
          window.location.href = `${config.routes.home}#cases`;
        }
      })
      .catch(err => {
        console.error('Backend login network error:', err);
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.innerHTML = `<span>[ ENTER INVESTIGATION ]</span> <span aria-hidden="true">→</span>`;
        }
        if (errorAlert) {
          const errorDesc = errorAlert.querySelector('.login-error-desc');
          if (errorDesc) errorDesc.textContent = 'Network communication failure. Could not connect to authentication server.';
          errorAlert.style.display = 'block';
          errorAlert.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }
      });
    });

    // Fullscreen activation screen click
    if (enterFsBtn) {
      enterFsBtn.addEventListener('click', function () {
        const docEl = document.documentElement;
        const requestFs = docEl.requestFullscreen || 
                          docEl.webkitRequestFullscreen || 
                          docEl.mozRequestFullScreen || 
                          docEl.msRequestFullscreen;

        if (requestFs) {
          requestFs.call(docEl).then(() => {
            window.location.href = `${config.routes.home}#cases`;
          }).catch(() => {
            window.location.href = `${config.routes.home}#cases`;
          });
        } else {
          window.location.href = `${config.routes.home}#cases`;
        }
      });
    }
  }

  /**
   * Initializes Case Selection Protocol
   */
  function initCases() {
    const grid = document.getElementById('cases-grid-container');
    const openBtn = document.getElementById('btn-open-case');
    const hintText = document.getElementById('case-selection-hint');

    // Homepage Enter Investigation button: seamless in-page switch
    const enterInvBtn = document.getElementById('btn-enter-investigation');
    if (enterInvBtn && !enterInvBtn.dataset.listenerAttached) {
      enterInvBtn.dataset.listenerAttached = 'true';
      enterInvBtn.addEventListener('click', function (e) {
        let authSession = null;
        try {
          authSession = JSON.parse(sessionStorage.getItem('traceX_auth_session') || 'null');
        } catch (err) {}

        if (!authSession || !authSession.authenticated) {
          e.preventDefault();
          window.location.href = config.routes.login;
          return;
        }

        if (document.getElementById('view-case-selection')) {
          e.preventDefault();
          NavigationManager.switchView('cases');
          try {
            history.pushState({ view: 'cases' }, '', '#cases');
          } catch (err) {}
        }
      });
    }

    // Back to homepage links inside case selection
    const backHomeLinks = document.querySelectorAll('#view-case-selection .back-home-link, #btn-back-home');
    backHomeLinks.forEach(link => {
      if (!link.dataset.listenerAttached) {
        link.dataset.listenerAttached = 'true';
        link.addEventListener('click', function (e) {
          if (document.getElementById('view-homepage')) {
            e.preventDefault();
            NavigationManager.switchView('home');
            try {
              history.pushState({ view: 'home' }, '', '#');
            } catch (err) {}
          }
        });
      }
    });

    if (!grid || !openBtn) return; // Not on the case selection page/view

    const caseCards = grid.querySelectorAll('.case-card');
    let selectedCaseData = null;
    const activeTeamId = getActiveTeamId();

    // Check server-persisted case for this specific authenticated team
    async function syncTeamCaseSelection() {
      try {
        const res = await fetch(`/api/teams/progress?team_id=${encodeURIComponent(activeTeamId)}`);
        if (res.ok) {
          const data = await res.json();
          if (data && data.progress && data.progress.caseId) {
            const serverCaseId = data.progress.caseId;
            const matchingCard = grid.querySelector(`[data-case-id="${serverCaseId}"]`);
            if (matchingCard) {
              caseCards.forEach(c => {
                c.classList.remove('selected');
                c.setAttribute('aria-checked', 'false');
              });
              matchingCard.classList.add('selected');
              matchingCard.setAttribute('aria-checked', 'true');
              selectedCaseData = {
                caseId: serverCaseId,
                caseName: data.progress.caseName || matchingCard.getAttribute('data-case-name')
              };
              openBtn.disabled = false;
              if (hintText) {
                hintText.textContent = `ASSIGNED: ${selectedCaseData.caseName} // CLICK OPEN CASE TO PROCEED`;
                hintText.style.color = 'var(--color-amber-bright)';
              }
              sessionStorage.setItem(`traceX_${activeTeamId}_selectedCase`, JSON.stringify(selectedCaseData));
              return;
            }
          }
        }
      } catch (err) {}

      // Fallback to team-scoped sessionStorage
      try {
        const storedCase = JSON.parse(sessionStorage.getItem(`traceX_${activeTeamId}_selectedCase`) || 'null');
        if (storedCase && storedCase.caseId) {
          selectedCaseData = storedCase;
          const matchingCard = grid.querySelector(`[data-case-id="${storedCase.caseId}"]`);
          if (matchingCard) {
            caseCards.forEach(c => {
              c.classList.remove('selected');
              c.setAttribute('aria-checked', 'false');
            });
            matchingCard.classList.add('selected');
            matchingCard.setAttribute('aria-checked', 'true');
            openBtn.disabled = false;
            if (hintText) {
              hintText.textContent = `SELECTED: ${storedCase.caseName} // CLICK OPEN CASE TO PROCEED`;
              hintText.style.color = 'var(--color-amber-bright)';
            }
          }
        } else {
          // New team with no case: ensure clean slate
          caseCards.forEach(c => {
            c.classList.remove('selected');
            c.setAttribute('aria-checked', 'false');
          });
          selectedCaseData = null;
          openBtn.disabled = true;
          if (hintText) {
            hintText.textContent = 'SELECT AN INVESTIGATION DOSSIER TO COMMENCE FORENSIC TRIAGE';
            hintText.style.color = '';
          }
        }
      } catch (e) {}
    }

    syncTeamCaseSelection();

    caseCards.forEach(card => {
      function selectCard() {
        // Deselect all cards
        caseCards.forEach(c => {
          c.classList.remove('selected');
          c.setAttribute('aria-checked', 'false');
        });

        // Select clicked card
        card.classList.add('selected');
        card.setAttribute('aria-checked', 'true');

        let caseId = card.getAttribute('data-case-id');
        if (caseId === 'case-010') caseId = 'case-10';
        const caseName = card.getAttribute('data-case-name');

        selectedCaseData = {
          caseId: caseId,
          caseName: caseName,
          selectedAt: new Date().toISOString()
        };

        // Preserve selected case scoped by team ID
        try {
          sessionStorage.setItem(`traceX_${activeTeamId}_selectedCase`, JSON.stringify(selectedCaseData));
        } catch (err) {
          console.warn('Session storage write error:', err);
        }

        // Enable Open Case button
        openBtn.disabled = false;

        if (hintText) {
          hintText.textContent = `SELECTED: ${caseName} // CLICK OPEN CASE TO PROCEED`;
          hintText.style.color = 'var(--color-amber-bright)';
        }
      }

      if (!card.dataset.listenerAttached) {
        card.dataset.listenerAttached = 'true';
        card.addEventListener('click', selectCard);
        card.addEventListener('keydown', function (e) {
          if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            selectCard();
          }
        });
      }
    });

    // Handle Open Case click
    if (!openBtn.dataset.listenerAttached) {
      openBtn.dataset.listenerAttached = 'true';
      openBtn.addEventListener('click', async function () {
        if (!selectedCaseData) return;

        // Persist selected case on the server before entering investigation
        try {
          openBtn.disabled = true;
          openBtn.innerHTML = `<span>[ INITIALIZING DOSSIER... ]</span>`;

          const res = await fetch('/api/teams/select-case', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              teamId: activeTeamId,
              caseId: selectedCaseData.caseId
            })
          });
          const sData = await res.json();
          if (!res.ok || !sData.success) {
            console.warn('Server case assignment warning:', sData.error);
            if (hintText) {
              hintText.textContent = sData.error || 'Failed to assign case.';
              hintText.style.color = 'var(--color-crimson-bright)';
            }
          }
        } catch (err) {
          console.warn('Network error assigning case to server:', err);
        } finally {
          openBtn.disabled = false;
          openBtn.innerHTML = `<span>[ OPEN CASE ]</span> <span aria-hidden="true">→</span>`;
        }

        // Preserve selected case in team-scoped sessionStorage
        try {
          sessionStorage.setItem(`traceX_${activeTeamId}_selectedCase`, JSON.stringify(selectedCaseData));
        } catch (err) {
          console.warn('Session storage write error:', err);
        }

        function openInvestigationWorkstation() {
          hideFullscreenRetryModal();
          if (document.getElementById('view-investigation')) {
            NavigationManager.switchView('investigation', selectedCaseData.caseId);
            try {
              history.pushState({ view: 'investigation', case: selectedCaseData.caseId }, '', `#investigation?case=${encodeURIComponent(selectedCaseData.caseId)}`);
            } catch (err) {}
          } else {
            // Fallback for standalone cases.html
            window.location.href = `${config.routes.investigation}?case=${encodeURIComponent(selectedCaseData.caseId)}`;
          }
        }

        // Check whether browser fullscreen is already active
        const isAlreadyFullscreen = Boolean(
          document.fullscreenElement || 
          document.webkitFullscreenElement || 
          document.mozFullScreenElement || 
          document.msFullscreenElement
        );

        if (isAlreadyFullscreen) {
          // If fullscreen is already active, do NOT request it again
          openInvestigationWorkstation();
        } else {
          // If fullscreen is not active, request fullscreen through Fullscreen API
          const docEl = document.documentElement;
          const requestFs = docEl.requestFullscreen || 
                            docEl.webkitRequestFullscreen || 
                            docEl.mozRequestFullScreen || 
                            docEl.msRequestFullscreen;

          if (requestFs) {
            try {
              const fsPromise = requestFs.call(docEl);
              if (fsPromise && typeof fsPromise.then === 'function') {
                fsPromise.then(() => {
                  openInvestigationWorkstation();
                }).catch(err => {
                  console.warn('Fullscreen activation was rejected or cancelled:', err);
                  showFullscreenRetryModal(selectedCaseData);
                });
              } else {
                // Browser without promise support
                setTimeout(() => {
                  const isFsConfirmed = Boolean(document.fullscreenElement || document.webkitFullscreenElement);
                  if (isFsConfirmed) {
                    openInvestigationWorkstation();
                  } else {
                    showFullscreenRetryModal(selectedCaseData);
                  }
                }, 150);
              }
            } catch (err) {
              console.warn('Fullscreen invocation error:', err);
              showFullscreenRetryModal(selectedCaseData);
            }
          } else {
            // Fullscreen API not supported
            showFullscreenRetryModal(selectedCaseData);
          }
        }
      });
    }

    // Wire Retry Fullscreen button
    const retryFsBtn = document.getElementById('btn-retry-fullscreen');
    if (retryFsBtn && !retryFsBtn.dataset.listenerAttached) {
      retryFsBtn.dataset.listenerAttached = 'true';
      retryFsBtn.addEventListener('click', function () {
        const docEl = document.documentElement;
        const requestFs = docEl.requestFullscreen || 
                          docEl.webkitRequestFullscreen || 
                          docEl.mozRequestFullScreen || 
                          docEl.msRequestFullscreen;

        let activeCase = selectedCaseData;
        if (!activeCase) {
          try {
            activeCase = JSON.parse(sessionStorage.getItem('traceX_selectedCase') || 'null');
          } catch (e) {}
        }
        if (!activeCase) {
          activeCase = { caseId: 'case-01', caseName: 'CASE 01 — STOLEN SOCIAL MEDIA ACCOUNT' };
        }

        if (requestFs) {
          try {
            const p = requestFs.call(docEl);
            if (p && typeof p.then === 'function') {
              p.then(() => {
                hideFullscreenRetryModal();
                NavigationManager.switchView('investigation', activeCase.caseId);
              }).catch(err => {
                console.warn('Retry fullscreen still rejected:', err);
                hideFullscreenRetryModal();
                NavigationManager.switchView('investigation', activeCase.caseId);
              });
            } else {
              hideFullscreenRetryModal();
              NavigationManager.switchView('investigation', activeCase.caseId);
            }
          } catch (err) {
            hideFullscreenRetryModal();
            NavigationManager.switchView('investigation', activeCase.caseId);
          }
        } else {
          hideFullscreenRetryModal();
          NavigationManager.switchView('investigation', activeCase.caseId);
        }
      });
    }

    // Wire Cancel Retry button
    const cancelRetryBtn = document.getElementById('btn-cancel-retry-fs');
    if (cancelRetryBtn && !cancelRetryBtn.dataset.listenerAttached) {
      cancelRetryBtn.dataset.listenerAttached = 'true';
      cancelRetryBtn.addEventListener('click', function () {
        hideFullscreenRetryModal();
        NavigationManager.switchView('cases');
      });
    }
  }

  function showFullscreenRetryModal(caseData) {
    const retryModal = document.getElementById('fullscreen-retry-modal');
    if (retryModal) {
      retryModal.style.display = 'flex';
    }
  }

  function hideFullscreenRetryModal() {
    const retryModal = document.getElementById('fullscreen-retry-modal');
    if (retryModal) {
      retryModal.style.display = 'none';
    }
  }

  /**
   * Initializes Home Session Presence & Persistent Fullscreen Activation
   */
  function initHomeSession() {
    try {
      const session = JSON.parse(sessionStorage.getItem('traceX_auth_session') || 'null');
      if (session && session.authenticated) {
        // Update header status and navigation button if on homepage
        const headerStatus = document.querySelector('.header-status .sys-indicator span:last-child');
        if (headerStatus) {
          headerStatus.textContent = `AUTHENTICATED // ${session.teamId}`;
        }
        const loginNavBtn = document.getElementById('btn-participant-login');
        if (loginNavBtn) {
          loginNavBtn.textContent = `TEAM: ${session.teamId}`;
          loginNavBtn.title = `Authenticated as ${session.teamName || session.teamId}`;
          loginNavBtn.href = '#cases';
        }

        // Check if fullscreen activation is pending for this authenticated session
        const needsFs = sessionStorage.getItem('traceX_pending_fullscreen') === 'true';
        const isFs = Boolean(
          document.fullscreenElement || 
          document.webkitFullscreenElement || 
          document.mozFullScreenElement || 
          document.msFullscreenElement
        );

        const fsModal = document.getElementById('fullscreen-activation-modal');
        const enterFsBtn = document.getElementById('btn-enter-fullscreen');
        const enterFsInvBtn = document.getElementById('btn-enter-fs-investigation');
        const enterFsHomeBtn = document.getElementById('btn-enter-fs-home');
        const fsDesc = document.getElementById('fs-modal-desc');

        if (needsFs && !isFs && fsModal) {
          if (fsDesc && session.teamName) {
            fsDesc.textContent = `Participant access granted for ${session.teamName} (${session.teamId}). The TRACE × X cyber crime investigation environment operates in dedicated fullscreen mode. Click below to enter fullscreen and begin your investigation.`;
          }
          fsModal.style.display = 'flex';

          function activateFs(targetView) {
            const docEl = document.documentElement;
            const requestFs = docEl.requestFullscreen || 
                              docEl.webkitRequestFullscreen || 
                              docEl.mozRequestFullScreen || 
                              docEl.msRequestFullscreen;

            sessionStorage.removeItem('traceX_pending_fullscreen');
            fsModal.style.display = 'none';

            const dest = targetView || 'cases';

            if (requestFs) {
              requestFs.call(docEl).then(() => {
                NavigationManager.switchView(dest);
                try { history.pushState({ view: dest }, '', dest === 'home' ? '#' : `#${dest}`); } catch (e) {}
              }).catch(err => {
                console.warn('Fullscreen activation was rejected:', err);
                NavigationManager.switchView(dest);
                try { history.pushState({ view: dest }, '', dest === 'home' ? '#' : `#${dest}`); } catch (e) {}
              });
            } else {
              NavigationManager.switchView(dest);
              try { history.pushState({ view: dest }, '', dest === 'home' ? '#' : `#${dest}`); } catch (e) {}
            }
          }

          // Main enter fullscreen button opens cases/investigation directly
          if (enterFsBtn && !enterFsBtn.dataset.bound) {
            enterFsBtn.dataset.bound = 'true';
            enterFsBtn.addEventListener('click', () => activateFs('cases'));
          }

          if (enterFsInvBtn && !enterFsInvBtn.dataset.bound) {
            enterFsInvBtn.dataset.bound = 'true';
            enterFsInvBtn.addEventListener('click', () => activateFs('cases'));
          }

          if (enterFsHomeBtn && !enterFsHomeBtn.dataset.bound) {
            enterFsHomeBtn.dataset.bound = 'true';
            enterFsHomeBtn.addEventListener('click', () => activateFs('home'));
          }
        }
      }
    } catch (e) {}
  }

  let investigationEventsAttached = false;
  let activeRoundTimerInterval = null;

  /**
   * Initializes the Investigation Workstation (Supports Round 1, Round 2 & Evaluation)
   */
  function initInvestigation(targetCaseId) {
    const timerDisplay = document.getElementById('round1-timer-display');
    const evidenceList = document.getElementById('evidence-records-list');
    if (!timerDisplay || !evidenceList) return; // Not on the investigation workstation page

    // Retrieve Team Credentials First
    const teamId = getActiveTeamId();

    // 1. Resolve Active Case Data
    let caseId = targetCaseId || '';
    const hashQuery = window.location.hash.includes('?') ? window.location.hash.split('?')[1] : '';
    const hashParams = new URLSearchParams(hashQuery);
    const searchParams = new URLSearchParams(window.location.search);
    const queryCaseId = searchParams.get('case') || hashParams.get('case');
    const queryRound = searchParams.get('round') || hashParams.get('round');

    if (targetCaseId) {
      caseId = targetCaseId;
    } else if (queryCaseId && window.TRACE_INVESTIGATION_CASES && window.TRACE_INVESTIGATION_CASES[queryCaseId]) {
      caseId = queryCaseId;
    } else {
      try {
        const teamStoredCase = JSON.parse(sessionStorage.getItem(`traceX_${teamId}_selectedCase`) || 'null');
        if (teamStoredCase && teamStoredCase.caseId && window.TRACE_INVESTIGATION_CASES[teamStoredCase.caseId]) {
          caseId = teamStoredCase.caseId;
        } else {
          const storedCase = JSON.parse(sessionStorage.getItem('traceX_selectedCase') || 'null');
          if (storedCase && storedCase.caseId && window.TRACE_INVESTIGATION_CASES[storedCase.caseId]) {
            caseId = storedCase.caseId;
          }
        }
      } catch (e) {
        console.warn('Case session read error:', e);
      }
    }

    if (!caseId) caseId = 'case-01';
    if (caseId === 'case-010') caseId = 'case-10';

    const casesRepo = window.TRACE_INVESTIGATION_CASES || {};
    const activeCase = casesRepo[caseId] || casesRepo['case-01'];
    if (!activeCase) {
      console.error('Investigation dataset unavailable for case:', caseId);
      return;
    }

    // 2. Storage Keys & Session State (Strictly scoped to authenticated teamId)
    const violationsStorageKey = `traceX_${teamId}_violations_${activeCase.id}`;
    const r1SubmittedKey = `traceX_${teamId}_round1_submitted_${activeCase.id}`;
    const r1SubmittedEarlyKey = `traceX_${teamId}_round1_submittedEarly_${activeCase.id}`;
    const r2SubmittedKey = `traceX_${teamId}_round2_submitted_${activeCase.id}`;
    const r2SubmittedEarlyKey = `traceX_${teamId}_round2_submittedEarly_${activeCase.id}`;
    const r2StartedKey = `traceX_${teamId}_round2_started_${activeCase.id}`;
    const activeRoundKey = `traceX_${teamId}_active_round_${activeCase.id}`;
    const evalTimerKey = `traceX_${teamId}_eval_timer_${activeCase.id}`;

    // Determine Active Round (Strict Guard: Round 2 ONLY allowed if Round 1 is officially completed)
    let isR1Submitted = sessionStorage.getItem(r1SubmittedKey) === 'true';
    let isR2Submitted = sessionStorage.getItem(r2SubmittedKey) === 'true';
    let isR2Started = sessionStorage.getItem(r2StartedKey) === 'true';

    let currentRound = 1;
    if (isR1Submitted && (queryRound === '2' || isR2Started || sessionStorage.getItem(activeRoundKey) === '2')) {
      currentRound = 2;
    } else {
      currentRound = 1;
      sessionStorage.removeItem(r2StartedKey);
      sessionStorage.setItem(activeRoundKey, '1');
    }

    // DOM Elements - General
    const hudCaseTitle = document.getElementById('hud-case-title');
    const hudCaseTag = document.getElementById('hud-case-tag');
    const hudTimerRound = document.querySelector('.hud-timer-round');
    const hudTimerCard = document.getElementById('hud-timer-card');
    const evidenceSummary = document.getElementById('evidence-case-summary');
    const evidenceCounterBadge = document.getElementById('evidence-counter-badge');

    // DOM Elements - Questionnaire
    const qCounterDisplay = document.getElementById('question-counter-display');
    const qAnsweredStatus = document.getElementById('question-answered-status');
    const qProgressFill = document.getElementById('question-progress-fill');
    const qPrefixLabel = document.getElementById('question-prefix-label');
    const qText = document.getElementById('question-text');
    const optionsStack = document.getElementById('options-stack');
    const btnPrev = document.getElementById('btn-prev-question');
    const nextActionWrapper = document.getElementById('next-action-wrapper');
    const indicatorsStrip = document.getElementById('question-indicators-strip');
    const allAnsweredBanner = document.getElementById('round-all-answered-banner');

    // DOM Elements - Modals & Waiting Screen
    const violationOverlay = document.getElementById('violation-overlay');
    const violationCounterDisplay = document.getElementById('violation-counter-display');
    const violationWarningNote = document.getElementById('violation-warning-note');
    const btnViolationReturn = document.getElementById('btn-violation-return');

    const confirmModal = document.getElementById('confirm-submit-modal');
    const confirmTitle = document.getElementById('confirm-modal-title');
    const confirmStatDisplay = document.getElementById('confirm-stat-display');
    const btnCancelSubmit = document.getElementById('btn-cancel-submit');
    const btnProceedSubmit = document.getElementById('btn-proceed-submit');

    const waitingScreen = document.getElementById('round-waiting-screen');
    const waitingTimerDisplay = document.getElementById('waiting-timer-display');
    const waitingBadgeText = document.getElementById('waiting-badge-text');
    const waitingMainHeading = document.getElementById('waiting-main-heading');
    const waitingSubPrimary = document.getElementById('waiting-subtext-primary');
    const waitingSubSecondary = document.getElementById('waiting-subtext-secondary');
    const waitingCaseTitle = document.getElementById('waiting-case-title');
    const waitingTeamId = document.getElementById('waiting-team-id');
    const waitingAnswersCount = document.getElementById('waiting-answers-count');
    const waitingNextStatus = document.getElementById('waiting-next-status');

    const completionScreen = document.getElementById('completion-screen');
    const compCaseTitle = document.getElementById('comp-case-title');
    const compTeamId = document.getElementById('comp-team-id');
    const compTimestamp = document.getElementById('comp-timestamp');
    const compAnswersCount = document.getElementById('comp-answers-count');
    const btnEnterRound2 = document.getElementById('btn-enter-round2');

    const evaluationScreen = document.getElementById('evaluation-screen');
    const evalCaseTitle = document.getElementById('eval-case-title');
    const evalTeamId = document.getElementById('eval-team-id');
    const evalR1Count = document.getElementById('eval-r1-count');
    const evalR2Count = document.getElementById('eval-r2-count');
    const evalTimerDisplay = document.getElementById('eval-timer-display');

    // Dynamic Variables for Active Round
    let currentQuestionIndex = 0;
    let roundTimerInterval = null;
    let evalTimerInterval = null;
    let activeQuestions = [];
    let activeEvidence = [];
    let savedAnswers = {};
    let answersStorageKey = '';
    let timerStorageKey = '';
    const DURATION_SECONDS = 10 * 60; // 600 seconds (10:00)

    // Option Badges
    const optionLetters = ['A', 'B', 'C', 'D'];

    // -------------------------------------------------------------------------
    // 3. Evaluation Phase Screen (5 Minutes)
    // -------------------------------------------------------------------------
    function showEvaluationScreen() {
      if (roundTimerInterval) clearInterval(roundTimerInterval);
      window.location.href = `evaluation.html?case=${encodeURIComponent(activeCase.id)}`;
    }

    // -------------------------------------------------------------------------
    // 4. Waiting Screen Mechanics (For Early Submissions)
    // -------------------------------------------------------------------------
    function isCurrentRoundSubmittedEarly() {
      const key = (currentRound === 1) ? r1SubmittedEarlyKey : r2SubmittedEarlyKey;
      return sessionStorage.getItem(key) === 'true';
    }

    function showWaitingScreen() {
      if (!waitingScreen) return;
      const answeredCount = Object.keys(savedAnswers).length;
      const totalQ = activeQuestions.length || 15;

      if (waitingBadgeText) waitingBadgeText.textContent = `ROUND ${currentRound} SUBMITTED`;
      if (waitingMainHeading) waitingMainHeading.textContent = `ROUND ${currentRound} SUBMITTED`;
      if (waitingSubPrimary) waitingSubPrimary.textContent = 'Waiting for the round to end...';
      if (waitingSubSecondary) {
        const subMsg = (currentRound === 1)
          ? 'All selected answers have been cryptographically saved and locked. In accordance with official event rules, Round 2 unlocks strictly when the countdown reaches 00:00.'
          : 'All selected answers have been cryptographically saved and locked. In accordance with official event rules, the 5-minute evaluation phase begins strictly when the countdown reaches 00:00.';
        waitingSubSecondary.textContent = subMsg;
      }

      if (waitingCaseTitle) waitingCaseTitle.textContent = activeCase.name.toUpperCase();
      if (waitingTeamId) waitingTeamId.textContent = teamId;
      if (waitingAnswersCount) waitingAnswersCount.textContent = `${answeredCount} / ${totalQ} QUESTIONS LOCKED`;
      if (waitingNextStatus) {
        waitingNextStatus.textContent = (currentRound === 1) ? 'ROUND 2 UNLOCKS AT 00:00' : 'EVALUATION UNLOCKS AT 00:00';
      }

      waitingScreen.style.display = 'flex';

      if (optionsStack) {
        optionsStack.classList.add('locked');
      }
      if (allAnsweredBanner) {
        allAnsweredBanner.style.display = 'none';
      }
    }

    const btnWaitingAdvance = document.getElementById('btn-waiting-advance-now');
    if (btnWaitingAdvance) {
      btnWaitingAdvance.addEventListener('click', () => {
        hideWaitingScreen();
        if (currentRound === 1) {
          showRound1CompletionScreen();
        } else {
          window.location.href = `evaluation.html?case=${encodeURIComponent(activeCase.id)}&early=1`;
        }
      });
    }

    function hideWaitingScreen() {
      if (waitingScreen) {
        waitingScreen.style.display = 'none';
      }
      if (optionsStack) {
        optionsStack.classList.remove('locked');
      }
    }

    function checkAllQuestionsAnsweredBanner() {
      if (!allAnsweredBanner) return;
      const totalQ = activeQuestions.length || 15;
      const answeredCount = Object.keys(savedAnswers).length;
      const earlySub = isCurrentRoundSubmittedEarly();

      if (answeredCount >= totalQ && !earlySub) {
        allAnsweredBanner.style.display = 'flex';
      } else {
        allAnsweredBanner.style.display = 'none';
      }
    }

    // -------------------------------------------------------------------------
    // 5. Round 1 Completion Screen (Unlocks strictly at 00:00)
    // -------------------------------------------------------------------------
    function showRound1CompletionScreen() {
      if (roundTimerInterval) {
        clearInterval(roundTimerInterval);
        roundTimerInterval = null;
      }
      hideWaitingScreen();
      if (confirmModal) confirmModal.style.display = 'none';
      if (violationOverlay) violationOverlay.style.display = 'none';

      let r1Answers = {};
      try {
        r1Answers = JSON.parse(sessionStorage.getItem(`traceX_${teamId}_round1_answers_${activeCase.id}`) || sessionStorage.getItem(`traceX_round1_answers_${activeCase.id}`) || '{}');
      } catch (e) {}

      let answeredCount = Object.keys(r1Answers).length;
      if (answeredCount === 0 && savedAnswers && Object.keys(savedAnswers).length > 0) {
        answeredCount = Object.keys(savedAnswers).length;
      }
      if (answeredCount === 0) {
        answeredCount = activeQuestions.length || 15;
      }

      const nowTime = new Date().toUTCString().split(' ').slice(4, 5)[0] + ' UTC';

      if (compCaseTitle) compCaseTitle.textContent = activeCase.name.toUpperCase();
      if (compTeamId) compTeamId.textContent = teamId;
      if (compTimestamp) compTimestamp.textContent = nowTime;
      if (compAnswersCount) compAnswersCount.textContent = `${answeredCount} / 15`;

      if (completionScreen) {
        completionScreen.style.display = 'flex';
      }
    }

    // Wire [ ENTER ROUND 2 ] Action — Unlocked immediately for early finishers
    if (btnEnterRound2) {
      btnEnterRound2.addEventListener('click', () => {
        // Immediate transition into Round 2 with fresh timer without waiting for remaining time
        sessionStorage.setItem(r1SubmittedKey, 'true');
        sessionStorage.setItem(r2StartedKey, 'true');
        sessionStorage.setItem(activeRoundKey, '2');
        currentRound = 2;

        if (completionScreen) {
          completionScreen.style.display = 'none';
        }

        // Initialize Round 2 Workstation immediately
        setupRound(2);
      });
    }

    // -------------------------------------------------------------------------
    // 6. Setup Active Round (Round 1 or Round 2)
    // -------------------------------------------------------------------------
    function setupRound(roundNumber) {
      currentRound = roundNumber;
      currentQuestionIndex = 0;

      // Update HUD Labels
      if (hudTimerRound) {
        hudTimerRound.textContent = `ROUND ${currentRound}`;
      }
      if (hudCaseTag) {
        hudCaseTag.textContent = `${activeCase.id.toUpperCase()} // ROUND ${currentRound}`;
      }
      if (hudCaseTitle) {
        hudCaseTitle.textContent = activeCase.name.toUpperCase();
      }

      // Configure Active Datasets (Scoped strictly to teamId)
      if (currentRound === 1) {
        activeQuestions = activeCase.questions || [];
        activeEvidence = activeCase.evidence || [];
        answersStorageKey = `traceX_${teamId}_round1_answers_${activeCase.id}`;
        timerStorageKey = `traceX_${teamId}_round1_timer_${activeCase.id}`;
      } else {
        activeQuestions = activeCase.round2Questions || activeCase.questions || [];
        activeEvidence = activeCase.round2Evidence || activeCase.evidence || [];
        answersStorageKey = `traceX_${teamId}_round2_answers_${activeCase.id}`;
        timerStorageKey = `traceX_${teamId}_round2_timer_${activeCase.id}`;
      }

      // Load Answers
      try {
        savedAnswers = JSON.parse(sessionStorage.getItem(answersStorageKey) || '{}');
      } catch (e) {
        savedAnswers = {};
      }

      // Render Left Panel Evidence
      if (evidenceSummary) {
        if (currentRound === 2) {
          evidenceSummary.textContent = `${activeCase.summary} [ROUND 2 DEEP FORENSICS: Examine deeper technical logs, session traces, and threat indicators to resolve the investigation.]`;
        } else {
          evidenceSummary.textContent = activeCase.summary;
        }
      }
      if (evidenceCounterBadge) {
        evidenceCounterBadge.textContent = `${activeEvidence.length} ARTIFACTS (ROUND ${currentRound})`;
      }

      evidenceList.innerHTML = '';
      activeEvidence.forEach(item => {
        const card = document.createElement('div');
        card.className = 'evidence-card';
        card.innerHTML = `
          <div class="evidence-meta-row">
            <span class="evidence-tag">${escapeHtml(item.tag)}</span>
            <span class="evidence-timestamp">${escapeHtml(item.time)}</span>
          </div>
          <div class="evidence-card-title">${escapeHtml(item.title)}</div>
          <div class="evidence-card-details">${escapeHtml(item.details)}</div>
        `;
        evidenceList.appendChild(card);
      });

      // Start 10-Minute Timer for Active Round (continuous countdown)
      startRoundTimer();

      // Check if this round was submitted early — allow immediate progression without waiting
      if (isCurrentRoundSubmittedEarly()) {
        if (currentRound === 1) {
          showRound1CompletionScreen();
        } else {
          window.location.href = `evaluation.html?case=${encodeURIComponent(activeCase.id)}&early=1`;
        }
      } else {
        hideWaitingScreen();
        renderQuestion(0);
        renderIndicatorsStrip();
        checkAllQuestionsAnsweredBanner();
      }
    }

    // -------------------------------------------------------------------------
    // 7. Round Timer Mechanics (10:00 Authoritative Countdown with Server Sync)
    // -------------------------------------------------------------------------
    let isEventStandby = false;
    let standbyPollInterval = null;

    async function syncTimerWithServer() {
      try {
        const res = await fetch(`/api/round/timer?round=${currentRound}&team_id=${encodeURIComponent(teamId)}&case_id=${encodeURIComponent(activeCase.id)}`);
        if (res.ok) {
          const sData = await res.json();
          // Event is always active — no standby blocking needed
          {
            isEventStandby = false;
            const standbyOverlay = document.getElementById('event-standby-overlay');
            if (standbyOverlay) standbyOverlay.style.display = 'none';

            if (standbyPollInterval) {
              clearInterval(standbyPollInterval);
              standbyPollInterval = null;
            }
            if (hudCaseTag) hudCaseTag.textContent = `${activeCase.id.toUpperCase()} // ROUND ${currentRound}`;
          }

          if (sData && sData.endTime) {
            const timerState = {
              startTime: sData.startTime,
              endTime: sData.endTime,
              duration: sData.duration,
              serverSynced: true
            };
            sessionStorage.setItem(timerStorageKey, JSON.stringify(timerState));
            if (sData.isSubmittedEarly) {
              const earlyKey = (currentRound === 1) ? r1SubmittedEarlyKey : r2SubmittedEarlyKey;
              sessionStorage.setItem(earlyKey, 'true');
              if (currentRound === 1) {
                showRound1CompletionScreen();
              } else {
                window.location.href = `evaluation.html?case=${encodeURIComponent(activeCase.id)}&early=1`;
              }
            }
            return timerState;
          }
        }
      } catch (e) {
        // Offline fallback: keep local sessionStorage timer
      }
      return null;
    }

    function startRoundTimer() {
      if (roundTimerInterval) clearInterval(roundTimerInterval);

      let timerState = null;
      try {
        timerState = JSON.parse(sessionStorage.getItem(timerStorageKey) || 'null');
      } catch (e) {}

      const now = Date.now();
      if (!timerState || !timerState.endTime || typeof timerState.endTime !== 'number') {
        timerState = {
          startTime: now,
          endTime: now + (DURATION_SECONDS * 1000),
          duration: DURATION_SECONDS
        };
        sessionStorage.setItem(timerStorageKey, JSON.stringify(timerState));
      }

      let serverChecked = false;
      // Sync with server authoritative timer
      syncTimerWithServer().then(serverState => {
        serverChecked = true;
        if (serverState && serverState.endTime) {
          timerState = serverState;
        }
      });

      function updateRoundTimer() {
        if (isEventStandby) {
          if (timerDisplay) timerDisplay.textContent = '10:00';
          if (waitingTimerDisplay) waitingTimerDisplay.textContent = '10:00';
          return;
        }

        // Wait for server state check to complete before assessing expiry
        if (!serverChecked) {
          if (timerDisplay) timerDisplay.textContent = '10:00';
          return;
        }

        const currentTime = Date.now();
        const remainingMs = Math.max(0, timerState.endTime - currentTime);
        const remainingSeconds = Math.floor(remainingMs / 1000);

        const mins = Math.floor(remainingSeconds / 60);
        const secs = remainingSeconds % 60;
        const formatted = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;

        if (timerDisplay) {
          timerDisplay.textContent = formatted;
        }

        if (waitingTimerDisplay) {
          waitingTimerDisplay.textContent = formatted;
        }

        if (hudTimerCard) {
          if (remainingSeconds <= 60 && remainingSeconds > 0) {
            hudTimerCard.classList.add('timer-critical');
          } else {
            hudTimerCard.classList.remove('timer-critical');
          }
        }

        // Official Round Expiry strictly at 00:00 when active!
        if (remainingSeconds <= 0 && !isEventStandby && serverChecked) {
          clearInterval(roundTimerInterval);
          roundTimerInterval = null;
          onOfficialRoundExpiry(currentRound);
        }
      }

      roundTimerInterval = setInterval(updateRoundTimer, 500);
      updateRoundTimer();
    }

    // -------------------------------------------------------------------------
    // 8. Official Round Expiry Transition (Triggered ONLY when Timer reaches 00:00)
    // -------------------------------------------------------------------------
    function onOfficialRoundExpiry(round) {
      if (roundTimerInterval) {
        clearInterval(roundTimerInterval);
        roundTimerInterval = null;
      }

      hideWaitingScreen();

      if (round === 1) {
        // Officially mark Round 1 completed
        sessionStorage.setItem(r1SubmittedKey, 'true');
        sessionStorage.removeItem(r1SubmittedEarlyKey);

        // Sync with backend auto-submit
        try {
          fetch('/api/round/auto-submit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              round: 1,
              teamId: teamId,
              caseId: activeCase.id,
              answers: savedAnswers
            })
          }).catch(() => {});
        } catch (e) {}

        // Show Round 1 completion screen (enabling [ ENTER ROUND 2 ])
        showRound1CompletionScreen();

      } else {
        // Officially mark Round 2 completed
        sessionStorage.setItem(r2SubmittedKey, 'true');
        sessionStorage.removeItem(r2SubmittedEarlyKey);

        // Sync with backend auto-submit
        try {
          fetch('/api/round/auto-submit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              round: 2,
              teamId: teamId,
              caseId: activeCase.id,
              answers: savedAnswers
            })
          }).catch(() => {});
        } catch (e) {}

        // Proceed to 5-minute evaluation phase
        window.location.href = `evaluation.html?case=${encodeURIComponent(activeCase.id)}`;
      }
    }

    // -------------------------------------------------------------------------
    // 9. Question Renderer & Option Selection
    // -------------------------------------------------------------------------
    function renderQuestion(index) {
      if (!activeQuestions[index]) return;
      const q = activeQuestions[index];
      const qNumber = index + 1;
      const totalQ = activeQuestions.length || 15;
      const formattedQNum = String(qNumber).padStart(2, '0');

      if (qCounterDisplay) qCounterDisplay.textContent = `QUESTION ${formattedQNum} / ${String(totalQ).padStart(2, '0')}`;
      if (qPrefixLabel) qPrefixLabel.textContent = `QUESTION ${formattedQNum}`;
      if (qText) qText.textContent = q.text;

      if (qProgressFill) {
        const pct = (qNumber / totalQ) * 100;
        qProgressFill.style.width = `${pct}%`;
      }

      const isEarlySub = isCurrentRoundSubmittedEarly();
      const isAnswered = savedAnswers[index] !== undefined;
      if (qAnsweredStatus) {
        if (isEarlySub) {
          qAnsweredStatus.textContent = `SUBMISSION LOCKED (OPTION ${optionLetters[savedAnswers[index]] || 'NONE'})`;
          qAnsweredStatus.style.color = 'var(--color-crimson-bright)';
        } else if (isAnswered) {
          qAnsweredStatus.textContent = `ANSWER RECORDED (OPTION ${optionLetters[savedAnswers[index]]})`;
          qAnsweredStatus.style.color = 'var(--color-crimson-bright)';
        } else {
          qAnsweredStatus.textContent = 'SELECT ONE ANSWER';
          qAnsweredStatus.style.color = 'var(--color-text-muted)';
        }
      }

      if (optionsStack) {
        optionsStack.innerHTML = '';
        if (isEarlySub) {
          optionsStack.classList.add('locked');
        } else {
          optionsStack.classList.remove('locked');
        }

        q.options.forEach((optText, optIdx) => {
          const optCard = document.createElement('div');
          optCard.className = 'option-card';
          optCard.setAttribute('role', 'radio');
          optCard.setAttribute('tabindex', isEarlySub ? '-1' : '0');
          optCard.setAttribute('data-option-index', optIdx);

          const isSelected = savedAnswers[index] === optIdx;
          if (isSelected) {
            optCard.classList.add('selected');
            optCard.setAttribute('aria-checked', 'true');
          } else {
            optCard.setAttribute('aria-checked', 'false');
          }

          optCard.innerHTML = `
            <div class="option-badge">${optionLetters[optIdx]}</div>
            <div class="option-label-text">${escapeHtml(optText)}</div>
          `;

          function selectThisOption() {
            if (isCurrentRoundSubmittedEarly()) {
              return; // Submissions are permanently locked
            }
            savedAnswers[index] = optIdx;
            sessionStorage.setItem(answersStorageKey, JSON.stringify(savedAnswers));

            const allCards = optionsStack.querySelectorAll('.option-card');
            allCards.forEach(c => {
              c.classList.remove('selected');
              c.setAttribute('aria-checked', 'false');
            });
            optCard.classList.add('selected');
            optCard.setAttribute('aria-checked', 'true');

            if (qAnsweredStatus) {
              qAnsweredStatus.textContent = `ANSWER RECORDED (OPTION ${optionLetters[optIdx]})`;
              qAnsweredStatus.style.color = 'var(--color-crimson-bright)';
            }

            renderIndicatorsStrip();
            checkAllQuestionsAnsweredBanner();
          }

          if (!isEarlySub) {
            optCard.addEventListener('click', selectThisOption);
            optCard.addEventListener('keydown', e => {
              if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                selectThisOption();
              }
            });
          }

          optionsStack.appendChild(optCard);
        });
      }

      if (btnPrev) {
        btnPrev.disabled = (index === 0);
      }

      if (nextActionWrapper) {
        const isLastQuestion = (index === totalQ - 1);
        if (isLastQuestion) {
          nextActionWrapper.innerHTML = `
            <button type="button" class="btn-nav-submit" id="btn-submit-round">
              <span>REVIEW &amp; SUBMIT ROUND ${currentRound}</span>
              <span aria-hidden="true">✓</span>
            </button>
          `;
          const btnSubmit = document.getElementById('btn-submit-round');
          if (btnSubmit) {
            btnSubmit.addEventListener('click', openSubmissionModal);
          }
        } else {
          nextActionWrapper.innerHTML = `
            <button type="button" class="btn-nav-next" id="btn-next-question">
              <span>NEXT QUESTION</span>
              <span aria-hidden="true">→</span>
            </button>
          `;
          const btnNext = document.getElementById('btn-next-question');
          if (btnNext) {
            btnNext.addEventListener('click', () => {
              if (currentQuestionIndex < totalQ - 1) {
                currentQuestionIndex++;
                renderQuestion(currentQuestionIndex);
                renderIndicatorsStrip();
              }
            });
          }
        }
      }

      renderIndicatorsStrip();
      checkAllQuestionsAnsweredBanner();
    }

    // Question Indicator Bullets Strip
    function renderIndicatorsStrip() {
      if (!indicatorsStrip) return;
      indicatorsStrip.innerHTML = '';
      const totalQ = activeQuestions.length || 15;

      for (let i = 0; i < totalQ; i++) {
        const bullet = document.createElement('button');
        bullet.type = 'button';
        bullet.className = 'indicator-bullet';
        bullet.textContent = String(i + 1).padStart(2, '0');
        bullet.setAttribute('aria-label', `Jump to Question ${i + 1}`);

        if (i === currentQuestionIndex) {
          bullet.classList.add('current');
        }
        if (savedAnswers[i] !== undefined) {
          bullet.classList.add('answered');
        }

        bullet.addEventListener('click', () => {
          currentQuestionIndex = i;
          renderQuestion(currentQuestionIndex);
        });

        indicatorsStrip.appendChild(bullet);
      }
    }

    // Previous Button Click
    if (btnPrev) {
      btnPrev.addEventListener('click', () => {
        if (currentQuestionIndex > 0) {
          currentQuestionIndex--;
          renderQuestion(currentQuestionIndex);
          renderIndicatorsStrip();
        }
      });
    }

    // -------------------------------------------------------------------------
    // 10. Final Submission Confirmation Modal & Early Submit Flow
    // -------------------------------------------------------------------------
    function openSubmissionModal() {
      const answeredCount = Object.keys(savedAnswers).length;
      const totalQ = activeQuestions.length || 15;
      if (confirmTitle) {
        confirmTitle.textContent = `CONFIRM ROUND ${currentRound} SUBMISSION`;
      }
      if (confirmStatDisplay) {
        confirmStatDisplay.textContent = `ANSWERED: ${answeredCount} OF ${totalQ} QUESTIONS (ROUND ${currentRound})`;
      }
      const confirmDesc = document.querySelector('.confirm-desc');
      if (confirmDesc) {
        if (currentRound === 1) {
          confirmDesc.textContent = `Are you sure you wish to submit your Round 1 investigation dossier? Once submitted, all answers are permanently locked. Since you completed early, you will advance to Round 2 immediately without waiting for the timer.`;
        } else {
          confirmDesc.textContent = `Are you sure you wish to submit your final Round 2 investigation dossier? Once submitted, your investigation is complete and you will advance to evaluation immediately so you can proceed to your next symposium competition without waiting.`;
        }
      }
      if (confirmModal) {
        confirmModal.style.display = 'flex';
      }
    }

    if (btnCancelSubmit) {
      btnCancelSubmit.addEventListener('click', () => {
        if (confirmModal) confirmModal.style.display = 'none';
      });
    }

    if (btnProceedSubmit) {
      btnProceedSubmit.addEventListener('click', () => {
        if (confirmModal) confirmModal.style.display = 'none';
        handleEarlySubmission();
      });
    }

    function handleEarlySubmission() {
      // 1. Save all selected answers to storage
      sessionStorage.setItem(answersStorageKey, JSON.stringify(savedAnswers));

      // 2. Inform server of early submission
      try {
        fetch('/api/round/submit-early', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            round: currentRound,
            teamId: teamId,
            caseId: activeCase.id,
            answers: savedAnswers
          })
        }).catch(() => {});
      } catch (e) {}

      // 3. Lock options and stop active round countdown
      if (optionsStack) {
        optionsStack.classList.add('locked');
      }
      if (allAnsweredBanner) {
        allAnsweredBanner.style.display = 'none';
      }
      if (roundTimerInterval) {
        clearInterval(roundTimerInterval);
        roundTimerInterval = null;
      }

      // 4. Advance immediately according to core logic (no remaining time waiting!)
      if (currentRound === 1) {
        // Officially mark Round 1 completed
        sessionStorage.setItem(r1SubmittedKey, 'true');
        sessionStorage.removeItem(r1SubmittedEarlyKey);

        try {
          fetch('/api/round/auto-submit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              round: 1,
              teamId: teamId,
              caseId: activeCase.id,
              answers: savedAnswers
            })
          }).catch(() => {});
        } catch (e) {}

        // Show Round 1 completion screen immediately with [ ENTER ROUND 2 ] active
        showRound1CompletionScreen();
      } else {
        // Officially mark Round 2 completed
        sessionStorage.setItem(r2SubmittedKey, 'true');
        sessionStorage.removeItem(r2SubmittedEarlyKey);

        try {
          fetch('/api/round/auto-submit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              round: 2,
              teamId: teamId,
              caseId: activeCase.id,
              answers: savedAnswers
            })
          }).catch(() => {});
        } catch (e) {}

        // Proceed to evaluation immediately with fast-track flag
        window.location.href = `evaluation.html?case=${encodeURIComponent(activeCase.id)}&early=1`;
      }
    }

    // -------------------------------------------------------------------------
    // 11. Complete Active Round (Emergency/Violation Handler)
    // -------------------------------------------------------------------------
    function completeActiveRound(reason) {
      onOfficialRoundExpiry(currentRound);
    }

    // -------------------------------------------------------------------------
    // 12. Initial State Routing
    // -------------------------------------------------------------------------
    if (isR2Submitted) {
      window.location.href = `evaluation.html?case=${encodeURIComponent(activeCase.id)}`;
      return;
    }

    // Authoritative Server State Sync: Ensure team only accesses permitted round and case
    fetch(`/api/teams/progress?team_id=${encodeURIComponent(teamId)}`)
      .then(res => res.ok ? res.json() : null)
      .then(prog => {
        if (!prog) return;
        if (prog.logicalState === 'CASE_NOT_SELECTED') {
          console.warn('[TRACE × X] Team has not selected a case yet. Redirecting to case selection.');
          NavigationManager.switchView('cases');
          return;
        }
        if (prog.caseId && (!targetCaseId || targetCaseId !== prog.caseId)) {
          if (activeCase.id !== prog.caseId) {
            console.warn(`[TRACE × X] Switching to team assigned case: ${prog.caseId}`);
            NavigationManager.switchView('investigation', prog.caseId);
            return;
          }
        }
        if (prog.round1 && prog.round1.completed) {
          sessionStorage.setItem(r1SubmittedKey, 'true');
          if (prog.round2 && prog.round2.completed) {
            sessionStorage.setItem(r2SubmittedKey, 'true');
            window.location.href = `evaluation.html?case=${encodeURIComponent(activeCase.id)}`;
            return;
          }
          if (currentRound === 1 && !isR2Started) {
            showRound1CompletionScreen();
          }
        } else {
          // Round 1 not completed on server - clear any fraudulent or stale client round 2 progression
          sessionStorage.removeItem(r1SubmittedKey);
          sessionStorage.removeItem(r2StartedKey);
          if (currentRound === 2) {
            setupRound(1);
          }
        }
      })
      .catch(() => {});

    // Setup active round through server-synchronized state
    setupRound(currentRound);

    // -------------------------------------------------------------------------
    // 11. Security System: Tab Switching, Blur & Fullscreen Violations
    // -------------------------------------------------------------------------
    let violationCount = parseInt(sessionStorage.getItem(violationsStorageKey) || '0', 10);
    let isDebouncingViolation = false;

    function handleViolationEvent(sourceType) {
      // Guard: Only monitor violations during active investigation!
      if (NavigationManager.getCurrentView() !== 'investigation') return;
      if (NavigationManager.isInternalNavigating()) return;

      // If completed all rounds, ignore
      if (sessionStorage.getItem(r2SubmittedKey) === 'true') return;
      if (isDebouncingViolation) return; // Debounce simultaneous blur & visibilitychange

      isDebouncingViolation = true;
      setTimeout(() => {
        isDebouncingViolation = false;
      }, 2000);

      violationCount++;
      sessionStorage.setItem(violationsStorageKey, violationCount.toString());

      // Log violation event to authoritative backend
      try {
        fetch('/api/violations/log', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            teamId: teamId,
            violationType: sourceType,
            violationCount: violationCount,
            actionTaken: (violationCount >= 3) ? 'AUTOMATED_DISQUALIFICATION' : `Warning ${violationCount} of 3`
          })
        }).catch(err => console.warn('Violation logging failed:', err));
      } catch (err) {}

      if (violationCount >= 3) {
        if (violationCounterDisplay) {
          violationCounterDisplay.textContent = `VIOLATION 03 / 03`;
        }
        if (violationWarningNote) {
          violationWarningNote.textContent = 'TERMINATED: Maximum allowable violations exceeded. Investigation session submitted.';
          violationWarningNote.style.color = '#FF2438';
        }
        completeActiveRound('EXCEEDED_MAX_VIOLATIONS');
        return;
      }

      if (violationCounterDisplay) {
        violationCounterDisplay.textContent = `VIOLATION 0${violationCount} / 03`;
      }
      if (violationWarningNote) {
        if (violationCount === 1) {
          violationWarningNote.textContent = 'Please return to the investigation. Warning 1 of 3 recorded.';
          violationWarningNote.style.color = 'var(--color-text-muted)';
        } else if (violationCount === 2) {
          violationWarningNote.textContent = 'CRITICAL WARNING: Next incident will automatically terminate and submit your investigation.';
          violationWarningNote.style.color = '#FF2438';
        }
      }

      if (violationOverlay) {
        violationOverlay.style.display = 'flex';
      }
    }

    if (!investigationEventsAttached) {
      investigationEventsAttached = true;

      document.addEventListener('visibilitychange', () => {
        if (document.hidden) {
          handleViolationEvent('VISIBILITY_CHANGE');
        }
      });

      window.addEventListener('blur', () => {
        handleViolationEvent('WINDOW_BLUR');
      });

      document.addEventListener('fullscreenchange', () => {
        const isFs = Boolean(
          document.fullscreenElement ||
          document.webkitFullscreenElement ||
          document.mozFullScreenElement ||
          document.msFullscreenElement
        );
        if (!isFs && sessionStorage.getItem(r2SubmittedKey) !== 'true') {
          handleViolationEvent('FULLSCREEN_EXIT');
        }
      });

      if (btnViolationReturn) {
        btnViolationReturn.addEventListener('click', () => {
          if (violationOverlay) {
            violationOverlay.style.display = 'none';
          }

          const isFs = Boolean(document.fullscreenElement);
          if (!isFs) {
            const docEl = document.documentElement;
            const requestFs = docEl.requestFullscreen ||
                              docEl.webkitRequestFullscreen ||
                              docEl.mozRequestFullScreen ||
                              docEl.msRequestFullscreen;
            if (requestFs) {
              requestFs.call(docEl).catch(() => {});
            }
          }
        });
      }

      const switchCaseBtn = document.getElementById('btn-switch-case');
      if (switchCaseBtn) {
        switchCaseBtn.addEventListener('click', (e) => {
          e.preventDefault();
          if (document.getElementById('view-case-selection')) {
            NavigationManager.switchView('cases');
          } else {
            window.location.href = config.routes.cases;
          }
        });
      }

      // -------------------------------------------------------------------------
      // 12. Distraction Restrictions (Anti-Cheating Integrity)
      // -------------------------------------------------------------------------
      document.addEventListener('contextmenu', e => {
        if (NavigationManager.getCurrentView() === 'investigation') {
          e.preventDefault();
          return false;
        }
      });

      document.addEventListener('copy', e => {
        if (NavigationManager.getCurrentView() === 'investigation') {
          e.preventDefault();
        }
      });

      document.addEventListener('cut', e => {
        if (NavigationManager.getCurrentView() === 'investigation') {
          e.preventDefault();
        }
      });

      document.addEventListener('keydown', e => {
        if (NavigationManager.getCurrentView() === 'investigation') {
          const isCtrl = e.ctrlKey || e.metaKey;
          if (isCtrl && (e.key === 'c' || e.key === 'C' || e.key === 'u' || e.key === 'U' || e.key === 'x' || e.key === 'X')) {
            e.preventDefault();
          }
          if (e.key === 'F12') {
            e.preventDefault();
          }
        }
      });
    }

    // -------------------------------------------------------------------------
    // 13. Network Connection Status Monitor
    // -------------------------------------------------------------------------
    const connBadge = document.getElementById('hud-connection-status');
    const connText = document.getElementById('conn-status-text');

    function updateNetworkStatus(online) {
      if (!connBadge || !connText) return;
      if (online) {
        connBadge.className = 'hud-conn-badge reconnected';
        connText.textContent = 'CONNECTION RESTORED';
        setTimeout(() => {
          connBadge.className = 'hud-conn-badge';
          connText.textContent = 'CONNECTION: SECURE';
        }, 2200);
      } else {
        connBadge.className = 'hud-conn-badge offline';
        connText.textContent = 'CONNECTION LOST — RECONNECTING';
      }
    }

    window.addEventListener('online', () => updateNetworkStatus(true));
    window.addEventListener('offline', () => updateNetworkStatus(false));
  }

  /**
   * Initializes the Admin Evaluation Console (Step 7 Update: 30 Questions Evaluation)
   */
  function initAdmin() {
    const caseSelect = document.getElementById('admin-case-select');
    if (!caseSelect) return; // Not on the admin page

    const casesRepo = window.TRACE_INVESTIGATION_CASES || {};
    const caseKeys = Object.keys(casesRepo);
    if (caseKeys.length === 0) return;

    // Populate Case Select dropdown with all 15 cases
    caseSelect.innerHTML = '';
    caseKeys.forEach(cid => {
      const opt = document.createElement('option');
      opt.value = cid;
      opt.textContent = `${casesRepo[cid].name}`;
      caseSelect.appendChild(opt);
    });

    // Default to active case if stored
    let selectedCaseId = 'case-01';
    try {
      const storedCase = JSON.parse(sessionStorage.getItem('traceX_selectedCase') || 'null');
      if (storedCase && storedCase.caseId && casesRepo[storedCase.caseId]) {
        selectedCaseId = storedCase.caseId;
      }
    } catch (e) {}
    caseSelect.value = selectedCaseId;

    // Team ID
    let teamId = 'TX-2026-TEAM';
    try {
      const authSession = JSON.parse(sessionStorage.getItem('traceX_auth_session') || 'null');
      if (authSession && authSession.teamId) {
        teamId = authSession.teamId;
      }
    } catch (e) {}

    const teamIdDisplay = document.getElementById('admin-team-id');
    if (teamIdDisplay) teamIdDisplay.textContent = teamId;

    const r1Stack = document.getElementById('admin-r1-questions-stack');
    const r2Stack = document.getElementById('admin-r2-questions-stack');
    const r1ScoreDisplay = document.getElementById('admin-r1-score');
    const r2ScoreDisplay = document.getElementById('admin-r2-score');
    const totalScoreDisplay = document.getElementById('admin-total-score');
    const accuracyDisplay = document.getElementById('admin-accuracy-rate');
    const btnRecalculate = document.getElementById('btn-recalculate-score');

    const optionLetters = ['A', 'B', 'C', 'D'];

    function renderAdminEvaluation() {
      const activeCid = caseSelect.value;
      const cdata = casesRepo[activeCid];
      if (!cdata) return;

      const r1Questions = cdata.questions || [];
      const r2Questions = cdata.round2Questions || [];

      // Load participant submitted answers for this case
      let r1Answers = {};
      let r2Answers = {};
      try {
        r1Answers = JSON.parse(sessionStorage.getItem(`traceX_round1_answers_${activeCid}`) || '{}');
        r2Answers = JSON.parse(sessionStorage.getItem(`traceX_round2_answers_${activeCid}`) || '{}');
      } catch (e) {}

      let violations = 0;
      try {
        violations = parseInt(sessionStorage.getItem(`traceX_violations_${activeCid}`) || '0', 10);
      } catch (e) {}

      let r1Score = 0;
      let r2Score = 0;

      // Render Question Stack Helper
      function renderStack(questions, answers, stackEl, isR2) {
        if (!stackEl) return 0;
        stackEl.innerHTML = '';
        let correctCount = 0;

        questions.forEach((q, idx) => {
          const qNum = String(idx + 1).padStart(2, '0');
          const userAns = answers[idx];
          const isAnswered = userAns !== undefined;
          const isCorrect = isAnswered && (userAns === q.answer);

          if (isCorrect) correctCount++;

          const card = document.createElement('div');
          card.className = 'admin-q-card';

          let statusBadge = '';
          if (!isAnswered) {
            statusBadge = `<span class="admin-q-status unanswered">NOT ANSWERED (0/1)</span>`;
          } else if (isCorrect) {
            statusBadge = `<span class="admin-q-status correct">✓ CORRECT (+1)</span>`;
          } else {
            statusBadge = `<span class="admin-q-status incorrect">✗ INCORRECT (0/1)</span>`;
          }

          let optionsHtml = '';
          q.options.forEach((optText, optIdx) => {
            const isKey = (optIdx === q.answer);
            const isUser = isAnswered && (userAns === optIdx);
            let optClass = 'admin-opt-item';
            if (isKey) optClass += ' key-correct';
            if (isUser && !isKey) optClass += ' user-selected';

            optionsHtml += `
              <div class="${optClass}">
                <span class="admin-opt-letter">[${optionLetters[optIdx]}]</span>
                <span>${escapeHtml(optText)}</span>
                ${isKey ? '<span style="color: #00E676; margin-left: auto; font-size: 0.72rem; font-weight: 700;">(KEY)</span>' : ''}
                ${isUser ? '<span style="color: var(--color-amber-bright); margin-left: auto; font-size: 0.72rem; font-weight: 700;">(TEAM CHOICE)</span>' : ''}
              </div>
            `;
          });

          card.innerHTML = `
            <div class="admin-q-header">
              <span class="admin-q-num">QUESTION ${qNum} / 15</span>
              ${statusBadge}
            </div>
            <div class="admin-q-text">${escapeHtml(q.text)}</div>
            <div class="admin-options-grid">
              ${optionsHtml}
            </div>
            <div class="admin-key-summary-bar">
              <span class="ans-key-tag">OFFICIAL KEY: OPTION ${optionLetters[q.answer]}</span>
              <span class="ans-user-tag">SUBMITTED: ${isAnswered ? 'OPTION ' + optionLetters[userAns] : 'NONE'}</span>
            </div>
          `;

          stackEl.appendChild(card);
        });

        return correctCount;
      }

      r1Score = renderStack(r1Questions, r1Answers, r1Stack, false);
      r2Score = renderStack(r2Questions, r2Answers, r2Stack, true);

      const totalScore = r1Score + r2Score;
      const totalQuestions = r1Questions.length + r2Questions.length; // Exactly 30
      const pct = totalQuestions > 0 ? ((totalScore / totalQuestions) * 100).toFixed(1) : 0;

      if (r1ScoreDisplay) r1ScoreDisplay.textContent = `${r1Score} / 15`;
      if (r2ScoreDisplay) r2ScoreDisplay.textContent = `${r2Score} / 15`;
      if (totalScoreDisplay) totalScoreDisplay.textContent = `${totalScore} / 30`;
      if (accuracyDisplay) accuracyDisplay.textContent = `${pct}% (${violations} VIO)`;
    }

    caseSelect.addEventListener('change', renderAdminEvaluation);
    if (btnRecalculate) btnRecalculate.addEventListener('click', renderAdminEvaluation);

    // Initial evaluation render
    renderAdminEvaluation();
  }

  /**
   * Step 8: TRACE × X Dedicated Evaluation Screen
   * Manages 5-minute authoritative countdown, 4 digital forensic stages,
   * connection telemetry, anti-cheating violation tracking, and auto-transition to results.
   */
  function initEvaluation() {
    const timerDisplay = document.getElementById('eval-countdown-display');
    if (!timerDisplay) return; // Not on evaluation.html

    const casesRepo = window.TRACE_INVESTIGATION_CASES || {};
    const urlParams = new URLSearchParams(window.location.search);
    let caseId = urlParams.get('case');

    // Participant Session
    const teamId = getActiveTeamId();

    if (!caseId || !casesRepo[caseId]) {
      try {
        const teamCase = JSON.parse(sessionStorage.getItem(`traceX_${teamId}_selectedCase`) || 'null');
        if (teamCase && teamCase.caseId && casesRepo[teamCase.caseId]) {
          caseId = teamCase.caseId;
        } else {
          const storedCase = JSON.parse(sessionStorage.getItem('traceX_selectedCase') || 'null');
          if (storedCase && storedCase.caseId && casesRepo[storedCase.caseId]) {
            caseId = storedCase.caseId;
          }
        }
      } catch (e) {}
    }

    if (!caseId || !casesRepo[caseId]) {
      caseId = 'case-01';
    }

    const activeCase = casesRepo[caseId] || { name: 'CASE 01 — STOLEN SOCIAL MEDIA ACCOUNT' };

    // Guard: Verify Round 2 is officially completed before allowing entry to Evaluation
    const isR2Submitted = sessionStorage.getItem(`traceX_${teamId}_round2_submitted_${caseId}`) === 'true' || sessionStorage.getItem(`traceX_round2_submitted_${caseId}`) === 'true';
    let r2Timer = null;
    try {
      r2Timer = JSON.parse(sessionStorage.getItem(`traceX_${teamId}_round2_timer_${caseId}`) || sessionStorage.getItem(`traceX_round2_timer_${caseId}`) || 'null');
    } catch (e) {}
    const isR2TimerDone = r2Timer && r2Timer.endTime && (Date.now() >= r2Timer.endTime);

    // Verify against authoritative server team progression
    fetch(`/api/teams/progress?team_id=${encodeURIComponent(teamId)}`)
      .then(res => res.ok ? res.json() : null)
      .then(prog => {
        if (!prog) return;
        if (prog.logicalState === 'CASE_NOT_SELECTED') {
          window.location.replace('index.html#cases');
        } else if (prog.round2 && !prog.round2.completed) {
          console.warn('Round 2 is not completed on server. Redirecting back to investigation.');
          window.location.replace(`index.html#investigation?case=${encodeURIComponent(prog.caseId || caseId)}&round=2`);
        }
      })
      .catch(() => {});

    if (!isR2Submitted && !isR2TimerDone) {
      console.warn('Round 2 is not completed yet. Redirecting back to investigation.');
      window.location.replace(`index.html#investigation?case=${encodeURIComponent(caseId)}&round=2`);
      return;
    }

    // Populate Safe Telemetry (Strict Score Privacy — NO marks, points, scores, or keys exposed)
    const caseNameEl = document.getElementById('eval-case-name');
    const teamCodeEl = document.getElementById('eval-team-code');
    const totalResponsesEl = document.getElementById('eval-total-responses');

    if (caseNameEl) caseNameEl.textContent = activeCase.name.toUpperCase();
    if (teamCodeEl) teamCodeEl.textContent = teamId;

    let r1Answers = {};
    let r2Answers = {};
    try {
      r1Answers = JSON.parse(sessionStorage.getItem(`traceX_${teamId}_round1_answers_${caseId}`) || sessionStorage.getItem(`traceX_round1_answers_${caseId}`) || '{}');
      r2Answers = JSON.parse(sessionStorage.getItem(`traceX_${teamId}_round2_answers_${caseId}`) || sessionStorage.getItem(`traceX_round2_answers_${caseId}`) || '{}');
    } catch (e) {}

    const totalAnswered = Object.keys(r1Answers).length + Object.keys(r2Answers).length;
    if (totalResponsesEl) {
      totalResponsesEl.textContent = `${totalAnswered} / 30 QUESTIONS SEALED`;
    }

    // -------------------------------------------------------------------------
    // 5-Minute Evaluation Timer Countdown (300 Seconds)
    // -------------------------------------------------------------------------
    const EVAL_DURATION_SECONDS = 5 * 60; // Exactly 300 seconds (05:00)
    const evalTimerKey = `traceX_${teamId}_eval_timer_${caseId}`;
    const evalTimerPanel = document.getElementById('eval-timer-panel');

    let evalTimerState = null;
    try {
      evalTimerState = JSON.parse(sessionStorage.getItem(evalTimerKey) || 'null');
    } catch (e) {}

    const now = Date.now();
    if (!evalTimerState || !evalTimerState.endTime || typeof evalTimerState.endTime !== 'number') {
      evalTimerState = {
        startTime: now,
        endTime: now + (EVAL_DURATION_SECONDS * 1000),
        duration: EVAL_DURATION_SECONDS
      };
      sessionStorage.setItem(evalTimerKey, JSON.stringify(evalTimerState));
    }

    // Authoritative Server Timing Sync (Browser refresh must not restart the timer)
    async function syncAuthoritativeTimer() {
      try {
        const res = await fetch(`/api/round/timer?round=eval&team_id=${encodeURIComponent(teamId)}&case_id=${encodeURIComponent(caseId)}`);
        if (res.ok) {
          const data = await res.json();
          if (typeof data.remainingSeconds === 'number') {
            const serverNow = Date.now();
            evalTimerState = {
              startTime: serverNow - ((data.durationSeconds || 300) - data.remainingSeconds) * 1000,
              endTime: serverNow + (data.remainingSeconds * 1000),
              duration: data.durationSeconds || 300
            };
            sessionStorage.setItem(evalTimerKey, JSON.stringify(evalTimerState));
            tickEvaluation();
          }
        }
      } catch (err) {
        // Continue with sessionStorage timer
      }
    }
    syncAuthoritativeTimer();

    // Stage DOM Elements
    const stageCards = [
      document.getElementById('eval-stage-1'),
      document.getElementById('eval-stage-2'),
      document.getElementById('eval-stage-3'),
      document.getElementById('eval-stage-4')
    ];
    const stagePills = [
      document.getElementById('stage-pill-1'),
      document.getElementById('stage-pill-2'),
      document.getElementById('stage-pill-3'),
      document.getElementById('stage-pill-4')
    ];
    const currentStageNumEl = document.getElementById('current-stage-num');

    function updateStagesProgress(elapsedSec) {
      // Stage 1: Securing Submissions (0 - 60s)
      // Stage 2: Validating Responses (60 - 150s)
      // Stage 3: Processing Evaluation (150 - 240s)
      // Stage 4: Finalizing Results (240 - 300s)
      let activeStageIdx = 0;

      if (elapsedSec < 60) {
        activeStageIdx = 0;
      } else if (elapsedSec < 150) {
        activeStageIdx = 1;
      } else if (elapsedSec < 240) {
        activeStageIdx = 2;
      } else {
        activeStageIdx = 3;
      }

      if (currentStageNumEl) {
        currentStageNumEl.textContent = `0${activeStageIdx + 1}`;
      }

      stageCards.forEach((card, idx) => {
        if (!card) return;
        const pill = stagePills[idx];
        card.classList.remove('completed', 'active');
        if (pill) pill.classList.remove('completed', 'active', 'pending');

        if (idx < activeStageIdx) {
          card.classList.add('completed');
          if (pill) {
            pill.classList.add('completed');
            pill.textContent = 'COMPLETED';
          }
        } else if (idx === activeStageIdx) {
          card.classList.add('active');
          if (pill) {
            pill.classList.add('active');
            pill.textContent = 'IN PROGRESS';
          }
        } else {
          if (pill) {
            pill.classList.add('pending');
            pill.textContent = 'QUEUED';
          }
        }
      });
    }

    let evalInterval = null;

    function tickEvaluation() {
      const currentTime = Date.now();
      const remainingMs = Math.max(0, evalTimerState.endTime - currentTime);
      const remainingSec = Math.floor(remainingMs / 1000);
      const elapsedSec = Math.min(EVAL_DURATION_SECONDS, Math.max(0, Math.floor((currentTime - evalTimerState.startTime) / 1000)));

      const mins = Math.floor(remainingSec / 60);
      const secs = remainingSec % 60;
      const formatted = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;

      if (timerDisplay) {
        timerDisplay.textContent = formatted;
      }

      if (evalTimerPanel) {
        if (remainingSec <= 30 && remainingSec > 0) {
          evalTimerPanel.classList.add('timer-critical');
        } else {
          evalTimerPanel.classList.remove('timer-critical');
        }
      }

      updateStagesProgress(elapsedSec);

      // Auto Transition at 00:00 to Final Results after verifying processing
      if (remainingSec <= 0) {
        finishEvaluationAndProceed();
      }
    }

    function finishEvaluationAndProceed() {
      if (evalInterval) {
        clearInterval(evalInterval);
        evalInterval = null;
      }
      
      // Mark all stages completed
      stageCards.forEach((c, i) => {
        if (c) {
          c.classList.remove('active');
          c.classList.add('completed');
        }
        if (stagePills[i]) {
          stagePills[i].className = 'stage-status-pill completed';
          stagePills[i].textContent = 'COMPLETED';
        }
      });
      if (currentStageNumEl) currentStageNumEl.textContent = '04';
      if (timerDisplay) timerDisplay.textContent = '00:00';
      const sub = document.getElementById('eval-countdown-sub');
      if (sub) sub.textContent = 'EVALUATION SEALED // ADVANCING TO FINAL CLEARANCE...';

      // Record completion and proceed to results
      sessionStorage.setItem(`traceX_eval_completed_${caseId}`, 'true');
      fetch(`/api/participant/result?team_id=${encodeURIComponent(teamId)}`)
        .then(() => {
          setTimeout(() => {
            window.location.href = `results.html?case=${encodeURIComponent(caseId)}&early=1`;
          }, 600);
        })
        .catch(() => {
          setTimeout(() => {
            window.location.href = `results.html?case=${encodeURIComponent(caseId)}&early=1`;
          }, 600);
        });
    }

    // Wire button to complete immediately without waiting
    const btnFastComplete = document.getElementById('btn-fast-complete-eval');
    if (btnFastComplete) {
      btnFastComplete.addEventListener('click', () => {
        finishEvaluationAndProceed();
      });
    }

    // If candidate finished early, run a rapid 2-second visual evaluation progression then proceed
    const isEarlySub = urlParams.get('early') === '1' || urlParams.get('early') === 'true' || sessionStorage.getItem(`traceX_round2_submitted_${caseId}`) === 'true';
    if (isEarlySub) {
      let rapidStep = 0;
      evalInterval = setInterval(() => {
        rapidStep++;
        updateStagesProgress(rapidStep * 75);
        if (timerDisplay) {
          const rem = Math.max(0, 4 - rapidStep);
          timerDisplay.textContent = `00:0${rem}`;
        }
        if (rapidStep >= 4) {
          clearInterval(evalInterval);
          evalInterval = null;
          finishEvaluationAndProceed();
        }
      }, 500);
    } else {
      evalInterval = setInterval(tickEvaluation, 500);
      tickEvaluation();
    }

    // -------------------------------------------------------------------------
    // Network Connection Telemetry
    // -------------------------------------------------------------------------
    const connBadge = document.getElementById('eval-connection-status');
    const connText = document.getElementById('eval-conn-status-text');

    function updateEvalConnStatus(online) {
      if (!connBadge || !connText) return;
      if (online) {
        connBadge.className = 'hud-conn-badge reconnected';
        connText.textContent = 'CONNECTION RESTORED';
        setTimeout(() => {
          connBadge.className = 'hud-conn-badge';
          connText.textContent = 'CONNECTION STATUS: SECURE';
        }, 2200);
      } else {
        connBadge.className = 'hud-conn-badge offline';
        connText.textContent = 'CONNECTION LOST — RECONNECTING';
      }
    }

    window.addEventListener('online', () => updateEvalConnStatus(true));
    window.addEventListener('offline', () => updateEvalConnStatus(false));

    // -------------------------------------------------------------------------
    // Reused Fullscreen & Security Violation Monitoring
    // -------------------------------------------------------------------------
    const violationsStorageKey = `traceX_violations_${caseId}`;
    let violationCount = parseInt(sessionStorage.getItem(violationsStorageKey) || '0', 10);
    let isDebouncingViolation = false;

    const violationOverlay = document.getElementById('violation-overlay');
    const violationCounterDisplay = document.getElementById('violation-counter-display');
    const violationWarningNote = document.getElementById('violation-warning-note');
    const btnViolationReturn = document.getElementById('btn-violation-return');

    function handleEvalViolation(sourceType) {
      if (sessionStorage.getItem(`traceX_eval_completed_${caseId}`) === 'true') return;
      if (isDebouncingViolation) return;

      isDebouncingViolation = true;
      setTimeout(() => {
        isDebouncingViolation = false;
      }, 2000);

      violationCount++;
      sessionStorage.setItem(violationsStorageKey, violationCount.toString());

      if (violationCounterDisplay) {
        violationCounterDisplay.textContent = `VIOLATION 0${violationCount} / 03`;
      }
      if (violationWarningNote) {
        if (violationCount === 1) {
          violationWarningNote.textContent = 'Warning 1 of 3: Incident recorded. Return to evaluation immediately.';
        } else if (violationCount === 2) {
          violationWarningNote.textContent = 'CRITICAL WARNING: Next incident will be flagged to CSE evaluation faculty.';
          violationWarningNote.style.color = '#FF2438';
        } else {
          violationWarningNote.textContent = 'Evaluation integrity log locked with multiple violation incidents.';
        }
      }

      if (violationOverlay) {
        violationOverlay.style.display = 'flex';
      }
    }

    document.addEventListener('visibilitychange', () => {
      if (document.hidden) handleEvalViolation('VISIBILITY_CHANGE');
    });

    window.addEventListener('blur', () => {
      handleEvalViolation('WINDOW_BLUR');
    });

    document.addEventListener('fullscreenchange', () => {
      const isFs = Boolean(
        document.fullscreenElement ||
        document.webkitFullscreenElement ||
        document.mozFullScreenElement ||
        document.msFullscreenElement
      );
      if (!isFs && sessionStorage.getItem(`traceX_eval_completed_${caseId}`) !== 'true') {
        handleEvalViolation('FULLSCREEN_EXIT');
      }
    });

    if (btnViolationReturn) {
      btnViolationReturn.addEventListener('click', () => {
        if (violationOverlay) violationOverlay.style.display = 'none';
        const isFs = Boolean(document.fullscreenElement);
        if (!isFs) {
          const docEl = document.documentElement;
          const requestFs = docEl.requestFullscreen ||
                            docEl.webkitRequestFullscreen ||
                            docEl.mozRequestFullScreen ||
                            docEl.msRequestFullscreen;
          if (requestFs) {
            requestFs.call(docEl).catch(() => {});
          }
        }
      });
    }
  }

  /**
   * Initializes Results Standby Page (results.html)
   */
  function initResults() {
    const resCaseName = document.getElementById('results-case-name');
    if (!resCaseName) return; // Not on results.html

    const casesRepo = window.TRACE_INVESTIGATION_CASES || {};
    const urlParams = new URLSearchParams(window.location.search);
    const teamId = getActiveTeamId();
    let caseId = urlParams.get('case') || urlParams.get('caseId') || '';

    if (!caseId || !casesRepo[caseId]) {
      try {
        const teamCase = JSON.parse(sessionStorage.getItem(`traceX_${teamId}_selectedCase`) || 'null');
        if (teamCase && teamCase.caseId && casesRepo[teamCase.caseId]) {
          caseId = teamCase.caseId;
        } else {
          const storedCase = JSON.parse(sessionStorage.getItem('traceX_selectedCase') || 'null');
          if (storedCase && storedCase.caseId && casesRepo[storedCase.caseId]) {
            caseId = storedCase.caseId;
          }
        }
      } catch (e) {}
    }

    if (!caseId || !casesRepo[caseId]) {
      caseId = 'case-01';
    }

    const activeCase = casesRepo[caseId] || { name: 'CASE 01 — STOLEN SOCIAL MEDIA ACCOUNT' };
    resCaseName.textContent = activeCase.name.toUpperCase();

    const resTeamId = document.getElementById('results-team-id');
    if (resTeamId) resTeamId.textContent = teamId;

    // Check Publication Status (Strict Score Privacy — NEVER expose marks, scores or answer keys)
    const mainHeading = document.getElementById('results-main-heading');
    const introSub = document.getElementById('results-intro-sub');
    const statusBadge = document.getElementById('results-status-badge');
    const statusNotice = document.getElementById('results-status-notice');

    async function checkPublication() {
      try {
        let token = '';
        try {
          const auth = JSON.parse(sessionStorage.getItem('traceX_auth_session') || '{}');
          token = auth.token || '';
        } catch (e) {}

        const headers = {};
        if (token) headers['Authorization'] = `Bearer ${token}`;

        const res = await fetch(`/api/participant/result?team_id=${encodeURIComponent(teamId)}`, { headers });
        if (res.ok) {
          const data = await res.json();
          if (data && data.isPublished) {
            const finalStat = data.status || 'QUALIFIED';
            if (mainHeading) mainHeading.textContent = 'FINAL RESULTS';
            if (introSub) introSub.innerHTML = `<strong>OFFICIAL STANDING: ${escapeHtml(finalStat)}</strong><br>Your investigation dossier has been officially evaluated and confirmed.`;
            if (statusBadge) {
              statusBadge.textContent = finalStat;
              statusBadge.className = (finalStat === 'QUALIFIED') ? 'status-pill badge-qualified' : 'status-pill badge-not-qualified';
            }
            if (statusNotice) {
              statusNotice.textContent = `OFFICIAL NOTIFICATION: Your team has been designated as ${finalStat} for the TRACE × X Cyber Crime Investigation. Further instructions will be provided by the CSE event coordination team.`;
            }
          } else {
            if (mainHeading) mainHeading.textContent = 'INVESTIGATION COMPLETE';
            if (introSub) introSub.innerHTML = '<strong>RESULTS UNDER REVIEW</strong><br>Your investigation has been submitted successfully. Final results will be available after the organizers publish them.';
            if (statusBadge) {
              statusBadge.textContent = 'RESULTS UNDER REVIEW';
              statusBadge.className = 'status-pill badge-registered';
            }
            if (statusNotice) {
              statusNotice.textContent = 'INVESTIGATION COMPLETE // RESULTS UNDER REVIEW: Your investigation has been submitted successfully. Final results will be available after the organizers publish them.';
            }
          }
        }
      } catch (err) {
        if (statusBadge) {
          statusBadge.textContent = 'RESULTS UNDER REVIEW';
          statusBadge.className = 'status-pill badge-registered';
        }
      }
    }

    // Wire [ EXIT & PROCEED TO NEXT EVENT ] Action
    const btnProceedOther = document.getElementById('btn-proceed-other-event') || document.getElementById('btn-exit-to-events');
    if (btnProceedOther) {
      btnProceedOther.addEventListener('click', () => {
        try {
          fetch('/api/participant/exit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ teamId: teamId })
          }).catch(() => {});
        } catch (e) {}

        try {
          sessionStorage.removeItem('traceX_auth_session');
          sessionStorage.removeItem('traceX_selectedCase');
        } catch (e) {}

        alert('Investigation dossier successfully locked. You are cleared to proceed to your next symposium competition!');
        window.location.href = 'index.html?cleared=1';
      });
    }

    checkPublication();
  }

  /**
   * 19. TRACE × X DUAL-SLASH CINEMATIC INTRO — EXACT 6-STEP STORYBOARD
   * Exact 10.0-Second Opening Sequence:
   * - Step 1 (0.0s–0.8s): Black Screen (pure black, zero elements)
   * - Step 2 (0.8s–2.0s): Dual Slash (two sharp crimson-red metallic slashes collide at center)
   * - Step 3 (2.0s–3.7s): Exact Screen-Crack Effect (central impact flash, formed X, radiating branching cracks)
   * - Step 4 (3.7s–5.2s): Fullscreen Digital Display Reveal (entire browser viewport display, edge lighting, scanlines)
   * - Step 5 (5.2s–9.0s): Fullscreen Welcome Title ("WELCOME TO TRACE × X" across full screen)
   * - Step 6 (9.0s–10.0s): Final hold; automatic smooth transition to homepage at exactly 10.0s
   */
  function initCinematicIntro() {
    const overlay = document.getElementById('cinematic-intro-overlay');
    if (!overlay) return;

    // Support query parameters for manual replay/testing (?intro=1, ?replay=1, or ?t=4.5)
    const urlParams = new URLSearchParams(window.location.search);
    const forceReplay = urlParams.get('intro') === '1' || urlParams.get('replay') === '1' || urlParams.has('t');

    if (forceReplay) {
      try {
        sessionStorage.removeItem('traceX_intro_completed');
      } catch (e) {}
      document.documentElement.classList.remove('intro-bypassed');
    }

    // Check if intro has already been viewed in the current browser-tab session
    let hasSeenIntro = false;
    try {
      hasSeenIntro = sessionStorage.getItem('traceX_intro_completed') === 'true';
    } catch (e) {}

    if (hasSeenIntro && !forceReplay) {
      overlay.style.display = 'none';
      overlay.setAttribute('aria-hidden', 'true');
      return;
    }

    // Lock page scroll during the 10-second cinematic intro
    document.body.classList.add('intro-active');

    // Time-freeze mode for visual verification & screenshotting: e.g. ?t=1.4, ?t=2.5, ?t=4.2, ?t=6.5, ?t=9.5
    if (urlParams.has('t')) {
      const tSec = parseFloat(urlParams.get('t'));
      if (!isNaN(tSec)) {
        const animatedEls = overlay.querySelectorAll(
          '.intro-stage-container, .slash-blade, .slash-flare, .impact-flash, .impact-star-flare, .impact-x-energy, .crack-ray, .crack-sub, .crack-core, .crack-core-ring, .crack-shard, .intro-fullscreen-display, .display-edge-lighting, .display-scanline-sheen, .display-ambient-core, .intro-welcome-group, .intro-welcome-sub, .intro-welcome-heading'
        );
        animatedEls.forEach(el => {
          el.style.animationDelay = `-${tSec}s`;
          el.style.animationPlayState = 'paused';
        });
        return; // Retain paused state for verification
      }
    }

    let isFinished = false;
    let sequenceTimer = null;

    function completeIntro(instant = false) {
      if (isFinished) return;
      isFinished = true;
      if (sequenceTimer) {
        clearTimeout(sequenceTimer);
        sequenceTimer = null;
      }

      try {
        sessionStorage.setItem('traceX_intro_completed', 'true');
      } catch (e) {}
      document.body.classList.remove('intro-active');
      document.documentElement.classList.remove('intro-active');

      if (instant) {
        overlay.style.display = 'none';
        overlay.setAttribute('aria-hidden', 'true');
      } else {
        overlay.classList.add('fade-out');
        setTimeout(() => {
          overlay.style.display = 'none';
          overlay.setAttribute('aria-hidden', 'true');
        }, 850);
      }
    }

    // Natural Animation Completion Handler on Welcome Title
    const welcomeGroup = document.getElementById('intro-welcome-group') || document.getElementById('intro-welcome-heading');
    if (welcomeGroup) {
      welcomeGroup.addEventListener('animationend', () => {
        completeIntro(false);
      });
    }

    // Exact 10.0-Second Sequence Transition (Guaranteed fallback timer at exactly 10,000ms)
    sequenceTimer = setTimeout(() => {
      completeIntro(false);
    }, 10000);
  }

  /**
   * Core initialization entry point
   */
  function init() {
    initCinematicIntro();
    initRegistration();
    initLogin();
    initCases();
    initHomeSession();
    initInvestigation();
    initEvaluation();
    initResults();
    initAdmin();

    // Check URL hash or initial route on unified pages (e.g. index.html)
    if (document.getElementById('view-homepage')) {
      const hash = window.location.hash;
      if (hash.startsWith('#cases')) {
        NavigationManager.switchView('cases');
      } else if (hash.startsWith('#investigation')) {
        const queryCase = new URLSearchParams(hash.split('?')[1] || '').get('case');
        NavigationManager.switchView('investigation', queryCase);
      } else {
        NavigationManager.switchView('home');
      }

      window.addEventListener('popstate', function () {
        const h = window.location.hash;
        if (h.startsWith('#cases')) {
          NavigationManager.switchView('cases');
        } else if (h.startsWith('#investigation')) {
          const qCase = new URLSearchParams(h.split('?')[1] || '').get('case');
          NavigationManager.switchView('investigation', qCase);
        } else {
          NavigationManager.switchView('home');
        }
      });
    }

    console.info(`[TRACE × X] Application Architecture Ready. Module: ${config.version}`);
  }

  return {
    init: init,
    NavigationManager: NavigationManager,
    getConfig: function () {
      return Object.freeze({ ...config });
    }
  };
})();

// DOM Ready Hook
document.addEventListener('DOMContentLoaded', function () {
  TraceApp.init();
});


