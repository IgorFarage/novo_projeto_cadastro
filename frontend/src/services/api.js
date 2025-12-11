// File: frontend/src/services/api.js

import axios from 'axios';

// Cria uma instância do Axios com configurações customizadas
const api = axios.create({
    baseURL: 'http://127.0.0.1:8000', // URL do backend Django
    timeout: 30000, // Timeout de 30 segundos (aumentado para imagens do Bitrix)
    headers: {
        'Content-Type': 'application/json'
    }
});

// --- INTERCEPTOR (O Segredo da Produção) ---
// Antes de cada requisição sair, o axios verifica se tem token e o adiciona no cabeçalho.
api.interceptors.request.use(
    (config) => {
        // Pega o token salvo no Login.jsx (notei que lá você usou 'accessToken')
        const token = localStorage.getItem('accessToken');

        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// --- FUNÇÕES DE E-COMMERCE (Passo 6 efetivo) ---

export const ecommerceService = {
    /**
     * Busca a lista de produtos (integrado ao Bitrix via Django)
     */
    getProducts: async () => {
        try {
            // Chama a rota criada no backend: /api/cadastro/products/
            const response = await api.get('/api/cadastro/products/');
            return response.data;
        } catch (error) {
            console.error("Erro ao buscar produtos:", error);
            throw error;
        }
    },

    /**
     * Envia o checkout para o backend
     */
    checkout: async (checkoutData) => {
        try {
            // Chama a rota criada no backend: /api/cadastro/checkout/
            const response = await api.post('/api/cadastro/checkout/', checkoutData);
            return response.data;
        } catch (error) {
            // Retorna o erro tratado para o componente exibir (ex: "Pagamento Recusado")
            throw error.response ? error.response.data : error.message;
        }
    }
};

export default api;