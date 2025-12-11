import React, { createContext, useState, useEffect, useContext } from 'react';

// Chave para o localStorage
const CART_STORAGE_KEY = 'shoppingCart';

// 1. Criação do Contexto
const CartContext = createContext();

// Função para buscar o carrinho do localStorage
const getInitialCart = () => {
    const storedCart = localStorage.getItem(CART_STORAGE_KEY);
    // Retorna o array parseado ou um array vazio
    return storedCart ? JSON.parse(storedCart) : [];
};

// 2. Criação do Provedor (Provider)
export const CartProvider = ({ children }) => {
    // Estado para armazenar os itens do carrinho: [{ id, name, price, quantity }]
    const [cartItems, setCartItems] = useState(getInitialCart);

    // Efeito para persistir o carrinho no localStorage sempre que cartItems mudar
    useEffect(() => {
        localStorage.setItem(CART_STORAGE_KEY, JSON.stringify(cartItems));
    }, [cartItems]);

    // --- Funções de Manipulação do Carrinho ---

    /**
     * Adiciona um produto ao carrinho ou aumenta sua quantidade.
     * @param {object} product - O objeto produto do Bitrix/Django (deve ter id, name, price, image).
     * @param {number} quantity - Quantidade a ser adicionada.
     */
    const addToCart = (product, quantity = 1) => {
        setCartItems(prevItems => {
            const existingItemIndex = prevItems.findIndex(item => item.id === product.id);

            if (existingItemIndex > -1) {
                // Item existe: aumenta a quantidade
                const newItems = [...prevItems];
                newItems[existingItemIndex].quantity += quantity;
                return newItems;
            } else {
                // Item novo: adiciona ao carrinho
                return [
                    ...prevItems,
                    {
                        id: product.id,
                        name: product.name,
                        price: parseFloat(product.price), // Garante que o preço é numérico
                        image: product.image,
                        quantity: quantity,
                    },
                ];
            }
        });
    };

    /**
     * Atualiza a quantidade de um item no carrinho.
     */
    const updateQuantity = (productId, newQuantity) => {
        setCartItems(prevItems => {
            if (newQuantity <= 0) {
                // Se a quantidade for zero, remove o item
                return prevItems.filter(item => item.id !== productId);
            }

            return prevItems.map(item =>
                item.id === productId ? { ...item, quantity: newQuantity } : item
            );
        });
    };

    /**
     * Remove um item completamente do carrinho.
     */
    const removeFromCart = (productId) => {
        setCartItems(prevItems => prevItems.filter(item => item.id !== productId));
    };

    /**
     * Limpa o carrinho.
     */
    const clearCart = () => {
        setCartItems([]);
    };

    // --- Cálculos e Formatação ---

    const totalItems = cartItems.reduce((acc, item) => acc + item.quantity, 0);

    // Calcula o subtotal (precisão com parseFloat)
    const subtotalValue = cartItems.reduce((acc, item) => acc + (item.price * item.quantity), 0);

    // Formata o valor para BRL
    const formatBRL = (value) => {
        return new Intl.NumberFormat('pt-BR', {
            style: 'currency',
            currency: 'BRL',
        }).format(value);
    };


    const contextValue = {
        cartItems,
        totalItems,
        subtotal: subtotalValue.toFixed(2), // Valor numérico formatado
        formattedSubtotal: formatBRL(subtotalValue), // Valor em formato de moeda
        addToCart,
        updateQuantity,
        removeFromCart,
        clearCart,
        formatBRL, // Exporta o formatador para uso em outros componentes
    };

    return (
        <CartContext.Provider value={contextValue}>
            {children}
        </CartContext.Provider>
    );
};

// 3. Hook Customizado para usar o Carrinho
export const useCart = () => {
    const context = useContext(CartContext);
    if (context === undefined) {
        throw new Error('useCart must be used within a CartProvider');
    }
    return context;
};