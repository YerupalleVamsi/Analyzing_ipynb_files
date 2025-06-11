import nbformat
import difflib

def load_notebook(file):
    nb = nbformat.read(file, as_version=4)
    return [cell['source'] for cell in nb.cells if cell.cell_type == 'code']

def compare_notebooks(orig_cells, test_cells):
    matcher = difflib.SequenceMatcher(None, orig_cells, test_cells)
    diffs = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        diffs.append((tag, orig_cells[i1:i2], test_cells[j1:j2]))
    return diffs

def compute_creativity_score(diffs):
    score = 0
    for tag, orig, test in diffs:
        if tag == 'replace':
            score += 10 * len(test)
        elif tag == 'insert':
            score += 5 * len(test)
        elif tag == 'delete':
            score += 2 * len(orig)
    return min(score, 100)
