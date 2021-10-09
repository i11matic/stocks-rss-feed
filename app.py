#!/usr/bin/env python

import stocks_rss_feed
import streamlit as st

if __name__ == "__main__":
    stocks = stocks_rss_feed.stocks()
    st.title('Stock Information')
    st.dataframe(stocks.output_data_frame)
    with st.expander("Expand for Financial News!"):
        for title in stocks.titles:
            st.markdown("* " + title.text)