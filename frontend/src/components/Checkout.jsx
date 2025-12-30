// frontend/src/components/Checkout.jsx
import React, { useEffect, useState } from 'react';
import { initMercadoPago, Payment } from '@mercadopago/sdk-react';

function Checkout() {
    // 1. Inicializa o SDK com sua Public Key (Front-end usa a PÚBLICA, Back-end a PRIVADA)
    useEffect(() => {
        initMercadoPago('TEST-41741a4f-fb28-4d04-b73c-3141dfaeb972', {
            locale: 'pt-BR'
        });
    }, []);

    // Estado para controlar feedback visual
    const [resultado, setResultado] = useState(null);

    // 2. Configuração do Valor a ser cobrado
    const initialization = {
        amount: 100.00, // Valor fixo para teste (R$ 100,00)
        payer: {
            email: 'cliente_teste_v01@gmail.com', // Email fictício para o Brick pré-preencher
        },
    };

    // 3. Customização visual (Opcional)
    const customization = {
        paymentMethods: {
            creditCard: 'all', // Aceitar todos cartões
            bankTransfer: 'all', // Aceitar Pix
            maxInstallments: 12
        },
    };

    // 4. Função que é chamada quando o usuário clica em "Pagar"
    const onSubmit = async ({ formData }) => {
        const token = localStorage.getItem('accessToken');

        try {
            // Envia os dados criptografados do Brick para o NOSSO Backend
            const response = await fetch('http://127.0.0.1:8000/api/pagamentos/processar/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}` // Autenticação JWT
                },
                body: JSON.stringify(formData) // O Brick já entrega o JSON pronto
            });

            const data = await response.json();

            if (response.ok) {
                setResultado({ tipo: 'sucesso', msg: `✅ Pagamento Aprovado! ID: ${data.id_pagamento}` });
            } else {
                setResultado({ tipo: 'erro', msg: `❌ Erro: ${data.detail || 'Pagamento recusado'}` });
            }

        } catch (error) {
            setResultado({ tipo: 'erro', msg: '❌ Erro de conexão com o servidor.' });
            console.error(error);
        }
    };

    const onError = async (error) => {
        console.log(error); // Erro de validação do próprio Brick (ex: cartão vencido)
    };

    const onReady = async () => {
        // O Brick carregou e está visível
    };

    return (
        <div style={{ maxWidth: '500px', margin: '20px auto', padding: '20px', border: '1px solid #ccc', borderRadius: '8px' }}>
            <h2>💳 Finalizar Compra</h2>

            {/* O Componente Mágico do Mercado Pago */}
            <Payment
                initialization={initialization}
                customization={customization}
                onSubmit={onSubmit}
                onReady={onReady}
                onError={onError}
            />

            {/* Exibe mensagem de Sucesso ou Erro */}
            {resultado && (
                <div style={{
                    marginTop: '20px',
                    padding: '15px',
                    backgroundColor: resultado.tipo === 'sucesso' ? '#d4edda' : '#f8d7da',
                    color: resultado.tipo === 'sucesso' ? '#155724' : '#721c24',
                    borderRadius: '5px'
                }}>
                    <strong>{resultado.msg}</strong>
                </div>
            )}
        </div>
    );
}

export default Checkout;