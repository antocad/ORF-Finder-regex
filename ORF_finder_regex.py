from Bio.Seq import Seq
import re

def DNA2AA(seq):
    """
    Converts a given DNA sequence into its corresponding protein sequence (amino acid chain).
    The function translates the input DNA sequence in triplets (codons) using a predefined genetic code.
    
    Args:
    seq (str): DNA sequence (must be a string of valid nucleotides A, T, C, G).

    Returns:
    str: Translated protein sequence where each triplet (codon) is mapped to an amino acid.
         Unknown codons are represented as 'X'.
    """
    protein = []
    GENETIC_CODE = {
        'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M', 
        'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T', 
        'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K', 
        'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',                  
        'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L', 
        'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P', 
        'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q', 
        'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R', 
        'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V', 
        'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A', 
        'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E', 
        'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G', 
        'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S', 
        'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L', 
        'TAC':'Y', 'TAT':'Y', 'TAA':'*', 'TAG':'*', 
        'TGC':'C', 'TGT':'C', 'TGA':'*', 'TGG':'W'
    }
    for i in range(0, len(seq), 3):
        codon = seq[i:i+3]
        protein.append(GENETIC_CODE.get(codon, 'X'))  # Use 'X' for unknown codons
    return ''.join(protein)

def remove_contained_ranges(ranges, reversed=False):
    # Sort based on whether the ranges are reversed or not
    if reversed: ranges.sort(key=lambda x: (x[1], -x[0]))  # Sort by start, reverse by stop if ranges are reversed
    else: ranges.sort(key=lambda x: (x[0], -x[1]))  # Normal sort by start, reverse by stop
    result = []
    prev_end = -1

    for a, b, obj in ranges:
        # Depending on whether the ranges are reversed or not, a and b swap roles
        start, end = (b, a) if reversed else (a, b)
        # Add range if it's not fully contained in the last added range
        if end > prev_end:
            result.append([a, b, obj])
            prev_end = end
    return result

def find_orfs(sequences, min_dna_len=30):
    """
    Finds open reading frames (ORFs) in the provided DNA sequences.
    
    Args:
    sequences (dict): Dictionary of sequences where keys are sequence IDs and values are DNA sequences.
    min_dna_len (int): Minimum length for an ORF to be considered (default: 30 nucleotides).

    Returns:
    dict: A dictionary of ORFs for each sequence and strand, organized by reading frames.
    """
    # Regular expression to detect ORFs: starts with ATG (start codon) and ends with a stop codon.
    pattern = re.compile(r'(?=(ATG(?:[ATGC]{3})*?(?:TAA|TAG|TGA|(?=[ATCG]{1,2}?$)|(?:[ATCG]{1,2})?$)))')
    orfs = dict()
    
    # Loop through each sequence in the input dictionary.
    for record_id, dna_sequence in sequences.items():
        len_seq = len(dna_sequence)
        if record_id not in orfs: orfs[record_id] = dict()

        # Process both strands: the original and the reverse complement.
        for strand, seq in [(0, dna_sequence), (1, str(Seq(dna_sequence).reverse_complement()))]:
            if strand not in orfs[record_id]: orfs[record_id][strand] = dict()

            # Search for ORFs using the regular expression.
            matches = pattern.finditer(seq)
            for match in matches:
                orf = match.group(1)
                start_index = len_seq - match.start(1) if strand == 1 else match.start(1) + 1
                end_index = len_seq - match.end(1) + 1 if strand == 1 else match.end(1)
                frame = (start_index-1)%3
                if frame not in orfs[record_id][strand]: orfs[record_id][strand][frame] = []
                if len(orf) % 3 == 0 and \
                   len(orf) >= min_dna_len:
                    orfs[record_id][strand][frame].append([start_index, end_index, orf])

            # Remove nested ORFs that are contained within larger ones (for a same frame).
            for frame, candidates in orfs[record_id][strand].items(): orfs[record_id][strand][frame] = remove_contained_ranges(candidates, reversed = strand==1)
    
    return orfs

def display(orfs):
    """
    Displays the found ORFs in a readable format.
    
    Args:
    orfs (dict): Dictionary containing the ORFs for each sequence and strand.
    """
    for seq, seq_obj in orfs.items():
        print("\n-----------------------------------", seq)
        for strand, strand_obj in seq_obj.items():
            print(f"\nSTRAND {(strand*-2)+1}:")
            for frame, frame_obj in strand_obj.items():
                print("\tframe", frame+1)
                for s, e, orf in frame_obj:
                    print(f"\t\tstart_pos: {s},\tstop_pos: {e},\tseq_protein: {DNA2AA(orf)}")


sequences = {
    "seq0": "GAGATCAGCTTTTGTTCAGAACCTGCGGCCGCTGAGGAGACGGTGACCTGGGTCCCCTGGCCCCAACAGTCCCTCTGATCGACTATCGGATCTCTGGCACAGTAATACACGGCCGTGTCCTCAGGGGTCACAGAGCTCAGCTGCAGGGAGAACTGGTTCTTGGACGTGTCCCTGGAGATGGAAGTGCGACTCTTGAGGGATGGACTGTAGTAAGTGCTGCCATCATAAGCTATGACTCCCATCCACTCCAGCCCCTTCCCTGAGGGCTGGCGGATCCAGCTCCAAGTATAATAGCTGGTTGTGATGGAGCCACCAGAGAAAGTGCAGGTGAGGGAGAGCGTCTGCGAGGGCTTCACCAGACTGGACCAGCTGCACCTGGGCCATGGCCGGCTGAGCTGCCAGCAGCAGCAA",
}
orfs = find_orfs(sequences, min_dna_len=30)
display(orfs)
