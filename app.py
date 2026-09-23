import streamlit as st
import requests
import base64

st.set_page_config(page_title="TikTok Affiliate AI Control Panel", layout="centered", page_icon="🚀")

st.title("🚀 TikTok Affiliate AI Control Panel")
st.write("Input detail produk & upload foto langsung dari galeri HP untuk memicu generasi video otomatis via n8n AI Engine.")

# URL Webhook dari n8n Anda
N8N_WEBHOOK_URL = "https://n8n-affiliate.onrender.com/webhook/generate-tiktok-video"

with st.form("product_form"):
    product_name = st.text_input("Nama Produk", placeholder="Misal: Kemeja Oversize Streetwear")
    category = st.selectbox("Kategori", ["Fashion", "Electronics", "Beauty", "Home & Living", "Automotive"])
    selling_points = st.text_area("Keunggulan Produk", placeholder="Bahan katun combed 24s, adem, tidak mudah luntur...")
    price = st.text_input("Harga", placeholder="Rp 89.000")
    
    # Upload Foto Langsung dari Galeri HP
    uploaded_file = st.file_uploader("Upload Foto Produk (Galeri HP)", type=["jpg", "jpeg", "png", "webp"])
    
    affiliate_link = st.text_input("Link Keranjang Kuning / Affiliate", placeholder="https://vt.tiktok.com/xxxx/")
    
    submit_button = st.form_submit_button("🎬 Buat Video Autopilot")

if submit_button:
    if not product_name:
        st.error("Mohon isi Nama Produk!")
    elif not uploaded_file:
        st.error("Mohon upload foto produk dari galeri HP Anda!")
    else:
        bytes_data = uploaded_file.getvalue()
        image_base64 = base64.b64encode(bytes_data).decode("utf-8")
        image_filename = uploaded_file.name
            
        payload = {
            "Product Name": product_name,
            "Category": category,
            "Selling Points": selling_points,
            "Price": price,
            "Image Base64": image_base64,
            "Image Filename": image_filename,
            "Affiliate Link": affiliate_link
        }
        
        with st.spinner("Mengirim perintah & foto ke n8n AI Engine..."):
            try:
                response = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=30)
                if response.status_code == 200:
                    st.success("✅ Perintah berhasil dikirim! AI sedang memproses naskah, voiceover, dan render video.")
                    st.info("Cek aplikasi Telegram di HP Anda untuk pratinjau hasil video.")
                else:
                    st.error(f"Gagal menghubungkan ke n8n. Status Code: {response.status_code}")
            except Exception as e:
                st.error(f"Terjadi kesalahan koneksi: {str(e)}")
    
