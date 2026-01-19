from doi_functions import parse_doi, get_top_n_papers, map_doi_to_title, get_paper_title
from textbook_functions import parse_textbook, get_top_n_textbooks, get_textbook_title


target_tags = []
nontarget_tags = ["Review"]


def test_paper_functions():
    list_of_paper_references = parse_doi('All_Decks_Cards.txt', target_tags = target_tags, nontarget_tags = nontarget_tags)

    doi_to_title_dict = map_doi_to_title(list_of_paper_references)

    top_reference_list = get_top_n_papers(list_of_paper_references, 40)

    get_paper_title(top_reference_list, doi_to_title_dict)

def test_textbook_functions():
    list_of_textbook_references = parse_textbook('All_Decks_Cards.txt', target_tags = target_tags, nontarget_tags = nontarget_tags)

    top_textbook_list = get_top_n_textbooks(list_of_textbook_references, 20)
    get_textbook_title(top_textbook_list)



test_paper_functions()