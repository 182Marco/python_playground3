from .clean import dehyphenate, keep_between_markers, normalize_unicode, normalize_whitespace, reflow_paragraphs, remove_repeated_lines, remove_page_numbers, remove_citation_markers, drop_sections

PIPELINES = {
    ".txt": [                                  
        keep_between_markers("*** START", "*** END"),
        normalize_unicode,
        reflow_paragraphs,
    ],
    ".pdf": [                                   
        dehyphenate,
        remove_repeated_lines(min_repeats=3),
        remove_page_numbers,
        normalize_whitespace,
    ],
    ".html": [                                  
        remove_citation_markers(),
        drop_sections(["Note", "Bibliografia", "Voci correlate", "Collegamenti esterni"]),
        normalize_whitespace,
    ],
}

################
from collections.abc import Callable



def clean(txt: str, steps:list[Callable[[str], str]]) -> str:
    for step in steps:
       txt = step(txt)
    return txt


DEFAULT_STEPS = [normalize_unicode, normalize_whitespace]

def pipeline_for(path: str) -> list:
    from pathlib import Path
    return PIPELINES.get(Path(path).suffix.lower(), DEFAULT_STEPS)


def clean_file(path: str) -> str:
    from .loaders import load          
    grezzo = "\n".join(d.text for d in load(path)) 
    return clean(grezzo, pipeline_for(path))