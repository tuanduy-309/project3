# How to run the code

## 1. Set up Neo4j
- Step 1: Create a local DBMS in Neo4j
- Step 2: Download the dataset music2.csv
- Step 3: Put the csv file into the import folder of the created DBMS
- Step 3: Run the DBMS and create the graph database in Neo4j Browser
  ```bash
  LOAD CSV WITH HEADERS FROM 'file:///music2.csv' AS row
  MERGE (artist:Artist {name: row.artistLabel, birthYear: toInteger(row.birthYear)})
  MERGE (song:Song {
  title: row.songLabel,
  releaseDate: row.releaseDate,
  genre: row.genreLabel
  })
  MERGE (composer:Composer {name: row.composerLabel})
  MERGE (artist)-[:PERFORMED]->(song)
  MERGE (composer)-[:COMPOSED]->(song)```

## 2. Install required package
  ``` pip install -r requirement,txt ```

## 3. Run the ``` openai_tuning.ipynb ```

>[!NOTE]
>After finishing creating the fine tuning job, you must wait 5 mins for the fine tuning to be processed
>Then run the remaining part of the code 

