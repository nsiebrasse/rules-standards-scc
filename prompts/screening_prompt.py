# File: screening_prompt.py
# A dedicated, simple prompt for the one-time case informativeness screening.

def get_screening_prompt(full_text: str, parq_row: int) -> str:
    """
    Generates a simple, direct prompt to classify a case as informative or not.

    Args:
        full_text: The complete text of the SCC decision.
        parq_row: The unique ParqRow identifier for the case.

    Returns:
        A formatted prompt string.
    """
    
    prompt = f"""
        You are a legal research assistant. For context, the objective of the project you are a part of will is to compare two Supreme Court of Canada (SCC) appeal decisions to see whether the key legal test in one is more or less rule-like than the key legal test in the other. 
        That comparison will be carried out solely on the basis of the decision itself, without any extrinsic aids (without a web search, without knowledge of the decision below, without the knowledge of any subsequent commentary, and without any other source expect the full text of the decision as scraped from the Supreme Court website.)
        Further, the comparison will focus on the reasons for decision; the headnote should not be considered.

        Your specific task right now is to help pre-screen the cases to determine if the decision contains enough substantive reasoning to be usefully analysed in this comparison. 
        For example, sometimes the SCC will dismiss an appeal in a single sentence: "The appeal is dismissed substantially for the reasons of the Court of Appeal." 
        Without knowledge of the decision below, this does not allow us to determine whether the SCC was endorsing a rule or a standard. 
        Sometimes the SCC will also add some brief remarks. For example, one decision was as follows:
            "Lamer C.J. ‑‑ We are all of the view that this appeal fails.  We agree with the Court of Appeal's conclusion that this legislation can be construed and was properly construed as being of strict liability.  The existence of a restriction to s. 11(d) is governed by this Court's decision in R. v. Wholesale Travel Group Inc., [1991] 3 S.C.R. 154. 
            The section 1 analysis in Wholesale is applicable here, as there is no difference of substance between the nature of the legislation in that case and this one."
        This is still not nearly enough to decide whether the SCC is endorsing a rule or a standard.
        Brief reasons are not suitable for analysis even if they include a brief description of the facts and conclusion drawn from the decision below. 
        The overarching question is whether the reasons of the SCC are sufficiently developed to identify the legal test. 
        It is not necessary for you to assess whether the test is a more like a rule or a more like a standard. 
        At this point, your only goal is to assess whether the decision contains a test which is is amenable to subsequent analysis.
        
        Read the case text provided below and assess whether the decision contains a test which is is amenable to subsequent analysis.
        You may answer "Yes", "No" or "Uncertain." 

        ***OUTPUT INSTRUCTIONS***
        Your final output must be a single, valid JSON object and nothing else. Do not wrap it in markdown.
        Adhere strictly to the following JSON schema:
        {{
          "ParqRow": {parq_row},
          "is_informative": "Yes"
        }}
        ***CASE TEXT***
        {full_text}
    """
    return prompt
