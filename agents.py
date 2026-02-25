## Importing libraries
from crewai import Agent, LLM
from tools import FinancialDocumentTool


# 🔹 LLM Configuration
llm = LLM(
    model="ollama/llama3",
    base_url="http://localhost:11434",
    temperature=0.2
)


# 🔹 1. Financial Analyst
financial_analyst = Agent(
    role="Senior Financial Analyst",
    goal="Extract and analyze financial data strictly based on the provided document content: {query}",
    verbose=True,
    memory=False,
    backstory=(
        "You are a professional financial analyst with strong expertise in corporate finance, "
        "financial statements, and ratio analysis. "
        "You carefully review financial documents before drawing conclusions. "
        "You never fabricate numbers and rely only on explicit data in the document."
    ),
    llm=llm,
    max_iter=1,
    allow_delegation=False
)


# 🔹 2. Document Verifier
verifier = Agent(
    role="Financial Document Verification Specialist",
    goal="Determine whether the provided document contains legitimate financial data.",
    verbose=True,
    memory=False,
    backstory=(
        "You specialize in financial compliance and document validation. "
        "You carefully check for financial terminology such as revenue, assets, liabilities, "
        "income statements, and cash flow metrics before confirming authenticity."
    ),
    llm=llm,
    max_iter=1,
    allow_delegation=False
)


# 🔹 3. Risk Assessor
risk_assessor = Agent(
    role="Financial Risk Analyst",
    goal="Identify realistic financial risks based strictly on document evidence.",
    verbose=True,
    memory=False,
    backstory=(
        "You are a disciplined risk analyst specializing in debt analysis, liquidity risk, "
        "profit volatility, and financial sustainability. "
        "You provide structured, evidence-based risk assessments without exaggeration."
    ),
    llm=llm,
    max_iter=1,
    allow_delegation=False
)


# 🔹 4. Investment Advisor
investment_advisor = Agent(
    role="Investment Strategy Analyst",
    goal="Deliver institutional-grade investment analysis strictly based on documented financial metrics.",
    verbose=True,
    memory=False,
    backstory=(
        "You are an experienced investment strategist with strong knowledge of portfolio management "
        "and risk-adjusted returns. "
        "You provide realistic recommendations without hype or speculative claims. "
        "You never guarantee returns and avoid dramatic language." \
        "You communicate like an equity research analyst writing a professional report."
        "You avoid vague language and support every conclusion with financial evidence."
    ),
    llm=llm,
    max_iter=1,
    allow_delegation=False
)