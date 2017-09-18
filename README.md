# OnlineNewsPopularity
Using Machine Learning techniques to determine the popularity of online news.  

We've tried to implement and improvise upon the techniques implemented in this paper - <http://cs229.stanford.edu/proj2015/328_report.pdf>. The dataset we use is the `UCI's Online News Popularity dataset` - <https://archive.ics.uci.edu/ml/datasets/Online+News+Popularity>  

For dimensionality reduction, `Fischer Scores` were used as doing so yielded better results than `PCA`.  

The ML algos used are:  
1. Linear Regression  
2. Logistic Regression  
3. Naive Bayes classifier  
4. MLP/Neural Nets  
5. SVM  
6. Random Forest  
7. REPTree  

Some of them are library implementations - `scikit-learn`, while some are coded from scratch.  

And then we used the `TFIDF` approach followed by the above ML algos.  

- Most of the code in the root dir can be run with a simple `python filename.py` where the filename indicates the ML algorithm implemented. Some of them can take quite some time to run.  
- The root dir also contains various graphs and plots generated based on the results.  
- `OnlineNewsPopularity.csv` is the dataset.  
- The file `NewOnlineNewsPopularity.arff` is an input for `Algorithmia's` ML algos - <https://algorithmia.com/tags/machine%20learning> which can be run online.  
- The directory `Feature Extractor` contains code to select a subset of the original features based on `Fischer scores`  
- The directory `FetchPost` contains code in Go - this was our first attempt at `scraping full articles` off the `Mashable url's` provided in the dataset.  
- The directory `newfetchpost` contains working code to scrape full articles using `python goose` - takes quite some time. It also contains `counter.py` which implements various ML algos as pipelines on the extracted full articles using the `TFIDF` approach - again, this takes time as the TFIDF approach inherently implies usage of a rich feature set.  
- `201503003.zip` is the final submission.  

**Please refer to `SMAI Final Presentation.pdf` for a detailed discussion of the implementation and results**

