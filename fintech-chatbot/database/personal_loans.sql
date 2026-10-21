INSERT INTO questions (question, answer, category, keywords, source_url, last_verified_at)
SELECT 'What is the eligibility for a personal loan?',
       'According to the official IOB personal loan information, employees in government, public sector undertakings, reputed private enterprises, firms, companies and similar organizations may be eligible if they are confirmed in service, and the take-home pay after deducting the proposed loan installment should be more than 50% of gross pay. LIC agents may also be eligible subject to conditions. This answer is educational and not an official IOB service channel; please verify current policy on the official website before applying.',
       'personal_loan_eligibility',
       'personal loan eligibility, take home pay, government employee, PSU, lic agent, confirmed employee',
       'https://www.iob.bank.in/en/',
       '2026-10-15'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE question = 'What is the eligibility for a personal loan?');

INSERT INTO questions (question, answer, category, keywords, source_url, last_verified_at)
SELECT 'What is the maximum loan amount for personal loans?',
       'According to the official IOB personal loan information, for Category A and B borrowers, the eligible loan amount is up to 25/20 times of gross monthly salary or Rs 30.00 Lakhs, whichever is lower. For Category C borrowers, it is up to 10 times of gross monthly salary or Rs 15.00 Lakhs, whichever is lower. These figures are taken from the official published product information and should be rechecked on IOB''s current page before relying on them for an application.',
       'personal_loan_limit',
       'personal loan amount, max loan limit, category a, category b, category c, gross monthly salary',
       'https://www.iob.bank.in/en/',
       '2026-10-15'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE question = 'What is the maximum loan amount for personal loans?');

INSERT INTO questions (question, answer, category, keywords, source_url, last_verified_at)
SELECT 'What is the repayment period for a personal loan?',
       'The official IOB personal loan information states the maximum repayment period is 84 months. This value is educational and should be confirmed against the latest official scheme page before making a decision.',
       'personal_loan_repayment',
       'repayment period, tenure, personal loan maximum months, 84 months, EMI term',
       'https://www.iob.bank.in/en/',
       '2026-10-15'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE question = 'What is the repayment period for a personal loan?');

INSERT INTO questions (question, answer, category, keywords, source_url, last_verified_at)
SELECT 'What documents are required for a personal loan?',
       'The official document list includes the application form, salary certificate of the applicant and guarantor with deduction details, undertaking letter from the employer to deduct monthly instalment and recover dues from terminal benefits if required, and applicable application or online submission process. This is an educational summary based on official source content and not a substitute for final bank verification.',
       'personal_loan_documents',
       'documents required, personal loan documents, employer undertaking, salary certificate, guarantor, application form',
       'https://www.iob.bank.in/en/',
       '2026-10-15'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE question = 'What documents are required for a personal loan?');

INSERT INTO questions (question, answer, category, keywords, source_url, last_verified_at)
SELECT 'What are the security requirements for a personal loan?',
       'The official IOB personal loan policy states that Category A requires irrevocable PDC/ECS/SI. Category B requires employer undertaking to deduct the EMI or salary transfer with irrevocable standing instruction. Category C requires a single third-party guarantee whose salary is equal to or more than that of the borrower, or joint guarantee of two guarantors whose combined gross salary exceeds the borrower''s gross salary. This is a source-based explanation and must be confirmed on the official page before use.',
       'personal_loan_security',
       'security, PDC, ECS, standing instruction, guarantor, employer undertaking',
       'https://www.iob.bank.in/en/',
       '2026-10-15'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE question = 'What are the security requirements for a personal loan?');
