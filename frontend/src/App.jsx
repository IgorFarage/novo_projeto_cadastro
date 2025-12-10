import React, { useState, useEffect } from 'react';
import Login from './components/Login';
import Register from './components/Register';
import UserInfo from './components/UserInfo';
import CadastroForm from './components/CadastroForm';
import ListaBitrix from './components/ListaBitrix'; // <--- Importamos a lista nova

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [showRegister, setShowRegister] = useState(false);

  // Verifica se já tem token salvo ao abrir o site
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

  // --- TELA DO SISTEMA (QUANDO LOGADO) ---
  if (isLoggedIn) {
    return (
      <div style={{ maxWidth: '900px', margin: '0 auto', fontFamily: 'Arial', paddingBottom: '50px' }}>
        <h1 style={{ textAlign: 'center', color: '#333' }}>Sistema de Gestão de Leads</h1>

        {/* 1. Barra de Topo com Info do Usuário */}
        <UserInfo onLogout={handleLogout} />

        <hr style={{ margin: '30px 0', border: 'none', borderTop: '1px solid #ddd' }} />

        {/* 2. Formulário de Cadastro */}
        <CadastroForm aoSucesso={() => {
          alert("Lead Cadastrado com Sucesso!");
          // Dica: Aqui poderíamos forçar a lista a atualizar automaticamente
          window.location.reload(); // Maneira simples de atualizar a lista abaixo
        }} />

        <hr style={{ margin: '30px 0', border: 'none', borderTop: '1px solid #ddd' }} />

        {/* 3. Lista de Leads vindos do Bitrix */}
        <ListaBitrix />

      </div>
    );
  }

  // --- TELA DE ACESSO (QUANDO NÃO LOGADO) ---
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