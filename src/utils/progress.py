from tqdm import tqdm

def progress_bar(iterable, total=None, desc="Processing"):
    return tqdm(iterable, total=total, desc=desc, ncols=100, leave=False)