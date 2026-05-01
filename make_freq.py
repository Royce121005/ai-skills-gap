import pandas as pd 
import random 
random.seed(42) 
skills = ['Python','SQL','Machine Learning','Data Analysis','Excel','Communication','Project Management','Java','JavaScript','Cloud Computing','Deep Learning','NLP','TensorFlow','PyTorch','Docker','Kubernetes','Git','Agile','Power BI','Tableau','R','Scala','Spark','Hadoop','Azure','AWS','GCP','Linux','REST API','Microservices','Statistics','Data Visualization','Cybersecurity','Networking','DevOps','Scrum','JIRA','Figma','UI UX','Product Management'] 
counts = sorted([random.randint(10000,100000) for _ in skills], reverse=True) 
pd.DataFrame({'skill_name':skills,'job_postings':counts}).to_csv('data/raw/skill_counts.csv',index=False) 
print('skill_counts.csv created') 
