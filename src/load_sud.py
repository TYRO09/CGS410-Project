from conllu import parse_incr


def load_sentences(file_path, max_len=12):
    """
    Yield sentences from an SUD CoNLL-U file with length <= max_len.
    Filters out multiword tokens and special nodes.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        for sentence in parse_incr(f):

            tokens = []
            for token in sentence:
                if isinstance(token["id"], int):  # ignore multiword tokens
                    tokens.append(token)

            if len(tokens) <= max_len:
                yield tokens