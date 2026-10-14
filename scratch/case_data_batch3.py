# scratch/case_data_batch3.py
# Complete, detailed questions and evidence for Case 11 to Case 15

BATCH_3 = {
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
            # Round 1
            {
                "text": "What anonymous handle was used to send the threatening messages?",
                "options": ["@dark_spectre_99", "@friendly_student", "@college_official", "@admin_user"],
                "answer": 0,
                "explanation": "Evidence 1 states the messages were sent from anonymous handle '@dark_spectre_99'."
            },
            {
                "text": "What college network was the message delivery IP traced back to?",
                "options": ["The college hostel Wi-Fi gateway", "The campus library desktop lab", "The principal's office", "An international airport Wi-Fi"],
                "answer": 0,
                "explanation": "Evidence 2 traced the public IP to the college hostel Wi-Fi gateway (103.21.144.10)."
            },
            {
                "text": "Between what hours of the evening did the network telemetry record the messages?",
                "options": ["22:00 and 23:30 (10:00 PM to 11:30 PM)", "06:00 and 07:00 AM", "12:00 and 01:00 PM", "03:00 and 04:00 AM"],
                "answer": 0,
                "explanation": "Evidence 2 notes messages were sent between 22:00 and 23:30."
            },
            {
                "text": "What physical network hardware address (MAC address) was identified in the DHCP lease log?",
                "options": ["FC:FB:FB:12:34:56", "00:11:22:33:44:55", "AA:BB:CC:DD:EE:FF", "12:34:56:78:90:AB"],
                "answer": 0,
                "explanation": "Evidence 3 identifies MAC address 'FC:FB:FB:12:34:56'."
            },
            {
                "text": "What internal private IP address was leased to the suspect's device during the harassment?",
                "options": ["192.168.4.88", "10.0.0.1", "127.0.0.1", "172.16.0.2"],
                "answer": 0,
                "explanation": "Evidence 3 correlates the device to internal IP 192.168.4.88."
            },
            {
                "text": "What crucial best practice did the victim follow regarding evidence preservation?",
                "options": [
                    "Captured timestamped screenshots showing full headers and content without deleting or replying",
                    "Deleted all messages immediately and restarted phone",
                    "Replied back with threatening messages of their own",
                    "Threw their smartphone into water"
                ],
                "answer": 0,
                "explanation": "Evidence 4 records the victim captured timestamped screenshots without replying, escalating, or deleting."
            },
            {
                "text": "Over what time period were the repeated threatening messages received?",
                "options": ["A 48-hour period", "10 years", "5 minutes only", "6 months"],
                "answer": 0,
                "explanation": "Evidence 1 states the messages occurred over a 48-hour period."
            },
            {
                "text": "What public IP address represented the college hostel Wi-Fi gateway?",
                "options": ["103.21.144.10", "8.8.8.8", "1.1.1.1", "192.168.1.1"],
                "answer": 0,
                "explanation": "Evidence 2 records the hostel gateway IP as 103.21.144.10."
            },
            {
                "text": "Why is it important NOT to reply with insults or threats when receiving cyberbullying messages?",
                "options": [
                    "Replying escalates conflict, gives the bully satisfaction, and can muddy the legal evidence record",
                    "Replying uses up extra mobile phone battery",
                    "Replying breaks the smartphone screen",
                    "Replying is illegal under traffic laws"
                ],
                "answer": 0,
                "explanation": "Retaliation complicates investigations and may compromise victim status in disciplinary proceedings."
            },
            {
                "text": "What network service assigns IP addresses to devices connected to a hostel Wi-Fi router?",
                "options": ["DHCP (Dynamic Host Configuration Protocol)", "DNS", "FTP", "SMTP"],
                "answer": 0,
                "explanation": "DHCP dynamically leases IP addresses and maintains logs pairing IPs to device MAC addresses."
            },
            {
                "text": "Can using an anonymous social media handle completely hide your identity on a campus network?",
                "options": [
                    "No, network logs and DHCP lease records link connections to physical device hardware addresses",
                    "Yes, anonymous usernames make you 100% invisible to all routers",
                    "Yes, Wi-Fi routers cannot see anonymous accounts",
                    "Yes, usernames change the physical MAC address"
                ],
                "answer": 0,
                "explanation": "Underlying network transport packets carry source IP and MAC addresses regardless of application handle."
            },
            {
                "text": "What authority on a college campus should cyberbullying incidents be formally reported to?",
                "options": [
                    "College Disciplinary Committee, Anti-Ragging Cell, or Campus Security",
                    "The canteen food supplier",
                    "The campus bus driver",
                    "The local library gardener"
                ],
                "answer": 0,
                "explanation": "Formal reporting to Disciplinary Committees / Anti-Ragging Cells initiates institutional investigations."
            },
            {
                "text": "What does a MAC (Media Access Control) address represent on a computer?",
                "options": [
                    "A unique physical hardware identifier assigned to the network interface card",
                    "The student's college roll number",
                    "The password of the computer",
                    "The speed of the processor in gigahertz"
                ],
                "answer": 0,
                "explanation": "A MAC address is a 48-bit hardware identifier uniquely burned into physical network adapters."
            },
            # Tricky Q14
            {
                "text": "Why are timestamped screenshots more valuable than simple forwarded text in cyber investigations?",
                "options": [
                    "They preserve visual context, sender handle, profile pictures, and exact chronological timestamps",
                    "They take up less storage space on memory cards",
                    "They automatically delete the bully's social account",
                    "They prove the victim owns the social media company"
                ],
                "answer": 0,
                "explanation": "Screenshots provide forensic corroboration of exact usernames, interface elements, and timing."
            },
            # Tricky Q15
            {
                "text": "Even if an abuser deletes their account immediately after sending messages, can they still be identified?",
                "options": [
                    "Yes, server logs, gateway NAT records, and router DHCP history preserve connection records",
                    "No, deleting an account instantly erases all router and server logs worldwide",
                    "No, internet routers explode when an account is deleted",
                    "Only if the abuser confesses in person"
                ],
                "answer": 0,
                "explanation": "Network telemetry, router lease logs, and ISP connection records persist independently of user profile state."
            }
        ],
        "round2Questions": [
            # Round 2
            {
                "text": "What device hostname was identified in the DHCP lease table for MAC 'FC:FB:FB:12:34:56'?",
                "options": ["KARTHIK-DELL-G15", "VIKRAM-HP-LAPTOP", "STUDENT-PC-01", "HOSTEL-DESKTOP"],
                "answer": 0,
                "explanation": "Evidence 2 states the DHCP lease table recorded device hostname 'KARTHIK-DELL-G15'."
            },
            {
                "text": "What hardware manufacturer was identified by the MAC address Organizationally Unique Identifier (OUI)?",
                "options": ["Dell Inc.", "Apple Inc.", "Lenovo", "HP Inc."],
                "answer": 0,
                "explanation": "Evidence 2 identifies MAC address 'FC:FB:FB:12:34:56' as a Dell Inc. network interface."
            },
            {
                "text": "Which student and room number were tied to the physical hostel entry turnstile log?",
                "options": ["Karthik R (Room 304)", "Vikram K (Room 102)", "Ramesh P (Room 215)", "Suresh S (Room 401)"],
                "answer": 0,
                "explanation": "Evidence 1 confirms biometric turnstile logs for student 'Karthik R (Room 304)' entering Block-B."
            },
            {
                "text": "What burner email address was discovered in the browser cache SQLite artifacts?",
                "options": ["spectre_dark99@proton.me", "shadow_relay_99@proton.me", "drop_box_rec@proton.me", "dark_user@gmail.com"],
                "answer": 0,
                "explanation": "Evidence 3 identified creation of ProtonMail account 'spectre_dark99@proton.me'."
            },
            {
                "text": "How many minutes before the harassment began was the burner ProtonMail account created?",
                "options": ["20 minutes before", "2 days before", "5 hours before", "After the harassment ended"],
                "answer": 0,
                "explanation": "Evidence 3 notes the email was created '20 minutes before messages began'."
            },
            {
                "text": "What specific institutional policy rule was violated according to the evidence?",
                "options": [
                    "College IT Disciplinary Rule 4.2 (Prohibition of cyber harassment and anonymous intimidation)",
                    "Hostel Library Rule 1.1",
                    "Campus Parking Regulation 3",
                    "Dress Code Policy 5"
                ],
                "answer": 0,
                "explanation": "Evidence 4 cites College IT Disciplinary Rule 4.2 governing cyber harassment and campus network misuse."
            },
            {
                "text": "What is an OUI (Organizationally Unique Identifier) in digital forensics?",
                "options": [
                    "The first 3 bytes (24 bits) of a MAC address that identify the hardware vendor / manufacturer",
                    "The name of the user's internet service provider",
                    "The serial number of the computer screen",
                    "The version number of the web browser"
                ],
                "answer": 0,
                "explanation": "The first 24 bits of a MAC address designate the registered manufacturer (IEEE OUI)."
            },
            {
                "text": "Why do private/incognito browsing windows still leave forensic traces on local storage?",
                "options": [
                    "DNS resolver cache, crash dumps, and uncommitted SQLite journal buffers can persist in RAM and swap files",
                    "Incognito windows automatically print all history to paper",
                    "Incognito windows share history with all college classmates",
                    "Incognito mode only works on Sundays"
                ],
                "answer": 0,
                "explanation": "Private browsing prevents persistent history writes, but memory artifacts and DNS caches persist until reboot."
            },
            # Medium-Hard Q9-Q13
            {
                "text": "How does correlating physical turnstile logs with digital DHCP timestamps establish culprit attribution?",
                "options": [
                    "It proves the suspect was physically present inside the hostel while their registered laptop transmitted the packets",
                    "It proves the suspect owns an iPhone",
                    "It proves the hostel Wi-Fi was installed in 2026",
                    "It proves the student is good at video games"
                ],
                "answer": 0,
                "explanation": "Synthesizing physical access control with network telemetry eliminates alibis and ties user to hardware."
            },
            {
                "text": "What legal provisions under Indian Law apply to online stalking and intimidation of students?",
                "options": [
                    "Section 354D IPC (Stalking), Section 507 IPC (Criminal intimidation), and Section 66E/67 IT Act",
                    "Income Tax Act Section 80C",
                    "Customs Duty Act Section 14",
                    "Consumer Protection Act Section 2"
                ],
                "answer": 0,
                "explanation": "Criminal intimidation, cyber stalking, and electronic harassment are prosecutable offenses under the IPC and IT Act."
            },
            {
                "text": "Can MAC address spoofing be detected on an enterprise-managed wireless network?",
                "options": [
                    "Yes, 802.1X user authentication, switch port security, and 802.11 frame sequence tracking expose anomalies",
                    "No, spoofed MAC addresses are 100% undetectable by any equipment",
                    "Only if the computer is painted black",
                    "Only if the router has less than 4 antennas"
                ],
                "answer": 0,
                "explanation": "Enterprise wireless networks correlate WPA2-Enterprise credentials and sequence numbers, exposing MAC spoofing."
            },
            {
                "text": "What is the role of an Anti-Ragging / Disciplinary Committee during digital evidence review?",
                "options": [
                    "To review forensic evidence impartially, conduct fair hearings, and enforce institutional penalties or police referral",
                    "To delete all college computer files",
                    "To charge fines to all hostel students equally",
                    "To shut down the college for one year"
                ],
                "answer": 0,
                "explanation": "Disciplinary bodies evaluate evidence objectively, ensuring due process and proportionate sanctions."
            },
            {
                "text": "Why is preserving unedited original digital files critical for police evidence admissibility under legal standards?",
                "options": [
                    "To satisfy Certificate under Section 65B of the Indian Evidence Act (BSA Section 63) proving data integrity",
                    "Because police only accept printed color photographs",
                    "Because modified files cannot be opened by Microsoft Windows",
                    "Because judges only read documents in Latin"
                ],
                "answer": 0,
                "explanation": "Section 65B (now BSA Sec 63) mandates integrity verification for electronic records presented in court."
            },
            # Challenging Q14-Q15
            {
                "text": "Synthesizing the complete investigative dossier, what three independent evidence streams converge on the perpetrator?",
                "options": [
                    "Digital network logs (MAC/hostname), physical biometric turnstile entry, and local browser cache artifacts",
                    "Anonymous social media rumors, handwritten letters, and phone battery percentage",
                    "Classroom grades, sports medals, and library attendance",
                    "Weather reports, electricity bills, and cafeteria receipts"
                ],
                "answer": 0,
                "explanation": "Triangulating network telemetry, physical presence logs, and endpoint forensic artifacts establishes decisive proof."
            },
            {
                "text": "What institutional safeguards should the college implement to prevent malicious anonymous abuse of hostel networks?",
                "options": [
                    "Deploy 802.1X user-authenticated network access, enforce content safety policies, and conduct student digital ethics training",
                    "Completely disable Wi-Fi in all hostels permanently",
                    "Allow anyone to connect without any password or logging",
                    "Inspect all student phones manually every morning"
                ],
                "answer": 0,
                "explanation": "WPA2/WPA3-Enterprise 802.1X ties every connection to individual student credentials, eliminating anonymity on campus."
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
            # Round 1
            {
                "text": "What typosquatting trick was used in the URL 'www.arnazon-prime-offers.com'?",
                "options": [
                    "Using the letters 'rn' placed side-by-side to visually mimic the letter 'm'",
                    "Spelling Amazon backward",
                    "Replacing Amazon with Google",
                    "Using numbers instead of letters"
                ],
                "answer": 0,
                "explanation": "Evidence 1 states: 'utilizing letter combination rn to visually mimic the letter m in amazon'."
            },
            {
                "text": "How many days old was the fraudulent website domain according to the certificate info?",
                "options": ["3 days ago", "10 years ago", "500 days ago", "1 month ago"],
                "answer": 0,
                "explanation": "Evidence 2 states the domain was registered 3 days ago."
            },
            {
                "text": "What absurd price was advertised for the iPhone 15 Pro on the scam page?",
                "options": ["₹2,999 (90% discount)", "₹1,20,000", "₹80,000", "Free of cost"],
                "answer": 0,
                "explanation": "Evidence 3 indicates the page offered an 'iPhone 15 Pro for ₹2,999'."
            },
            {
                "text": "What happened to the countdown timer whenever the user refreshed the webpage?",
                "options": [
                    "It reset back to 15:00 every time the page was refreshed",
                    "It counted down to zero and locked the screen",
                    "It displayed the actual current time in Delhi",
                    "It disappeared completely"
                ],
                "answer": 0,
                "explanation": "Evidence 3 notes the artificial countdown timer resets to 15:00 on every browser page refresh."
            },
            {
                "text": "What legitimate payment system was completely bypassed at checkout?",
                "options": [
                    "Verified payment gateways (like Razorpay, BillDesk, or bank gateways)",
                    "Direct cash courier",
                    "Barter exchange system",
                    "Gold coin payment"
                ],
                "answer": 0,
                "explanation": "Evidence 4 records: 'Checkout completely bypasses verified payment gateways and demands direct peer-to-peer UPI transfer'."
            },
            {
                "text": "What did the scam checkout demand instead of a standard payment gateway?",
                "options": ["Direct peer-to-peer UPI transfer to an unverified private QR code", "Credit card with zero CVV", "Student roll number only", "Signing a paper receipt"],
                "answer": 0,
                "explanation": "Evidence 4 states checkout demands direct peer-to-peer UPI transfer to an unverified private QR code."
            },
            {
                "text": "What is this visual URL deception called when attackers register visually similar domains?",
                "options": ["Typosquatting / Combosquatting", "Cross-Site Scripting", "Buffer Overflow", "Ransomware"],
                "answer": 0,
                "explanation": "Registering misspelled or lookalike domain names to deceive users is known as typosquatting."
            },
            {
                "text": "Does having a padlock icon (HTTPS) guarantee that an online shopping site is 100% trustworthy?",
                "options": [
                    "No, HTTPS only means the connection is encrypted; anyone, including scammers, can get free SSL certificates",
                    "Yes, a padlock icon means the police have verified the website owner",
                    "Yes, scam websites are physically unable to use HTTPS",
                    "Yes, HTTPS guarantees you will receive your ordered products"
                ],
                "answer": 0,
                "explanation": "Free automated SSL (DV certificates) encrypt traffic, but provide zero validation of business legitimacy."
            },
            {
                "text": "What psychological tactic was the fake 15-minute countdown timer designed to trigger?",
                "options": [
                    "Artificial urgency and fear of missing out (FOMO) to prevent critical verification",
                    "Patience and relaxation",
                    "Scientific curiosity about clocks",
                    "Sleepiness"
                ],
                "answer": 0,
                "explanation": "Fake countdowns create urgency, rushing buyers into sending money before spotting anomalies."
            },
            {
                "text": "What is the official domain of Amazon in India?",
                "options": ["www.amazon.in", "www.arnazon-prime-offers.com", "www.amazon-cheap-sale.xyz", "www.amazon99.org"],
                "answer": 0,
                "explanation": "The official verified domain in India is 'www.amazon.in'."
            },
            {
                "text": "Why should users be suspicious of consumer electronic deals offering 90% discounts on brand new phones?",
                "options": [
                    "Brand new flagship smartphones are never sold at 90% below manufacturing cost by legitimate retailers",
                    "Because smartphones only cost ₹10 to manufacture",
                    "Because discounts are illegal in India",
                    "Because brand new phones can only be bought at physical post offices"
                ],
                "answer": 0,
                "explanation": "Dramatically below-cost pricing is a universal hallmark of e-commerce advance-fee fraud."
            },
            {
                "text": "What certificate authority issued the free 90-day DV certificate in the evidence?",
                "options": ["Let's Encrypt", "DigiCert Extended Validation", "VeriSign Global", "Government of India CA"],
                "answer": 0,
                "explanation": "Evidence 2 states the site used a 90-day free Let's Encrypt automated DV certificate."
            },
            {
                "text": "What should a shopper do if an online store demands payment to a private personal UPI QR code?",
                "options": [
                    "Do not pay; close the website and report the fake storefront",
                    "Send the payment immediately to secure the deal",
                    "Ask for a 50% discount on the UPI amount",
                    "Send an email asking for their personal address"
                ],
                "answer": 0,
                "explanation": "Legitimate e-commerce platforms never request peer-to-peer QR transfers; close and report the site."
            },
            # Tricky Q14
            {
                "text": "Why do typosquatters target fonts where 'rn' looks identical to 'm'?",
                "options": [
                    "In sans-serif fonts on mobile screens, the letters 'r' and 'n' merge visually to form 'm'",
                    "Because computer keyboards do not have the letter 'm'",
                    "Because mobile phones cannot display the letter 'r'",
                    "Because search engines rank 'rn' higher than 'm'"
                ],
                "answer": 0,
                "explanation": "Kerning in common sans-serif typography blends 'r' and 'n' into an apparent 'm' at standard viewing sizes."
            },
            # Tricky Q15
            {
                "text": "What is the critical difference between a Domain Validation (DV) certificate and an Extended Validation (EV) certificate?",
                "options": [
                    "DV only proves automated control of the domain name; EV requires rigorous legal business identity verification",
                    "DV certificates work only on computers, while EV works only on phones",
                    "DV certificates cost millions of dollars",
                    "There is no difference between SSL certificates"
                ],
                "answer": 0,
                "explanation": "Domain Validation checks only DNS control, whereas Extended Validation verifies organizational incorporation."
            }
        ],
        "round2Questions": [
            # Round 2
            {
                "text": "What IP address received the submitted credit card and billing credentials from the fake form?",
                "options": ["185.190.140.88", "172.67.182.20", "192.168.1.1", "10.0.0.1"],
                "answer": 0,
                "explanation": "Evidence 2 states the form action targeted 'http://185.190.140.88/collector/steal_creds.php'."
            },
            {
                "text": "What endpoint path was configured on the credential harvester server?",
                "options": ["/collector/steal_creds.php", "/api/login", "/payment/process", "/checkout/confirm"],
                "answer": 0,
                "explanation": "Evidence 2 shows form action targeting '/collector/steal_creds.php'."
            },
            {
                "text": "What technique did the scam website use to display authentic Amazon styling and high-resolution images?",
                "options": [
                    "Direct CDN hotlinking to legitimate Amazon servers in their HTML source",
                    "Hacking into Amazon's headquarters database",
                    "Taking pictures of laptop screens with a camera",
                    "Using artificial intelligence to draw logos"
                ],
                "answer": 0,
                "explanation": "Evidence 1 explains the site hotlinked CSS and product images directly from Amazon's genuine CDN."
            },
            {
                "text": "What JavaScript file generated the fake real-time purchase notification popups?",
                "options": ["social-proof.js", "analytics.js", "payment.js", "bootstrap.js"],
                "answer": 0,
                "explanation": "Evidence 3 identifies 'social-proof.js' containing hardcoded notification arrays."
            },
            {
                "text": "How frequently did the fake purchase popup trigger according to script analysis?",
                "options": ["Every 8 seconds", "Once a day", "Every 60 minutes", "Only when clicked"],
                "answer": 0,
                "explanation": "Evidence 3 states the script generated fake buyer alerts every 8 seconds."
            },
            {
                "text": "In which Caribbean jurisdiction was the domain registrar privacy service located?",
                "options": ["Saint Kitts and Nevis", "Bahamas", "Bermuda", "Jamaica"],
                "answer": 0,
                "explanation": "Evidence 4 records registration through a privacy provider based in Saint Kitts and Nevis."
            },
            {
                "text": "What psychological bias is exploited by automated 'social proof' purchase popups?",
                "options": [
                    "Herd mentality / Bandwagon effect (believing others are actively buying safely)",
                    "Visual contrast bias",
                    "Confirmation bias about battery life",
                    "Auditory memory"
                ],
                "answer": 0,
                "explanation": "Simulated buyer notifications exploit social proof, making prospective victims believe the site is popular and verified."
            },
            {
                "text": "How can web developers prevent rogue third-party sites from hotlinking their brand CDN assets?",
                "options": [
                    "Configure Cross-Origin Resource Sharing (CORS) and HTTP Referer access controls",
                    "Delete all images from the CDN",
                    "Make all images black and white",
                    "Disable the internet during the night"
                ],
                "answer": 0,
                "explanation": "Restricting CDN asset delivery based on HTTP Referer headers and CORS blocks hotlinking on rogue domains."
            },
            # Medium-Hard Q9-Q13
            {
                "text": "Why did the form action target an unencrypted HTTP URL ('http://185.190.140.88/...') despite the main site having SSL?",
                "options": [
                    "The scammers deployed cheap SSL on the landing page for visual trust, but exfiltrated data directly to a raw backend IP",
                    "Because credit card data cannot be sent over HTTPS",
                    "Because Russian servers do not support HTTPS",
                    "Because the victim's browser forced the change"
                ],
                "answer": 0,
                "explanation": "Mixed content often occurs in phishing templates where landing pages use free SSL, but backends listen on raw IPs."
            },
            {
                "text": "What browser security feature flags forms that submit sensitive data from HTTPS pages to insecure HTTP endpoints?",
                "options": [
                    "Mixed Content / Insecure Form Submission browser warnings",
                    "Screen brightness auto-adjust",
                    "Dark mode inverter",
                    "Pop-up blocker sound"
                ],
                "answer": 0,
                "explanation": "Modern browsers trigger 'Insecure form submission' warnings when HTTPS pages submit data to HTTP targets."
            },
            {
                "text": "What is the primary motive behind scammers purchasing domain registrations with anonymous cryptocurrency?",
                "options": [
                    "To prevent financial tracking and credit card identity linkage back to the perpetrator",
                    "Because registrars give a 90% discount for Bitcoin",
                    "Because domain names can only be bought with crypto",
                    "To speed up domain registration by 5 seconds"
                ],
                "answer": 0,
                "explanation": "Cryptocurrency transactions through non-KYC privacy registrars break the financial paper trail."
            },
            {
                "text": "How can a consumer verify whether a specific shopping website is legally affiliated with a major brand?",
                "options": [
                    "Navigate exclusively to verified official domains via bookmarks, official brand apps, or validated social handles",
                    "Ask the website's live chat operator if they are real",
                    "Check if the website has a copyright notice in the footer",
                    "Trust the website if it appears as a sponsored ad on search engines"
                ],
                "answer": 0,
                "explanation": "Direct navigation to primary verified corporate domains completely neutralizes lookalike typosquatting traps."
            },
            {
                "text": "What threat classification does Google Safe Browsing and Microsoft SmartScreen assign to this domain?",
                "options": [
                    "Deceptive Site / Phishing / Fraudulent Storefront warning",
                    "High Performance Website",
                    "Educational Resource",
                    "Government Verified Portal"
                ],
                "answer": 0,
                "explanation": "Safe Browsing engines flag typosquatted credential and payment harvesting domains as 'Deceptive Site Ahead'."
            },
            # Challenging Q14-Q15
            {
                "text": "Reconstructing the deceptive web page architecture, what four technical components created the illusion of legitimacy?",
                "options": [
                    "Typosquatted domain name, free DV SSL padlock, CDN hotlinked assets, and automated social proof popups",
                    "Physical retail store, television broadcast, printed newspaper coupon, and billboard ad",
                    "Database encryption, VPN tunnel, proxy gateway, and firewall configuration",
                    "Operating system kernel, graphics driver, sound card, and USB port"
                ],
                "answer": 0,
                "explanation": "The illusion combined typosquatting, SSL encryption, stolen CDN branding, and scripted purchase popups."
            },
            {
                "text": "What systemic domain governance measure can trademark owners employ to protect their consumers from typosquatting?",
                "options": [
                    "Defensive domain registration of common typos, Brand Protection monitoring, and filing UDRP domain disputes",
                    "Asking search engines to shut down the internet",
                    "Lowering prices of real products to match the scam",
                    "Suing all domain registrars in the world"
                ],
                "answer": 0,
                "explanation": "Brands protect customers via defensive registration of lookalikes, automated monitoring, and UDRP arbitration."
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
            # Round 1
            {
                "text": "What message appeared on the screen when the user attempted to log in?",
                "options": ["Password changed 2 hours ago", "Account deleted permanently", "Server under maintenance", "Incorrect username"],
                "answer": 0,
                "explanation": "Evidence 1 states the user was prompted: 'Password changed 2 hours ago'."
            },
            {
                "text": "What two digits did the attacker's new recovery phone number end in?",
                "options": ["XX89", "XX00", "XX12", "XX99"],
                "answer": 0,
                "explanation": "Evidence 1 specifies the recovery number was replaced with a number ending in 'XX89'."
            },
            {
                "text": "What hidden rule did the attacker configure inside the victim's inbox?",
                "options": [
                    "An auto-forwarding rule sending emails with 'bank', 'OTP', or 'statement' to an external mailbox",
                    "A rule that deletes all photos on the computer",
                    "A rule that translates all emails into German",
                    "A rule that prints every incoming email on paper"
                ],
                "answer": 0,
                "explanation": "Evidence 2 states the attacker created a filter forwarding banking and OTP emails."
            },
            {
                "text": "To which email address were incoming banking and OTP emails secretly forwarded?",
                "options": ["relay_drop77@proton.me", "admin@google.com", "student@college.edu", "helpdesk@yahoo.com"],
                "answer": 0,
                "explanation": "Evidence 2 identifies the forwarding address as 'relay_drop77@proton.me'."
            },
            {
                "text": "Where had the user logged into their email yesterday without using a VPN?",
                "options": ["An open, unencrypted coffee shop Wi-Fi network", "The college computer lab", "Their home broadband", "A police station network"],
                "answer": 0,
                "explanation": "Evidence 3 indicates the user connected on an open coffee shop Wi-Fi network without VPN."
            },
            {
                "text": "What fatal mistake did the user make when receiving repeated 2FA prompts on their phone?",
                "options": [
                    "Tapped 'Yes, it was me' to dismiss the annoying notifications",
                    "Turned off their phone screen",
                    "Blocked the number immediately",
                    "Called their college professor"
                ],
                "answer": 0,
                "explanation": "Evidence 4 records: 'accidentally tapped Yes, it was me to dismiss the annoying notifications'."
            },
            {
                "text": "What attack technique involves flooding a user with continuous 2FA prompts until they approve?",
                "options": ["MFA Fatigue / Prompt Bombing", "SQL Injection", "Buffer Overflow", "Cross-Site Scripting"],
                "answer": 0,
                "explanation": "Flooding authentication prompts to wear down victim patience is called MFA Fatigue or Prompt Bombing."
            },
            {
                "text": "Why is public, unencrypted Wi-Fi dangerous for sensitive account logins?",
                "options": [
                    "Anyone on the same local network can intercept unencrypted data packets and execute eavesdropping attacks",
                    "Public Wi-Fi charges ₹1,000 per minute",
                    "Public Wi-Fi disables the phone's battery",
                    "Public Wi-Fi only connects to foreign websites"
                ],
                "answer": 0,
                "explanation": "Open Wi-Fi transmits frames without local encryption, allowing neighboring devices to capture traffic."
            },
            {
                "text": "What tool encrypts your internet traffic when connecting to untrusted public Wi-Fi networks?",
                "options": ["A Virtual Private Network (VPN)", "A bigger computer screen", "A USB mouse", "A Bluetooth speaker"],
                "answer": 0,
                "explanation": "A VPN wraps internet traffic in an encrypted tunnel, protecting payloads from local network snoopers."
            },
            {
                "text": "What should you do if your phone suddenly receives 2FA push prompts that you did not initiate?",
                "options": [
                    "Tap 'NO, IT'S NOT ME', change your master password immediately, and review active sessions",
                    "Tap 'Yes' to make the prompt go away",
                    "Forward the prompt to friends",
                    "Turn the phone off and ignore it"
                ],
                "answer": 0,
                "explanation": "Unsolicited 2FA prompts prove someone knows your password; reject the prompt and reset credentials immediately."
            },
            {
                "text": "Why do attackers target a victim's primary email account first?",
                "options": [
                    "Primary email is the master key to reset passwords for banking, social media, and crypto accounts",
                    "To read the student's homework notes",
                    "Because email is the slowest internet service",
                    "Because email servers are turned off on weekends"
                ],
                "answer": 0,
                "explanation": "Most online platforms use email for password recovery; controlling email unlocks all linked services."
            },
            {
                "text": "What security mechanism requires you to enter a matching 2-digit number displayed on the login screen?",
                "options": ["Number Matching in Authenticator Apps", "Password hint", "Email signature", "Captcha audio"],
                "answer": 0,
                "explanation": "Number matching prevents blind approval by forcing the user to type the exact number shown on the login screen."
            },
            {
                "text": "What should the user check inside their email settings immediately after recovering access?",
                "options": [
                    "Filters & Forwarding rules, connected third-party apps, and recovery phone/email settings",
                    "The font size of the inbox",
                    "The color of the compose button",
                    "The total number of sent emails"
                ],
                "answer": 0,
                "explanation": "Auditing forwarding rules, authorized apps, and recovery contacts clears persistent attacker footholds."
            },
            # Tricky Q14
            {
                "text": "Why did the attacker create an auto-forwarding rule instead of simply checking the inbox manually?",
                "options": [
                    "Forwarding operates silently in the background, exfiltrating OTPs even if the attacker is not actively logged in",
                    "Email servers do not allow manual reading",
                    "Forwarding rules increase the speed of the internet",
                    "Attackers are not allowed to open web browsers"
                ],
                "answer": 0,
                "explanation": "Automated rules ensure immediate real-time exfiltration of critical verification codes without manual effort."
            },
            # Tricky Q15
            {
                "text": "What makes simple 'Yes/No' 2FA push notifications vulnerable compared to hardware FIDO2 security keys?",
                "options": [
                    "Push notifications can be accidentally approved under fatigue; FIDO2 hardware keys require physical touch and cryptographic origin binding",
                    "FIDO2 security keys require a phone number",
                    "Push notifications only work on desktop computers",
                    "Hardware keys are easily hacked over Wi-Fi"
                ],
                "answer": 0,
                "explanation": "Hardware tokens (FIDO2/WebAuthn) bind to domain origins cryptographically and cannot be tricked by push fatigue."
            }
        ],
        "round2Questions": [
            # Round 2
            {
                "text": "How many push authorization requests were flooded to the victim's phone in 8 minutes?",
                "options": ["42 requests", "2 requests", "500 requests", "10 requests"],
                "answer": 0,
                "explanation": "Evidence 1 logs 42 push authorization requests sent within an 8-minute window."
            },
            {
                "text": "What network attack was executed on the public coffee shop AP to intercept gateway traffic?",
                "options": ["ARP Cache Poisoning / ARP Spoofing", "DNS Amplification", "BGP Hijacking", "SQL Injection"],
                "answer": 0,
                "explanation": "Evidence 2 confirms an active ARP cache poisoning attack redirecting gateway traffic."
            },
            {
                "text": "What MAC address was identified as the rogue attacker device poisoning the coffee shop ARP table?",
                "options": ["B8:27:EB:11:22:33 (Raspberry Pi Foundation)", "00:11:22:33:44:55", "AA:BB:CC:DD:EE:FF", "FC:FB:FB:12:34:56"],
                "answer": 0,
                "explanation": "Evidence 2 identifies rogue MAC 'B8:27:EB:11:22:33'."
            },
            {
                "text": "How quickly after the email takeover were password resets initiated for banking and crypto accounts?",
                "options": ["Within 45 minutes", "After 2 weeks", "After 1 year", "Never"],
                "answer": 0,
                "explanation": "Evidence 3 states password resets were initiated within 45 minutes of email takeover."
            },
            {
                "text": "What rogue application token was generated by the attacker to retain API persistence?",
                "options": ["SyncHelper_v1 (OAuth 2.0 offline refresh token)", "CryptoMiner_v2", "EmailViewer_App", "BackupHelper_v9"],
                "answer": 0,
                "explanation": "Evidence 4 records: 'generated an OAuth 2.0 offline refresh token for rogue client SyncHelper_v1'."
            },
            {
                "text": "How does ARP Cache Poisoning allow an attacker on local Wi-Fi to intercept network traffic?",
                "options": [
                    "By broadcasting forged ARP replies linking the router's IP to the attacker's MAC address, making traffic route through them",
                    "By physically cutting the internet cable with scissors",
                    "By changing the Wi-Fi password for all users",
                    "By turning off the coffee shop electricity"
                ],
                "answer": 0,
                "explanation": "Forged ARP responses associate the gateway IP with the adversary's MAC, enabling Man-in-the-Middle eavesdropping."
            },
            {
                "text": "Why does an OAuth 2.0 offline refresh token provide persistent access even after a password reset?",
                "options": [
                    "Refresh tokens remain valid until explicitly revoked in third-party connected app security settings",
                    "Refresh tokens are stored on the user's SIM card",
                    "Refresh tokens never expire on Google servers",
                    "Passwords have no relationship to email security"
                ],
                "answer": 0,
                "explanation": "OAuth tokens authenticate via API scopes independently of account password hashes until explicitly revoked."
            },
            {
                "text": "What hardware device is identified by the MAC OUI prefix 'B8:27:EB'?",
                "options": ["Raspberry Pi Foundation", "Cisco Systems", "Apple Inc.", "Intel Corporation"],
                "answer": 0,
                "explanation": "The OUI prefix 'B8:27:EB' is registered to the Raspberry Pi Foundation, commonly used for compact rogue drops."
            },
            # Medium-Hard Q9-Q13
            {
                "text": "What feature introduced in Microsoft Authenticator and Google Prompts specifically defeats MFA fatigue?",
                "options": [
                    "Number Matching (requiring the user to enter the 2-digit number shown on the login terminal)",
                    "Louder ringtones",
                    "Flashing phone screen colors",
                    "Vibrating every 2 seconds"
                ],
                "answer": 0,
                "explanation": "Number matching requires looking at the login screen, stopping victims from approving remote prompt floods."
            },
            {
                "text": "Why did the attacker pivot to password resets on cryptocurrency and banking services immediately?",
                "options": [
                    "Financial accounts often use email verification as the primary recovery channel for account takeovers",
                    "Because email servers are connected to bank vaults",
                    "Because banks require email accounts to open on Sundays",
                    "To send holiday greetings to bank managers"
                ],
                "answer": 0,
                "explanation": "Email control enables adversaries to trigger automated reset workflows and intercept security tokens."
            },
            {
                "text": "How can users detect hidden mailbox rules in Outlook or Gmail web settings?",
                "options": [
                    "Navigate to Settings -> Mail -> Rules / Filters and check for forwarding conditions matching keywords like OTP/Bank",
                    "Check the desktop recycling bin",
                    "Restart the computer 3 times",
                    "Change the email font to italics"
                ],
                "answer": 0,
                "explanation": "Reviewing Rules/Filters reveals unauthorized routing directives forwarding traffic to external drops."
            },
            {
                "text": "What is the primary network defense that protects users from ARP poisoning on public hotspots?",
                "options": [
                    "Using a reliable encrypted VPN tunnel or enforcing Wireless Client Isolation on the access point",
                    "Turning down computer volume",
                    "Disabling Bluetooth",
                    "Using the browser in full screen mode"
                ],
                "answer": 0,
                "explanation": "VPNs encrypt layer-3 payloads, rendering layer-2 ARP interception useless to local eavesdroppers."
            },
            {
                "text": "What does 'Client Isolation' do when configured on an enterprise coffee shop Wi-Fi network?",
                "options": [
                    "It prevents wireless clients from communicating with or eavesdropping on each other on the local subnet",
                    "It disconnects all users after 10 minutes",
                    "It blocks all websites except news portals",
                    "It charges a fee for using Wi-Fi"
                ],
                "answer": 0,
                "explanation": "Client Isolation blocks peer-to-peer communication among hotspot users, stopping ARP poisoning."
            },
            # Challenging Q14-Q15
            {
                "text": "Reconstructing the attacker's multi-stage kill chain, what was the sequential progression of the attack?",
                "options": [
                    "Coffee shop ARP poisoning -> Credentials intercepted -> 42 MFA fatigue prompts -> Recovery phone changed -> Forwarding rule created -> Linked banking resets",
                    "Linked banking resets -> Forwarding rule created -> 42 MFA fatigue prompts -> ARP poisoning",
                    "Forwarding rule created -> 42 MFA fatigue prompts -> Linked banking resets -> ARP poisoning",
                    "ARP poisoning -> Forwarding rule created -> Linked banking resets -> 42 MFA fatigue prompts"
                ],
                "answer": 0,
                "explanation": "The attack progressed from local interception, credential acquisition, MFA fatigue approval, persistence, to financial pivot."
            },
            {
                "text": "What comprehensive response protocol is necessary to fully evict the adversary from the compromised account ecosystem?",
                "options": [
                    "Revoke all active sessions, reset password, update recovery phone, delete forwarding rules, revoke OAuth app tokens, and contact banks",
                    "Simply change the password on the phone and do nothing else",
                    "Close the browser tab and restart the computer",
                    "Delete all emails in the inbox"
                ],
                "answer": 0,
                "explanation": "Complete eviction requires password reset, session termination, recovery channel audit, OAuth token revocation, and bank notifications."
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
            # Round 1
            {
                "text": "What size of confidential archives was downloaded from the internal fileserver?",
                "options": ["2.4 GB", "50 MB", "100 GB", "500 KB"],
                "answer": 0,
                "explanation": "Evidence 1 states 2.4 GB of confidential faculty archives were downloaded."
            },
            {
                "text": "At what day and time did the suspicious file transfer occur?",
                "options": ["Sunday at 01:22 AM UTC", "Monday at 10:00 AM UTC", "Friday at 03:00 PM UTC", "Wednesday at 12:00 PM UTC"],
                "answer": 0,
                "explanation": "Evidence 1 records the transfer on Sunday at 01:22 AM UTC."
            },
            {
                "text": "Whose user account credentials were used to authenticate the access?",
                "options": ["Former intern 'sanjay_intern'", "College Principal", "Head of Department", "Guest Wi-Fi user"],
                "answer": 0,
                "explanation": "Evidence 2 states access authenticated using credentials of former IT intern 'sanjay_intern'."
            },
            {
                "text": "How long ago did the intern's contract with the college end?",
                "options": ["3 months ago", "Yesterday", "10 years ago", "1 week ago"],
                "answer": 0,
                "explanation": "Evidence 2 notes the intern's contract ended 3 months ago."
            },
            {
                "text": "What institutional failure allowed the former intern to still log into the network?",
                "options": [
                    "Failure to deprovision or disable the account during the offboarding process",
                    "The intern hacked NASA satellites",
                    "The college server was infected with a hardware virus",
                    "The intern bought the college domain name"
                ],
                "answer": 0,
                "explanation": "Evidence 3 reveals HR and IT failed to disable or deprovision the account upon departure."
            },
            {
                "text": "What network tool was used to connect remotely to the internal college network from home?",
                "options": ["Campus Virtual Private Network (VPN)", "Bluetooth", "HDMI cable", "FM Radio transmitter"],
                "answer": 0,
                "explanation": "Evidence 4 records a VPN connection initiated from home residential broadband."
            },
            {
                "text": "What residential IP address initiated the remote VPN connection?",
                "options": ["122.164.89.200", "192.168.1.1", "10.0.0.1", "127.0.0.1"],
                "answer": 0,
                "explanation": "Evidence 4 identifies residential broadband IP 122.164.89.200."
            },
            {
                "text": "What type of confidential files were exfiltrated in the transfer?",
                "options": ["Faculty evaluation archives", "Public cafeteria food menus", "Sports field booking calendar", "Library book titles"],
                "answer": 0,
                "explanation": "Evidence 1 states the archive contained confidential faculty evaluation archives."
            },
            {
                "text": "Why is an offboarding checklist mandatory in enterprise and institutional IT governance?",
                "options": [
                    "To ensure departing personnel have all access tokens, accounts, and VPN keys revoked immediately",
                    "To print goodbye cards for departing staff",
                    "To give departing staff free software licenses",
                    "To delete all college student emails"
                ],
                "answer": 0,
                "explanation": "Offboarding protocols ensure comprehensive credential and access revocation upon employee separation."
            },
            {
                "text": "What term describes accounts belonging to former employees that remain active in the system?",
                "options": ["Dormant / Orphan accounts", "Superuser accounts", "Guest accounts", "Admin root accounts"],
                "answer": 0,
                "explanation": "Unmanaged active accounts belonging to departed users are called orphan or dormant accounts."
            },
            {
                "text": "Why was downloading data at 01:22 AM on Sunday an immediate behavioral red flag?",
                "options": [
                    "It was outside normal college working hours on a weekend, indicating stealth off-hours access",
                    "Because internet connections do not work on Sundays",
                    "Because all files downloaded at night are automatically corrupted",
                    "Because servers are only allowed to send data during morning hours"
                ],
                "answer": 0,
                "explanation": "Large data transfers during off-peak weekend hours diverge significantly from normal behavioral baselines."
            },
            {
                "text": "What security principle dictates that interns should only have access to data required for their specific tasks?",
                "options": ["Principle of Least Privilege", "Principle of Maximum Access", "Open Door Policy", "Public Access Rule"],
                "answer": 0,
                "explanation": "Least Privilege ensures users are granted only the minimum permissions necessary to perform their roles."
            },
            {
                "text": "What immediate technical action should IT take upon discovering the rogue transfer?",
                "options": [
                    "Immediately disable the intern account, terminate the active VPN tunnel, and preserve server audit logs",
                    "Wait 2 weeks to see if more files are downloaded",
                    "Send an email asking the intern why they downloaded the files",
                    "Format the entire college fileserver"
                ],
                "answer": 0,
                "explanation": "Immediate containment requires account suspension, VPN session kill, and forensic log preservation."
            },
            # Tricky Q14
            {
                "text": "Why are former employees with retained access classified as an 'Insider Threat'?",
                "options": [
                    "They possess legitimate credentials, understand internal network topography, and know where valuable data is stored",
                    "They are physically inside the building at all times",
                    "They are exempt from all cyber laws",
                    "They cannot be detected by antivirus scanners"
                ],
                "answer": 0,
                "explanation": "Departed insiders possess institutional knowledge and valid credentials, bypassing perimeter defenses."
            },
            # Tricky Q15
            {
                "text": "What is the primary operational distinction between an account compromise and an offboarding failure?",
                "options": [
                    "In an offboarding failure, legitimate credentials remain valid due to administrative negligence rather than external hacking",
                    "Account compromise only happens on Linux",
                    "Offboarding failure means the server was physically stolen",
                    "There is no difference; they are identical"
                ],
                "answer": 0,
                "explanation": "Offboarding failures stem from administrative gaps where valid credentials were simply never revoked."
            }
        ],
        "round2Questions": [
            # Round 2
            {
                "text": "What high-privilege Active Directory security group did the intern add themselves to before departure?",
                "options": ["Faculty-Archive-Admins", "Domain Admins", "Enterprise Admins", "Print Operators"],
                "answer": 0,
                "explanation": "Evidence 1 states the intern added themselves to 'Faculty-Archive-Admins'."
            },
            {
                "text": "What Windows Event ID explicitly logs the addition of a user to a security-enabled global group?",
                "options": ["Event ID 4728", "Event ID 4624", "Event ID 7045", "Event ID 1102"],
                "answer": 0,
                "explanation": "Evidence 1 cites Event ID 4728 ('A member was added to a security-enabled global group')."
            },
            {
                "text": "What Windows command-line utility was used to copy the directories recursively?",
                "options": ["robocopy", "copy", "xcopy", "ftp"],
                "answer": 0,
                "explanation": "Evidence 2 documents execution of 'robocopy \\\\fileserver\\confidential\\evaluations C:\\temp\\exfil /E /Z /R:1 /W:1'."
            },
            {
                "text": "What Windows utility was executed to attempt clearing the Security audit log?",
                "options": ["wevtutil cl Security", "del C:\\Windows\\System32\\winevt\\Logs", "clear-eventlog", "net stop eventlog"],
                "answer": 0,
                "explanation": "Evidence 3 identifies 'wevtutil cl Security' command executed to wipe security logs."
            },
            {
                "text": "What Windows Event ID is generated when an administrator or attacker clears the security log?",
                "options": ["Event ID 1102 ('The audit log was cleared')", "Event ID 4624", "Event ID 4672", "Event ID 6005"],
                "answer": 0,
                "explanation": "Evidence 3 notes clearing generated Event ID 1102, creating explicit forensic proof of tamper."
            },
            {
                "text": "To which cloud locker service was the 2.4 GB encrypted container exfiltrated?",
                "options": ["Mega.nz", "Google Drive", "Dropbox", "OneDrive"],
                "answer": 0,
                "explanation": "Evidence 4 records outbound upload to anonymous file storage host Mega.nz."
            },
            {
                "text": "How many days before the intern contract concluded did the unauthorized group addition occur?",
                "options": ["4 days before", "30 days before", "On the day of the download", "2 months after departure"],
                "answer": 0,
                "explanation": "Evidence 1 states the addition occurred 4 days before their contract concluded."
            },
            {
                "text": "What software was used to compress and password-protect the exfiltrated directory?",
                "options": ["7-Zip", "WinRAR", "Tar", "Gzip"],
                "answer": 0,
                "explanation": "Evidence 2 states the copy was followed by 7-Zip password-protected compression."
            },
            # Medium-Hard Q9-Q13
            {
                "text": "Why did the attacker's attempt to clear the audit log using 'wevtutil' fail to cover their tracks?",
                "options": [
                    "Clearing the security log automatically writes a tamper-evident Event ID 1102 with the executing username and timestamp",
                    "Windows does not allow event logs to be cleared",
                    "Event logs are printed on paper automatically",
                    "The command shut down the computer"
                ],
                "answer": 0,
                "explanation": "Windows explicitly logs Event ID 1102 whenever the security log is wiped, preserving the perpetrator's identity."
            },
            {
                "text": "What data egress monitoring tool should have alerted on a 2.4 GB outbound upload to Mega.nz?",
                "options": [
                    "Data Loss Prevention (DLP) / Cloud Access Security Broker (CASB)",
                    "Antivirus software",
                    "DHCP server",
                    "Local display driver"
                ],
                "answer": 0,
                "explanation": "DLP and CASB systems detect and block anomalous bulk data transfers to unauthorized cloud storage lockers."
            },
            {
                "text": "Why should temporary intern accounts always have hard expiration dates configured in Active Directory?",
                "options": [
                    "Account expiration automatically disables the account on the set date regardless of manual HR offboarding oversights",
                    "It makes the computer run 50% faster",
                    "It prevents the intern from using the college library",
                    "It deletes all files created by the intern"
                ],
                "answer": 0,
                "explanation": "Setting account expiration dates ensures automatic deactivation even if HR forgets to submit tickets."
            },
            {
                "text": "What SIEM (Security Information and Event Management) alert rule would have flagged the privilege escalation immediately?",
                "options": [
                    "Real-time alert on Event ID 4728 monitoring changes to privileged administrative groups",
                    "An alert on mouse clicks per minute",
                    "A rule checking monitor screen resolution",
                    "An alert on daily printer paper usage"
                ],
                "answer": 0,
                "explanation": "Monitoring Event ID 4728 alerts security teams whenever accounts are added to sensitive security groups."
            },
            {
                "text": "What legal liability does a former intern face for unauthorized data exfiltration under cyber law?",
                "options": [
                    "Criminal prosecution under IT Act Section 43/66 (unauthorized data extraction, breach of confidentiality) and IPC/BNS",
                    "A certificate in advanced ethical hacking",
                    "Automatic promotion to senior system administrator",
                    "No liability because they had an account previously"
                ],
                "answer": 0,
                "explanation": "Accessing computer systems without authorization violates IT Act Sec 43/66, carrying prison terms and damages."
            },
            # Challenging Q14-Q15
            {
                "text": "Reconstructing the attacker's complete methodology, what were the four distinct phases of the intrusion?",
                "options": [
                    "Pre-departure privilege escalation (AD group addition) -> Post-departure off-hours VPN login -> Robocopy bulk extraction & log wipe -> Encrypted cloud exfiltration",
                    "Encrypted cloud exfiltration -> Robocopy extraction -> Privilege escalation -> VPN login",
                    "VPN login -> Encrypted cloud exfiltration -> Privilege escalation -> Robocopy extraction",
                    "Robocopy extraction -> Privilege escalation -> VPN login -> Encrypted cloud exfiltration"
                ],
                "answer": 0,
                "explanation": "The timeline proves: group addition 4 days prior, VPN entry at 01:22, robocopy/tamper at 01:24-01:28, and cloud upload at 01:32."
            },
            {
                "text": "What organizational and technical reforms are required to permanently prevent similar insider breaches?",
                "options": [
                    "Automated HR-IT offboarding deprovisioning, mandatory AD account expiration, MFA on VPN, and DLP egress blocking",
                    "Prohibiting all internships across the entire university",
                    "Deleting all administrative groups from Active Directory",
                    "Turning off the campus VPN server completely"
                ],
                "answer": 0,
                "explanation": "Preventing insider leaks requires syncing HR offboarding with automated IAM, enforcing account expirations, and DLP."
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
            # Round 1
            {
                "text": "How much money did the customer pay for the gaming laptop that never arrived?",
                "options": ["₹12,000", "₹1,00,000", "₹500", "₹5,000"],
                "answer": 0,
                "explanation": "Evidence 2 states the customer paid ₹12,000."
            },
            {
                "text": "Where did the victim originally encounter the fraudulent storefront advertisement?",
                "options": ["A sponsored Instagram social media ad", "A physical newspaper flyer", "A television commercial", "The college library notice board"],
                "answer": 0,
                "explanation": "Evidence 1 states the victim clicked an Instagram sponsored ad."
            },
            {
                "text": "What discount percentage was advertised to lure the buyer?",
                "options": ["80% discount", "5% discount", "No discount", "10% discount"],
                "answer": 0,
                "explanation": "Evidence 1 specifies an impossible 80% discount."
            },
            {
                "text": "What happened when the customer attempted to email customer support?",
                "options": [
                    "The email bounced back with 'Address not found'",
                    "Support replied with a full refund in 5 minutes",
                    "Support scheduled a phone call",
                    "The email was forwarded to the college dean"
                ],
                "answer": 0,
                "explanation": "Evidence 3 notes customer support email bounced with 'Address not found'."
            },
            {
                "text": "What VPA received the victim's ₹12,000 payment?",
                "options": ["gadget_hub_corp@ybl", "amazon_pay@sbi", "flipkart_hub@icici", "canteen@axis"],
                "answer": 0,
                "explanation": "Evidence 2 states the payment was sent to VPA 'gadget_hub_corp@ybl'."
            },
            {
                "text": "How quickly was the money withdrawn at an ATM after the customer transferred it?",
                "options": ["10 minutes later", "3 months later", "It was never withdrawn", "After 2 weeks"],
                "answer": 0,
                "explanation": "Evidence 2 states the funds were instantly withdrawn via ATM 10 minutes later."
            },
            {
                "text": "How old was the online shop's domain name according to WHOIS records?",
                "options": ["5 days old", "10 years old", "500 days old", "1 year old"],
                "answer": 0,
                "explanation": "Evidence 4 records the storefront domain was registered 5 days ago."
            },
            {
                "text": "What was the status of the customer care phone number when dialed?",
                "options": ["Permanently switched off", "Answered by friendly staff", "Connected to a bank manager", "Voicemail with return details"],
                "answer": 0,
                "explanation": "Evidence 3 states the phone number was permanently switched off."
            },
            {
                "text": "What payment method on legitimate e-commerce sites provides the best fraud protection for buyers?",
                "options": [
                    "Cash on Delivery (COD) or Verified Payment Gateways with buyer protection policies",
                    "Direct advance UPI to personal phone numbers",
                    "Gift card codes sent over chat",
                    "Cash sent in paper envelopes"
                ],
                "answer": 0,
                "explanation": "Cash on Delivery and reputable payment gateways provide buyer protection against fake storefronts."
            },
            {
                "text": "Does an ad appearing on Instagram or Facebook mean the seller is verified and genuine?",
                "options": [
                    "No, anyone can pay to run sponsored ads on social platforms without thorough product vetting",
                    "Yes, social media companies physically inspect every product before showing an ad",
                    "Yes, sponsored ads are guaranteed by the government",
                    "Yes, ads can only be created by licensed retail stores"
                ],
                "answer": 0,
                "explanation": "Social ad networks do not manually vet retail merchandise; scammers routinely pay for sponsored ads."
            },
            {
                "text": "What fake store name was used in the sponsored ad?",
                "options": ["NextGen-Electronics-Store", "Official Apple Store", "BestBuy India", "Amazon Super Store"],
                "answer": 0,
                "explanation": "Evidence 1 states the ad was from 'NextGen-Electronics-Store'."
            },
            {
                "text": "What top-level domain (TLD) extension was used for the customer support email?",
                "options": [".shop", ".com", ".gov.in", ".edu"],
                "answer": 0,
                "explanation": "Evidence 3 identifies 'support@nextgen-store.shop'."
            },
            {
                "text": "What should a victim do immediately after realizing they were defrauded by a fake online shop?",
                "options": [
                    "File an immediate complaint on the National Cybercrime Portal (cybercrime.gov.in) and report the transaction to their bank",
                    "Wait 30 days for the laptop to arrive",
                    "Order another laptop from the same website",
                    "Delete all receipts and text messages"
                ],
                "answer": 0,
                "explanation": "Reporting promptly to cybercrime.gov.in and the bank's fraud desk initiates fund tracking."
            },
            # Tricky Q14
            {
                "text": "Why do fraudulent stores withdraw money via physical ATMs almost immediately?",
                "options": [
                    "To prevent banks from placing an electronic freeze or lien on the account once the victim reports fraud",
                    "Because digital bank accounts cannot hold money overnight",
                    "Because ATMs give cash bonuses for fast withdrawals",
                    "To pay taxes to the government immediately"
                ],
                "answer": 0,
                "explanation": "Rapid cash withdrawal drains electronic accounts before victims realize the fraud and notify fraud desks."
            },
            # Tricky Q15
            {
                "text": "Why is customer review verification outside the seller's website critical before making online purchases?",
                "options": [
                    "On-site reviews can be fabricated by the scammers; independent consumer complaint portals expose real fraud reports",
                    "Reviews on the seller's site are verified by court judges",
                    "Independent portals are illegal in India",
                    "Reviews cannot be typed on mobile phones"
                ],
                "answer": 0,
                "explanation": "Scammers post fake positive reviews on their own pages; external forums reveal genuine complaints."
            }
        ],
        "round2Questions": [
            # Round 2
            {
                "text": "How did the fake package tracking page 'nextgen-track.com' simulate package movement?",
                "options": [
                    "Using client-side JavaScript math to display synthetic GPS checkpoints advancing every 4 hours automatically",
                    "Connecting to satellite tracking antennas",
                    "Calling the courier driver every 10 minutes",
                    "Displaying real-time drone video feeds"
                ],
                "answer": 0,
                "explanation": "Evidence 1 notes the fake tracking page displayed synthetic GPS checkpoints advancing via client-side JavaScript."
            },
            {
                "text": "Whose identity was used to open the fraudulent bank account that received the ₹12,000?",
                "options": [
                    "A compromised rural account holder whose KYC documents were stolen during a microloan scam (money mule)",
                    "The scammer's real legal personal bank account",
                    "The college principal's account",
                    "A fictitious account created without any documents"
                ],
                "answer": 0,
                "explanation": "Evidence 2 states the account belonged to a rural mule whose KYC documents were stolen in a loan scam."
            },
            {
                "text": "How was the sponsored Instagram ad campaign financed by the scammers?",
                "options": [
                    "From a hacked third-party business ad account funded by compromised corporate credit cards",
                    "With official bank loans",
                    "Instagram runs all shopping ads for free",
                    "With cash paid at the Instagram headquarters"
                ],
                "answer": 0,
                "explanation": "Evidence 3 indicates the campaign was launched from a hacked business ad account with stolen credit cards."
            },
            {
                "text": "How many similar fake storefront campaigns was the VPA 'gadget_hub_corp@ybl' linked to over 90 days?",
                "options": ["48 similar campaigns across 6 states", "Only this 1 campaign", "1,000,000 campaigns", "Zero campaigns"],
                "answer": 0,
                "explanation": "Evidence 4 records: 'linked to 48 similar fake storefront campaigns across 6 states over the past 90 days'."
            },
            {
                "text": "What is the primary function of a 'synthetic tracking page' in an e-commerce scam?",
                "options": [
                    "To delay the victim from reporting fraud to their bank for several days by showing fake 'in-transit' progress",
                    "To help the delivery driver find the address",
                    "To speed up airplane flights",
                    "To calculate courier fuel taxes"
                ],
                "answer": 0,
                "explanation": "Fake tracking portals pacify victims, letting scammers cash out and discard domains before complaints arise."
            },
            {
                "text": "What does 'KYC' stand for in banking and financial account regulation?",
                "options": ["Know Your Customer", "Keep Your Cash", "Key Yield Calculation", "Knowledge Year Credit"],
                "answer": 0,
                "explanation": "KYC (Know Your Customer) mandates verifying identity and address documentation for bank account holders."
            },
            {
                "text": "Why do cybercrime syndicates steal rural citizens' identity documents to create bank accounts?",
                "options": [
                    "To create disposable mule accounts that insulate the real syndicate leaders from police arrests",
                    "Because rural accounts have unlimited free international wires",
                    "Because rural accounts cannot be frozen by courts",
                    "Because rural citizens own all the ATMs"
                ],
                "answer": 0,
                "explanation": "Exploiting vulnerable individuals creates insulating layer accounts, diverting police scrutiny to innocent mules."
            },
            {
                "text": "What domain name was used to host the fake shipment tracking system?",
                "options": ["nextgen-track.com", "dhl.com", "fedex.com", "indiapost.gov.in"],
                "answer": 0,
                "explanation": "Evidence 1 specifies fake tracking domain 'nextgen-track.com'."
            },
            # Medium-Hard Q9-Q13
            {
                "text": "Why are social media platforms targeted by ad-account hijackers for scam distribution?",
                "options": [
                    "Hijacked ad accounts have verified billing history and high daily spending limits, evading new-account review algorithms",
                    "Social platforms have no users",
                    "Social platforms do not support video ads",
                    "Hijacked ad accounts can only run ads for laptops"
                ],
                "answer": 0,
                "explanation": "Aged, compromised corporate ad accounts bypass security filters and burn through credit before owners notice."
            },
            {
                "text": "How do cybercrime investigators correlate disparate scam campaigns to a single syndicate?",
                "options": [
                    "By cross-referencing shared VPAs, IFSC bank codes, registrar email addresses, and server hosting subnets",
                    "By looking at the color of the website buttons",
                    "By checking if the website font is Arial or Times New Roman",
                    "By measuring the size of the product photographs"
                ],
                "answer": 0,
                "explanation": "Shared payment handles, bank account clusters, WHOIS registrants, and C2 IPs connect serial campaigns."
            },
            {
                "text": "What is the role of an ATM CCTV footage audit in unmasking money mule cash-out networks?",
                "options": [
                    "It captures timestamped physical facial imagery and vehicle details of the runner withdrawing cash",
                    "It tests the clarity of ATM glass doors",
                    "It checks if the ATM keypad needs cleaning",
                    "It calculates how many bank customers visit each day"
                ],
                "answer": 0,
                "explanation": "CCTV logs tied to transaction timestamps provide physical visual identification of cash-out runners."
            },
            {
                "text": "What consumer protection regulation in India requires e-commerce entities to display nodal grievance officers?",
                "options": [
                    "Consumer Protection (E-Commerce) Rules, 2020",
                    "Factories Act of 1948",
                    "Merchant Shipping Act",
                    "Motor Vehicles Amendment Act"
                ],
                "answer": 0,
                "explanation": "The E-Commerce Rules (2020) mandate publishing registered business details, addresses, and grievance officers."
            },
            {
                "text": "How can prospective buyers verify whether an e-commerce website was registered only 5 days ago?",
                "options": [
                    "By checking domain creation dates on ICANN WHOIS lookup portals",
                    "By checking the battery percentage on their smartphone",
                    "By converting the webpage to a PDF",
                    "By checking the weather forecast"
                ],
                "answer": 0,
                "explanation": "ICANN WHOIS lookup displays exact domain creation dates, revealing disposable 5-day-old storefronts."
            },
            # Challenging Q14-Q15
            {
                "text": "Reconstructing the syndicated shopping fraud operation, what were the four key components of the criminal enterprise?",
                "options": [
                    "Hacked ad accounts for reach -> Disposable 5-day lookalike storefront -> Synthetic tracking page -> Stolen-KYC mule bank accounts with rapid ATM cash-out",
                    "Physical retail store -> TV advertising -> Post office delivery -> Government bank wire",
                    "Local Wi-Fi snooping -> Ransomware encryption -> Bitcoin ransom -> Decryption key",
                    "Social engineering phone call -> Desktop virus -> Hardware repair -> Invoice billing"
                ],
                "answer": 0,
                "explanation": "The enterprise synthesized ad hijacking, disposable storefronts, synthetic tracking, and rural mule cash-out infrastructure."
            },
            {
                "text": "What multi-agency coordination strategy is required to dismantle this 48-campaign fraud network?",
                "options": [
                    "Inter-state cyber police coordination, nodal bank account freezing, registrar domain takedowns, and social platform ad-fraud reporting",
                    "Asking students to avoid using the internet",
                    "Banning all online shopping in the country",
                    "Changing the currency notes again"
                ],
                "answer": 0,
                "explanation": "Dismantling serial syndicates requires law enforcement coordination, bank nodal freezes, domain takedowns, and ad platform remediation."
            }
        ]
    }
}
