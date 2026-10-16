def get_prompt(fulltext1, fulltext2, subjects1: list, subjects2: list, parqrow1: int, parqrow2: int):
    
# This is the working prompt with the GAMMA_results argument removed
    string = f"""
            ***INTRODUCTION***
            You are a research assistant. Your task is to compare two Supreme Court of Canada (SCC) decisions to see whether the key legal test in one is more or less rule-like than the key legal test in the other. 

            To perform this task, you will need three sets of guidelines:
            • ALPHA (Important Test) Guidelines, which will instruct you how to identify the most important test in the decision
            • BETA (Test Breakdown) Guidelines, which will instruct you how to characterize the most important test
            • GAMMA (Rule Standard) Guidelines, which will instruct you how to decide how rule-like the test is 
            The guidelines will be provided after this Introduction and the Final Output instructions.

            For each decision, you will be provided with:
              the full text of the decision;
              a unique ParqRow number, which will also appear in the output; and
              a list of subjects associated with the decision.
            This case information will be provided after the guidelines.

            Use the following scale to quantify the result of your comparison of the two cases:
            • 2: "Test A is substantially more rule-like than Test B."
            • 1: "Test A is slightly more rule-like than Test B."
            •  0: "Tests are approximately equal in rule-likeness."
            • -1: "Test A is slightly more standard-like than Test B."
            • -2: "Test A is substantially more standard-like than Test B."

            After analyzing each decision, select the subject for each case that most accurately describes the legal area of the specific test you identified as being most importat.

            ***FINAL OUTPUT***
            When returning the output for each comparison, adhere to the format set out in this section. Do not deviate from this output structure. Do not return any additional output.

            Your final output must be a single, valid JSON object and nothing else. Do not wrap it in markdown or any other text.
            Your output must include the ParqRow numbers for Decision A and Decision B, as shown in the format below. For both the ParqRow number and the score, substitute the actual integer values for the examples.
            
            Adhere strictly to the following JSON schema:
            {{
              "testA": {{
                "ParqRow": 7236,
                "name": "The name or concise summary of legal Test A.",
                "subject": "The chosen subject for Test A from its provided list.",
                "baseline": "The baseline for Test A (e.g., common law, statute)."
                "judge": "The name of the judge or entity (e.g., the Court) who wrote the reasons containing legal Test A)."
              }},
              "testB": {{
                "ParqRow": 865,
                "name": "The name or concise summary of legal Test B.",
                "subject": "The chosen subject for Test B from its provided list.",
                "baseline": "The baseline for Test B (e.g., common law, statute)."
                "judge": "The name of the judge or entity (e.g., the Court) who wrote the reasons containing legal Test B)."
              }},
              "comparison": {{
                "score": 2,
                "description": "The description corresponding to the numerical score from the scale."
              }}
            }}
            
            
            ***BEGINNING OF ALPHA (Important Test) GUIDELINES***

            You are a research assistant. These guidelines will help you identify the most important legal tests in SCC decisions. Consider the entire set of guidelines as you analyze the decisions.

            # Application Instructions
            1. Begin by identifying specific tests formulated or applied in the decision.
            2. Determine which tests were actually applied to resolve the case.
            3. Evaluate which tests received the most thorough explanation and application.
            4. Assess which tests represent significant developments in the law.
            5. Focus on tests that can be broken down into specific components for comparison.
            6. Distinguish between the conceptual issue being addressed and the specific test used to resolve it.

            # Factors for Identifying Important Legal Tests
            ## 1. Development, Refinement, and SCC Signaling of Test Importance
            • Introduction of a new legal test or analytical framework.
            • Significant modification of an existing test.
            • Clarification of how a test should be applied in specific contexts.
            • Adoption of a test from another jurisdiction.
            • Explicit statements that the SCC is addressing an unsettled question.
            • References to disagreement in lower courts that the decision aims to resolve.
            • Language indicating the SCC is establishing a new approach or modifying existing principles.
            • SCC's characterization of its analysis as clarifying or breaking new ground.
            • SCC's explanation of how its approach differs from previous cases.
            • Explicit overruling or modification of prior approaches.
            • SCC's framing of the test's relationship to existing jurisprudence.
            • Engagement with competing principles or values within the test.
            • Balancing of conflicting legal, social, or policy considerations in test design.
            ## 2. Distinguishing Development from Summarization
            • Carefully distinguish between when the SCC is developing or modifying a test versus merely summarizing existing law.
            • Pay attention to qualifying language that signals novel contribution (e.g., "we hold that," "we establish," "we reject the previous approach") versus summarization (e.g., "it is well established," "as previously stated").
            • Note attribution practices; direct quotations from earlier cases without modification signals less doctrinal development. 
            • Look for indications that the SCC is addressing an unsettled question or resolving conflicting approaches.
            • Consider whether a test is being applied in a novel context, even if the test itself is not new.
            • Identify the specific contested question that wasn't clearly answered by existing precedent.
            ## 3. Assessing Framework-Component Relationships
            • When evaluating tests with both an overarching framework and constituent components, assess the novelty and significance of each separately:
            • The framework may be new while components are established (e.g., reorganizing existing legal principles into a new structured approach).
            • Components may be new while the framework is established (e.g., adding a new factor to an existing multi-factor test).
            • Both framework and components may be independently novel (e.g., introducing both a new analytical structure and new substantive elements).
            • Different components within the same framework may have different scopes of application or levels of significance.
            • A component may function as an independent test in some contexts while serving as part of a larger framework in others.
            • Where significant novelty exists in both a framework and one or more of its components, consider whether each should be ranked separately based on their individual jurisprudential significance rather than treating the entire structure as a single test.
            • Pay attention to the SCC's discussion of when and how components apply, especially if certain components are applicable only in specific contexts while the framework applies more broadly.
            ## 4. Focus of Separate Opinions on the Test
            • Whether concurring or dissenting opinions focus on this specific test.
            • Points of strongest agreement or disagreement among the judges about the test.
            • Significant debate within the SCC about the test's formulation or application.
            • When judges disagree about a particular test, this often signals doctrinal significance regardless of length of discussion.
            • Areas of disagreement between majority and dissent often highlight where the law is being developed or clarified.
            ## 5. Depth of Treatment and Prominence in Decision
            • Amount of space devoted to explaining and applying the test.
            • Detail in the SCC's reasoning when working through the test.
            • Thoroughness of the SCC's engagement with each element of the test.
            • Emphasis on the test in the headnote or summary provided within the decision itself.
            • Placement of the test in the table of contents or issue statement (if present).
            • Prominence of the test in the introduction or conclusion of the judgment.
            ## 6. Explicit Test Formulation by the SCC
            • Direct articulation of a specific test, framework, or set of criteria.
            • Language signaling the introduction of a test (e.g., "The test to be applied is").
            • Structured presentation of elements, factors, or steps in an analysis.
            ## 7. Actual Application of the Test
            • Evidence that the SCC actually applied the test to the facts of the case.
            • Detailed explanation of how the test operates in practice.
            • Demonstration of how the test resolves the legal question at issue.
            • Identification of which test was dispositive or determinative of the outcome.
            • When a test affects the outcome, this often indicates importance, but even tests not affecting the outcome may be doctrinally significant.
            ## 8. Potential Breadth of Application of the Test
            • Whether the test addresses a matter with wide-ranging implications.
            • Applicability of the test to a variety of factual situations.
            • Relevance to frequently litigated areas of law.
            • Cross-cutting nature (applies across multiple legal domains).
            ## 9. Consider Document Structure and Organization
            • Pay attention to the structure and hierarchy of headings in modern decisions (generally post-1990), as they often indicate whether the SCC considers a particular analysis to be a standalone test or a component of a broader test.
            • Note that older decisions (pre-1990) frequently lack formal heading structures, requiring closer attention to transitional language, paragraph organization, and the SCC's own characterization of tests.
            • When headings are absent, look for other organizational cues such as numbered points, consistent terminology indicating new topics, or clear transitional statements that signal shifts from one test to another.
            • Be mindful that even without formal headings, the SCC often signals the relationship between concepts through language indicating subordination (e.g., "as part of this test," "within this framework," "this factor requires").

            # Quantification Guidance
            When ranking tests in order of legal significance, consider the factors in this approximate order of importance, while maintaining a holistic assessment:
            1. Development, Refinement, and Court Signaling of Test Importance: The SCC's novel contributions, refinements, or modifications to existing tests typically have the highest jurisprudential significance.
            2. Distinguishing Development from Summarization: Tests that represent genuine doctrinal development rather than summarization of established law should be prioritized.
            3. Assessing Framework-Component Relationships: Consider whether frameworks and components represent separate jurisprudential developments with independent significance.
            4. Focus of Separate Opinions on the Test: Tests that generate significant debate among judges often represent areas where the SCC is actively shaping doctrine.
            5. Depth of Treatment and Prominence in Decision: The space and attention devoted to a test reflects its centrality to the SCC's analysis, but must be considered in context, especially for older decisions that may be more concise.
            6. Explicit Test Formulation by the SCC: While clear articulation of a test is important, mere recitation of well-established tests without substantive modification should be given less weight.
            7. Actual Application of the Test: While application can indicate importance, tests fully developed but not applied due to procedural issues (e.g., standing) may still be highly significant.
            8. Potential Breadth of Application of the Test: Tests with wider applicability may have greater significance.
            9. Document Structure and Organization: The hierarchical relationship between tests and their components as indicated by headings and organization should inform how tests are identified and prioritized.
            Remember that this ranking is not rigid, and the assessment should remain holistic. The primary focus should be on identifying where the SCC is making its most significant contribution to legal doctrine, especially regarding the development of rules versus standards. Tests that represent a shift in how rule-like or standard-like the SCC's approach has become are particularly important to identify.

            ## What NOT to Consider as an Important Legal Test
            • The application of the Oakes test in every case other than R. v. Oakes [1986] 1 SCR 103. The Oakes test is applied in Charter cases and may also be called "Section 1 justification analysis," "Proportionality analysis," "Charter justification analysis," "Reasonable limits analysis," etc.
            • Purely factual determinations without an articulated analytical framework.
            • General statements of law that lack specific criteria or steps for application.
            • Observations or dicta that are not essential to resolving the case.
            • Citation or mention of tests without actual application or substantive analysis.
            • Tests that are merely referenced in passing.
            • Tests that are simply quoted from earlier decisions without modification or development.
            • Components, factors, or steps that are clearly part of a larger test rather than standalone tests, unless the component itself represents a significant novel development with independent jurisprudential importance.

            ***END OF ALPHA GUIDELINES***

            ***BEGINNING OF BETA (Test Breakdown) GUIDELINES***

            # Application Instructions
            Characterize the most important legal test in the SCC decision, as identified with the ALPHA guidelines.
            Read the entirety of the SCC decision (located in '{fulltext1}' or '{fulltext2}') before beginning.
            Produce a clear summary of the legal test—using direct quotes where possible—in order to maximize transparency of results and facilitate the verification of my work by other researchers.
            Identify the baseline. Is the legal test primarily based on common law, statute, regulation, or a combination of these sources?
            • If the legal test interprets or applies a statute/regulation: Identify the specific provision(s). 
            • If the legal test is based in common law: State the name(s) of the previous case(s) in which the original test was established. Look only for cases within the SCC decision itself.
            Identify the SCC contribution. 
            Identify the authoring judge. Based on the opinion from which you extracted the most important test, state the name of the authoring judge. The author may be identified as The Court or The Chief Justice, or similar terms indicating a role rather than a person, in which case you may use the same term to identify the authoring judge.

            ## Definitions
            • Baseline: Often, the SCC does not create a new legal test out of thin air. Often, a statute or regulation, or even a previous common law test provides the starting point that they then build on. That starting point is the baseline.
            • SCC contribution: Working from the baseline, the SCC can add, modify, interpret, remove, consolidate, etc. The SCC may have interpreted terms, filled statutory gaps, created factors or sub-rules, resolved conflicts between provisions, established interpretive principles, resolved other ambiguities, etc. These modifications, clarifications, etc. that the SCC made to the legal test are the SCC contribution.

            ***END OF BETA GUIDELINES***

            ***BEGINNING OF GAMMA (Rule Standard) GUIDELINES***
            You are a research assistant. These guidelines will help you assess the rule-like or standard-like nature of the SCC's contribution to the most important legal test in two cases and compare the two cases accordingly. Conduct your analysis according to the entire set of guidelines as broken down but do not print any output showing your analysis.
            Focus your analysis on the "SCC contribution" and not on the legal test overall. This is what I mean by that:
            Often, the SCC does not create a new legal test out of thin air. Often, a statute or regulation, or even a previous common law test provides the starting point that they then build on. That starting point is the baseline. The SCC contribution is what the SCC added, clarified, or removed from the legal test in a given case. The SCC may have interpreted terms, filled statutory gaps, created factors or sub-rules, resolved conflicts between provisions, established interpretive principles, resolved other ambiguities, etc. 

            # Core Concepts
            The "rules or standards debate" is a continuous and ongoing discussion in legal academia about the optimal way to formulate legal directives. Laws can be crafted as precise, clear-cut rules that specify particular conduct and its consequences, or as flexible, general standards that require an assessment of the specific circumstances of a case.
            Rules generally provide more predictability than standards, though this is not always true in specific comparisons. For example, a formal rule-like structure does not guarantee predictability if its components are unclear or highly evaluative. 
            A test provides predictability if it allows litigants to accurately predict how likely they are to win if their case goes to trial.
            Importantly, most legal tests contain elements of both rules and standards rather than falling purely into one category. No one element outweighs the others. However, certain criteria serve as strong indicators of a test's rule-like or standard-like nature. These are flagged for you below.
            Sections A-F of these guidelines identify typical characteristics of rules and standards but exceptions exist. These too are flagged for you below.
            
            # Application Instructions
            • Read the entirety of both SCC decisions before beginning the analysis.
            • Designate one legal test as "Test A" and the other legal test as "Test B."
            • Analyze each legal test according to the Criteria of Analysis (Sections A-F).
            • Keep the analysis of each legal test separate until the final comparison. 
            • Focus on the SCC's specific contribution to each legal test.
            • Consider how the SCC's specific contribution affects the predictability of the legal test.
            • Do not generate output to show this analysis.

            # Criteria of Analysis
            ## A. Elements of the Test 
            ### A1—Number of Elements or Steps
            A test with fewer elements is generally more rule-like; a test with more elements is generally more standard-like.
            EXCEPTION: Additional elements that constrain discretion (rather than expand it) may make a test more rule-like despite increasing the element count.
            - Did the SCC add, remove, or consolidate elements?
            - Did the SCC's contribution make the test more rule-like or more standard-like?
            ### A2—Nature of Elements
            A test with elements based on fact evidence is more rule-like; a test with elements based on expert evidence is more standard-like. 
            A test that turns on objective facts (e.g., the date a document was filed) is more rule-like; a test that turns on subjective facts (e.g., reasonableness, intent, bad faith) is more standard-like.
            A test focused on actual historical facts is more rule-like; a test requiring counterfactual or hypothetical analysis (e.g., "What would a reasonable person have done?") is more standard-like.
            #### A2.1—Clarity of Structural Elements
            When analyzing a test with multiple steps or factors, specifically assess the precision and nature of the concepts or determinations required by each structural step itself. Are terms which might be introduced to structure the analysis (e.g., "inventive concept," "main purpose," "predominant character") clearly defined and objectively ascertainable (rule-like) or do they introduce potential ambiguity and discretionary interpretation (standard-like)?
            - Did the SCC define the nature of one or more elements, for example by interpreting a statutory term?
            - Did the SCC's contribution make the test more rule-like or more standard-like?
            ## B. Structure and Combination Method
            ### B1—Combination Method
            A test where each element is mandatory is more rule-like; a test where each element is optional is more standard-like.
            A test where the elements are cumulative—where the outcome of one part leads to the next—is more rule-like; a test where the elements are alternative to each other is more standard-like.
            A test with threshold requirements is more rule-like.
            A test that combines elements by balancing them in a holistic assessment (e.g., totality of the circumstances, overall context) is more standard-like.
            - Did the SCC impose or clarify the combination method?
            - Did the SCC's contribution make the test more rule-like or more standard-like?
            ### B2—Hierarchical Structure
            A test with clear prioritization of elements is more rule-like; a test where all elements have equal weight is more standard-like.
            A test where certain elements are dispositive (determinative by themselves) is more rule-like.
            EXCEPTION: While a formal or hierarchical structure often tends towards rule-likeness, this effect is diminished or negated if the elements introduced by the structure are themselves vague, abstract, require significant subjective interpretation, or introduce new ambiguities not present in a simpler formulation. Assess the predictability impact of the structure itself; complexity without clarity increases points of potential dispute and makes a test more standard-like.
            - Did the SCC create or emphasize a hierarchy in the legal test?
            - Did the SCC's contribution make the test more rule-like or more standard-like?
            ## C. Language and Terminology
            ### C1—Precision of Language
            A test using precise or- a test using vague or abstract terms (e.g., "reasonable," "material," "substantial," "undue") is more standard-like.
            A test using quantitative (e.g., "within 30 days," "over $10,000") terms is more rule-like.
            - Assess key terms used both within the elements and to define the test's structure or sequence.
            - Did the SCC's interpretive language add precision or vagueness?
            - Did the SCC's contribution make the test more rule-like or more standard-like?
            ### C2—Definitive versus Evaluative Language
            A test articulated with mandatory, definitive language (e.g., "must," "shall," "if and only if") is more rule-like; a test articulated with discretionary, evaluative language (e.g., "consider," "weigh," "may," "appropriate") is more standard-like.
            - Did the SCC choose definitive or evaluative language?
            - Did the SCC's contribution make the test more rule-like or more standard-like?
            ### C3—Explicit Thresholds
            A test with clear quantitative thresholds or binary states (e.g., "more than 50%," "absence versus presence of a signature") is more rule-like; a test requiring assessment of degrees or qualitative levels without sharp boundaries is more standard-like.
            - Did the SCC create or reject clear thresholds?
            - Did the SCC's contribution make the test more rule-like or more standard-like?
            ## D. Discretion and Flexibility
            ### D1—Explicit Grant of Discretion
            A test that guides or limits judicial discretion through specific criteria is more rule-like; a test that explicitly grants discretion to the decision-maker (e.g., "in the court's discretion," "as is just and equitable") is more standard-like.
            - Did the SCC explicitly grant or constrain discretion?
            - Did the SCC's contribution make the test more rule-like or more standard-like?
            #### D1.1—Implicit Flexibility
            A test requiring significant interpretation of vague terms or balancing of qualitative factors embeds high implicit flexibility and is standard-like.
            - Assess the degree of judgment or evaluation required even without explicit grants of discretion.
            - Did the SCC's contribution increase or reduce the implicit flexibility of the test?
            - Did the SCC's contribution make the test more rule-like or more standard-like?
            ### D2—Exceptions
            A test with few, clearly defined exceptions is more rule-like; a test with numerous or broadly defined exceptions is more standard-like.
            The creation of a broad and discretionary exception can be a strong indicator of standard-likeness.
            - Did the SCC create or define exceptions?
            - Did the SCC's contribution make the test more rule-like or more standard-like?
            ### D3—Presumptions
            A test with irrebuttable presumptions is more rule-like than a test with rebuttable presumptions.
            A test with rebuttable presumptions is more rule-like than a test with no presumptions, but the rebuttal process often introduces standard-like elements.
            - Did the SCC introduce, clarify, or reject presumptions?
            - Did the SCC's contribution make the test more rule-like or more standard-like?
            ## E. Temporal and Burden Aspects
            ### E1—Burden and Standard of Proof
            A test with fixed, higher burdens of proof is more rule-like; a test with lower or shifting burdens is more standard-like.
            A test where the burden shifts based on preliminary showings is more standard-like.
            - Note who bears the burden of proof for each element of the legal test and what the standard of proof is at each step.
            - Identify if/when the burden of proof shifts.
            - Did the SCC assign or clarify the burden of proof?
            - Did the SCC's contribution make the test more rule-like or more standard-like?
            ### E2—Temporal Focus
            A test focused ex ante on guiding conduct before an event (e.g., setting specific compliance requirements beforehand) is typically more rule-like; a test focused ex post on evaluating conduct or results after an event (e.g., assessing reasonableness of actions taken) is often more standard-like.
            EXCEPTION: Ex post assessment tests are less standard-like if they contain a rigid temporal anchor (e.g., the assessment is strictly limited to facts known at a specific past date).   
            - Did the SCC introduce, alter, or specify an ex ante or ex post dimension to the legal test?
            - Did the SCC's contribution make the test more rule-like or more standard-like?
            ## F. Purpose and Application Context
            ### F1—Policy Considerations
            A test focused narrowly on specific interactions between parties based on pre-defined legal elements is more rule-like; a test that explicitly requires balancing broader public policy goals is more standard-like.
            An emphasis on policy balancing is a strong indicator of standard-likeness.
            - Did the SCC introduce or emphasize policy balancing?
            - Did the SCC's contribution make the test more rule-like or more standard-like?
            ### F2—Institutional Competence
            A test that can be applied by generalist judges without special expertise is more rule-like; a test that delegates specialized determinations to experts is more standard-like.
            - Did the SCC's approach require specialist input?
            - Did the SCC's contribution make the test more rule-like or more standard-like?

            # Synthesis and Conclusion
            ## Summary
            • Summarize the analysis regarding the rule-like or standard-like nature of the SCC's contribution to the legal test.
            • Do not print any output showing this summary.
            ## Analysis of Tension
            • Identify conflicting rule and standard indicators. Explain the tension. For example, note if there is a rule-like structure to a standard-like core assessment, or a rule-like structure that introduces vague standard-like elements. Critically evaluate whether the formal structure genuinely enhances predictability or if the ambiguous, evaluative nature of its components or the core question it leads to dominates.
            • Identify which factors are most significant for the overall assessment of the rule-like or standard-like nature of the SCC contribution to the given legal test. Do not produce output showing this process.
            ## Overall Assessment
            • Conclude whether the legal test functions predominantly as a rule or a standard.
            • After analyzing both tests, directly compare their rule-like characteristics to determine which is more rule-like and assign a score according to the scale below.

            ***END OF GAMMA GUIDELINES***

            Now analyze and compare the following cases:

            ***CASE INFORMATION***
            Decision A (ParqRow: {parqrow1})
            Subjects: {', '.join(subjects1)}
            Text:
            {fulltext1}

            Decision B (ParqRow: {parqrow2})
            Subjects: {', '.join(subjects2)}
            Text:
            {fulltext2}
            
            """
    return string