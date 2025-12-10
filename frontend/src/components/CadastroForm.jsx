import React, { useState } from 'react';

function CadastroForm({ aoSucesso }) {
    // Estado inicial
    const initialFormState = {
        nome: '',
        sobrenome: '',
        email: '',
        telefone: '',
        endereco_rua: '',
        endereco_cidade: '',
        endereco_estado: '',
        endereco_cep: '',
        endereco_pais: 'Brasil'
    };

    const [formData, setFormData] = useState(initialFormState);
    const [status, setStatus] = useState('');

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({
            ...formData,
            [name]: value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setStatus('Enviando cadastro...');

        const token = localStorage.getItem('accessToken');

        if (!token) {
            setStatus('❌ Erro: Usuário não autenticado. Faça login.');
            return;
        }

        try {
            const response = await fetch('http://127.0.0.1:8000/api/cadastro/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(formData)
            });

            const data = await response.json();

            if (response.ok) {
                setStatus(`✅ Sucesso! ID Interno: ${data.id_interno}. ID Bitrix: ${data.id_bitrix || 'Pendente'}`);

                // CORREÇÃO: Limpa o formulário corretamente resetando para o estado inicial
                setFormData(initialFormState);

                if (aoSucesso) aoSucesso();

            } else if (response.status === 401) {
                setStatus('❌ Erro 401: Token inválido. Faça login novamente.');
            }
            else {
                setStatus('❌ Erro no Servidor: ' + (data.mensagem || JSON.stringify(data)));
            }

        } catch (error) {
            console.error('Erro de conexão:', error);
            setStatus('❌ Erro de conexão com o servidor Django.');
        }
    };

    return (
        <div style={{ maxWidth: '600px', margin: '20px auto', padding: '20px', border: '1px solid #ccc', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
            <h2>Novo Cadastro Completo (Django + Bitrix)</h2>

            <form onSubmit={handleSubmit}>
                <fieldset style={{ border: '1px solid #ddd', padding: '15px', marginBottom: '20px' }}>
                    <legend style={{ fontWeight: 'bold' }}>Dados Pessoais</legend>
                    <div style={{ display: 'flex', gap: '15px' }}>
                        <div style={{ marginBottom: '15px', flex: 1 }}>
                            <label>Nome:</label><br />
                            <input type="text" name="nome" value={formData.nome} onChange={handleChange} required style={{ width: '100%', padding: '10px', marginTop: '5px' }} />
                        </div>
                        <div style={{ marginBottom: '15px', flex: 1 }}>
                            <label>Sobrenome:</label><br />
                            <input type="text" name="sobrenome" value={formData.sobrenome} onChange={handleChange} style={{ width: '100%', padding: '10px', marginTop: '5px' }} />
                        </div>
                    </div>
                    <div style={{ marginBottom: '15px' }}>
                        <label>Email:</label><br />
                        <input type="email" name="email" value={formData.email} onChange={handleChange} required style={{ width: '100%', padding: '10px', marginTop: '5px' }} />
                    </div>
                    <div style={{ marginBottom: '15px' }}>
                        <label>Telefone:</label><br />
                        <input type="text" name="telefone" value={formData.telefone} onChange={handleChange} style={{ width: '100%', padding: '10px', marginTop: '5px' }} />
                    </div>
                </fieldset>

                <fieldset style={{ border: '1px solid #ddd', padding: '15px', marginBottom: '20px' }}>
                    <legend style={{ fontWeight: 'bold' }}>Dados de Endereço</legend>
                    <div style={{ marginBottom: '15px' }}>
                        <label>Rua e Número:</label><br />
                        <input type="text" name="endereco_rua" value={formData.endereco_rua} onChange={handleChange} style={{ width: '100%', padding: '10px', marginTop: '5px' }} />
                    </div>
                    <div style={{ display: 'flex', gap: '15px', marginBottom: '15px' }}>
                        <div style={{ flex: 2 }}>
                            <label>Cidade:</label><br />
                            <input type="text" name="endereco_cidade" value={formData.endereco_cidade} onChange={handleChange} style={{ width: '100%', padding: '10px', marginTop: '5px' }} />
                        </div>
                        <div style={{ flex: 1 }}>
                            <label>Estado (UF):</label><br />
                            <input type="text" name="endereco_estado" value={formData.endereco_estado} onChange={handleChange} style={{ width: '100%', padding: '10px', marginTop: '5px' }} />
                        </div>
                        <div style={{ flex: 1 }}>
                            <label>CEP:</label><br />
                            <input type="text" name="endereco_cep" value={formData.endereco_cep} onChange={handleChange} style={{ width: '100%', padding: '10px', marginTop: '5px' }} />
                        </div>
                    </div>
                    <div style={{ marginBottom: '15px' }}>
                        <label>País:</label><br />
                        <input type="text" name="endereco_pais" value={formData.endereco_pais} onChange={handleChange} style={{ width: '100%', padding: '10px', marginTop: '5px' }} />
                    </div>
                </fieldset>

                <button type="submit" style={{ padding: '10px 20px', background: '#28a745', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', fontWeight: 'bold' }}>
                    CADASTRAR E ENVIAR AO BITRIX
                </button>
            </form>

            {status && <p style={{ marginTop: '15px', fontWeight: 'bold', color: status.startsWith('❌') ? 'red' : 'green' }}>{status}</p>}
        </div>
    );
}

export default CadastroForm;