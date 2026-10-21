import re
from typing import Any

from .database import fetch_questions

IOB_HOME = "https://www.iob.bank.in/en/"
MSME_URL = "https://www.iob.bank.in/en/msme"
MSME_EASY_URL = "https://www.iob.bank.in/en/iob-msme-easy"

STRUCTURED_KNOWLEDGE: dict[str, dict[str, Any]] = {
    "business_loan": {
        "question": "What is a business loan?",
        "answer": "A business loan is money borrowed to fund eligible business expenses such as working capital, machinery, inventory, expansion, or cash-flow support. Terms depend on the lender, scheme, and borrower profile.",
        "source_url": MSME_URL,
        "category": "business_loan",
        "requires_current_verification": False,
        "matches": ["business loan", "loan for business", "borrow for business"],
    },
    "msme_loan": {
        "question": "What is an MSME loan?",
        "answer": "An MSME loan is financing for eligible micro, small, and medium enterprises. It may support working capital, equipment purchases, business expansion, or other approved business needs.",
        "source_url": MSME_URL,
        "category": "msme_loan",
        "requires_current_verification": False,
        "matches": ["msme loan", "micro small medium enterprise", "small business loan"],
    },
    "business_loan_interest": {
        "question": "What is the interest rate for a business loan?",
        "answer": "The applicable rate depends on the scheme, the borrower profile, and current bank policy. Check the official IOB scheme page or branch for the current rate before relying on a value.",
        "source_url": MSME_URL,
        "category": "interest_rate",
        "requires_current_verification": True,
        "matches": ["interest rate", "rate of interest", "roi", "business loan interest"],
    },
    "business_loan_documents": {
        "question": "What documents are required for a business loan?",
        "answer": "Common documents may include PAN, identity proof, address proof, business registration documents, GST or tax records if applicable, financial statements, bank statements, and any scheme-specific documents requested by the lender.",
        "source_url": MSME_URL,
        "category": "documents",
        "requires_current_verification": False,
        "matches": ["documents", "required documents", "document checklist", "business loan documents"],
    },
    "business_loan_eligibility": {
        "question": "Who can apply for a business loan?",
        "answer": "Eligibility varies by scheme and lender. Applicants may include individual entrepreneurs, proprietors, partnerships, LLPs, private limited companies, and other eligible business entities, subject to registration, turnover, credit profile, and documentation checks.",
        "source_url": MSME_EASY_URL,
        "category": "eligibility",
        "requires_current_verification": False,
        "matches": ["eligibility", "who can apply", "eligible applicant", "new business loan"],
    },
    "account_breakdown": {
        "question": "Explain my account breakdown.",
        "answer": "Illustrative example: opening balance is ₹20,000, total credits are ₹15,000, total debits are ₹8,000, and closing balance is ₹27,000. The formula is Closing balance = Opening balance + Total credits − Total debits. This example is for understanding only; actual user data must come from an authorised account-data source.",
        "source_url": IOB_HOME,
        "category": "account_breakdown",
        "requires_current_verification": False,
        "matches": ["account breakdown", "opening balance", "closing balance", "transaction summary"],
    },
    "debit_credit_percentages": {
        "question": "How do I calculate debit and credit percentages?",
        "answer": "Using the illustrative example above, total credits are ₹15,000 and total debits are ₹8,000. Credit percentage = Credits ÷ (Credits + Debits) × 100 = 65.22%. Debit percentage = Debits ÷ (Credits + Debits) × 100 = 34.78%. These percentages reflect transaction activity share, not savings rate.",
        "source_url": IOB_HOME,
        "category": "account_analysis",
        "requires_current_verification": False,
        "matches": ["debit percentage", "credit percentage", "debits and credits", "percentage of activity"],
    },
    "fees_and_penalties": {
        "question": "Why am I paying fees and penalties on my account?",
        "answer": "Fees and penalties may come from service charges, transaction charges, minimum-balance charges, late-payment charges, loan processing fees, or prepayment or foreclosure charges. The exact charge depends on the account product, the associated schedule of charges, and the current bank policy.",
        "source_url": IOB_HOME,
        "category": "account_fees",
        "requires_current_verification": True,
        "matches": ["fees", "penalties", "charges", "late payment fee", "loan processing fee"],
    },
    "savings_guidance": {
        "question": "How can I save money each month?",
        "answer": "A simple sample monthly budget is: essentials 50% (₹15,000), savings 20% (₹6,000), lifestyle 20% (₹6,000), and emergency or irregular expenses 10% (₹3,000). This is an illustrative example, not personalised advice; actual allocations depend on rent, debt, dependants, and obligations.",
        "source_url": IOB_HOME,
        "category": "savings_advice",
        "requires_current_verification": False,
        "matches": ["savings", "save money", "monthly budget", "how can i save"],
    },
}


def normalize_text(value: str) -> str:
    return re.sub(r"[^a-z0-9\s]", " ", value.lower()).strip()


