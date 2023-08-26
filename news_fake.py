import streamlit as st
import pickle
import pandas as pd
import newspaper

# Load the trained model
with open('fake_news_Detector.pickle', 'rb') as model_file:
    model = pickle.load(model_file)

def extract_news_content(article_link):
    try:
        # Initialize the Article object
        article = newspaper.Article(article_link)
        
        # Download and parse the article
        article.download()
        article.parse()
        
        # Extract the title and text
        title = article.title
        text = article.text
        
        return title, text
    except Exception as e:
        return None, None

# Streamlit app
def main():
    st.title("Check If the news You Are Reading is Fake or not")

    article_link = st.text_input("Enter the link to the news article: ")

    if article_link:
        title, text = extract_news_content(article_link)
        
        if title and text:
            if st.button("Test"):
                input_dict = {
                    'X_test': text
                }
                input_df = pd.DataFrame([input_dict])
                prediction = model.predict(input_df)

                if prediction == 1:
                    st.error("The News with title '{}' is Fake".format(title))
                else:
                    st.success("The News with title '{}' is NOT Fake".format(title))
        else:
            st.warning("Invalid article link or unable to extract content")
            # streamlit run news_fake.py

if __name__ == '__main__':
    main()
