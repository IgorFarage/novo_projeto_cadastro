import React, { useState } from 'react';

function Login({ onLogin, switchToRegister }) {
    const [formData, setFormData] = useState({ username: '', password: '' });
    const [error, setError] = useState('');

    const handleChange = (e) => setFormData({ ...formData, [e.target.name]: e.target.value });

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            // Rota para pegar os Tokens
            const response = await fetch('http://127.0.0.1:8000/auth/jwt/create/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });

            if (response.ok) {
                const data = await response.json();
                // Salva os tokens
                localStorage.setItem('accessToken', data.access);
                localStorage.setItem('refreshToken', data.refresh);
                onLogin();
            } else {
                setError('Usuário ou senha inválidos.');
            }
        } catch (err) {
            setError('Erro de conexão.');
        }
    };

    return (
        <div style={{ maxWidth: '300px', margin: '50px auto', padding: '20px', border: '1px solid #ccc' }}>
            <h2>🔐 Acesso Restrito</h2>
            <form onSubmit={handleSubmit}>
                <input type="text" name="username" placeholder="Usuário" onChange={handleChange} required style={{ width: '100%', marginBottom: '10px', padding: '8px' }} />
                <input type="password" name="password" placeholder="Senha" onChange={handleChange} required style={{ width: '100%', marginBottom: '10px', padding: '8px' }} />
                {error && <p style={{ color: 'red' }}>{error}</p>}
                <button type="submit" style={{ width: '100%', padding: '10px', background: '#007bff', color: 'white', border: 'none' }}>ENTRAR</button>
            </form>
            <p style={{ textAlign: 'center', marginTop: '10px' }}>
                <button onClick={switchToRegister} style={{ background: 'none', border: 'none', color: 'blue', cursor: 'pointer' }}>Criar Conta</button>
            </p>
        </div>
    );
}

export default Login;