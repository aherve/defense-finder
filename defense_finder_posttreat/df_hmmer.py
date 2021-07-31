import csv
import os

def get_hit_sort_attr(hit):
    return hit['hit_id']

def remove_duplicates(hmmer_hits):
    temp_list = []
    for i in hmmer_hits:
        if i not in temp_list:
            temp_list.append(i)
    return temp_list

def export_defense_finder_hmmer_hits():
    paths = get_hmmer_paths()
    hmmer_hits = []
    for path in paths:
        d = parse_hmmer_results_file(path)
        hmmer_hits = hmmer_hits + remove_duplicates(d)
    sorted_hmmer_hits = sorted(hmmer_hits, key=get_hit_sort_attr)
    hmmer_hits_list = hmmer_to_list(sorted_hmmer_hits)
    write_defense_finder_hmmer(hmmer_hits_list)

def write_defense_finder_hmmer(hmmer_hits_list):
    with open('/tmp/defense-finder/output/defense_finder_hmmer.tsv', 'w') as defense_finder_hmmer_file:
        write = csv.writer(defense_finder_hmmer_file, delimiter='\t')
        write.writerows(hmmer_hits_list)
        defense_finder_hmmer_file.close()

def get_hmmer_keys():
    return ['hit_id', 'gene_name', 'i-eval', 'score', 'profile_coverage']

def parse_hmmer_results_file(path):
    tsv_file = open(path)
    tsv = csv.reader(tsv_file, delimiter='\t')
    data = []
    for row in tsv:
        if not row[0].startswith('#'):
            data.append(row)
    tsv_file.close()
    out = []
    for l in data:
        if not l: continue
        line_as_dict = {}
        for idx, val in enumerate(get_hmmer_keys()):
            line_as_dict[val] = l[idx]
        out.append(line_as_dict)
    return out

def get_hmmer_paths():
    files = []
    with os.scandir('/tmp/defense-finder/hmmer_results') as it:
        for entry in it:
            if entry.name.endswith('extract') and entry.is_file():
                files.append(entry)
    return list(map(lambda i: i.path, files))


def hmmer_to_list(hmmer_hits):
    header = get_hmmer_keys()
    out = [header]
    for s in hmmer_hits:
        l = []
        for key in header:
            l.append(s[key])
        out.append(l)
    return out