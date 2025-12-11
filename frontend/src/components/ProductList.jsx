import React, { useEffect, useState } from 'react';
import { ecommerceService } from '../services/api';
import { useCart } from '../context/CartContext';

const ProductList = () => {
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    // Hook do nosso Contexto de Carrinho
    const { addToCart } = useCart();

    useEffect(() => {
        loadProducts();
    }, []);

    const loadProducts = async () => {
        try {
            setLoading(true);
            console.log('🔄 Carregando produtos...');
            // Usa o serviço centralizado com Axios
            const data = await ecommerceService.getProducts();
            console.log('✅ Produtos recebidos:', data);
            console.log('📊 Quantidade de produtos:', data.length);
            setProducts(data);
            setError(''); // Limpa erro anterior
        } catch (err) {
            console.error('❌ Erro ao carregar produtos:', err);
            console.error('❌ Detalhes do erro:', err.response || err.message);
            setError('Não foi possível carregar o catálogo de produtos.');
        } finally {
            setLoading(false);
        }
    };

    if (loading) return <div style={{ textAlign: 'center', padding: '20px' }}>Carregando catálogo...</div>;
    if (error) return <div style={{ color: 'red', textAlign: 'center' }}>{error}</div>;

    return (
        <div style={{ padding: '20px' }}>
            <h2 style={{ marginBottom: '20px', borderBottom: '2px solid #eee', paddingBottom: '10px' }}>
                📦 Catálogo de Produtos
            </h2>

            <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fill, minmax(250px, 1fr))',
                gap: '20px'
            }}>
                {products.map((product) => (
                    <div key={product.id} style={{
                        border: '1px solid #ddd',
                        borderRadius: '8px',
                        padding: '15px',
                        display: 'flex',
                        flexDirection: 'column',
                        gap: '10px',
                        transition: 'box-shadow 0.2s',
                        cursor: 'pointer'
                    }}
                        onMouseEnter={(e) => e.currentTarget.style.boxShadow = '0 4px 12px rgba(0,0,0,0.15)'}
                        onMouseLeave={(e) => e.currentTarget.style.boxShadow = 'none'}
                    >
                        {/* Imagem do Produto com fallback */}
                        <img
                            src={product.image || 'https://via.placeholder.com/200x200/4A90E2/ffffff?text=Produto'}
                            alt={product.name}
                            onError={(e) => {
                                // Se a imagem falhar ao carregar, usa placeholder
                                e.target.onerror = null; // Previne loop infinito
                                e.target.src = 'https://via.placeholder.com/200x200/4A90E2/ffffff?text=Produto';
                            }}
                            style={{
                                width: '100%',
                                height: '200px',
                                objectFit: 'cover',
                                borderRadius: '4px',
                                backgroundColor: '#f0f0f0'
                            }}
                        />

                        <h3 style={{ fontSize: '1.1rem', margin: '0 0 10px 0' }}>{product.name}</h3>
                        <p style={{ fontSize: '0.9rem', color: '#666', flexGrow: 1 }}>
                            {product.description || 'Sem descrição.'}
                        </p>

                        <div style={{ marginTop: '15px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                            <span style={{ fontSize: '1.2rem', fontWeight: 'bold', color: '#2c3e50' }}>
                                R$ {product.price.toFixed(2).replace('.', ',')}
                            </span>

                            <button
                                onClick={() => addToCart(product)}
                                style={{
                                    background: '#28a745',
                                    color: '#fff',
                                    border: 'none',
                                    padding: '8px 15px',
                                    borderRadius: '4px',
                                    cursor: 'pointer',
                                    fontWeight: 'bold'
                                }}
                            >
                                + Adicionar
                            </button>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default ProductList;