def is_percentage_distribution_request(question: str) -> bool:
    text = normalize_text(question)
    if not text:
        return False

    has_percentage_word = any(
        keyword in text
        for keyword in [
            "percentage",
            "percent",
            "distribution",
            "share",
            "split",
        ]
    )
    has_breakdown_word = any(
        keyword in text
        for keyword in [
            "breakdown",
            "opening balance",
            "closing balance",
        ]
    )
    has_financial_word = any(
        keyword in text
        for keyword in [
            "debit",
            "credit",
            "fee",
            "fees",
            "penalty",
            "penalties",
            "transaction",
            "statement",
            "account",
        ]
    )
    return (has_percentage_word and has_financial_word) or (has_breakdown_word and has_financial_word and any(keyword in text for keyword in ["debit", "credit", "fee", "fees", "penalty", "penalties", "transaction", "statement"]))


def build_account_breakdown(question: str) -> dict[str, Any] | None:
    text = normalize_text(question)
    if not (
        is_percentage_distribution_request(question)
        or "account breakdown" in text
        or "opening balance" in text
        or "closing balance" in text
    ):
        return None

    if is_percentage_distribution_request(question):
        chart = {
            "title": "Percentage distribution of account activity",
            "items": [
                {"label": "Debits", "value": 42, "color": "#ef4444"},
                {"label": "Credits", "value": 35, "color": "#22c55e"},
                {"label": "Fees", "value": 15, "color": "#f59e0b"},
                {"label": "Penalties", "value": 8, "color": "#a855f7"},
            ],
        }
        answer = (
            "Here is an illustrative percentage breakdown: 42% debits, 35% credits, 15% fees, and 8% penalties. "
            "These values reflect transaction activity share, not the savings rate. "
            "For a bank-specific review, validate the latest statement details and fee schedule with the official IOB service channels."
        )
        return {
            "question": question,
            "answer": answer,
            "category": "account_breakdown",
            "source_url": IOB_HOME,
            "confidence": 100,
            "chart": chart,
        }

    answer = (
        "Illustrative account example: opening balance ₹20,000, total credits ₹15,000, total debits ₹8,000, closing balance ₹27,000. "
        "Calculation: Closing balance = Opening balance + Total credits − Total debits. "
        "This is an example for understanding only. A real customer balance must come from an authorised account-data source."
    )

    return {
        "question": question,
        "answer": answer,
        "category": "account_breakdown",
        "source_url": IOB_HOME,
        "confidence": 100,
    }


def build_fee_explanation(question: str) -> dict[str, Any]:
    return {
        "question": question,
        "answer": (
            "Fees and penalties may come from account maintenance, transaction fees, minimum-balance charges, late-payment charges, loan processing fees, or prepayment or foreclosure charges. "
            "The exact amount depends on the account type, scheme, and the current official schedule of charges. Always verify the current fee schedule with the official IOB service terms or branch before treating it as final."
        ),
        "category": "account_fees",
        "source_url": IOB_HOME,
        "confidence": 92,
    }


def build_savings_guidance(question: str) -> dict[str, Any]:
    return {
        "question": question,
        "answer": (
            "A simple example budget for ₹30,000 monthly income is: essentials 50% (₹15,000), savings 20% (₹6,000), lifestyle 20% (₹6,000), and emergency or irregular expenses 10% (₹3,000). "
            "This is illustrative and not a personalised recommendation. Actual allocations depend on rent, debt repayments, dependants, and obligations."
        ),
        "category": "savings_advice",
        "source_url": IOB_HOME,
        "confidence": 89,
    }


def retrieve_structured_knowledge(question: str) -> dict[str, Any] | None:
    text = normalize_text(question)
    if not text:
        return None

    if "interest rate" in text or "rate of interest" in text or "roi" in text:
        if not any(term in text for term in ["business loan", "msme", "loan scheme", "personal loan", "term loan", "business", "small business"]):
            return {
                "question": question,
                "answer": (
                    "Which loan scheme do you mean: business loan, MSME loan, or another product? Once you confirm the scheme, I can explain the relevant rate and remind you to verify the current official IOB rate before applying."
                ),
                "category": "clarification_required",
                "source_url": MSME_URL,
                "confidence": 95,
            }

    best_entry = None
    best_score = -1
    for key, entry in STRUCTURED_KNOWLEDGE.items():
        score = 0
        for phrase in [entry["question"], *entry.get("matches", [])]:
            normalized_phrase = normalize_text(phrase)
            if not normalized_phrase:
                continue
            if normalized_phrase in text:
                score += 6
            for token in normalized_phrase.split():
                if len(token) < 3:
                    continue
                if token in text.split():
                    score += 2
        if score > best_score:
            best_score = score
            best_entry = entry.copy()
            best_entry["_match_key"] = key

    if best_entry is None or best_score <= 0:
        return None

    if best_entry.get("requires_current_verification"):
        best_entry["answer"] = (
            best_entry["answer"]
            + " The information needs current verification before it is used as a final rate, fee, or rule for a specific customer."
        )

    return {
        "question": question,
        "answer": best_entry["answer"],
        "category": best_entry["category"],
        "source_url": best_entry.get("source_url") or IOB_HOME,
        "confidence": min(best_score * 10, 100),
    }


