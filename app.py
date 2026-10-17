import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Sayfa Yapılandırması ve Başlık
st.set_page_config(page_title="Akıllı Mutfak Asistanı", page_icon="🥑", layout="centered")

st.title("🥑 Akıllı Mutfak ve Buzdolabı Asistanı")
st.write("Evdeki malzemelerinizi seçin; sistem size uygun yemek tariflerini, eksik malzemeleri ve kalori analizini çıkarsın!")

# 1. Veri Tabanı
tarifler_verisi = {
    "Yemek_Adi": ["Menemen", "Makarna", "Omlet", "Tavuk Sote", "Peynirli Sandviç", "Mercimek Çorbası", "Salata"],
    "Ana_Malzemeler": [
        ["Yumurta", "Domates", "Biber", "Soğan"],
        ["Makarna", "Salça", "Sıvı Yağ"],
        ["Yumurta", "Peynir", "Tereyağı"],
        ["Tavuk", "Biber", "Domates", "Soğan"],
        ["Ekmek", "Peynir", "Domates"],
        ["Mercimek", "Soğan", "Su", "Sıvı Yağ"],
        ["Marul", "Domates", "Salatalık", "Zeytinyağı"]
    ],
    "Kategori": ["Kahvaltı", "Ana Yemek", "Kahvaltı", "Ana Yemek", "Atıştırmalık", "Çorba", "Atıştırmalık"],
    "Kalori": [300, 450, 250, 400, 280, 220, 150]
}
df_tarifler = pd.DataFrame(tarifler_verisi)
tum_malzemeler = sorted(list(set([m for alt in df_tarifler["Ana_Malzemeler"] for m in alt])))

# 2. Arayüz Seçimleri (Çoklu Seçim Kutusu)
st.subheader("🛒 Evdeki Malzemeleri Seçin")
evdeki_malzemeler = st.multiselect("Buzdolabında olan malzemeler:", tum_malzemeler, default=["Yumurta", "Domates"])

# 3. Hesaplama ve Gösterim Butonu
if st.button("🍳 Yemek Önerilerini ve Analizi Getir", type="primary"):
    if not evdeki_malzemeler:
        st.warning("Lütfen en az bir malzeme seçin!")
    else:
        evdekiler_set = set(evdeki_malzemeler)
        uygun_tarifler = []
        
        for index, satir in df_tarifler.iterrows():
            tarif_m = set(satir["Ana_Malzemeler"])
            ortak = tarif_m.intersection(evdekiler_set)
            eksik = tarif_m - evdekiler_set
            
            if len(ortak) > 0:
                uygun_tarifler.append({
                    "Yemek_Adi": satir["Yemek_Adi"],
                    "Kategori": satir["Kategori"],
                    "Kalori": satir["Kalori"],
                    "Eşleşen_Oran": len(ortak) / len(tarif_m),
                    "Eksik": list(eksik)
                })
                
        if uygun_tarifler:
            df_sonuc = pd.DataFrame(uygun_tarifler).sort_values(by="Eşleşen_Oran", ascending=False)
            
            st.success("🎉 Önerilen Tarifler:")
            
            for idx, row in df_sonuc.iterrows():
                yuzde = int(row["Eşleşen_Oran"] * 100)
                st.markdown(f"### 🍲 {row['Yemek_Adi']} ({row['Kategori']}) — Uygunluk: %{yuzde}")
                st.write(f"🔥 **Kalori:** {row['Kalori']} kcal")
                
                if len(row["Eksik"]) == 0:
                    st.info("✅ Tüm malzemeler evinizde hazır!")
                else:
                    st.warning(f"⚠️ Eksik Malzemeler: {', '.join(row['Eksik'])}")
                st.divider()
                
            # İstatistiksel Özet
            st.subheader("📊 Analiz Özeti")
            col1, col2 = st.columns(2)
            col1.metric("Bulunan Alternatif Sayısı", len(df_sonuc))
            col2.metric("Ortalama Kalori", f"{df_sonuc['Kalori'].mean():.1f} kcal")
            
            # Grafik
            st.subheader("📈 Kalori Karşılaştırma Grafiği")
            fig, ax = plt.subplots(figsize=(8, 4))
            bars = ax.bar(df_sonuc["Yemek_Adi"], df_sonuc["Kalori"], color='#4CAF50', edgecolor='darkgreen')
            ax.set_ylabel("Kalori (kcal)")
            ax.set_title("Önerilen Yemeklerin Kalorileri")
            plt.xticks(rotation=15)
            st.pyplot(fig)
        else:
            st.error("Seçtiğiniz malzemelerle uyuşan tarif bulunamadı.")
