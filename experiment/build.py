from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
d=Document()
for s in d.sections:
    s.top_margin=s.bottom_margin=s.left_margin=s.right_margin=Inches(1)
st=d.styles['Normal']; st.font.name='Times New Roman'; st.font.size=Pt(12)
st.element.rPr.rFonts.set(qn('w:eastAsia'),'Times New Roman')
pf=st.paragraph_format; pf.line_spacing=2.0; pf.space_before=Pt(0); pf.space_after=Pt(0)
# page number header
hp=d.sections[0].header.paragraphs[0]; hp.alignment=WD_ALIGN_PARAGRAPH.RIGHT
r=hp.add_run()
for t,txt in [('begin',None),(None,'PAGE'),('end',None)]:
    if t: e=OxmlElement('w:fldChar'); e.set(qn('w:fldCharType'),t)
    else: e=OxmlElement('w:instrText'); e.set(qn('xml:space'),'preserve'); e.text=txt
    r._r.append(e)
def para(text='',align=None,indent=True,bold=False,italic_parts=()):
    p=d.add_paragraph()
    if align is not None: p.alignment=align
    if indent and align is None: p.paragraph_format.first_line_indent=Inches(0.5)
    add(p,text,bold)
    return p
def add(p,text,bold=False):
    # *x* marks italics
    parts=text.split('*')
    for i,s in enumerate(parts):
        if s: rr=p.add_run(s); rr.italic=(i%2==1); rr.bold=bold
def h1(t): para(t,WD_ALIGN_PARAGRAPH.CENTER,bold=True)
def h2(t): p=para(t,WD_ALIGN_PARAGRAPH.LEFT,indent=False,bold=True)
# title page
for _ in range(3): para('',WD_ALIGN_PARAGRAPH.CENTER)
para("Case Study on the Application of Bayes’ Theorem in Spam Detection",WD_ALIGN_PARAGRAPH.CENTER,bold=True)
para('',WD_ALIGN_PARAGRAPH.CENTER)
for t in ['[Student Name]','[Department of Computer Science, University Name]','[Course Code]: Basics of Neural Networks and Deep Learning','[Instructor Name]','November 9, 2026']:
    para(t,WD_ALIGN_PARAGRAPH.CENTER)
