# CSC549 HW3 -- Vivienne Clarke 
#-------------------------------------------
# first locally install BLAST+ (i have a MacBook M1 so i downloaded ncbi-blast-2.16.0+-aarch64.dmg )
# brew install blast

#-------------------------------------------
# python code that parses the human sequences 

# imports
import subprocess
import os
from Bio.Blast.Applications import NcbiblastpCommandline
from Bio import SeqIO
from Bio.Blast import NCBIXML

# run makeblastdb to format the mouse.fa file
subprocess.run([
    "/opt/homebrew/bin/makeblastdb",  # path to makeblastdb executable
    "-in", "mouse.fa",
    "-dbtype", "prot",
    "-out", "mouse_db"
], check=True)

# define parameters
blastp_cline = NcbiblastpCommandline(
    cmd="/opt/homebrew/bin/blastp",  # path to the blastp executable
    query="human.fa",  # query protein file
    db="mouse_db",                   # database name
    evalue=0.001,             # e-value 
    out="output.xml",            # output file
    outfmt=5                  # output format (5 for XML)
)

#run the command
#stdout, stderr = blastp_cline()

try:
    stdout, stderr = blastp_cline()
except Exception as e:
    print(f"Error running BLAST: {e}")
    exit()


# open the output XML file so it can be read
with open("output.xml") as result_handle, open("blast_results.txt", "w") as output_file:
    
    # parse the BLAST XML output
    blast_records = NCBIXML.parse(result_handle)
    
    # iterate through each sequence
    for blast_record in blast_records:
        # each blast_record is a query sequence
        output_file.write(f"Query: {blast_record.query}\n")

        # iterate through alignments (each is a match in the database)
        for alignment in blast_record.alignments:
            output_file.write(f"Match: {alignment.hit_def}\n")

            # iterate through high-scoring segment pairs 
            for hsp in alignment.hsps:
                output_file.write(f"E-value: {hsp.expect}\n")
                output_file.write(f"Score: {hsp.score}\n")
                output_file.write(f"Alignment length: {hsp.align_length}\n")
                output_file.write(f"Query sequence: {hsp.query}\n")
                output_file.write(f"Match sequence: {hsp.sbjct}\n")
                output_file.write("-" * 60 + "\n")
                

#-------------------------------------------

