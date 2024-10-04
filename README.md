# Open Reading Frames (ORF) finder using regex.

## ORF is defined as:
- Start condition: codon "ATG"
- Stop condition:  codon "TAA" or "TAG" or "TGA" or the end of the sequence is reached.
- The length is a multiple of 3.
- An ORF can contain multiple start codons "ATG" but only one stop codon "TAA" or "TAG" or "TGA".
- Within the same frame, if an ORF is completely contained in a larger one, then we don't consider it.

## Exemple:

min_dna_len = 30
input: `GAGATCAGCTTTTGTTCAGAACCTGCGGCCGCTGAGGAGACGGTGACCTGGGTCCCCTGGCCCCAACAGTCCCTCTGATCGACTATCGGATCTCTGGCACAGTAATACACGGCCGTGTCCTCAGGGGTCACAGAGCTCAGCTGCAGGGAGAACTGGTTCTTGGACGTGTCCCTGGAGATGGAAGTGCGACTCTTGAGGGATGGACTGTAGTAAGTGCTGCCATCATAAGCTATGACTCCCATCCACTCCAGCCCCTTCCCTGAGGGCTGGCGGATCCAGCTCCAAGTATAATAGCTGGTTGTGATGGAGCCACCAGAGAAAGTGCAGGTGAGGGAGAGCGTCTGCGAGGGCTTCACCAGACTGGACCAGCTGCACCTGGGCCATGGCCGGCTGAGCTGCCAGCAGCAGCAA`

output:
```
STRAND 1:
        frame 1
                start_pos: 178, stop_pos: 210,  seq_protein: MEVRLLRDGL*
                start_pos: 232, stop_pos: 291,  seq_protein: MTPIHSSPFPEGXRIQLQV*
                start_pos: 304, stop_pos: 411,  seq_protein: MEPPEKVQVRESVXEGFTRLDQLHLGHGRLSXQQQQ
        frame 2
                start_pos: 200, stop_pos: 235,  seq_protein: MDXSKXXHHKL*

STRAND -1:
        frame 3
                start_pos: 384, stop_pos: 223,  seq_protein: MAQVQLVQSGEALADALPHLHFLXXLHHNQLLYLELDPPALREGAGVDGSHSL*
        frame 2
                start_pos: 242, stop_pos: 3,    seq_protein: MGVIAYDGSTYYSPSLKSRTSISRDTSKNQFSLQLSSVTPEDTAVYYXARDPIVDQRDXXGQGTQVTVSSAAAGSEQKLI
        frame 1
                start_pos: 226, stop_pos: 137,  seq_protein: MMAALTTVHPSRVALPSPGTRPRTSSPXS*
```

The results are the same as those obtained from https://www.ncbi.nlm.nih.gov/orffinder/
