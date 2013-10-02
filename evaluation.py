

def average_precision(preds, refs):
    if not isinstance(refs, set):
    	refs = set(refs)
    assert any(l in refs for l in preds)

    total = 0.0; num_correct = 0
    for k,pred in enumerate(preds):
        if pred in refs:
            num_correct += 1
            p = float(num_correct/float(k+1))
            total += p
    return total / num_correct if total > 0 else 0.0