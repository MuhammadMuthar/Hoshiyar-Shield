# `ml/data/contrib/`: externally authored evaluation data

This folder holds messages written by **someone other than the author of the
training templates**, mainly ChatGPT (see `docs/COLLABORATION.md` §2.2-A).

- `chatgpt_challenge.jsonl`: independent challenge set. One JSON object per
  line, schema in COLLABORATION §5.1.
- Files here are used **only for evaluation**, never for training. `train.py`
  picks up every `*.jsonl` file here automatically, reports it as a separate
  "independent author" score in `ml/artifacts/metrics.json` and
  `docs/model-evaluation.md`, and leaves the trained model unchanged.
- Don't tune the model or templates against these files after looking at the
  results. If you do, say so in the docs, because the score is no longer an
  independent estimate.
