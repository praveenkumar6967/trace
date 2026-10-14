# scratch/case_data_batch2.py
# Complete, detailed questions and evidence for Case 06 to Case 10

BATCH_2 = {
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
            # Round 1
            {
                "text": "What was the student's compromised password revealed in the breach database?",
                "options": ["College2024!", "admin123", "password@123", "Secret99#"],
                "answer": 0,
                "explanation": "Evidence 1 clearly states the student's password was 'College2024!'."
            },
            {
                "text": "What bad security habit made the student vulnerable across multiple websites?",
                "options": [
                    "Using the exact same password across university email, portal, and social accounts",
                    "Writing passwords in a locked personal diary",
                    "Changing passwords every two weeks",
                    "Using passwords that contain special characters"
                ],
                "answer": 0,
                "explanation": "Evidence 2 states the student used the identical password across multiple platforms without variation."
            },
            {
                "text": "What type of website originally leaked the student's password in an old breach?",
                "options": ["A third-party gaming website", "The official college website", "A government tax portal", "A local hospital website"],
                "answer": 0,
                "explanation": "Evidence 1 specifies the credentials were found in an old third-party gaming site database breach."
            },
            {
                "text": "At what time was the automated suspicious login recorded in the access log?",
                "options": ["04:00 AM", "12:00 PM", "08:30 PM", "06:15 AM"],
                "answer": 0,
                "explanation": "Evidence 3 indicates the account was accessed at 04:00 AM."
            },
            {
                "text": "What hashing algorithm was used by the compromised gaming website?",
                "options": ["Unsalted MD5", "Bcrypt", "Argon2id", "PBKDF2 with SHA-256"],
                "answer": 0,
                "explanation": "Evidence 4 notes the gaming site used legacy unsalted MD5 hashes."
            },
            {
                "text": "Why are unsalted MD5 hashes considered insecure for password storage?",
                "options": [
                    "They can be reversed in seconds using precomputed rainbow tables",
                    "They can only store four-digit numbers",
                    "They automatically email passwords to the public",
                    "They require floppy disks to function"
                ],
                "answer": 0,
                "explanation": "Unsalted MD5 lacks cryptographic work factor and salt, making it trivial to reverse via rainbow tables."
            },
            {
                "text": "What IP address initiated the unauthorized access at 04:00 AM?",
                "options": ["185.220.101.9", "127.0.0.1", "192.168.0.1", "10.10.10.10"],
                "answer": 0,
                "explanation": "Evidence 3 identifies the automated stuffing tool IP as 185.220.101.9."
            },
            {
                "text": "What is the student's email address listed in the incident records?",
                "options": ["vikram.k@college.edu", "student123@gmail.com", "admin@college.edu", "test@yahoo.com"],
                "answer": 0,
                "explanation": "Evidence 1 states the student's email was 'vikram.k@college.edu'."
            },
            {
                "text": "What technique did attackers use to test breached credentials against multiple sites?",
                "options": ["Credential Stuffing", "Phishing email", "Physical lock picking", "DNS Poisoning"],
                "answer": 0,
                "explanation": "Evidence 3 specifically references an automated credential stuffing tool."
            },
            {
                "text": "What tool helps users generate and safely store unique passwords for every site?",
                "options": ["A password manager", "A spreadsheet on the desktop", "A text document on a USB drive", "Sticky notes on the monitor"],
                "answer": 0,
                "explanation": "Password managers store and generate strong, unique passwords for every account."
            },
            {
                "text": "Why should users never reuse the same password on gaming sites and college portals?",
                "options": [
                    "If the gaming site is hacked, attackers will immediately test the password on the college portal",
                    "Gaming sites charge extra money for college passwords",
                    "Browsers do not allow college passwords on games",
                    "Gaming passwords can only be typed on weekends"
                ],
                "answer": 0,
                "explanation": "Password reuse allows a breach on an insecure hobby site to compromise critical academic and financial accounts."
            },
            {
                "text": "What security mechanism alerts users whenever an unfamiliar IP logs into their account?",
                "options": ["Login notification alerts", "Screen brightness dimming", "Volume increase", "Mouse cursor changing color"],
                "answer": 0,
                "explanation": "Security alert emails or push notifications notify users when logins occur from unrecognized locations."
            },
            {
                "text": "What should the student do first upon discovering their password was breached?",
                "options": [
                    "Change the password immediately on all accounts where it was used and enable 2FA",
                    "Close the browser and hope for the best",
                    "Delete all games from their computer",
                    "Share the breached password with classmates"
                ],
                "answer": 0,
                "explanation": "Immediate password resets across all shared accounts combined with 2FA stops ongoing unauthorized access."
            },
            # Tricky Q14
            {
                "text": "Why was the 04:00 AM login time an immediate indicator of automated compromise?",
                "options": [
                    "It occurred while the victim was offline and asleep, matching automated script scheduling",
                    "Servers are turned off at 04:00 AM every night",
                    "Internet cables do not transmit data at night",
                    "College accounts are programmed to delete themselves at 04:00 AM"
                ],
                "answer": 0,
                "explanation": "Adversary bots frequently run overnight when targets are asleep and unlikely to notice incoming alert notifications."
            },
            # Tricky Q15
            {
                "text": "What is the primary difference between a 'password leak' and a 'phishing attack'?",
                "options": [
                    "In a password leak, data is stolen from a breached server database; in phishing, the victim is tricked into typing credentials",
                    "A password leak only happens on Apple phones",
                    "Phishing requires stealing the physical computer",
                    "Password leaks only affect bank accounts"
                ],
                "answer": 0,
                "explanation": "Leaks originate from compromised backend service databases, while phishing tricks the end user directly."
            }
        ],
        "round2Questions": [
            # Round 2
            {
                "text": "In which country was the commercial VPN exit node located?",
                "options": ["Romania", "United States", "India", "Singapore"],
                "answer": 0,
                "explanation": "Evidence 1 states the session was routed through a commercial VPN exit node in Romania."
            },
            {
                "text": "What email address did the attacker configure to receive forwarded reset emails?",
                "options": ["drop_box_rec@proton.me", "shadow_relay_99@proton.me", "admin@college.edu", "backup@gmail.com"],
                "answer": 0,
                "explanation": "Evidence 2 identifies the silent forwarding address as 'drop_box_rec@proton.me'."
            },
            {
                "text": "What internal academic data was exfiltrated from the university portal?",
                "options": ["Internal student transcripts for the entire semester batch", "Faculty salary slips", "Library book receipts", "Hostel meal menus"],
                "answer": 0,
                "explanation": "Evidence 3 records: 'Downloaded internal student transcripts for the entire semester batch'."
            },
            {
                "text": "What was the title of the darknet combo list package containing the university credentials?",
                "options": ["Edu_Packs_2026", "College_Leaks_v1", "Student_Dumps_India", "Hack_Batch_99"],
                "answer": 0,
                "explanation": "Evidence 4 states credentials were packaged into a combo list titled 'Edu_Packs_2026'."
            },
            {
                "text": "Why did the attacker configure a rule to immediately delete incoming security alerts?",
                "options": [
                    "To prevent the legitimate student from noticing warning emails and resetting the password",
                    "To save storage space on the university server",
                    "To test whether the email server was responsive",
                    "Because security alerts are considered spam by default"
                ],
                "answer": 0,
                "explanation": "Deleting incoming alerts keeps the victim unaware of the intrusion, prolonging attacker dwell time."
            },
            {
                "text": "What is a 'credential combo list' in cybercrime terminology?",
                "options": [
                    "A curated text file of leaked email-and-password pairs compiled for automated stuffing attacks",
                    "A list of software license keys for gaming consoles",
                    "A directory of college professors and phone numbers",
                    "A list of verified antivirus programs"
                ],
                "answer": 0,
                "explanation": "Combo lists pair usernames and passwords from breaches to feed into automated credential stuffing engines."
            },
            {
                "text": "What cryptographic concept is 'salt' in modern password hashing algorithms?",
                "options": [
                    "A unique random string appended to each password before hashing to defeat rainbow tables",
                    "A physical substance used to clean server memory chips",
                    "An encryption key shared with all users",
                    "A password that can only contain letters"
                ],
                "answer": 0,
                "explanation": "Cryptographic salting guarantees that identical passwords produce completely different hashes, thwarting precomputed lookups."
            },
            {
                "text": "Why do cybercriminals route attacks through commercial VPN exit nodes?",
                "options": [
                    "To hide their true originating IP and bypass geolocation-based IP blocklists",
                    "To increase their download speed by 500%",
                    "Because universities only accept traffic from VPNs",
                    "To automatically crack passwords"
                ],
                "answer": 0,
                "explanation": "VPNs mask the genuine origin IP address, confounding attribution and basic geo-fencing controls."
            },
            # Medium-Hard Q9-Q13
            {
                "text": "How does credential stuffing differ from a standard dictionary brute force attack?",
                "options": [
                    "Stuffing tests known valid username-password pairs from breaches across other services; dictionary attacks guess random words",
                    "Stuffing only works on Wi-Fi networks",
                    "Dictionary attacks require stealing physical hard drives",
                    "Stuffing cannot be detected by server logs"
                ],
                "answer": 0,
                "explanation": "Credential stuffing exploits the high likelihood of password reuse by replaying credentials harvested from past breaches."
            },
            {
                "text": "What defensive control would have stopped the attacker at 04:02 UTC even with the valid password?",
                "options": [
                    "Enforced Multi-Factor Authentication (MFA) requiring an authenticator app code",
                    "Making the username longer",
                    "Changing the color of the login button to blue",
                    "Disabling CSS stylesheets on the login page"
                ],
                "answer": 0,
                "explanation": "MFA requires an out-of-band proof of identity, preventing access even when valid passwords are submitted."
            },
            {
                "text": "Why should email mailbox forwarding rules be audited regularly by enterprise security teams?",
                "options": [
                    "Attackers frequently establish stealth forwarding rules to maintain covert surveillance on victim correspondence",
                    "Forwarding rules cause email servers to run out of electricity",
                    "Forwarding rules are not supported in modern email clients",
                    "They prevent users from sending attachments"
                ],
                "answer": 0,
                "explanation": "Adversaries abuse hidden forwarding rules to persistently monitor victim inboxes and harvest OTPs."
            },
            {
                "text": "What forensic artifact confirms lateral movement within the university environment?",
                "options": [
                    "Using the single email compromise to access and dump the university grade database",
                    "The student checking their timetable on a phone",
                    "The campus server rebooting for a scheduled update",
                    "The student downloading a class lecture PDF"
                ],
                "answer": 0,
                "explanation": "Lateral movement occurs when an attacker uses initial access in one system to pivot into deeper internal databases."
            },
            {
                "text": "How can website administrators protect their users against credential stuffing attacks?",
                "options": [
                    "Implement CAPTCHAs, rate limiting per IP/account, and check passwords against breach APIs (like HaveIBeenPwned)",
                    "Disable the login page during daytime hours",
                    "Allow unlimited password attempts to be user-friendly",
                    "Display the full password on the screen"
                ],
                "answer": 0,
                "explanation": "Rate limiting, CAPTCHAs, and breach database checks effectively disrupt automated stuffing bots."
            },
            # Challenging Q14-Q15
            {
                "text": "Reconstructing the adversary timeline, what was the sequential chain of actions performed by the attacker?",
                "options": [
                    "Harvest breached combo list -> VPN login at 04:02 -> Create silent forwarding rule -> Dump batch transcripts -> Package credentials for dark web resale",
                    "Dump transcripts -> Harvest combo list -> Package on dark web -> Create forwarding rule",
                    "Create forwarding rule -> Package on dark web -> Harvest combo list -> VPN login",
                    "Package on dark web -> Dump transcripts -> VPN login -> Create forwarding rule"
                ],
                "answer": 0,
                "explanation": "The timeline shows credentials acquired from breach, tested via VPN, persistence established, data dumped, and resold."
            },
            {
                "text": "What is the primary corporate lesson for the university IT administration regarding student identity governance?",
                "options": [
                    "Mandatory MFA on all student portals, continuous credential compromise monitoring, and strict mailbox rule auditing",
                    "Banning all students from playing video games",
                    "Instructing students never to access email after 10 PM",
                    "Only permitting email access from physical desktop labs on campus"
                ],
                "answer": 0,
                "explanation": "Modern identity governance requires multi-factor authentication, breach intelligence integration, and behavioral anomaly audits."
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
            # Round 1
            {
                "text": "What salary was promised to the student for only 2 hours of daily data entry work?",
                "options": ["₹80,000/month", "₹5,000/month", "₹1,000/month", "₹10,000/month"],
                "answer": 0,
                "explanation": "Evidence 1 states the email offered ₹80,000/month for 2 hours of daily work."
            },
            {
                "text": "How much 'refundable security deposit' did the scammer demand for courier shipment?",
                "options": ["₹3,000", "₹500", "₹50,000", "₹100"],
                "answer": 0,
                "explanation": "Evidence 2 states the recruiter demanded a deposit of ₹3,000."
            },
            {
                "text": "What equipment did the scammer falsely promise to courier to the student?",
                "options": ["A high-end corporate MacBook Pro laptop", "A bicycle", "A textbook", "A coffee mug"],
                "answer": 0,
                "explanation": "Evidence 2 states the deposit was demanded for dispatching a corporate MacBook Pro."
            },
            {
                "text": "What free public email service was used by the recruiter?",
                "options": ["Gmail (@gmail.com)", "ProtonMail", "Yahoo", "Outlook"],
                "answer": 0,
                "explanation": "Evidence 3 shows the email address was 'hr.infotech.careers@gmail.com'."
            },
            {
                "text": "What did the official corporate registry (MCA) search reveal about the company?",
                "options": [
                    "No company was registered under that name at the stated address",
                    "It was the largest software company in the country",
                    "The company had 100,000 employees",
                    "The company was founded in 1850"
                ],
                "answer": 0,
                "explanation": "Evidence 4 notes the MCA registry search revealed no company registered under that name."
            },
            {
                "text": "What critical interview step was completely bypassed in this suspicious job offer?",
                "options": [
                    "Technical screening, resume evaluation, and formal interview",
                    "Signing up for social media",
                    "Downloading a mobile game",
                    "Buying a new phone case"
                ],
                "answer": 0,
                "explanation": "Evidence 1 specifies the offer came with zero interview and no resume screening."
            },
            {
                "text": "What is the universal rule regarding legitimate job offers and upfront payments?",
                "options": [
                    "Legitimate companies NEVER ask candidates to pay money for laptops or recruitment fees",
                    "All genuine companies charge ₹3,000 upfront",
                    "Job deposits must always be paid via cash",
                    "Upfront fees are legally required by the government"
                ],
                "answer": 0,
                "explanation": "Legitimate employers cover equipment and onboarding costs; demanding money upfront is a definitive hallmark of employment scams."
            },
            {
                "text": "What payment method did the scam recruiter demand for the deposit?",
                "options": ["UPI transfer", "Cryptocurrency only", "Cash sent through post", "Gold coins"],
                "answer": 0,
                "explanation": "Evidence 2 records the deposit was demanded 'via UPI'."
            },
            {
                "text": "Why do scammers offer absurdly high salaries like ₹80,000 for basic 2-hour data entry?",
                "options": [
                    "To generate irresistible greed and excitement, blinding victims to obvious fraud signs",
                    "Because data entry is the most difficult job in the world",
                    "Because companies have too much cash to give away",
                    "Because government rules mandate high salaries for freshers"
                ],
                "answer": 0,
                "explanation": "Unrealistic payouts lure desperate job seekers into ignoring suspicious demands."
            },
            {
                "text": "What was the sender's full email address in the incident record?",
                "options": ["hr.infotech.careers@gmail.com", "careers@microsoft.com", "jobs@google.com", "tcs_hr@tcs.com"],
                "answer": 0,
                "explanation": "Evidence 3 identifies the address as 'hr.infotech.careers@gmail.com'."
            },
            {
                "text": "Why should job seekers be cautious when HR recruiters use free @gmail.com addresses?",
                "options": [
                    "Genuine corporate HR recruiters use official company domain emails (e.g., @company.com)",
                    "Gmail addresses cannot send PDFs",
                    "Gmail accounts expire every month",
                    "Gmail is only allowed for personal gaming"
                ],
                "answer": 0,
                "explanation": "Legitimate organizations communicate using established corporate email domains, not anonymous free webmail."
            },
            {
                "text": "What should a student do if an unknown recruiter demands a refundable laptop deposit?",
                "options": [
                    "Refuse payment, terminate contact, and report the fraud to cybercrime authorities",
                    "Immediately send ₹3,000 to reserve the laptop",
                    "Negotiate the deposit down to ₹1,500",
                    "Send credit card details over chat"
                ],
                "answer": 0,
                "explanation": "Never transfer funds for employment; terminate communication and file an official complaint."
            },
            {
                "text": "What government ministry in India manages company registrations (MCA)?",
                "options": ["Ministry of Corporate Affairs", "Ministry of Agriculture", "Ministry of Health", "Ministry of Railways"],
                "answer": 0,
                "explanation": "MCA (Ministry of Corporate Affairs) maintains the authoritative registry of incorporated companies in India."
            },
            # Tricky Q14
            {
                "text": "Why did the scammer describe the deposit as 'refundable'?",
                "options": [
                    "To create a false sense of financial safety, making the victim feel they have nothing to lose",
                    "Because banks legally require all deposits to be returned within an hour",
                    "Because the scammer truly intends to refund the money after 10 days",
                    "To test if the student understands accounting terms"
                ],
                "answer": 0,
                "explanation": "Labeling fraudulent charges as 'refundable' lowers psychological resistance to sending money."
            },
            # Tricky Q15
            {
                "text": "Even if an offer letter contains a company logo, why is that insufficient proof of legitimacy?",
                "options": [
                    "Logos can easily be copied from internet image searches and pasted onto fake PDF templates",
                    "Company logos cannot be printed in color",
                    "Logos are automatically deleted when saved as PDF",
                    "Only government documents are allowed to have logos"
                ],
                "answer": 0,
                "explanation": "Corporate graphics are publicly accessible; anyone can copy logos onto fraudulent stationery."
            }
        ],
        "round2Questions": [
            # Round 2
            {
                "text": "How many days old was the lookalike domain 'infotech-careers-portal.site'?",
                "options": ["4 days old", "5 years old", "6 months old", "10 years old"],
                "answer": 0,
                "explanation": "Evidence 1 states the domain was registered just 4 days prior."
            },
            {
                "text": "What top-level domain (TLD) extension was used for the fake recruiting site?",
                "options": [".site", ".com", ".gov.in", ".edu"],
                "answer": 0,
                "explanation": "Evidence 1 records the domain as 'infotech-careers-portal.site'."
            },
            {
                "text": "What Virtual Payment Address (VPA) received the fraudulent ₹3,000 deposit?",
                "options": ["hr_dep_proc@okaxis", "quick_refund_desk@ybl", "college@sbi", "admin@icici"],
                "answer": 0,
                "explanation": "Evidence 2 states the deposit went to VPA 'hr_dep_proc@okaxis'."
            },
            {
                "text": "In which city was the stolen money withdrawn from an ATM?",
                "options": ["Noida", "Mumbai", "Chennai", "Kolkata"],
                "answer": 0,
                "explanation": "Evidence 2 states the funds were cashed out at an ATM in Noida."
            },
            {
                "text": "What key identifier on the forged offer letter was proven to be invalid upon verification?",
                "options": [
                    "CIN (Corporate Identity Number)",
                    "Page number",
                    "Font color",
                    "Paper thickness"
                ],
                "answer": 0,
                "explanation": "Evidence 3 highlights that the letter contained an invalid Corporate Identity Number (CIN)."
            },
            {
                "text": "Why did the scammer insist on shifting communication to Telegram handle '@HR_Sneha_Verify'?",
                "options": [
                    "To evade corporate email traceability, law enforcement subpoenas, and automated spam filtering",
                    "Because Telegram is the mandatory tool for all HR departments in India",
                    "Because email servers cannot attach PDF offer letters",
                    "To send larger video files of the laptop"
                ],
                "answer": 0,
                "explanation": "Encrypted messaging apps like Telegram provide anonymity, shielding perpetrators from email logging."
            },
            {
                "text": "What does a 21-character Indian Corporate Identity Number (CIN) identify?",
                "options": [
                    "A unique registration code assigned by the Registrar of Companies to legal corporate entities",
                    "The bank account number of the company's CEO",
                    "The IP address of the company's web server",
                    "The Wi-Fi password of the corporate headquarters"
                ],
                "answer": 0,
                "explanation": "CIN is an authoritative 21-digit alphanumeric identifier assigned to every registered company in India."
            },
            {
                "text": "What visual quality issue in the offer letter PDF pointed to forgery during document analysis?",
                "options": [
                    "A low-resolution stolen logo with typographical errors",
                    "The document was saved in landscape orientation",
                    "The text was printed in black ink",
                    "The PDF was only two pages long"
                ],
                "answer": 0,
                "explanation": "Evidence 3 notes a low-resolution stolen logo filled with typographical errors."
            },
            # Medium-Hard Q9-Q13
            {
                "text": "How do newly registered domains (NRDs) feature in threat intelligence risk scoring?",
                "options": [
                    "Domains under 30 days old are heavily categorized as high risk because threat actors create them for short-lived scams",
                    "New domains are automatically granted verified status by Google",
                    "New domains cannot be accessed by mobile phones",
                    "They are exempt from all cyber laws"
                ],
                "answer": 0,
                "explanation": "NRDs (under 30 days old) lack reputational history and account for a vast majority of phishing infrastructure."
            },
            {
                "text": "What is the typical operational role of an ATM cash-out operative in an organized cyber scam gang?",
                "options": [
                    "To physically withdraw digital stolen funds as cash immediately upon receipt before bank freezes can take effect",
                    "To design the HTML templates for fake websites",
                    "To manage the cloud server firewalls",
                    "To write the legal terms and conditions"
                ],
                "answer": 0,
                "explanation": "Cash-out runners withdraw electronic transfers into untraceable cash at physical ATMs across state borders."
            },
            {
                "text": "Why are cheap generic TLDs like '.site', '.xyz', or '.top' disproportionately favored by scam operations?",
                "options": [
                    "They offer low registration costs and minimal identity verification, making disposable campaigns cheap to deploy",
                    "They provide free satellite internet to customers",
                    "They are owned by the United Nations",
                    "They cannot be blocked by modern web browsers"
                ],
                "answer": 0,
                "explanation": "Low prices and lax registrar vetting make budget gTLDs ideal for disposable, high-turnover scam domains."
            },
            {
                "text": "What legal liability could a student face if they fall for a 'money transfer job' and receive funds for others?",
                "options": [
                    "They could be criminally charged as an unwitting money mule participating in financial fraud and money laundering",
                    "They are awarded a certificate in digital banking",
                    "They are automatically hired by the national bank",
                    "They receive free college tuition"
                ],
                "answer": 0,
                "explanation": "Allowing personal accounts to route third-party funds constitutes illegal money muling under criminal statutes."
            },
            {
                "text": "What forensic verification tool can be used to check if a corporate domain was registered only 4 days ago?",
                "options": [
                    "WHOIS lookup tools / ICANN Domain Registration Data Lookup",
                    "Calculator app",
                    "Disk defragmenter",
                    "Task Manager"
                ],
                "answer": 0,
                "explanation": "WHOIS lookups provide domain registration creation dates, registrars, and nameserver histories."
            },
            # Challenging Q14-Q15
            {
                "text": "Analyzing the scam's multi-stage operational model, what was the primary monetization mechanism?",
                "options": [
                    "Extorting multiple small upfront deposits (₹3,000) from dozens of victims, then severing communication",
                    "Selling high-end laptops at a wholesale markup",
                    "Providing legitimate IT consulting services",
                    "Mining cryptocurrency on the victim's phone"
                ],
                "answer": 0,
                "explanation": "High-volume recruitment fraud aggregates small, non-refundable deposits from hundreds of vulnerable freshers."
            },
            {
                "text": "What comprehensive verification protocol should a candidate follow before accepting an unknown job offer?",
                "options": [
                    "Verify corporate MCA registry, check domain age via WHOIS, cross-check official company career portals, and reject upfront fees",
                    "Pay the requested deposit immediately and wait for the courier tracking code",
                    "Ask the recruiter on Telegram if they are genuine",
                    "Share banking PINs to verify account compatibility"
                ],
                "answer": 0,
                "explanation": "Rigorous vetting includes checking government registrations, domain seniority, primary career channels, and zero upfront fees."
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
            # Round 1
            {
                "text": "What handle username was used by the impersonating social media account?",
                "options": ["@student_official_2026", "@real_student_99", "@official_tjs_college", "@support_desk_user"],
                "answer": 0,
                "explanation": "Evidence 1 states the fake account used username '@student_official_2026'."
            },
            {
                "text": "How many hours before the incident was the fake profile created?",
                "options": ["14 hours ago", "5 years ago", "1 month ago", "365 days ago"],
                "answer": 0,
                "explanation": "Evidence 3 indicates the fake profile was created only 14 hours ago."
            },
            {
                "text": "How much money did the fake account request from classmates?",
                "options": ["₹2,000", "₹50,000", "₹100", "₹20,000"],
                "answer": 0,
                "explanation": "Evidence 2 states the scammer pleaded for ₹2,000 emergency transfers."
            },
            {
                "text": "What emotional pretext did the impersonator use to demand money?",
                "options": ["An urgent hospital medical emergency", "A winning lottery ticket fee", "A college library fine", "A movie ticket booking"],
                "answer": 0,
                "explanation": "Evidence 2 notes the messages claimed an urgent hospital emergency."
            },
            {
                "text": "How many classmates were messaged by the fake account?",
                "options": ["30 classmates", "2 classmates", "500 classmates", "None"],
                "answer": 0,
                "explanation": "Evidence 2 confirms the profile messaged 30 classmates."
            },
            {
                "text": "How many classmates filed official impersonation reports with the platform?",
                "options": ["Ten classmates", "Zero", "One hundred", "Only the victim"],
                "answer": 0,
                "explanation": "Evidence 4 records: 'Ten classmates filed impersonation reports with trust and safety team'."
            },
            {
                "text": "What was suspicious about the profile's post history?",
                "options": [
                    "It had zero posts prior to the scam messages",
                    "It had 10,000 photos of college exams",
                    "It had posts dating back to 2010",
                    "All posts were written in French"
                ],
                "answer": 0,
                "explanation": "Evidence 3 highlights that the account had zero posts prior to broadcasting requests."
            },
            {
                "text": "What should a friend do before sending money to a classmate asking for emergency cash online?",
                "options": [
                    "Call the friend directly via phone or voice call to verify their identity and situation",
                    "Immediately transfer the money without asking questions",
                    "Send double the requested amount",
                    "Post about it on an open social media story"
                ],
                "answer": 0,
                "explanation": "Voice or in-person verification immediately exposes cloned profile impostors."
            },
            {
                "text": "How did the impersonator acquire the victim's profile pictures?",
                "options": [
                    "By copying public photos already visible on the student's social accounts",
                    "By hacking into a national satellite system",
                    "By taking photos through the student's bedroom window",
                    "By drawing sketches by hand"
                ],
                "answer": 0,
                "explanation": "Impersonators scrape publicly accessible profile photos to create convincing clones."
            },
            {
                "text": "What platform feature allows users to report someone pretending to be them?",
                "options": ["Report Account -> Impersonation", "Delete Account", "Add Close Friends", "Archive Story"],
                "answer": 0,
                "explanation": "Major platforms provide dedicated 'Report -> Impersonation' workflows."
            },
            {
                "text": "Why do scammers target multiple mutual friends of the victim simultaneously?",
                "options": [
                    "Mutual friends are more likely to trust messages that seem to come from a real acquaintance",
                    "To test who has the fastest internet speed",
                    "Because social platforms only allow sending 30 messages",
                    "To improve the victim's social media follower count"
                ],
                "answer": 0,
                "explanation": "Social proximity exploits interpersonal trust, making friends less skeptical of emergency pleas."
            },
            {
                "text": "What privacy setting on social media prevents strangers from viewing your friend lists and photos?",
                "options": ["Setting the profile to Private (Friends Only)", "Setting the profile to Public", "Enabling autoplay videos", "Disabling dark mode"],
                "answer": 0,
                "explanation": "Private accounts restrict visibility of friend lists and galleries to confirmed followers."
            },
            {
                "text": "What is this specific cybercrime called when an attacker creates a replica profile to defraud friends?",
                "options": ["Social Media Cloning / Impersonation Fraud", "Cryptojacking", "SQL Injection", "Distributed Denial of Service"],
                "answer": 0,
                "explanation": "Duplicating social profiles to solicit funds is categorized as social media cloning/impersonation fraud."
            },
            # Tricky Q14
            {
                "text": "Why did the scammer choose a username with '_official_2026' added to the student's name?",
                "options": [
                    "The victim's exact username was already taken, so the scammer added realistic-sounding suffixes",
                    "Because official platforms require all users to end with '_2026'",
                    "Because the student had legally registered that trademark",
                    "To ensure the profile was verified by government authorities"
                ],
                "answer": 0,
                "explanation": "Clone accounts append words like 'official', 'real', or numbers to approximate the victim's identity."
            },
            # Tricky Q15
            {
                "text": "What is the critical distinction between 'Account Takeover' and 'Account Cloning'?",
                "options": [
                    "In an Account Takeover, the original account password is stolen; in Cloning, a completely separate fake profile is created",
                    "Account Cloning requires a physical fingerprint scanner",
                    "Account Takeover only happens on desktop computers",
                    "There is no difference; they are identical concepts"
                ],
                "answer": 0,
                "explanation": "Cloning creates a new lookalike account; the legitimate user still retains full access to their real account."
            }
        ],
        "round2Questions": [
            # Round 2
            {
                "text": "What type of IP network masked the real creator of '@student_official_2026'?",
                "options": ["A rotating residential proxy network (AS133612)", "The college hostel Wi-Fi network", "A government satellite connection", "An unencrypted Bluetooth link"],
                "answer": 0,
                "explanation": "Evidence 2 confirms logins originated from a rotating Indian residential proxy network."
            },
            {
                "text": "What virtual phone number country code was used to register the fake account via SMS?",
                "options": ["+1 (United States)", "+91 (India)", "+44 (United Kingdom)", "+49 (Germany)"],
                "answer": 0,
                "explanation": "Evidence 3 specifies a virtual burner VoIP number (+1 202-555-0143)."
            },
            {
                "text": "What Virtual Payment Address (VPA) was given to classmates for the emergency transfers?",
                "options": ["urgent_help_med77@paytm", "quick_refund_desk@ybl", "student_fund@okaxis", "hospital_care@sbi"],
                "answer": 0,
                "explanation": "Evidence 4 notes the UPI address provided was 'urgent_help_med77@paytm'."
            },
            {
                "text": "What forensic clue in the VPA proved that the money was NOT going to the student?",
                "options": [
                    "The linked bank account holder had a completely different name and was located in another state",
                    "The VPA used capital letters",
                    "Paytm is not permitted to accept money in India",
                    "The VPA expired after 10 minutes"
                ],
                "answer": 0,
                "explanation": "Evidence 4 records the account was linked to an unrelated holder in another state (money mule)."
            },
            {
                "text": "What does EXIF metadata in an original photo typically reveal before being stripped?",
                "options": [
                    "Camera model, timestamp, exposure settings, and GPS geolocation coordinates",
                    "The password of the photographer's computer",
                    "The photographer's bank balance",
                    "The full home address of everyone in the picture"
                ],
                "answer": 0,
                "explanation": "EXIF data stores technical capture parameters, timestamps, and optional GPS coordinates."
            },
            {
                "text": "Why do fraudsters use residential proxies rather than standard commercial VPNs?",
                "options": [
                    "Residential proxy IPs belong to genuine home broadband users, avoiding automated fraud detection flags",
                    "Residential proxies make photos appear in higher quality",
                    "Residential proxies are completely free for all hackers",
                    "Residential proxies make accounts permanently verified"
                ],
                "answer": 0,
                "explanation": "Social platforms heavily block known datacenters; residential proxies mimic ordinary home users."
            },
            {
                "text": "How do temporary online SMS reception websites enable fraudulent social media signups?",
                "options": [
                    "They provide shared virtual numbers that receive verification OTP codes without requiring identity KYC",
                    "They manufacture physical plastic SIM cards",
                    "They allow calling anyone in the world for free",
                    "They bypass internet service providers"
                ],
                "answer": 0,
                "explanation": "Temporary SMS services expose incoming verification text messages publicly, enabling unverified burner signups."
            },
            {
                "text": "What evidence should the victim gather before reporting the impersonating account for deletion?",
                "options": [
                    "Timestamped screenshots of the profile URL, account handle, and chat messages with payment VPAs",
                    "A handwritten drawing of the profile picture",
                    "A video of the victim closing their laptop",
                    "Deleting their own real account"
                ],
                "answer": 0,
                "explanation": "Preserving the profile link, handle, chat logs, and beneficiary payment handles ensures evidentiary value."
            },
            # Medium-Hard Q9-Q13
            {
                "text": "What is the primary motive behind verifying the beneficiary name in UPI apps before sending funds?",
                "options": [
                    "UPI apps display the official bank account holder name, exposing if the payee is a stranger",
                    "To check how many friends the payee has",
                    "To see what phone model the payee is using",
                    "To verify the payee's battery percentage"
                ],
                "answer": 0,
                "explanation": "UPI resolves VPAs to the registered banking account holder's legal name, instantly exposing mule mismatches."
            },
            {
                "text": "How do social media Trust & Safety teams verify legitimate identity during impersonation claims?",
                "options": [
                    "By requiring government-issued photo ID verification matching the genuine account owner's legal name",
                    "By asking all followers to vote in a public poll",
                    "By measuring the size of the profile picture",
                    "By checking who has logged in most frequently this week"
                ],
                "answer": 0,
                "explanation": "Platforms require formal government identity documentation to validate ownership and eliminate clones."
            },
            {
                "text": "Why is public social media friend list visibility a major risk factor for cloning attacks?",
                "options": [
                    "It provides scammers with a ready-made directory of close contacts to target with personalized messages",
                    "It slows down internet connection speeds",
                    "It causes the phone to heat up when opened",
                    "It forces friends to change their passwords"
                ],
                "answer": 0,
                "explanation": "Public friend lists hand attackers the exact targets needed to execute convincing social engineering."
            },
            {
                "text": "What legal section under the Information Technology Act in India penalizes identity theft and impersonation?",
                "options": ["Section 66C and Section 66D of the IT Act", "Section 144 of CrPC", "Section 302 of IPC", "Motor Vehicles Act Section 12"],
                "answer": 0,
                "explanation": "Sections 66C (identity theft) and 66D (cheating by personation using computer resource) specifically penalize this crime."
            },
            {
                "text": "How can telecom and bank authorities freeze the mule account 'urgent_help_med77@paytm'?",
                "options": [
                    "By filing an immediate cybercrime portal complaint (cybercrime.gov.in) triggering an inter-bank lien freeze",
                    "By sending an SMS asking the scammer to return the money",
                    "By unlinking all ATMs in the country",
                    "By calling the local police station in London"
                ],
                "answer": 0,
                "explanation": "Cybercrime portal / 1930 notifications route alerts to nodal banking officers to freeze beneficiary wallets."
            },
            # Challenging Q14-Q15
            {
                "text": "Synthesizing the digital evidence, what was the adversary's complete operational setup?",
                "options": [
                    "Scraped public photo gallery -> Burner VoIP number for SMS OTP -> Residential proxy for login -> Third-party mule VPA for cash collection",
                    "Trojanized Android APK -> Hardware keylogger -> Physical SIM clone -> Direct bank wire",
                    "Wi-Fi eavesdropping -> Man-in-the-Middle certificate injection -> Database drop -> Ransom demand",
                    "Zero-day exploit -> Firmware rewrite -> Memory dump -> Satellite uplink"
                ],
                "answer": 0,
                "explanation": "The forensic records prove: scraped assets, disposable VoIP registration, residential proxy masking, and mule VPA routing."
            },
            {
                "text": "What preventative measures should colleges educate students on to guard against identity cloning?",
                "options": [
                    "Keep friend lists private, limit photo visibility, never send funds without voice verification, and report fake profiles immediately",
                    "Never take any photographs with digital cameras",
                    "Delete all social media accounts permanently",
                    "Change smartphone numbers every two weeks"
                ],
                "answer": 0,
                "explanation": "Proactive privacy lockdowns, out-of-band verification, and rapid reporting build resilient personal defense."
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
            # Round 1
            {
                "text": "What pirated file did the student download from the torrent website?",
                "options": ["Photoshop_Crack_Setup.exe", "homework_notes.docx", "family_vacation.mp4", "college_timetable.pdf"],
                "answer": 0,
                "explanation": "Evidence 1 states the downloaded file was 'Photoshop_Crack_Setup.exe'."
            },
            {
                "text": "What hidden background process was consuming 98% of the computer's CPU?",
                "options": ["system_host32.exe", "chrome.exe", "notepad.exe", "calculator.exe"],
                "answer": 0,
                "explanation": "Evidence 2 identifies the background process as 'system_host32.exe'."
            },
            {
                "text": "What activity was the malicious background process performing?",
                "options": ["Mining cryptocurrency", "Playing video games", "Editing photographs", "Printing documents"],
                "answer": 0,
                "explanation": "Evidence 2 states the process was utilizing 98% of CPU to mine cryptocurrency."
            },
            {
                "text": "Why did the student manually disable Windows Defender antivirus?",
                "options": [
                    "Following instructions inside the pirated crack download",
                    "Windows Defender asked to be turned off",
                    "To make the screen brighter",
                    "To increase internet download speed"
                ],
                "answer": 0,
                "explanation": "Evidence 3 notes Windows Defender was manually disabled following crack instructions."
            },
            {
                "text": "To what port was continuous outbound traffic directed in the network log?",
                "options": ["Port 3333", "Port 80", "Port 443", "Port 21"],
                "answer": 0,
                "explanation": "Evidence 4 notes traffic to IP 185.220.101.5 on port 3333."
            },
            {
                "text": "What IP address was identified as the malicious mining pool destination?",
                "options": ["185.220.101.5", "192.168.1.1", "127.0.0.1", "10.0.0.1"],
                "answer": 0,
                "explanation": "Evidence 4 records traffic to malicious mining pool IP 185.220.101.5."
            },
            {
                "text": "Why do crack websites commonly instruct users to 'turn off your antivirus'?",
                "options": [
                    "Because antivirus software detects the bundled malware and Trojan droppers",
                    "Because antivirus software makes the download take 3 days",
                    "Because antivirus software turns the computer off",
                    "Because antivirus software charges a fee for cracks"
                ],
                "answer": 0,
                "explanation": "Instructions to disable antivirus are designed to permit malicious Trojans to execute unhindered."
            },
            {
                "text": "What physical symptom on a laptop typically indicates high CPU cryptomining?",
                "options": [
                    "The laptop runs extremely hot, the cooling fan spins at maximum speed, and performance slows drastically",
                    "The screen turns upside down",
                    "The keyboard letters change order",
                    "The power cable unplugs itself"
                ],
                "answer": 0,
                "explanation": "Cryptominers consume 100% of CPU/GPU capacity, causing thermal throttling, fan noise, and extreme lag."
            },
            {
                "text": "Where should users download legitimate software applications from?",
                "options": [
                    "Official vendor websites and verified app stores",
                    "Anonymous torrent sites",
                    "Random download buttons on illegal streaming pages",
                    "Unverified file sharing chat groups"
                ],
                "answer": 0,
                "explanation": "Official software repositories ensure cryptographic signatures and absence of malware."
            },
            {
                "text": "What term describes malware that stealthily uses a victim's hardware to mine cryptocurrency?",
                "options": ["Cryptojacker / Cryptominer malware", "Phishing email", "Spyware", "Adware"],
                "answer": 0,
                "explanation": "Illicit background mining on a victim's machine is called cryptojacking."
            },
            {
                "text": "What tool in Windows allows users to view CPU usage by running processes?",
                "options": ["Task Manager", "Paint", "Notepad", "File Explorer"],
                "answer": 0,
                "explanation": "Windows Task Manager provides real-time CPU, RAM, and disk utilization per process."
            },
            {
                "text": "What type of malware file pretends to be a useful program but contains a malicious payload?",
                "options": ["A Trojan horse", "A computer monitor", "An optical mouse", "A hard drive cable"],
                "answer": 0,
                "explanation": "Trojans disguise themselves as legitimate software (like photo editors or games) while harboring payloads."
            },
            {
                "text": "What is the first step when you suspect your computer is infected with an active mining Trojan?",
                "options": [
                    "Disconnect from the network (unplug Wi-Fi) and run a full bootable antivirus scan",
                    "Leave the computer on for 48 hours to finish mining",
                    "Buy more RAM memory",
                    "Turn the monitor off and keep working"
                ],
                "answer": 0,
                "explanation": "Isolating from network stops C2 communication and data exfiltration while malware is sanitized."
            },
            # Tricky Q14
            {
                "text": "Why did the malware name its process 'system_host32.exe'?",
                "options": [
                    "To disguise itself as a legitimate Windows operating system service (like svchost.exe)",
                    "Because Windows requires all programs to have 'host32' in the title",
                    "Because the computer was built in the year 1932",
                    "To improve computer gaming performance"
                ],
                "answer": 0,
                "explanation": "Malware adopts deceptive system-like filenames to blend in with legitimate OS processes during quick inspection."
            },
            # Tricky Q15
            {
                "text": "Why is downloading pirated software often described as the most common entry vector for student malware infections?",
                "options": [
                    "Users voluntarily bypass their own antivirus defenses and grant administrative permissions to run the installer",
                    "Pirated files are downloaded over satellite frequencies",
                    "Pirated files can only be opened on government computers",
                    "Torrent software is illegal in all countries"
                ],
                "answer": 0,
                "explanation": "Users willingly disable security controls and accept UAC admin prompts to install cracked tools, opening full access."
            }
        ],
        "round2Questions": [
            # Round 2
            {
                "text": "In what directory path did the malware hide the binary 'system_host32.exe'?",
                "options": [
                    "C:\\Users\\User\\AppData\\Roaming\\Microsoft\\svchost\\",
                    "C:\\Program Files\\Adobe\\Photoshop\\",
                    "C:\\Windows\\System32\\",
                    "C:\\Users\\User\\Desktop\\"
                ],
                "answer": 0,
                "explanation": "Evidence 1 records the dropped location as 'C:\\Users\\User\\AppData\\Roaming\\Microsoft\\svchost\\'."
            },
            {
                "text": "What registry key was modified to ensure the miner launches automatically every time the PC boots?",
                "options": [
                    "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run",
                    "HKLM\\System\\CurrentControlSet\\Services",
                    "HKCU\\Control Panel\\Desktop",
                    "HKLM\\Software\\Classes"
                ],
                "answer": 0,
                "explanation": "Evidence 2 states persistence was established under 'HKCU\\...\\CurrentVersion\\Run'."
            },
            {
                "text": "What deceptive name was given to the startup registry key?",
                "options": ["WindowsAudioService", "CryptoMiner99", "PhotoshopCrack", "MalwareRunner"],
                "answer": 0,
                "explanation": "Evidence 2 records the key name was 'WindowsAudioService'."
            },
            {
                "text": "What critical system file was tampered with to prevent the antivirus from downloading signature updates?",
                "options": [
                    "C:\\Windows\\System32\\drivers\\etc\\hosts",
                    "C:\\Windows\\explorer.exe",
                    "C:\\Windows\\boot.ini",
                    "C:\\Windows\\regedit.exe"
                ],
                "answer": 0,
                "explanation": "Evidence 3 shows the 'hosts' file was modified to redirect update domains to 127.0.0.1."
            },
            {
                "text": "To what IP address did the modified hosts file redirect antivirus update services?",
                "options": ["127.0.0.1 (localhost)", "8.8.8.8", "192.168.1.1", "0.0.0.0"],
                "answer": 0,
                "explanation": "Redirecting domains to 127.0.0.1 loops connection attempts back to the local machine, silently failing updates."
            },
            {
                "text": "What specific cryptocurrency was targeted by the mining pool configuration file?",
                "options": ["Monero (XMR)", "Bitcoin (BTC)", "Ethereum (ETH)", "Dogecoin (DOGE)"],
                "answer": 0,
                "explanation": "Evidence 4 extracts pool 'xmr-pool.minexmr.com:3333', identifying Monero (XMR)."
            },
            {
                "text": "Why is Monero (XMR) the preferred cryptocurrency for illicit cryptojacking campaigns?",
                "options": [
                    "It uses privacy-centric ring signatures and stealth addresses, making illicit transactions untraceable",
                    "It can only be mined on Apple iPhones",
                    "It is owned by the United Nations",
                    "It does not require any CPU power to mine"
                ],
                "answer": 0,
                "explanation": "Monero's privacy features hide transaction senders, amounts, and recipient wallet balances."
            },
            {
                "text": "What process ID (PID) was assigned to the dropped mining payload 'system_host32.exe'?",
                "options": ["PID 7912", "PID 4820", "PID 100", "PID 0"],
                "answer": 0,
                "explanation": "Evidence 1 process tree records: 'dropped system_host32.exe (PID 7912)'."
            },
            # Medium-Hard Q9-Q13
            {
                "text": "How did the initial installer 'Photoshop_Crack_Setup.exe' execute the hidden payload without showing a window?",
                "options": [
                    "It spawned a hidden PowerShell background execution with '-WindowStyle Hidden' and '-ExecutionPolicy Bypass'",
                    "It unplugged the computer monitor temporarily",
                    "It converted the code into an MP3 song",
                    "It waited for the user to close their eyes"
                ],
                "answer": 0,
                "explanation": "Attackers leverage PowerShell execution flags to launch background tasks silently without user interface cues."
            },
            {
                "text": "Why is the 'AppData\\Roaming' folder frequently used by malware droppers on Windows?",
                "options": [
                    "It has write permissions for standard user accounts and does not require administrative elevation to place files",
                    "It is the only folder that can run .exe files",
                    "It is automatically encrypted by Microsoft",
                    "Files in AppData are invisible to antivirus engines"
                ],
                "answer": 0,
                "explanation": "Standard users can write to AppData without triggering UAC elevation prompts, making it ideal for droppers."
            },
            {
                "text": "What technique did the malware employ when routing update domains to 127.0.0.1 in the hosts file?",
                "options": [
                    "DNS sinkholing / Local hosts file hijacking",
                    "BGP route hijacking",
                    "ARP cache poisoning",
                    "SSL certificate pinning"
                ],
                "answer": 0,
                "explanation": "Overwriting hosts file entries maps target domain lookups to the local loopback address, neutralizing security connections."
            },
            {
                "text": "How can a forensic analyst identify unauthorized modifications to the Windows hosts file?",
                "options": [
                    "By inspecting the file's last modified timestamp and comparing entries against the default clean template",
                    "By counting the total letters in the document",
                    "By converting the file to a JPEG image",
                    "By checking the desktop background wallpaper"
                ],
                "answer": 0,
                "explanation": "Default hosts files contain only comments; non-commented entries mapping antivirus domains to loopback indicate tamper."
            },
            {
                "text": "What is the primary indicator of compromise (IOC) associated with network telemetry in this case?",
                "options": [
                    "Persistent outbound TCP connections on port 3333 to IP 185.220.101.5 (Stratum mining protocol)",
                    "HTTP web traffic on port 80 to wikipedia.org",
                    "DNS queries on port 53 to google.com",
                    "NTP time synchronization on port 123"
                ],
                "answer": 0,
                "explanation": "Continuous outbound traffic on port 3333 represents the Stratum mining protocol communicating with mining pools."
            },
            # Challenging Q14-Q15
            {
                "text": "Reconstructing the infection lifecycle, what were the four stages from download to ongoing exploitation?",
                "options": [
                    "Torrent download -> User disables Defender -> Dropper writes to AppData & Registry Run -> Outbound Stratum mining beaconing",
                    "Outbound mining -> Torrent download -> Dropper writes to AppData -> Defender disabled",
                    "Registry Run -> Outbound mining -> Torrent download -> Dropper writes to AppData",
                    "Defender disabled -> Outbound mining -> Torrent download -> Dropper writes to AppData"
                ],
                "answer": 0,
                "explanation": "The lifecycle follows: acquisition via torrent, defense impairment, payload drop with persistence, and active mining."
            },
            {
                "text": "What is the comprehensive remediation plan required to restore this machine to a verified clean state?",
                "options": [
                    "Kill PID 7912, delete malicious Roaming folder, delete Run registry key, restore default hosts file, and enable Defender",
                    "Simply close Task Manager and restart the laptop once",
                    "Delete the torrent file from the Downloads folder only",
                    "Disconnect the power cord while running"
                ],
                "answer": 0,
                "explanation": "Full remediation requires terminating active processes, removing dropped binaries, excising persistence keys, and fixing hosts."
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
            # Round 1
            {
                "text": "In what city and country did the suspicious new device sign-in occur?",
                "options": ["Sao Paulo, Brazil", "Chennai, India", "London, UK", "Tokyo, Japan"],
                "answer": 0,
                "explanation": "Evidence 1 states the sign-in was detected from Sao Paulo, Brazil."
            },
            {
                "text": "What operating system and browser were reported in the security alert?",
                "options": ["Safari on macOS", "Chrome on Windows", "Firefox on Linux", "Edge on Android"],
                "answer": 0,
                "explanation": "Evidence 1 specifies 'Safari on macOS'."
            },
            {
                "text": "What hardware devices does the student actually own?",
                "options": ["An Android smartphone and an HP Windows laptop", "A MacBook Pro and an iPad", "Only an Apple iPhone", "Only a Linux server"],
                "answer": 0,
                "explanation": "Evidence 2 states the student only owns an Android smartphone and an HP Windows laptop."
            },
            {
                "text": "How many kilometers apart are Chennai and Sao Paulo geographically?",
                "options": ["Approximately 14,000 km", "100 km", "500 km", "10 km"],
                "answer": 0,
                "explanation": "Evidence 3 indicates the two sessions were active 14,000 km apart."
            },
            {
                "text": "How many minutes elapsed between the Chennai session and the Sao Paulo session?",
                "options": ["5 minutes", "24 hours", "3 days", "60 minutes"],
                "answer": 0,
                "explanation": "Evidence 3 states the Chennai session was active at 02:35 UTC, followed 5 minutes later by Sao Paulo at 02:40 UTC."
            },
            {
                "text": "Why is logging in from two locations 14,000 km apart within 5 minutes physically impossible for one person?",
                "options": [
                    "A human cannot travel 14,000 kilometers in 5 minutes (impossible travel time)",
                    "Because computers do not function across oceans",
                    "Because internet connections cannot travel across the equator",
                    "Because flights only take off once a month"
                ],
                "answer": 0,
                "explanation": "Impossible travel anomalies occur when consecutive logins happen faster than physical transportation allows."
            },
            {
                "text": "What action was immediately executed by the Brazilian session upon accessing the account?",
                "options": [
                    "Initiated an archive download of private chat messages and cloud drive files",
                    "Changed the language to Spanish",
                    "Played music on YouTube",
                    "Deleted the student's browser bookmarks"
                ],
                "answer": 0,
                "explanation": "Evidence 4 records: 'initiated an archive download of private chat messages and cloud drive files'."
            },
            {
                "text": "Why should users take 'New Device Sign-in' email notifications seriously?",
                "options": [
                    "They warn users of unauthorized account access from unknown devices immediately",
                    "They are sent as promotional spam by device manufacturers",
                    "They give users discounts on new laptops",
                    "They change the user's password automatically"
                ],
                "answer": 0,
                "explanation": "New device alerts are critical security telemetry notifying users of potential intrusions."
            },
            {
                "text": "At what UTC time was the suspicious Sao Paulo sign-in recorded?",
                "options": ["02:40 UTC", "12:00 UTC", "08:15 UTC", "18:45 UTC"],
                "answer": 0,
                "explanation": "Evidence 1 states the alert was timestamped at 02:40 UTC."
            },
            {
                "text": "What setting in modern accounts allows users to instantly terminate all unfamiliar active sessions?",
                "options": ["Log out of all other devices / Sign out all sessions", "Change profile picture", "Export contacts", "Clear search history"],
                "answer": 0,
                "explanation": "The 'Sign out of all sessions' feature immediately revokes active authentication tokens across all devices."
            },
            {
                "text": "Does owning only an Android and Windows laptop make a 'macOS Safari' login alert suspicious?",
                "options": [
                    "Yes, it proves someone on an unrecognized Apple device accessed the account",
                    "No, Windows laptops frequently report themselves as macOS Safari",
                    "No, Android phones are made by Apple",
                    "No, all devices look identical to web servers"
                ],
                "answer": 0,
                "explanation": "A user-agent mismatch confirms access from a device type not possessed by the account owner."
            },
            {
                "text": "What feature should you immediately activate after logging out unauthorized sessions?",
                "options": ["Two-Factor Authentication (2FA) with an Authenticator App", "High contrast mode", "Bigger font size", "Airplane mode for 5 days"],
                "answer": 0,
                "explanation": "Enabling 2FA prevents adversaries from logging back in even if credentials remain compromised."
            },
            {
                "text": "What security term describes an impossible travel anomaly in identity security?",
                "options": ["Impossible Travel / Geolocation Velocity alert", "Buffer Overflow", "SQL Injection", "DDoS attack"],
                "answer": 0,
                "explanation": "Geolocation velocity / impossible travel flags logins occurring faster than maximum physical flight velocity."
            },
            # Tricky Q14
            {
                "text": "Why did the attacker prioritize downloading the chat archive and cloud files immediately?",
                "options": [
                    "To exfiltrate sensitive personal data before the account owner wakes up and revokes the session",
                    "To test their internet download speed",
                    "Because cloud backups are deleted every 10 minutes",
                    "To help the student save storage space"
                ],
                "answer": 0,
                "explanation": "Adversaries extract sensitive archives rapidly to maximize data theft before the intrusion is contained."
            },
            # Tricky Q15
            {
                "text": "Could using a standard commercial VPN on the student's phone explain this anomaly?",
                "options": [
                    "Even if the IP changed via VPN, it would NOT change the device user-agent from Android to macOS Safari",
                    "Yes, VPNs automatically convert Android phones into MacBooks",
                    "Yes, VPNs only connect to Brazil",
                    "Yes, VPNs change your device brand randomly every minute"
                ],
                "answer": 0,
                "explanation": "A VPN changes IP geolocation, but browser user-agent headers and device fingerprints remain tied to the client OS."
            }
        ],
        "round2Questions": [
            # Round 2
            {
                "text": "How did the Brazilian session bypass password entry and 2FA authentication completely?",
                "options": [
                    "By presenting a stolen, active session cookie ('session_id=8f91a...')",
                    "By guessing the student's password on the first try",
                    "By calling customer support on the phone",
                    "By hacking into the telecommunications satellite"
                ],
                "answer": 0,
                "explanation": "Evidence 1 states the attacker bypassed login and 2FA by presenting a cloned session cookie (Session Hijacking)."
            },
            {
                "text": "What rogue software on the student's laptop extracted and exfiltrated the session cookie?",
                "options": [
                    "An unverified browser extension 'DarkTheme_Pro_v4'",
                    "The official HP printer driver",
                    "Windows Calculator",
                    "Google Docs"
                ],
                "answer": 0,
                "explanation": "Evidence 2 identifies an unverified browser extension 'DarkTheme_Pro_v4' installed 2 days ago."
            },
            {
                "text": "What was the size of the downloaded cloud storage archive 'user_archive_backup.zip'?",
                "options": ["2.1 GB", "10 MB", "500 KB", "100 GB"],
                "answer": 0,
                "explanation": "Evidence 3 specifies a 2.1 GB archive downloaded to IP 177.136.240.18."
            },
            {
                "text": "What IP address received the 2.1 GB exfiltrated archive download?",
                "options": ["177.136.240.18", "192.168.1.1", "10.0.0.1", "127.0.0.1"],
                "answer": 0,
                "explanation": "Evidence 3 identifies adversary IP 177.136.240.18."
            },
            {
                "text": "What setting did the attacker tamper with to prevent the owner from noticing future alerts?",
                "options": [
                    "Disabled 'New Login Emails' and 'Password Change Alerts'",
                    "Changed the account timezone to UTC",
                    "Turned off computer monitor brightness",
                    "Deleted all emails older than 1 year"
                ],
                "answer": 0,
                "explanation": "Evidence 4 records: 'updated preferences to disable New Login Emails and Password Change Alerts'."
            },
            {
                "text": "Why are malicious browser extensions particularly dangerous for session token security?",
                "options": [
                    "Extensions with broad permissions can read all cookies and web requests across every visited tab",
                    "Extensions make computer fans run backward",
                    "Extensions only work when the computer is turned off",
                    "Extensions automatically delete the operating system"
                ],
                "answer": 0,
                "explanation": "Extensions with broad host permissions can inspect 'chrome.cookies' and siphon active tokens directly."
            },
            {
                "text": "What is the technical term for stealing an active session token to impersonate an authenticated user?",
                "options": ["Session Hijacking / Cookie Theft", "Buffer Overflow", "SYN Flood", "ARP Poisoning"],
                "answer": 0,
                "explanation": "Stealing active session cookies to bypass credentials and MFA is known as Session Hijacking."
            },
            {
                "text": "Why did traditional SMS Two-Factor Authentication fail to stop the attacker at 02:40 UTC?",
                "options": [
                    "Session cookies represent an already-authenticated session, so the server never prompted for 2FA",
                    "The SMS was intercepted by a drone",
                    "The phone battery was completely dead",
                    "The student's mobile carrier shut down"
                ],
                "answer": 0,
                "explanation": "Session cookies bypass the authentication checkpoint entirely; the server assumes the session was already verified."
            },
            # Medium-Hard Q9-Q13
            {
                "text": "How can modern web applications mitigate session cookie replay across geographically disparate devices?",
                "options": [
                    "Enforce device fingerprint binding, IP subnet correlation, and invalidate sessions on sudden impossible travel",
                    "Make passwords twice as long",
                    "Require users to change passwords every 30 minutes",
                    "Block all users from using dark mode themes"
                ],
                "answer": 0,
                "explanation": "Binding sessions to device fingerprints and TLS client certificates prevents stolen cookies from working on foreign hardware."
            },
            {
                "text": "What browser permission should users scrutinize before installing third-party extensions?",
                "options": [
                    "'Read and change all your data on all websites'",
                    "'Play audio notifications'",
                    "'Display notifications'",
                    "'Change browser theme color'"
                ],
                "answer": 0,
                "explanation": "The 'read and change all data on all websites' permission grants total access to DOM content, forms, and cookies."
            },
            {
                "text": "What action must the student take to ensure the stolen cookie 'session_id=8f91a...' is completely invalidated?",
                "options": [
                    "Trigger 'Sign out of all sessions' or reset the master password to invalidate active token hashes on the server",
                    "Clear browser cache on the student's phone only",
                    "Uninstall the browser and reinstall it",
                    "Restart the Wi-Fi router"
                ],
                "answer": 0,
                "explanation": "Resetting the account password or invoking 'Sign out of all sessions' revokes all server-side session records."
            },
            {
                "text": "How long did it take the adversary to exfiltrate the 2.1 GB archive?",
                "options": ["Over a 4-minute window", "2 days", "3 hours", "10 seconds"],
                "answer": 0,
                "explanation": "Evidence 3 confirms the 2.1 GB archive was downloaded over a 4-minute window."
            },
            {
                "text": "What proactive security measure prevents extension-based token theft in enterprise environments?",
                "options": [
                    "Enterprise browser policies whitelisting strictly verified extensions and blocking unapproved third-party addons",
                    "Prohibiting students from using the internet",
                    "Deleting all browser history every 5 minutes",
                    "Requiring users to type using only one hand"
                ],
                "answer": 0,
                "explanation": "Enterprise policy controls allow organizations to restrict extension installation to vetted, signed addons."
            },
            # Challenging Q14-Q15
            {
                "text": "Synthesizing the complete attack timeline, what was the adversary's exact sequence of exploitation?",
                "options": [
                    "Malicious extension installed -> Session cookie stolen -> Session injected in Brazil -> 2.1 GB archive downloaded -> Security alerts muted",
                    "Security alerts muted -> 2.1 GB archive downloaded -> Session injected in Brazil -> Extension installed",
                    "2.1 GB archive downloaded -> Extension installed -> Session injected in Brazil -> Security alerts muted",
                    "Session injected in Brazil -> Extension installed -> Security alerts muted -> 2.1 GB archive downloaded"
                ],
                "answer": 0,
                "explanation": "The timeline shows extension installation 2 days ago, cookie theft, session injection at 02:40, exfiltration at 02:45, and tampering at 02:47."
            },
            {
                "text": "What is the full incident response plan required to clean and restore the student's digital environment?",
                "options": [
                    "Remove the malicious extension, terminate all active sessions, reset password, enable app-based 2FA, and re-enable alert notifications",
                    "Simply close the browser window and restart the computer",
                    "Delete all photos from the student's phone",
                    "Install five more extensions to find the virus"
                ],
                "answer": 0,
                "explanation": "Complete eradication demands removing the malicious addon, killing hijacked sessions, resetting credentials, and fixing alert preferences."
            }
        ]
    }
}
