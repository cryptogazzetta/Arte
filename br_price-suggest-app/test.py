import streamlit as st

def main():
    # Crie um espaço reservado para o conteúdo que você deseja atualizar
    content_placeholder = st.empty()

    # Exiba o div com a classe "price-estimate"
    show_price_estimate(content_placeholder)

def show_price_estimate(placeholder):
    # Crie o div com a classe "price-estimate"
    placeholder.markdown('''
    <style>
    .price-estimate {
        position: relative;
        width: 300px;
        height: 200px;
        background-color: #54A45E;
        color: white;
        font-size: 24px;
        font-weight: bold;
        border-radius: 5px;
        padding: 10px;
    }

    .centered-content {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
    }

    .centered-button {
        position: absolute;
        bottom: 10px;
        left: 50%;
        transform: translateX(-50%);
    }
    </style>
    
    <div class="price-estimate">
        <div class="centered-content">
            <h2>Preço sugerido</h2>
            <div class="price" id="price" style="display:none;">1234.56</div>
            <button class="centered-button" id="show_price_button" onclick="togglePrice()">Mostrar Preço</button>
        </div>
    </div>
    
    <script>
    function togglePrice() {
        var priceDiv = document.getElementById("price");
        if (priceDiv.style.display === "none") {
            priceDiv.style.display = "block";
        } else {
            priceDiv.style.display = "none";
        }
    }
    </script>
    ''', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
