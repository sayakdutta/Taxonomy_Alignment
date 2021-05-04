 # PIDGIN Alignment  #
This folder has four different files:-
1) pidgin.py:- This file generates the seeds and the input-graph file from paris results and interlingua respectively
2) json_loader.py:- Read json files contained coreNLP parsed wikipedia entities and creates an interlingua from it
3) data_gen.py:- This file takes the two output files obtained from running pidgin twice with dbpedia and wikidata labels respectively and creating the final alignment result
4) verb_alignment.py:- Simply takes the highest equivalent dbpedia relation label for each verb and creates a synonyms file that can be indexed by a dbpedia relation

DATASET:- You can generate interlingua yourself  or use a sample one from [here](https://drive.google.com/drive/folders/1LaaMKcXp29KsnHzfmKP7p5w0YLBeqLzX?usp=sharing)<br/>
## How to Run ##

After generating the input graph and seeds, run the MAD algorithm as specified in [junto](https://github.com/parthatalukdar/junto).
