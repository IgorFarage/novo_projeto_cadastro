// frontend/src/components/UserInfo.jsx

import React, { useState, useEffect } from 'react';

function UserInfo({ onLogout }) {
    const [user, setUser] = useState(null);

    useEffect(() => {
        const fetchMe = async () => {
            const token = localStorage.getItem('accessToken');

            if (!token) { onLogout(); return; }

            try {
                // Endpoint que usa o token para saber 'quem sou eu'
                const response = await fetch('http://127.0.0.1:8000/auth/users/me/', {
                    headers: {
                        // PADRÃO OAUTH 2.0: Bearer Token
                        'Authorization': `Bearer ${token}`
                    }
                });

                if (response.ok) {
                    const data = await response.json();
                    setUser(data); // data contém {id, username, email}
                } else {
                    onLogout(); // Se o token falhar ou expirar, desloga
                }
            } catch (error) { console.error("Erro ao buscar info:", error); onLogout(); }
        };
        fetchMe();
    }, [onLogout]);

    if (!user) return <p>Carregando...</p>;

    return (
        <div style={{ padding: '20px', background: '#e6f7ff', border: '1px solid #91d5ff' }}>
            <h3>Você está logado com o nome: <span style={{ color: 'blue' }}>{user.username}</span></h3>
            <p>Seu email: {user.email}</p>
            <button onClick={onLogout}>Sair (Logout)</button>
        </div>
    );
}

export default UserInfo;