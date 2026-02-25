from crewai import Task
from agents import financial_analyst, verifier, risk_assessor, investment_advisor


# 1️⃣ Document Verification Task
verification_task = Task(
    description="""
    Step 1: Document Validation

    Access the document located at {document_text}.
    Determine whether it is a financial report.

    Look for:
    - Financial statements (Income Statement, Balance Sheet, Cash Flow)
    - Revenue, expenses, profit figures
    - Financial terminology

    If it is not a financial document, clearly state that.
    Do not fabricate interpretation.
    """,
    expected_output="""
    Output Format:
    - Document Type:
    - Is Financial Report (Yes/No):
    - Brief Justification:
    """,
    agent=verifier,
)


# 2️⃣ Financial Analysis Task
analysis_task = Task(
    description="""
    Step 2: Financial Analysis

    Using the verified financial document at {document_text},
    extract factual financial data.

    Focus on:
    - Revenue trends
    - Net income
    - Operating expenses
    - Assets and liabilities
    - Cash flow position

    Then address the user query: {query}

    Only use data explicitly found in the document.
    If information is missing, state it clearly.
    """,
    expected_output="""
    Output Format:
    1. Executive Summary
    2. Key Financial Metrics
    3. Observed Trends
    4. Strengths
    5. Weaknesses
    """,
    agent=financial_analyst,
)


# 3️⃣ Risk Assessment Task
risk_task = Task(
    description="""
    Step 3: Risk Evaluation

    Based on the financial analysis results,
    assess financial and operational risks.

    Evaluate:
    - Debt exposure
    - Liquidity risk
    - Revenue volatility
    - Cash flow stability

    Avoid exaggeration.
    Do not introduce external assumptions.
    """,
    expected_output="""
    Provide structured risk assessment:
    
    1. Financial Risks (with reference to actual metrics)
    2. Operational Risks (if mentioned in document)
    3. Liquidity Risk
    4. Overall Risk Rating (Low / Medium / High)
    5. Justification using document data    
    """,
    agent=risk_assessor,
)


# 4️⃣ Investment Recommendation Task
investment_task = Task(
    description="""
    Step 4: Investment Outlook

    Using the financial analysis and risk assessment,
    provide a balanced and realistic investment outlook.

    Consider:
    - Financial health
    - Risk exposure
    - Stability of earnings

    Do not guarantee profits.
    Do not use extreme language.
    """,
    expected_output="""
    Provide a structured investment recommendation with:

    1. Executive Summary (2-3 sentences summarizing company performance)

    2. Key Financial Highlights
       - Total Revenue (latest quarter)
       - Net Income
       - Operating Margin
       - Free Cash Flow
       - Cash Position

    3. Risk Considerations
       - Revenue trends
       - Margin compression
       - Cash flow sustainability
       - Macroeconomic risks

    4. Investment Outlook
       - Outlook Category (Positive / Neutral / Cautious)
       - Clear reasoning referencing financial metrics
       - Suggested strategy (Long-term / Hold / Avoid)
    
    Strictly reference financial figures from the document.
    Do not fabricate numbers.
    Avoid generic statements.
    """,
    agent=investment_advisor,
)