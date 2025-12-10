import React, { useState, useEffect } from 'react';
import Login from './components/Login';
import Register from './components/Register';
import UserInfo from './components/UserInfo';
import CadastroForm from './components/CadastroForm';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [showRegister, setShowRegister] = useState(false);

  // Verifica se já existe um token salvo ao carregar a página
  useEffect(() => {
    if (localStorage.getItem('accessToken')) {
      setIsLoggedIn(true);
    }
  }, []);

  const handleLogin = () => {
    setIsLoggedIn(true);
    setShowRegister(false);
  };

  const handleLogout = () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    setIsLoggedIn(false);
  };

  // --- TELA DO SISTEMA (LOGADO) ---
  if (isLoggedIn) {
    return (
      <div style={{ maxWidth: '800px', margin: '0 auto', fontFamily: 'Arial' }}>
        <h1 style={{ textAlign: 'center', color: '#333' }}>Sistema de Leads</h1>

        {/* Mostra quem está logado e botão de sair */}
        <UserInfo onLogout={handleLogout} />

        <hr style={{ margin: '30px 0', borderTop: '1px solid #ccc' }} />

        {/* Formulário Protegido */}
        <CadastroForm />
      </div>
    );
  }

  // --- TELA DE ACESSO (NÃO LOGADO) ---
  return (
    <div style={{ fontFamily: 'Arial' }}>
      <h1 style={{ textAlign: 'center' }}>Portal de Acesso</h1>
      {showRegister ? (
        <Register onSwitchToLogin={() => setShowRegister(false)} />
      ) : (
        <Login onLogin={handleLogin} switchToRegister={() => setShowRegister(true)} />
      )}
    </div>
  );
}

export default App;