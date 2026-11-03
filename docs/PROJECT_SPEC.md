<h1> Project Spec: Food Safety Advisor </h1>

<h2> 1. Problem Statement </h2>
<p>Given a photo of a product's ingredient list and a user profile
(age, gender, BMI, diabetes, hypertension, obesity, smoker), the system
returns a verdict (Safe / Limit / Avoid) for a general person and for the
specific user, with the top 3 driving ingredients and a one-line reason each.</p>

<h2>2. Input / Output Contract </h2>
<h3> Input </h3>
- Image: ingredient list photo <br>
- Profile: age, gender, BMI, diabetes (Y/N), hypertension (Y/N),
  obesity (Y/N), smoker (Y/N)

<h3> Output </h3>
<b>json </b>
<pre>
{
  "general":  { "verdict": "Limit", "top3": [{"ingredient": "", "reason": ""}] },
  "personal": { "verdict": "Avoid", "top3": [{"ingredient": "", "reason": ""}] },
  "ocr_confidence": 0.0,
  "unrecognized_ingredients": []
}
</pre>

<h2> 3. Scope Decisions </h2>
<pre>
1. Input type: (your answer)
2. Market and language: (your answer)
3. Deliverable: (your answer)
4. Time budget: (your answer)
5. Health authorities cited: (your answer)</pre>

<h2> 4. Verdict Definitions</h2>
<table>
<tr><th>Verdict</th><th>Meaning</th></tr>
<tr><td>safe</td><td>---</td></tr>
<tr><td>Limit</td><td>---</td></tr>
<tr><td>Avoid</td><td>---</td></tr>
</table>
<h3> Combination rules </h3>
- Multiple conditions: (your rule)<br>
- Can personal verdict be better than general? (your answer)

<h2> 5. Dataset Findings </h2>
- (3 to 5 bullets, filled in after Part 5 below)

<h2> 6. Success Metrics </h2>
 <table>
<tr><th>Stage</th><th>Metric</th><th>Target</th></tr>
<tr><td>OCR</td><td>word accuracy</td><td>>=90%</td></tr>
<tr><td>parsing</td><td>ingredient</td><td>>=90%</td></tr>
<tr><td>knowledge base</td><td>covrage</td><td>>=85%</td></tr>
<tr><td>verdict</td><td>agreement with dataset</td><td>TBD</td></tr>
<tr><td>safety</td><td>'safe' when truth is 'avoid'</td><td>~0%</td></tr>
<tr><td>explaination</td><td>humman rated correct</td><td>>=85%</td></tr>
</table>
<h2> 7. Disclaimer </h2>
This tool is for informational purposes only. It is not medical advice,diagnosis, or treatment. Consult a qualified healthcare professional.