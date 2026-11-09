# Bayes' Theorem in Spam Detection

A case study report and experiment for *Basics of Neural Networks and Deep Learning*. It shows how a naive Bayes spam filter works and evaluates it on the SpamAssassin public email corpus.

## Contents

| Path | What it is |
|------|------------|
| `Bayes_Spam_Detection_Report.pdf` / `.docx` | APA-format report |
| `ipynb/spam_naive_bayes.ipynb` | Notebook that reproduces every number in the report, with outputs saved |
| `experiment/nb.py` | The same experiment as a plain script |
| `experiment/build.py` | Script that generated the Word report |

## Results (test set, n = 1,210)

| Model | Accuracy | Precision | Recall | F1 |
|-------|---------:|----------:|-------:|---:|
| Multinomial NB (counts) | .962 | .956 | .921 | .938 |
| Bernoulli NB (binary) | .948 | .968 | .863 | .912 |
| Multinomial NB (TF-IDF) | .975 | .976 | .945 | .960 |

## Running it

```sh
pip install scikit-learn numpy jupyter
cd ipynb && jupyter notebook spam_naive_bayes.ipynb
```

The notebook downloads the [SpamAssassin public corpus](https://spamassassin.apache.org/old/publiccorpus/) (about 7 MB) into `data/` on first run. The dataset is not included in this repository.
