

0. If you dont already have poetry, run pip install poetry 
1. Clone the repository.
2. Run : cd pubmed-fetcher
3. Run : poetry install --no-root
4. To use, use command : poetry run get-papers-list "YOUR QUERY" -f YOUR-FILE-NAME.csv -d
6. If you don't want the file to be saved then you can skip the -f parameter, in which case the output will be printed to console.
7. For help use: poetry run get-papers-list -h         

        
