from stats_functions import parse_tags, get_tag_counts, tag_dict_organiser
from core import generate_paper_frequencies, generate_textbook_frequencies

filename = 'All_Decks_Cards.txt'
top_n_papers = 100
top_n_textbooks = 20

target_tags = []
nontarget_tags = []


generate_paper_frequencies(filename, top_n_papers, target_tags, nontarget_tags)
#generate_textbook_frequencies(filename, top_n_textbooks, target_tags, nontarget_tags)

"""
tag_list = parse_tags('All_Decks_Cards.txt')
tag_counts = get_tag_counts(tag_list)
print(tag_counts)

all_journal_tags, journal_parent_tags, journal_terminal_tags = tag_dict_organiser(tag_counts)

"""