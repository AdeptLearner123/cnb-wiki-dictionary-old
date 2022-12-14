from config import (
    TITLE_FILTERED,
    DICTIONARY,
)
from cnb_wiki_dictionary.download.caches import PageViewsCache, SummariesCache
from cnb_wiki_dictionary.utils.title import title_to_text
from cnb_wiki_dictionary.utils.spacy import make_doc
from cnb_wiki_dictionary.utils.word_forms import get_word_forms
from cnb_wiki_dictionary.utils.knownness import views_to_knownness
from cnb_wiki_dictionary.utils.process_summary import process_summary

import json
from tqdm import tqdm


def main():
    with open(TITLE_FILTERED, "r") as file:
        titles = file.read().splitlines()

    dictionary = dict()

    title_to_summary = SummariesCache().get_key_to_value()
    title_to_views = PageViewsCache().get_key_to_value()

    for title in tqdm(titles):
        if title not in title_to_summary or title not in title_to_views:
            continue

        knownness = views_to_knownness(title_to_views[title])

        if knownness < 0:
            continue

        summary = process_summary(title_to_summary[title])

        if len(summary) == 0:
            continue

        doc = make_doc(summary)

        dictionary[title] = {
            "word": title_to_text(title),
            "pos": "noun",
            "definition": summary,
            "knownness": knownness,
            "wordForms": get_word_forms(title, doc),
        }

    print("Dictionary size", len(dictionary))

    with open(DICTIONARY, "w+") as file:
        file.write(json.dumps(dictionary, indent=4, sort_keys=True, ensure_ascii=False))


if __name__ == "__main__":
    main()
