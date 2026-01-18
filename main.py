from doi_functions import parse_doi, get_top_n_papers, map_doi_to_title, get_paper_title
from textbook_functions import parse_textbook, get_top_n_textbooks


tag_list = ["Orbital", "Mechanism"]


def test_paper_functions():
    list_of_paper_references = parse_doi('All_Decks_Cards.txt', tag_list)

    doi_to_title_dict = map_doi_to_title(list_of_paper_references)

    print(doi_to_title_dict)
    top_reference_list = get_top_n_papers(list_of_paper_references, 20)
    print(top_reference_list)

    get_paper_title(top_reference_list, doi_to_title_dict)

def test_textbook_functions():
    list_of_textbook_references = parse_textbook('All_Decks_Cards.txt', tag_list)
    print(list_of_textbook_references)

    top_textbook_list = get_top_n_textbooks(list_of_textbook_references, 10)
    print(top_textbook_list)


test_textbook_functions()