from doi_functions import parse_doi, get_list_of_papers, map_doi_to_title, get_paper_title
from textbook_functions import parse_textbook, get_list_of_textbooks, get_range_of_textbooks
from stats_functions import parse_tags, get_tag_counts, tag_dict_organiser

def generate_paper_frequencies(filename, ref_range, target_tags=[], nontarget_tags=[]):
    """
    Finds the top n most frequently occurring DOI's from a file, filtered by target and nontarget tags.
    
    Args:
        filename: Path to the file to be parsed
        top_n: Number of top occurrences to return
        target_tags: List of tags that must be present in a reference
        nontarget_tags: List of tags that must not be present in a reference
    
    Returns:
        None; prints the top n DOI's with their corresponding titles
    """
    list_of_paper_references = parse_doi(filename, target_tags = target_tags, nontarget_tags = nontarget_tags)

    doi_to_title_dict = map_doi_to_title(list_of_paper_references)

    full_reference_list = get_list_of_papers(list_of_paper_references)

    get_paper_title(ref_range, full_reference_list, doi_to_title_dict)


def generate_textbook_frequencies(filename, ref_range, target_tags=[], nontarget_tags=[]):
    """
    Finds the top n most frequently occurring textbook titles from a file, filtered by target and nontarget tags.
    
    Args:
        filename: Path to the file to be parsed
        top_n: Number of top occurrences to return
        target_tags: List of tags that must be present in a reference
        nontarget_tags: List of tags that must not be present in a reference
    
    Returns:
        None; prints the top n textbook titles
    """
    list_of_textbook_references = parse_textbook(filename, target_tags = target_tags, nontarget_tags = nontarget_tags)

    full_textbook_list = get_list_of_textbooks(list_of_textbook_references)
    get_range_of_textbooks(ref_range, full_textbook_list)