d.paragraphs[-1].add_run().add_break(WD_BREAK.PAGE)
# body
h1("Case Study on the Application of Bayes’ Theorem in Spam Detection")
para("Spam, or unsolicited bulk email, wastes bandwidth and user attention, and it is a common way to deliver phishing links and malware (Dada et al., 2019). Spammers keep changing their wording, so hand-written rules go out of date quickly, and filters that learn from labeled examples have become the standard defence (Blanzieri & Bryl, 2008). The naive Bayes classifier is one of the oldest of these methods and is still widely used because it is fast and works well on text (Guzella & Caminhas, 2009).")
h1("Overview of Bayes’ Theorem")
para("Bayes’ theorem updates the probability of a hypothesis *H* after observing evidence *E*:")
para("*P*(*H* | *E*) = *P*(*E* | *H*) *P*(*H*) / *P*(*E*)                                        (1)",WD_ALIGN_PARAGRAPH.CENTER)
para("Here *P*(*H*) is the prior, *P*(*E* | *H*) is the likelihood, *P*(*E*) is the overall probability of the evidence, and *P*(*H* | *E*) is the posterior. In spam filtering, the hypothesis is that a message belongs to class *c* ∈ {spam, ham}, where “ham” means legitimate mail, and the evidence is the words in the message. The theorem turns a hard question (“given these words, is this spam?”) into quantities that can be counted in labeled data. For example, in the training data used below, 31.4% of messages are spam, and the word “click” appears in 54.4% of spam and 4.7% of ham. Therefore *P*(spam | click) = (0.544 × 0.314) / (0.544 × 0.314 + 0.047 × 0.686) ≈ 0.84. A real filter combines such evidence from every word.")
h1("Description of the Dataset")
para("A Bayesian filter learns from emails that have each been labeled spam or ham. Common public corpora include Ling-Spam, Enron-Spam, and the SpamAssassin public corpus (Dada et al., 2019). This study uses the SpamAssassin corpus: 6,046 raw emails, of which 4,150 are ham (68.6%) and 1,896 are spam (31.4%). The ham set includes 250 “hard” messages, such as newsletters, that resemble spam. This kind of data is imbalanced, so the prior is not 0.5. It is also sparse: the vocabulary has tens of thousands of words, but each message uses only a few hundred. And it changes over time as spam campaigns change (Blanzieri & Bryl, 2008). The corpus was split into 4,836 training messages (80%) and 1,210 test messages (20%). Both parts kept the original class ratio.")
h1("Data Preprocessing")
h2("Parsing and Tokenization")
para("Each email was parsed with a MIME parser. The subject and text parts were kept, HTML tags were removed, and the text was lowercased. URLs, email addresses, and numbers were replaced with placeholder tokens (URLTOKEN, EMAILTOKEN, NUMTOKEN). Tokenization then split the text into words of two or more letters. Stop words such as “the” were removed because they carry no class evidence.")
h2("Vectorization")
para("Each message was then turned into a numeric vector using the bag-of-words model. A vocabulary of *V* = 23,164 words that appear in at least two training messages was built. Each message became a vector *x* = (*x*₁, …, *x*ᵥ), where *x*ᵢ counts how often word *i* occurs. Two alternatives were also tested. Binary presence/absence features are used by Bernoulli naive Bayes. TF-IDF weighting gives less weight to words that appear in many documents (Salton & Buckley, 1988).")
h1("How the Theorem Classifies Messages")
para("By Bayes’ theorem, *P*(*c* | *x*) ∝ *P*(*c*) *P*(*x* | *c*). Estimating *P*(*x* | *c*) for every possible combination of words is impossible. The *naive* assumption solves this by treating words as independent once the class is known, which gives the multinomial naive Bayes decision rule:")
para("ĉ = argmax꜀ [ log *P*(*c*) + Σᵢ *x*ᵢ log *P*(*w*ᵢ | *c*) ]                                (2)",WD_ALIGN_PARAGRAPH.CENTER)
para("Training only requires counting. *P*(*c*) is the share of training messages in class *c*. Each word likelihood uses Laplace smoothing: *P*(*w*ᵢ | *c*) = (*N*꜀ᵢ + 1) / (*N*꜀ + *V*), where *N*꜀ᵢ is how often word *i* occurs in class *c* and *N*꜀ is the total word count of that class. Without smoothing, a word never seen in training ham would get probability zero and cancel all other evidence. Logarithms are added instead of multiplying raw probabilities, which would underflow (Guzella & Caminhas, 2009). To classify a new email, the filter computes Equation 2 for both classes, or equivalently computes *P*(spam | *x*), and marks the email as spam if that probability is above a threshold (0.5 by default). In effect, each word votes with weight log[*P*(*w* | spam) / *P*(*w* | ham)]. In the trained model, the strongest spam words included “mortgage” and “annuity,” and the strongest ham words included “kernel” and “perl.”")
h1("Performance Analysis")
para("The classifiers were built with scikit-learn and tested on the 1,210 held-out messages, with spam as the positive class. Accuracy alone can be misleading when the classes are imbalanced, so the evaluation also reports precision (the share of flagged messages that really are spam), recall (the share of spam that was caught), F1, specificity, and AUC (Dada et al., 2019).")
p=para("Table 1",WD_ALIGN_PARAGRAPH.LEFT,indent=False,bold=True)
para("*Test-Set Performance of Three Naive Bayes Variants (n = 1,210)*",WD_ALIGN_PARAGRAPH.LEFT,indent=False)
rows=[["Model","Accuracy","Precision","Recall","F1","Specificity","AUC","5-fold CV"],
["Multinomial (counts)",".962",".956",".921",".938",".981",".990",".970"],
["Bernoulli (binary)",".948",".968",".863",".912",".987",".993",".947"],
["Multinomial (TF-IDF)",".975",".976",".945",".960",".989",".998",".974"]]
t=d.add_table(rows=4,cols=8)
for i,row in enumerate(rows):
    for j,v in enumerate(row):
        c=t.cell(i,j); c.text=''; pp=c.paragraphs[0]; pp.paragraph_format.line_spacing=1.0
        pp.alignment=WD_ALIGN_PARAGRAPH.LEFT if j==0 else WD_ALIGN_PARAGRAPH.CENTER
        rr=pp.add_run(v); rr.font.size=Pt(10)
