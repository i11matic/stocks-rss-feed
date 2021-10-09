#! /usr/bin/env python

import requests
import spacy
from bs4 import BeautifulSoup
import yfinance as yf
import pandas
import pkgutil
from io import StringIO


class stocks:
    def __init__(
        self,
        url="https://economictimes.indiatimes.com/markets/stocks/rssfeeds/2146842.cms",
    ):
        self.url = url
        self.response = self.__get_url(self.url)
        self.titles = self.__get_titles()
        self.companies = self.__get_companies()
        self.nifty_company_list = self.__load_nifty_list()
        self.stock_dict = {
            "Org": [],
            "Symbol": [],
            "currentPrice": [],
            "dayHigh": [],
            "dayLow": [],
            "forwardPE": [],
            "dividendYield": [],
        }
        self.output_data_frame = self.__load()

    def __get_url(self, url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err.response)
        return response

    def __load_nifty_list(self):
        return pandas.read_csv(
            StringIO(
                pkgutil.get_data(__name__, "resources/ind_nifty500list.csv").decode(
                    "utf-8"
                )
            )
        )

    def __get_titles(self):
        titles = BeautifulSoup(self.response.content, features="xml")
        return titles.find_all("title")

    def __get_companies(self):
        companies = []
        nlp = spacy.load("en_core_web_sm")
        for title in self.titles:
            for token in nlp(title.text).ents:
                if token.label_ == "ORG":
                    companies.append(token.text)
        return companies

    def __load(self):
        for company in self.companies:
            if self.nifty_company_list["Company Name"].str.contains(company).sum():
                symbol = self.nifty_company_list[
                    self.nifty_company_list["Company Name"].str.contains(company)
                ]["Symbol"].values[0]
                org_name = self.nifty_company_list[
                    self.nifty_company_list["Company Name"].str.contains(company)
                ]["Company Name"].values[0]
                self.stock_dict["Org"].append(org_name)
                self.stock_dict["Symbol"].append(symbol)
                stock_info = yf.Ticker(symbol + ".NS").info
                self.stock_dict["currentPrice"].append(stock_info["currentPrice"])
                self.stock_dict["dayHigh"].append(stock_info["dayHigh"])
                self.stock_dict["dayLow"].append(stock_info["dayLow"])
                self.stock_dict["forwardPE"].append(stock_info["forwardPE"])
                self.stock_dict["dividendYield"].append(stock_info["dividendYield"])
        return pandas.DataFrame(self.stock_dict)
