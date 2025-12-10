import React, { useState } from 'react';

function CadastroForm({ aoSucesso }) {
    // 1. Estado inicial com todos os campos novos
    const [formData, setFormData] = useState({
        nome: '',
        sobrenome: '',        // Novo
        email: '',
        telefone: '',
        endereco_rua: '',     // Novo
        endereco_cidade: '',  // Novo
        endereco_estado: '',  // Novo
        endereco_cep: '',     // Novo
        endereco_pais: 'Brasil'
    });

    const [status, setStatus] = useState('');

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setStatus('Enviando...');

        // 2. BUSCA O TOKEN DE SEGURANÇA
        const token = localStorage.getItem('accessToken');

        if (!token) {
            setStatus('❌ Erro: Você não está logado.');
            return;
        }

        try {
            const response = await fetch('http://127.0.0.1:8000/api/cadastro/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    // 3. ENVIA O TOKEN (Padrão Bearer)
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(formData)
            });

            const data = await response.json();

            if (response.ok) {
                setStatus(`✅ Sucesso! Lead criado. ID Bitrix: ${data.id_bitrix || 'N/A'}`);
                // Limpa o formulário
                setFormData({
                    nome: '', sobrenome: '', email: '', telefone: '',
                    endereco_rua: '', endereco_cidade: '', endereco_estado: '',
                    endereco_cep: '', endereco_pais: 'Brasil'
                });
                if (aoSucesso) aoSucesso();

            } else {
                // Trata erros específicos (ex: Token expirado)
                if (response.status === 401) {
                    setStatus('❌ Sessão expirada. Faça login novamente.');
                } else {
                    setStatus('❌ Erro: ' + JSON.stringify(data));
                }
            }
        } catch (error) {
            setStatus('❌ Erro de conexão.');
        }
    };

    return (
        <div style={{ maxWidth: '600px', margin: '20px auto', padding: '20px', border: '1px solid #ddd', borderRadius: '8px' }}>
            <h2>Novo Lead (Integrado)</h2>
            <form onSubmit={handleSubmit}>

                {/* DADOS PESSOAIS */}
                <fieldset style={{ border: 'none', padding: 0, marginBottom: '15px' }}>
                    <div style={{ display: 'flex', gap: '10px' }}>
                        <input type="text" name="nome" placeholder="Nome" value={formData.nome} onChange={handleChange} required style={{ flex: 1, padding: '8px' }} />
                        <input type="text" name="sobrenome" placeholder="Sobrenome" value={formData.sobrenome} onChange={handleChange} style={{ flex: 1, padding: '8px' }} />
                    </div>
                    <input type="email" name="email" placeholder="Email" value={formData.email} onChange={handleChange} required style={{ width: '100%', padding: '8px', marginTop: '10px' }} />
                    <input type="text" name="telefone" placeholder="Telefone" value={formData.telefone} onChange={handleChange} style={{ width: '100%', padding: '8px', marginTop: '10px' }} />
                </fieldset>

                {/* ENDEREÇO */}
                <fieldset style={{ border: '1px solid #eee', padding: '10px', marginBottom: '15px' }}>
                    <legend>Endereço</legend>
                    <input type="text" name="endereco_rua" placeholder="Rua e Número" value={formData.endereco_rua} onChange={handleChange} style={{ width: '100%', padding: '8px', marginBottom: '10px' }} />
                    <div style={{ display: 'flex', gap: '10px' }}>
                        <input type="text" name="endereco_cidade" placeholder="Cidade" value={formData.endereco_cidade} onChange={handleChange} style={{ flex: 2, padding: '8px' }} />
                        <input type="text" name="endereco_estado" placeholder="UF" value={formData.endereco_estado} onChange={handleChange} style={{ flex: 1, padding: '8px' }} />
                    </div>
                    <input type="text" name="endereco_cep" placeholder="CEP" value={formData.endereco_cep} onChange={handleChange} style={{ width: '100%', padding: '8px', marginTop: '10px' }} />
                </fieldset>

                <button type="submit" style={{ width: '100%', padding: '10px', background: '#28a745', color: 'white', border: 'none', cursor: 'pointer' }}>
                    CADASTRAR
                </button>
            </form>
            {status && <p style={{ marginTop: '10px', fontWeight: 'bold' }}>{status}</p>}
        </div>
    );
}

export default CadastroForm;