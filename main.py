import streamlit as st
import plotly.express as px
from model import SentimentAnalyzer
from utils import preprocess_text, get_sample_texts
import pandas as pd
from database import save_sentiment_analysis, get_recent_analyses

# Page configuration
st.set_page_config(
    page_title="Türkçe Duygu Analizi",
    page_icon="🔍",
    layout="wide"
)

# Custom CSS
with open('/Users/sema/Documents/Repo/sentiment-analysis/sentiment-analysis/styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Initialize sentiment analyzer
analyzer = SentimentAnalyzer()

def main():
    st.title("🔍 Türkçe Duygu Analizi")
    st.markdown("---")

    # Sidebar
    st.sidebar.header("Hakkında")
    st.sidebar.info(
        "Bu uygulama, Türkçe metinler üzerinde duygu analizi yapar. "
        "Metninizi girin veya örnek metinlerden birini seçin."
    )

    # Display recent analyses in sidebar
    st.sidebar.markdown("---")
    st.sidebar.header("Son Analizler")
    recent_analyses = get_recent_analyses(5)
    for analysis in recent_analyses:
        with st.sidebar.expander(f"{analysis.sentiment.title()} ({analysis.confidence:.2%})"):
            st.write(analysis.input_text[:100] + "..." if len(analysis.input_text) > 100 else analysis.input_text)
            st.caption(f"Tarih: {analysis.created_at.strftime('%Y-%m-%d %H:%M')}")

    # Main content
    col1, col2 = st.columns([2, 1])

    with col1:
        # Text input
        text_input = st.text_area(
            "Analiz edilecek metni girin:",
            height=150,
            placeholder="Metninizi buraya yazın..."
        )

        # Sample text selection
        st.markdown("### veya örnek bir metin seçin:")
        sample_texts = get_sample_texts()
        selected_sample = st.selectbox(
            "Örnek metinler:",
            ["Seçiniz..."] + list(sample_texts.keys())
        )

        if selected_sample != "Seçiniz...":
            text_input = sample_texts[selected_sample]
            st.text_area("Seçilen örnek:", value=text_input, height=150, disabled=True)

    # Analysis
    if st.button("Analiz Et") and text_input:
        try:
            with st.spinner("Analiz yapılıyor..."):
                # Preprocess text
                processed_text = preprocess_text(text_input)

                # Get sentiment
                sentiment, probability = analyzer.predict(processed_text)

                # Save to database
                save_sentiment_analysis(text_input, sentiment, probability)

                # Display results
                with col2:
                    st.markdown("### Analiz Sonucu")

                    # Sentiment indicator
                    if sentiment == "positive":
                        st.markdown(
                            f'<div class="sentiment-box positive">'
                            f'<h3>😊 Pozitif</h3>'
                            f'<p>Güven: {probability:.2%}</p>'
                            f'</div>',
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                            f'<div class="sentiment-box negative">'
                            f'<h3>😔 Negatif</h3>'
                            f'<p>Güven: {probability:.2%}</p>'
                            f'</div>',
                            unsafe_allow_html=True
                        )

                    # Confidence visualization
                    fig = px.bar(
                        x=['Pozitif', 'Negatif'],
                        y=[probability if sentiment == "positive" else 1-probability,
                           probability if sentiment == "negative" else 1-probability],
                        title="Duygu Analizi Güven Oranları",
                        color_discrete_sequence=['#00CC96', '#EF553B']
                    )
                    fig.update_layout(
                        xaxis_title="Duygu",
                        yaxis_title="Güven Oranı",
                        showlegend=False
                    )
                    st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"Bir hata oluştu: {str(e)}")

    else:
        with col2:
            st.info("Analiz için metin girin ve 'Analiz Et' butonuna tıklayın.")

if __name__ == "__main__":
    main()