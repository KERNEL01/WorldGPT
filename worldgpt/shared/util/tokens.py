import tiktoken


def count_prompt_tokens(message: str, model: str = "gpt-4"):
    """ Counts the number of tokens in a prompt using tiktoken. """
    encoder = tiktoken.encoding_for_model(model)
    return len(encoder.encode(message))