def build_official_loan_answer(question: str) -> dict[str, Any] | None:
    text = normalize_text(question)
    if not text:
        return None

    if "interest rate" in text or "rate of interest" in text or "roi" in text:
        if not any(term in text for term in ["business loan", "msme", "loan scheme", "personal loan", "term loan", "business", "small business"]):
            return {
                "question": question,
                "answer": (
                    "Which loan scheme do you mean: business loan, MSME loan, or another product? Once you confirm the scheme, I can explain the relevant rate and remind you to verify the current official IOB rate before applying."
                ),
                "category": "clarification_required",
                "source_url": MSME_URL,
                "confidence": 95,
            }

    if "business loan" in text or "loan for business" in text:
        return {
            "question": question,
            "answer": (
                "A business loan is money borrowed to fund eligible business needs such as working capital, equipment, inventory, expansion, or cash-flow support. "
                "The exact terms depend on the lender, loan scheme, and borrower profile. For official IOB sources, please check the MSME portal and the relevant scheme page."
            ),
            "category": "business_loan",
            "source_url": MSME_URL,
            "confidence": 96,
        }

    if "msme" in text or "micro small medium" in text or "small business loan" in text:
        return {
            "question": question,
            "answer": (
                "An MSME loan is financing for eligible micro, small, and medium enterprises. It may support working capital, equipment purchases, expansion, or other business needs. "
                "IOB provides MSME financing options, including the MSME Easy scheme, subject to scheme conditions and verification. Official information: https://www.iob.bank.in/en/msme and https://www.iob.bank.in/en/iob-msme-easy"
            ),
            "category": "msme_loan",
            "source_url": MSME_URL,
            "confidence": 97,
        }

    if "eligibility" in text or "who can apply" in text or "eligible" in text:
        if "business" in text or "loan" in text or "msme" in text:
            return {
                "question": question,
                "answer": (
                    "Eligibility varies by lender and scheme. Applicants may include proprietors, partnership firms, LLPs, private limited companies, or other eligible business entities, subject to registration, turnover, financial profile, and documentation checks. "
                    "For MSME-specific requirements, confirm the current IOB scheme terms on the official website before applying."
                ),
                "category": "eligibility",
                "source_url": MSME_EASY_URL,
                "confidence": 96,
            }

    if "document" in text or "documents" in text or "required documents" in text:
        if "business" in text or "loan" in text or "msme" in text:
            return {
                "question": question,
                "answer": (
                    "Commonly requested documents may include PAN, identity proof, address proof, business registration documents, GST or tax records if applicable, financial statements, bank statements, and any lender-specific documents. "
                    "The exact checklist depends on scheme requirements and the borrowing profile. The final list should be confirmed on the official IOB scheme page."
                ),
                "category": "documents",
                "source_url": MSME_URL,
                "confidence": 95,
            }

    if "interest rate" in text or "rate of interest" in text or "roi" in text:
        if "business" in text or "loan" in text or "msme" in text:
            return {
                "question": question,
                "answer": (
                    "The applicable rate depends on the specific scheme, borrower profile, and current bank policy. Do not treat a single rate as universal. Check the current official IOB page or a branch before relying on any figure."
                ),
                "category": "interest_rate",
                "source_url": MSME_URL,
                "confidence": 94,
            }

    if "fee" in text or "fees" in text or "penalty" in text or "penalties" in text or "charges" in text:
        return build_fee_explanation(question)

    if "savings" in text or "save money" in text or "save more" in text or "savings options" in text:
        return build_savings_guidance(question)

    return None


def score_question_match(user_question: str, row: dict[str, Any]) -> int:
    text = normalize_text(user_question)
    question = normalize_text(row["question"])
    keywords = normalize_text(row.get("keywords", ""))

    score = 0
    if question and question in text:
        score += 5

    for token in text.split():
        if len(token) < 3:
            continue
        if token in question or token in keywords:
            score += 2

    return score


def find_best_answer(user_question: str):
    breakdown_response = build_account_breakdown(user_question)
    if breakdown_response is not None:
        return breakdown_response

    structured_response = retrieve_structured_knowledge(user_question)
    if structured_response is not None:
        return structured_response

    official_response = build_official_loan_answer(user_question)
    if official_response is not None:
        return official_response

    rows = fetch_questions()
    if not rows:
        return None

    best_row = None
    best_score = -1

    for row in rows:
        score = score_question_match(user_question, row)
        if score > best_score:
            best_score = score
            best_row = row

    if best_row is None or best_score <= 0:
        return None

    return {
        "question": best_row["question"],
        "answer": best_row["answer"],
        "category": best_row["category"],
        "source_url": best_row.get("source_url") or IOB_HOME,
        "confidence": min(best_score * 20, 100),
    }
