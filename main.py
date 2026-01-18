from helper_functions import parse_file_with_regex, get_top_n_strings, map_doi_to_title, get_paper_title


list_of_references = parse_file_with_regex('All_Decks_Cards.txt')
#print(list_of_references)

doi_to_title_dict = map_doi_to_title(list_of_references)


print(doi_to_title_dict)
top_reference_list = get_top_n_strings(list_of_references, 20)
print(top_reference_list)

get_paper_title(top_reference_list, doi_to_title_dict)