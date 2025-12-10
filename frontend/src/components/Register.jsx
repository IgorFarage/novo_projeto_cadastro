import React, { useState } from 'react';

function Register({ onSwitchToLogin }) {
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: '',
        re_password: '' // 🔒 Campo extra exigido pelo Djoser para segurança
    });
    const [msg, setMsg] = useState('');

    const handleChange = (e) => setFormData({ ...formData, [e.target.name]: e.target.value });

    const handleSubmit = async (e) => {
        e.preventDefault();

        // Validação simples no frontend
        if (formData.password !== formData.re_password) {
            setMsg('❌ As senhas não coincidem!');
            return;
        }

        try {
            // Rota de registro de USUÁRIOS (com senha)
            const response = await fetch('http://127.0.0.1:8000/auth/users/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });

            if (response.ok) {
                alert('Conta criada com sucesso! Agora faça login.');
                onSwitchToLogin(); // Volta para a tela de login
            } else {
                const data = await response.json();
                setMsg('❌ Erro: ' + JSON.stringify(data));
            }
        } catch (error) {
            setMsg('❌ Erro de conexão.');
        }
    };

    return (
        <div style={{ maxWidth: '300px', margin: '50px auto', padding: '20px', border: '1px solid #ccc' }}>
            <h2>📝 Criar Conta de Usuário</h2>
            <form onSubmit={handleSubmit}>
                <div style={{ marginBottom: '10px' }}>
                    <input type="text" name="username" placeholder="Usuário" onChange={handleChange} required style={{ width: '100%' }} />
                </div>
                <div style={{ marginBottom: '10px' }}>
                    <input type="email" name="email" placeholder="Email" onChange={handleChange} required style={{ width: '100%' }} />
                </div>
                <div style={{ marginBottom: '10px' }}>
                    <input type="password" name="password" placeholder="Senha" onChange={handleChange} required style={{ width: '100%' }} />
                </div>
                <div style={{ marginBottom: '10px' }}>
                    <input type="password" name="re_password" placeholder="Confirmar Senha" onChange={handleChange} required style={{ width: '100%' }} />
                </div>

                {msg && <p style={{ color: msg.startsWith('❌') ? 'red' : 'green' }}>{msg}</p>}

                <button type="submit" style={{ width: '100%', padding: '10px', background: 'green', color: 'white' }}>CADASTRAR</button>
            </form>

            <button onClick={onSwitchToLogin} style={{ marginTop: '10px', background: 'none', border: 'none', color: 'blue', cursor: 'pointer' }}>
                Já tenho conta
            </button>
        </div>
    );
}

export default Register;