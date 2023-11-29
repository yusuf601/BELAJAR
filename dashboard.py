# -*- coding: utf-8 -*-
"""Untitled14.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1s-pFIY8xxyP9zCCEjeI7v74WatXkzNeL
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

order_reviews = pd.read_csv('https://raw.githubusercontent.com/yusuf601/BELAJAR/main/order_reviews_dataset.csv')
orders = pd.read_csv('orders_dataset.csv')

order_reviews.info()

order_reviews["review_comment_message"].fillna("", inplace=True)
order_reviews["review_comment_title"].fillna("", inplace=True)

orders["order_delivered_customer_date"] = pd.to_datetime(orders["order_delivered_customer_date"])
orders["order_estimated_delivery_date"] = pd.to_datetime(orders["order_estimated_delivery_date"])



order_reviews["review_creation_date"] = pd.to_datetime(order_reviews["review_creation_date"])
order_reviews["review_answer_timestamp"] = pd.to_datetime(order_reviews["review_answer_timestamp"])

order_reviews["customer_satisfaction"] = order_reviews.apply(lambda x: "puas" if x["review_score"] >= 4 and x["review_comment_message"] else "tidak puas", axis=1)

st.set_page_config(layout="wide")
with st.container():


    st.title("Dashboard analisis data ")

# Membuat selectbox untuk memilih nilai k
k = st.sidebar.selectbox("Pilih nilai k", [2, 3, 4, 5])
k_options = ["2 (recommended)", "3", "4 ⚠️", "5 ⚠️"]
k = st.sidebar.selectbox("Pilih nilai k", k_options)
k = int(k[0])
if k > 3: st.warning("Nilai k yang tinggi akan menyebabkan overfitting.")

# Menampilkan data order_reviews
st.write("Data order_reviews")
st.dataframe(order_reviews)

# Ubah nilai customer_satisfaction menjadi numerik
order_reviews["customer_satisfaction"] = order_reviews["customer_satisfaction"].map({"puas": 1, "tidak puas": 0})
X = order_reviews[["review_score", "customer_satisfaction"]]
st.write("Pusat cluster awal:") 
centroids = X.sample(k)
st.dataframe(centroids)
labels = np.zeros(len(X))
iterations = 0


stop = False


while not stop:

    distances = np.sqrt(((X - centroids.iloc[0])**2).sum(axis=1))
    for i in range(1, k):
        distances = np.c_[distances, np.sqrt(((X - centroids.iloc[i])**2).sum(axis=1))]


    new_labels = np.argmin(distances, axis=1)


    if np.array_equal(labels, new_labels):

        stop = True
    else:

        labels = new_labels

        centroids = X.groupby(labels).mean()

        iterations += 1
        st.write(f"Iterasi ke-{iterations}:")
        st.dataframe(centroids)
st.write("Hasil akhir:")
st.dataframe(centroids)
st.write(f"Jumlah iterasi: {iterations}")

fig, ax = plt.subplots()
ax.scatter(X["review_score"], X["customer_satisfaction"], c=labels, cmap="rainbow")
ax.scatter(centroids["review_score"], centroids["customer_satisfaction"], marker="*", s=200, c="black")
ax.set_xlabel("review_score")
ax.set_ylabel("customer_satisfaction")
ax.set_title("Clustering dengan K-means sederhana")
st.pyplot(fig)

    # Membuat kontainer untuk menampilkan data orders
with st.container():
        # Menampilkan data orders
        st.write("Data orders")
        st.dataframe(orders)
        orders["delivery_difference"] = orders["order_delivered_customer_date"] - orders["order_estimated_delivery_date"]
        st.write("Persentase pesanan yang terkirim")
        st.write(orders["order_status"].value_counts(normalize=True)["delivered"] * 100)
        avg_diff = orders.groupby("customer_id")["delivery_difference"].mean()
        fig, ax = plt.subplots()
        ax.bar(avg_diff.index, avg_diff.values)
        ax.set_title("Rata-Rata Delivery Difference per Customer ID")
        ax.set_xlabel("Customer ID")
        ax.set_ylabel("Delivery Difference")
        ax.set_xticklabels(avg_diff.index, rotation=90)
        st.pyplot(fig)

# Membuat bagian yang dapat diperluas untuk menampilkan data order_reviews
with st.expander(label="Data order_reviews", expanded=True):
    # Membuat selectbox untuk memilih nilai k
    k = st.sidebar.selectbox("Pilih nilai k", [2, 3, 4, 5])
    k_options = ["2 (recommended)", "3", "4 ⚠️", "5 ⚠️"]
    k = st.sidebar.selectbox("Pilih nilai k", k_options)
    k = int(k[0])
    if k > 3: st.warning("Nilai k yang tinggi akan menyebabkan overfitting.")

    # Menampilkan data order_reviews
    st.write("Data order_reviews")
    st.dataframe(order_reviews)
order_reviews["customer_satisfaction"] = order_reviews["customer_satisfaction"].map({"puas": 1, "tidak puas": 0})
X = order_reviews[["review_score", "customer_satisfaction"]]
st.write("Pusat cluster awal:")
st.dataframe(centroids)
labels = np.zeros(len(X))
iterations = 0

    # Menampilkan data order_reviews
st.write("Data order_reviews")
st.dataframe(order_reviews)

col1, col2 = st.columns(2, width=6)
with col1:

    k = st.sidebar.selectbox("Pilih nilai k", [2, 3, 4, 5])
    k_options = ["2 (recommended)", "3", "4 ⚠️", "5 ⚠️"]
    k = st.sidebar.selectbox("Pilih nilai k", k_options)
    k = int(k[0])
    if k > 3: st.warning("Nilai k yang tinggi akan menyebabkan overfitting.")

    # Menampilkan data order_reviews
    st.write("Data order_reviews")
    st.dataframe(order_reviews)

    # Ubah nilai customer_satisfaction menjadi numerik
    order_reviews["customer_satisfaction"] = order_reviews["customer_satisfaction"].map({"puas": 1, "tidak puas": 0})
    X = order_reviews[["review_score", "customer_satisfaction"]]
    centroids = X.sample(k, random_state=42)
    st.write("Pusat cluster awal:")
    st.dataframe(centroids)
    labels = np.zeros(len(X))
    iterations = 0

    stop = False

    while not stop:

        distances = np.sqrt(((X - centroids.iloc[0])**2).sum(axis=1))
        for i in range(1, k):
            distances = np.c_[distances, np.sqrt(((X - centroids.iloc[i])**2).sum(axis=1))]

        new_labels = np.argmin(distances, axis=1)

        if np.array_equal(labels, new_labels):

            stop = True
        else:

            labels = new_labels

            centroids = X.groupby(labels).mean()

            iterations += 1
            st.write(f"Iterasi ke-{iterations}:")
            st.dataframe(centroids)
    st.write("Hasil akhir:")
    st.dataframe(centroids)
    st.write(f"Jumlah iterasi: {iterations}")

    fig, ax = plt.subplots()
    ax.scatter(X["review_score"], X["customer_satisfaction"], c=labels, cmap="rainbow")
    ax.scatter(centroids["review_score"], centroids["customer_satisfaction"], marker="*", s=200, c="black")
    ax.set_xlabel("review_score")
    ax.set_ylabel("customer_satisfaction")
    ax.set_title("Clustering dengan K-means sederhana")
    st.pyplot(fig)

# Mengisi kolom kedua dengan data orders
with col2:
    # Menampilkan data orders
    st.write("Data orders")
    st.dataframe(orders)
    orders["delivery_difference"] = orders["order_delivered_customer_date"] - orders["order_estimated_delivery_date"]
    st.write("Persentase pesanan yang terkirim")
    st.write(orders["order_status"].value_counts(normalize=True)["delivered"] * 100)
    avg_diff = orders.groupby("customer_id")["delivery_difference"].mean()
    fig, ax = plt.subplots()
    ax.bar(avg_diff.index, avg_diff.values)
    ax.set_title("Rata-Rata Delivery Difference per Customer ID")
    ax.set_xlabel("Customer ID")
    ax.set_ylabel("Delivery Difference")
    ax.set_xticklabels(avg_diff.index, rotation=90)
    st.pyplot(fig)