def border(cell,side):
    tcPr=cell._tc.get_or_add_tcPr(); b=tcPr.find(qn('w:tcBorders'))
    if b is None: b=OxmlElement('w:tcBorders'); tcPr.append(b)
    e=OxmlElement(f'w:{side}'); e.set(qn('w:val'),'single'); e.set(qn('w:sz'),'6'); b.append(e)
for c in t.rows[0].cells: border(c,'top'); border(c,'bottom')
for c in t.rows[-1].cells: border(c,'bottom')
t.autofit=False
for r_ in t.rows:
    for j,c in enumerate(r_.cells): c.width=Inches([1.55,0.75,0.75,0.65,0.55,0.85,0.55,0.85][j])
for j,gc in enumerate(t._tbl.tblGrid.findall(qn('w:gridCol'))): gc.set(qn('w:w'),str(int([1.55,0.75,0.75,0.65,0.55,0.85,0.55,0.85][j]*1440)))
para("*Note.* Model names give the naive Bayes event model and features; CV = cross-validation; AUC = area under the ROC curve. Smoothing α = 1 for count models, α = 0.1 for TF-IDF.",WD_ALIGN_PARAGRAPH.LEFT,indent=False)
para("The standard word-count model reached 96.2% accuracy, with 349 true positives, 30 false negatives (spam that reached the inbox), 16 false positives (ham marked as spam), and 815 true negatives. Five-fold cross-validation gave 97.0% ± 0.3%. TF-IDF weighting improved every metric (F1 = .960, only nine false positives), because it stops common but uninformative words from dominating Equation 2. The Bernoulli model had high precision but the lowest recall. It ignores how often a word is repeated, which shows that the choice of event model matters (Guzella & Caminhas, 2009).")
para("The two kinds of error do not cost the same, because losing a real email is worse than receiving a spam message. Raising the decision threshold from 0.5 to 0.99 cut false positives from 16 to 11, but recall fell from .921 to .900. AUC values above .99 show that spam and ham are well separated, so most errors come from where the threshold sits. Naive Bayes is fast and interpretable, but the independence assumption ignores word order, its probability estimates tend to be overconfident, and spammers can evade it by misspelling words or adding ordinary ham words (Blanzieri & Bryl, 2008). Even so, it remains a strong baseline and a good first stage in a layered filter.")
h1("Conclusion")
para("Bayes’ theorem gives spam filtering a simple principle: combine how common spam is with how strongly each word points to it. Once the emails are tokenized and vectorized, a naive Bayes model can be trained just by counting. On the SpamAssassin corpus it caught 92%–95% of spam and flagged only 1%–2% of legitimate mail, with TF-IDF giving the best results.")
# references
d.paragraphs[-1].add_run().add_break(WD_BREAK.PAGE)
h1("References")
refs=["Blanzieri, E., & Bryl, A. (2008). A survey of learning-based techniques of email spam filtering. *Artificial Intelligence Review, 29*(1), 63–92. https://doi.org/10.1007/s10462-009-9109-6",
"Dada, E. G., Bassi, J. S., Chiroma, H., Abdulhamid, S. M., Adetunmbi, A. O., & Ajibuwa, O. E. (2019). Machine learning for email spam filtering: Review, approaches and open research problems. *Heliyon, 5*(6), Article e01802. https://doi.org/10.1016/j.heliyon.2019.e01802",
"Guzella, T. S., & Caminhas, W. M. (2009). A review of machine learning approaches to spam filtering. *Expert Systems with Applications, 36*(7), 10206–10222. https://doi.org/10.1016/j.eswa.2009.02.037",
"Salton, G., & Buckley, C. (1988). Term-weighting approaches in automatic text retrieval. *Information Processing & Management, 24*(5), 513–523. https://doi.org/10.1016/0306-4573(88)90021-0"]
for r_ in refs:
    p=d.add_paragraph(); p.paragraph_format.left_indent=Inches(0.5); p.paragraph_format.first_line_indent=Inches(-0.5); add(p,r_)
d.save('Bayes_Spam_Detection_Report.docx')
