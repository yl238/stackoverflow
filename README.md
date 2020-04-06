StackExchange Similar Questions
==============================

Use unsupervised learning to identify similar questions in StackExchange.

This project uses the [spaCy](https://spacy.io/usage) library. After installation we need to download a language model.

```sh
pip install spacy
python -m spacy download en_core_web_[sm/md/lg]
```

The data is stored locally in mongodb database. To extract, run

```sh
mongoexport -h localhost -d cooking -c Posts --type=csv --fields Id,Title,Body,Tags,Score,AcceptedAnswerId,AnswerCount,FavoriteCount -q '{"PostTypeId":"1"}' --out ../data/interim/cooking_questions.csv
```

Directory structure based on the [cookiecutter data science project template](https://drivendata.github.io/cookiecutter-data-science/).
