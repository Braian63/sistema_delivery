const menu = document.getElementById("menu")
const cartBtn = document.getElementById("cart-btn")
const cartModal = document.getElementById("cart-modal")
const cartItemsContainer = document.getElementById("cart-items")
const cartTotal = document.getElementById("cart-total")
// talvez tirar esse const checkoutBtn- motivo: inutil por enquanto
const checkoutBtn = document.getElementById("checkout-btn")
const closeModalBtn = document.getElementById("close-modal-btn")
const cartCounter = document.getElementById("cart-count")
const addressInput = document.getElementById("address")
const addressWarn = document.getElementById("address-warn")

let cart = [];
// Abrir modal carrinho
cartBtn.addEventListener("click", function() {
    updateCarrinho();
    cartModal.style.display = "flex"
})

// Fechar o modal quando click fora
cartModal.addEventListener("click", function (e) {
    if(e.target === cartModal){
        cartModal.style.display = "none"
    }
}) 

closeModalBtn.addEventListener("click", function () {
    cartModal.style.display = "none"
})

//add carrinho
menu.addEventListener('click', function(e) {
    let parentButton = e.target.closest(".add-to-cart-btn")

    if (parentButton) {
        const name = parentButton.getAttribute("data-name")
        const price = parentButton.getAttribute("data-price")
        addToCart(name, price)
    }
})

function addToCart(name, price){
    const existItem = cart.find(item => item.name == name);
    
    if (existItem) {
        existItem.quant += 1;
        return;
    }
    cart.push({name, price, quant: 1})
    updateCarrinho()
}

function updateCarrinho() {
    cartItemsContainer.innerHTML = "";
    let total = 0;
    cart.forEach((item) =>{
        const cartItemElement = document.createElement("div");
        cartItemElement.classList.add("flex", "justify-between", "mb-4", "flex-col")
    cartItemElement.innerHTML = `
    <div class="flex items-center justify-between">
        <div> 
            <p class="font-medium">${item.name}</p>
            <p>Qtd: ${item.quant}</p>
            <p class="font-medium mt-2">R$ ${item.price}</p>
        </div> 
        <div>
            <button class="remove-from-cart-btn" data-name="${item.name}">Remover</button> 
        </div>
    </div>`

    total += item.price * item.quant
    cartItemsContainer.appendChild(cartItemElement)   
    })
    cartTotal.textContent = total.toLocaleString("pt-BR", {style: "currency", currency: "BRL"});
    cartCounter.innerHTML = cart.length;
}

cartItemsContainer.addEventListener('click', function(e){
    const name = e.target.getAttribute("data-name")

    removerItem(name);
})

function removerItem(name) {
    const index = cart.findIndex((item)=>item.name === name);
    if (index !== -1) {
        const item = cart[index];
        if(item.quant > 1){
            item.quant -= 1;
            updateCarrinho();
            return;
        }
        cart.splice(index, 1);
        updateCarrinho();
    }
}

addressInput.addEventListener("input", function (event) {
    let inputValue = event.target.value;

    if(inputValue !== ""){
        addressInput.classList.remove("border-red-500")
        addressWarn.classList.add("hidden")
    }
})
// talvez tirar isso - motivo: inutil 
checkoutBtn.addEventListener("click", function() {
    const isOpen = RestauranteIsOpen();
    if (!isOpen){
        Toastify({
            text: "This is a toast",
            duration: 3000,
            close: true,
            gravity: "top", // `top` or `bottom`
            position: "left", // `left`, `center` or `right`
            stopOnFocus: true, // Prevents dismissing of toast on hover
            style: {
              background: "linear-gradient(to right, #00b09b, #96c93d)",
            },
          }).showToast();
        return;
    }
    if (cart.length === 0) return;
    if (addressInput.value === ""){
        addressWarn.classList.remove("hidden")
        addressInput.classList.add("border-red-500")
        return;
    }
    const cartItems = cart.map((item) => {
        return (
           `${item.name} Quantidade: (${item.quant}) Preço: R$${item.price} |`
           )
    }).join("")
    const message = encodeURIComponent(cartItems)
    const phone = "89994438317"

    window.open(`https://wa.me/${phone}?text=${message} Endereço ${addressInput.value}`, "_blank")

    cart = [];
    updateCarrinho();
})

function RestauranteIsOpen(){
    const data = new Date()
    const hora = data.getHours();
    return hora >= 18 && hora < 24; 
}

const spanItem = document.getElementById("date-span")
const isOpen =  RestauranteIsOpen();
if (isOpen) {
    spanItem.classList.remove("bg-red-500");
    spanItem.classList.add("bg-green-600")
    } else {
    spanItem.classList.remove("bg-green-600")
    spanItem.classList.add("bg-red-500")
    }
    
    document.getElementById('checkout-btn').addEventListener('click', function() {
        const userName = document.getElementById('user-name').value;
        const referencePoint = document.getElementById('reference-point').value;
        const cep = document.getElementById('cep').value;
        const street = document.getElementById('street').value;
        const number = document.getElementById('number').value;
        const neighborhood = document.getElementById('neighborhood').value;
        const phone = document.getElementById('phone').value;
    
        // Verifica se os campos de nome e endereço estão preenchidos
        if (!userName) {
            document.getElementById('name-warn').classList.remove('hidden');
            return;
        } else {
            document.getElementById('name-warn').classList.add('hidden');
        }
    
        if (!cep || !street || !number || !neighborhood || !phone) {
            document.getElementById('address-warn').classList.remove('hidden');
            return;
        } else {
            document.getElementById('address-warn').classList.add('hidden');
        }
    
        // Capturando os itens do carrinho
        let cartItems = [];
        document.querySelectorAll('#cart-items div').forEach(item => {
            cartItems.push({
                name: item.querySelector('.item-name').innerText,
                price: item.querySelector('.item-price').innerText
            });
        });
    
        // Criação do objeto de dados do pedido
        const orderData = {
            name: userName,
            reference_point: referencePoint,
            address: {
                cep: cep,
                street: street,
                number: number,
                neighborhood: neighborhood
            },
            phone: phone,
            items: cartItems,
            total: document.getElementById('cart-total').innerText
        };
    
        // Enviando o pedido para o backend
        fetch('/enviar-pedido/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken() // Captura o token CSRF se necessário
            },
            body: JSON.stringify(orderData)
        }).then(response => response.json())
          .then(data => {
            if (data.success) {
                Toastify({
                    text: "Pedido enviado com sucesso!",
                    duration: 3000,
                    gravity: "top",
                    position: "right",
                    backgroundColor: "#4CAF50"
                }).showToast();
                document.getElementById('cart-modal').classList.add('hidden');
            }
          }).catch(error => console.error('Erro:', error));
    });
    
    // Função para obter o token CSRF (se estiver usando Django)
    function getCSRFToken() {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [name, value] = cookie.trim().split('=');
            if (name === 'csrftoken') {
                return value;
            }
        }
        return null;
    }
        