import React, { useState } from 'react';
import { useCart } from '../context/CartContext';
import { ecommerceService } from '../services/api';

const CartSidebar = () => {
    const {
        cartItems,
        updateQuantity,
        removeFromCart,
        formattedSubtotal,
        clearCart
    } = useCart();

    const [isProcessing, setIsProcessing] = useState(false);
    const [checkoutStatus, setCheckoutStatus] = useState(null); // 'success' | 'error'

    // Simulação de Dados de Formulário (Hardcoded para teste rápido)
    // Em produção, você criaria inputs para o usuário digitar.
    const handleCheckout = async () => {
        if (cartItems.length === 0) return;

        setIsProcessing(true);
        setCheckoutStatus(null);

        const checkoutData = {
            items: cartItems.map(item => ({
                bitrix_product_id: String(item.id),
                quantity: item.quantity
            })),
            endereco_completo: "Rua Exemplo, 123 - São Paulo, SP",
            // Cartão terminando em 1 = SUCESSO na nossa lógica do backend
            card_number: "1234123412341231",
            card_holder_name: "TESTE USER",
            expiry_date: "12/30",
            cvv: "123"
        };

        try {
            const result = await ecommerceService.checkout(checkoutData);
            console.log("Compra realizada:", result);
            setCheckoutStatus('success');
            clearCart(); // Limpa o carrinho após sucesso
        } catch (error) {
            console.error("Erro no checkout:", error);
            alert(`Erro: ${error.detail || 'Falha no pagamento'}`);
            setCheckoutStatus('error');
        } finally {
            setIsProcessing(false);
        }
    };

    if (checkoutStatus === 'success') {
        return (
            <div style={styles.container}>
                <div style={{ textAlign: 'center', color: 'green', marginTop: '50px' }}>
                    <h2>🎉 Sucesso!</h2>
                    <p>Seu pedido foi processado e enviado ao Bitrix24.</p>
                    <button
                        onClick={() => setCheckoutStatus(null)}
                        style={{ ...styles.button, background: '#007bff', marginTop: '20px' }}
                    >
                        Fazer nova compra
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div style={styles.container}>
            <h3 style={{ borderBottom: '1px solid #ddd', paddingBottom: '10px' }}>
                🛒 Seu Carrinho ({cartItems.length})
            </h3>

            {cartItems.length === 0 ? (
                <p style={{ color: '#888', fontStyle: 'italic', marginTop: '20px' }}>
                    Seu carrinho está vazio.
                </p>
            ) : (
                <div style={{ flexGrow: 1, overflowY: 'auto', margin: '20px 0' }}>
                    {cartItems.map((item) => (
                        <div key={item.id} style={styles.itemCard}>
                            <div style={{ flexGrow: 1 }}>
                                <strong>{item.name}</strong>
                                <div style={{ fontSize: '0.9em', color: '#555' }}>
                                    R$ {item.price.toFixed(2)} un.
                                </div>
                            </div>

                            <div style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
                                <button onClick={() => updateQuantity(item.id, item.quantity - 1)} style={styles.qtyBtn}>-</button>
                                <span>{item.quantity}</span>
                                <button onClick={() => updateQuantity(item.id, item.quantity + 1)} style={styles.qtyBtn}>+</button>
                            </div>

                            <button
                                onClick={() => removeFromCart(item.id)}
                                style={{ ...styles.qtyBtn, background: '#ff4d4d', color: 'white', marginLeft: '10px' }}
                            >
                                x
                            </button>
                        </div>
                    ))}
                </div>
            )}

            {cartItems.length > 0 && (
                <div style={{ borderTop: '1px solid #ddd', paddingTop: '20px' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '15px', fontSize: '1.2em' }}>
                        <strong>Total:</strong>
                        <strong>{formattedSubtotal}</strong>
                    </div>

                    <button
                        onClick={handleCheckout}
                        disabled={isProcessing}
                        style={{
                            ...styles.button,
                            background: isProcessing ? '#ccc' : '#28a745',
                            cursor: isProcessing ? 'not-allowed' : 'pointer'
                        }}
                    >
                        {isProcessing ? 'Processando...' : 'Finalizar Compra'}
                    </button>
                </div>
            )}
        </div>
    );
};

// Estilos simples em objeto JS
const styles = {
    container: {
        width: '300px',
        borderLeft: '1px solid #ddd',
        padding: '20px',
        background: '#f8f9fa',
        display: 'flex',
        flexDirection: 'column',
        height: '100%', // Para ocupar altura total se estiver num layout flex
        minHeight: '400px'
    },
    itemCard: {
        background: '#fff',
        border: '1px solid #eee',
        borderRadius: '4px',
        padding: '10px',
        marginBottom: '10px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between'
    },
    qtyBtn: {
        width: '25px',
        height: '25px',
        border: '1px solid #ccc',
        background: '#fff',
        cursor: 'pointer',
        borderRadius: '3px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center'
    },
    button: {
        width: '100%',
        padding: '12px',
        color: 'white',
        border: 'none',
        borderRadius: '5px',
        fontSize: '1em',
        fontWeight: 'bold'
    }
};

export default CartSidebar;