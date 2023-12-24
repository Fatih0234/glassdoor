import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Job description text
job_description = """
As a Junior Data Scientist at BearingPoint your role will involve working with large datasets to extract meaningful insights and support decision-making processes. You will collaborate with senior data scientists and cross-functional teams to solve complex business problems using statistical analyses and machine learning techniques. Here is a more detailed description of the responsibilities and qualifications for a junior data scientist:


Responsibilities:

Data collection and preprocessing: Collecting, cleaning, and organizing data from various sources to ensure data quality and integrity.
Statistical analysis: Applying statistical methods to analyze data and identify patterns, correlations, and trends.
Machine learning model development: Developing and implementing predictive models using machine learning algorithms to solve specific business problems.
Data visualization: Creating clear and visually appealing dashboards and reports to communicate insights and findings to stakeholders.
Collaborating with cross-functional teams: Working closely with business stakeholders, data engineers, and senior data scientists to understand business requirements and align analytical solutions accordingly.
Data-driven decision-making: Using data analysis to provide recommendations and insights that drive business strategies and improve operational efficiency.
Continuous learning: Keeping up-to-date with the latest advancements in data science techniques, tools, and technologies to enhance skills and knowledge.
Documentation and reporting: Documenting data analysis processes, methodologies, and findings in a clear and organized manner.
Quality assurance: Ensuring the accuracy and reliability of data analyses and models by conducting tests and validations.
Ethical considerations: Maintaining data privacy and security while handling sensitive information and adhering to ethical guidelines.

Qualifications:

Bachelor's or Master's degree in a quantitative field such as computer science, statistics, mathematics, or data science.
Proficiency in programming languages such as Python or R, and experience with data manipulation and analysis libraries.
Knowledge of statistical concepts and experience applying statistical methods to data analysis.
Familiarity with machine learning algorithms and experience developing predictive models.
Strong data visualization skills using tools like Tableau, Power BI, or matplotlib.
Familiarity with SQL and databases for data extraction and manipulation.
Strong problem-solving skills and attention to detail.
Excellent communication and collaboration skills to work effectively in a team environment.
Ability to learn quickly and adapt to new technologies and methodologies.
Any relevant certifications or projects demonstrating practical experience in data science would be advantageous.
"""
job_description = job_description.lower()

# List of keyword categories and their corresponding keywords
keyword_categories = {
    'Programming Languages': ['python', 'r', 'java', 'scala', 'julia'],
    'Machine Learning Libraries and Frameworks': ['tensorflow', 'pytorch', 'scikit-learn', 'keras', 'spark mllib'],
    'Data Analysis Tools': ['pandas', 'numpy', 'jupyter', 'matlab'],
    'Statistical Analysis': ['statistics', 'statistical modeling', 'hypothesis testing', 'statistical inference', 'statistical analysis', 'statistical methods'],
    'Data Visualization': ['matplotlib', 'seaborn', 'tableau', 'power bi'],
    'Big Data Technologies': ['hadoop', 'apache spark', 'hive', 'pig'],
    'Database Systems': ['sql', 'nosql', 'mongodb', 'mysql'],
    'Feature Engineering': ['feature extraction', 'feature selection'],
    'Model Evaluation and Metrics': ['cross-validation', 'roc-auc', 'precision-recall', 'f1 score'],
    'Deep Learning': ['neural networks', 'cnn', 'rnn', 'nlp'],
    'Cloud Platforms': ['aws', 'azure', 'google cloud platform', 'gcp'],
    'Version Control': ['git', 'github', 'gitlab'],
    'Data Preprocessing': ['data cleaning', 'data transformation', 'imputation', 'data wrangling', 'preprocessing', 'data collection'],
    'Collaboration and Communication': ['team collaboration', 'communication skills', 'documentation'],
    'Domain-Specific Knowledge': ['healthcare', 'finance', 'e-commerce', 'telecom'],
    'Business Acumen': ['business intelligence', 'data-driven decision making', 'stakeholder engagement'],
    'Soft Skills': ['analytical thinking', 'problem solving', 'critical thinking'],
    'Educational Background': ['bachelor', 'master', 'phd'],
}

# Process the job description text using spaCy
doc = nlp(job_description)

# Create a dictionary to store matched keywords for each category
matched_keywords = {category: [] for category in keyword_categories}

# Check for keywords in the text and organize them into categories
for category, keywords in keyword_categories.items():
    for keyword in keywords:
        if keyword.lower() in doc.text.lower():
            matched_keywords[category].append(keyword)

# Print the matched keywords for each category
for category, keywords in matched_keywords.items():
    print(f'{category}: {keywords}')

# If no keywords are found in a category, print 'None'
for category, keywords in keyword_categories.items():
    if not matched_keywords[category]:
        print(f'{category}: None')