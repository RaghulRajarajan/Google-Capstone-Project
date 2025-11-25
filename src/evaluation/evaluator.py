"""
Tiny evaluator to exercise agent evaluation.
- Compares generated summary vs golden summary (if available) using simple overlap metric.
- Measures action extraction precision/recall against labeled test.
"""
import json
import logging
logger = logging.getLogger("evaluator")

def simple_overlap(a, b):
    aset = set(a.lower().split())
    bset = set(b.lower().split())
    if not bset:
        return 0.0
    return len(aset & bset) / len(bset)

def evaluate_summary(generated, golden):
    score = simple_overlap(generated, golden)
    logger.info("Summary overlap score: %.3f", score)
    return {"overlap": score}

def evaluate_actions(predicted, gold):
    # gold: list of text strings; predicted: list of dicts with text
    pred_texts = [p['text'].lower() for p in predicted]
    tp = 0
    for g in gold:
        for p in pred_texts:
            if g.lower() in p:
                tp += 1
                break
    precision = tp / max(1, len(pred_texts))
    recall = tp / max(1, len(gold))
    logger.info("Action extraction precision=%.3f recall=%.3f", precision, recall)
    return {"precision": precision, "recall": recall}
