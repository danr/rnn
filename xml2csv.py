# Download TinySeq XML format file from NCBI BioProject 33175:
# https://www.ncbi.nlm.nih.gov/bioproject?db=bioproject&Cmd=DetailsSearch&Term=33175%5Buid%5D
from bs4 import BeautifulSoup as BS
soup = BS(open('./sequence.fasta.xml'), 'lxml')

# You'll need to build the taxa taxadb database
from taxadb.taxid import TaxID
db = TaxID(dbtype='sqlite', dbname='taxadb.sqlite')

import sys

'''
soup.prettify()[:2100] ==
<html>
 <body>
  <tseqset>
   <tseq>
    <tseq_seqtype value="nucleotide">
    </tseq_seqtype>
    <tseq_accver>
     NR_170543.1
    </tseq_accver>
    <tseq_sid>
     gnl|REF_SSU16S|KU507537:1-1439
    </tseq_sid>
    <tseq_taxid>
     1849015
    </tseq_taxid>
    <tseq_orgname>
     Pseudoarcobacter acticola
    </tseq_orgname>
    <tseq_defline>
     Pseudoarcobacter acticola strain AR-13 16S ribosomal RNA, partial sequence
    </tseq_defline>
    <tseq_length>
     1439
    </tseq_length>
    <tseq_sequence>
     AGTGAACGCTGGCGGCGTGCTTAACACATGCAAGTCGAACGAGAACGGATTATAGCTTGCTATAATTGTCAGCTAAGTGGCGCACGGGTGAGTAATATATAGGTAACGTGCCCCAAAGAAGAGGATAACAGATGGAAACGTCTGCTAAGACTCTATATGCCTTTATGACAAAAGTCAGCAAGGGAAATATTTATAGCTTTGGGATCGGCCTGTACAGTATCAGTTAGTTGGTGAGGTAATGGCTCACCAAGACAATGACGCTTAACTGGTTTGAGAGGATGATCAGTCACACTGGAACTGAGACACGGTCCAGACTCCTACGGGAGGCAGCAGTGGGGAATATTGCACAATGGACGAAAGTCTGATGCAGCAACGCCGCGTGGAGGATGACACATTTCGGTGCGTAAACTCCTTTTATATGGGAAGATAATGACGGTACCATATGAATAAGCACCGGCTAACTCCGTGCCAGCAGCCGCGGTAATACGGAGGGTGCAAGCGTTACTCGGAATCACTGGGCGTAAAGAGCGTGTAGGCGGATAGGTAAGTCAGAAGTGAAATCCAATAGCTCAACTATTGAACTGCTTTTGAAACTGCTTATCTAGAATATGGGAGAGGTAGATGGAATTTCTGGTGTAGGGGTAAAATCCGTAGAGATCAGAAGGAATACCGATTGCGAAGGCGATCTACTGGAACATTATTGACGCTGAGACGCGAAAGCGTGGGGAGCAAACAGGATTAGATACCCTGGTAGTCCACGCCCTAAACGATGTACACTAGTTGTTGTGAGGCTCGACCTTGCAGTAATGCAGTTAACACATTAAGTGTACCGCCTGGGGAGTACGGTCGCAAGATTAAAACTCAAAGGAATAGACGGGGACCCGCACAAGCGGTGGAGCATGTGGTTTAATTCGACGATACACGAAGAACCTTACCTGGACTTGACATAGTAAGAACTTTCTAGAGATAGATTGGTGTCTGCTTGCAGAAACTTATATACAGGTGCTGCACGGCTGTCGTCAGCTCGTGTCGTGAGATGTTGGGTTAAGTCCCGCAACGAGCGCAACCCTCGTCATTAGTTGCTAACAGTTCGGCTGAGAACTCTAATGAGACTGCCTACGCAAGTAGGAGGAAGGTGAGGATGACGTCAAGTCATCATGGCCCTTACGTCCAGGGCTACACACGTGCTACAATGGGGTATACAAAGAGCAGCAATACGGTGACGTGGAGCAAATCTCAAAAATATCTCCCAGTTCGGATTGTAGTCTGCAACTCGACTACATGAAGTTGGAATCGCTAGTAATCGTAGATCAGCTATGCTACGGTGAATACGTTCCCGGGTCTTGTACTCACCGCCCGTCACACCATGGGAGTTGAACTCATTCGAAGCGGGGATGCTAAAATAGCTACCTTCCACAGTGGATTCAGCGACTGGGGTG
    </tseq_sequence>
   </tseq>
   <tseq>
    <tseq_seqtype value="nucleotide">
    </tseq_seqtype>
    <tseq_accver>
     NR_170542.1
'''

ranks = 'phylum class order family genus species'.split()

print(
    'taxid',
    'orgname',
    *ranks,
    'seq',
    sep=','
)

skipped = 0
for N, seq in enumerate(soup.find_all('tseq')):
    taxid = int(seq.find('tseq_taxid').get_text())
    lineage = dict(db.lineage_id(taxid, ranks=True))

    skip = False
    rs = []
    for rank in ranks:
        if rank in lineage:
            rs += [db.sci_name(lineage[rank])]
        else:
            print(f'{taxid=} has no {rank=} in {lineage=}, skipping...', file=sys.stderr)
            skip = True
            break

    if skip:
        skipped += 1
        continue

    print(
        taxid,
        seq.find('tseq_orgname').get_text(),
        *rs,
        seq.find('tseq_sequence').get_text(),
        sep=','
    )

print(f'{skipped=} / {N=}', file=sys.stderr)
