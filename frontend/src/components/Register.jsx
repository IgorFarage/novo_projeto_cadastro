// frontend/src/components/Register.jsx

import React, { useState } from 'react';

function Register({ onSwitchToLogin }) {
    // ... (Estados e lógica de handleChange)
    const [formData, setFormData] = useState({ username: '', email: '', password: '' });
    const [msg, setMsg] = useState('');

    // ... (Lógica de submit que usa /auth/users/ )
    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            // 🎯 Endpoint do Djoser
            const response = await fetch('http://127.0.0.1:8000/auth/users/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });

            if (response.ok) {
                alert('Conta criada! Faça login.');
                onSwitchToLogin();
            } else {
                setMsg('Erro ao criar conta.');
            }
        } catch (error) { setMsg('Erro de conexão.'); }
    };

    return (
        // ... (Renderização do formulário)
        <div style={{ maxWidth: '300px', margin: '50px auto', padding: '20px', border: '1px solid #ccc' }}>
            <h2>📝 Criar Conta</h2>
            <form onSubmit={handleSubmit}>
                <input type="text" name="username" placeholder="Usuário" onChange={handleChange} required />
                <input type="email" name="email" placeholder="Email" onChange={handleChange} required />
                <input type="password" name="password" placeholder="Senha" onChange={handleChange} required />
                <button type="submit">CADASTRAR</button>
            </form>
            <button onClick={onSwitchToLogin}>Já tenho conta</button>
        </div>
    );
}

export default Register;