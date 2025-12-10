// frontend/src/components/Login.jsx

import React, { useState } from 'react';

function Login({ onLogin, switchToRegister }) {
    // ... (Estados e lógica de handleChange)
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            // 🎯 Endpoint do Djoser/JWT para obter tokens
            const response = await fetch('http://127.0.0.1:8000/auth/jwt/create/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });

            if (response.ok) {
                const data = await response.json();

                // 🔐 SALVA OS TOKENS (Chave principal do OAuth)
                localStorage.setItem('accessToken', data.access);
                localStorage.setItem('refreshToken', data.refresh);

                onLogin();
            } else {
                setError('Credenciais inválidas.');
            }
        } catch (err) { setError('Erro de conexão.'); }
    };

    return (
        // ... (Renderização do formulário)
        <div style={{ maxWidth: '300px', margin: '50px auto', padding: '20px', border: '1px solid #ccc' }}>
            <h2>🔐 Login</h2>
            <form onSubmit={handleSubmit}>
                <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} required />
                <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
                {error && <p style={{ color: 'red' }}>{error}</p>}
                <button type="submit">Entrar</button>
            </form>
            <button onClick={switchToRegister}>Não tem conta?</button>
        </div>
    );
}

export default Login;