// frontend/src/App.jsx

import React, { useState, useEffect } from 'react';
import Login from './components/Login';
import Register from './components/Register';
import UserInfo from './components/UserInfo';

function App() {
  // ... (Estados e lógica de login/logout/registro)
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [showRegister, setShowRegister] = useState(false);

  useEffect(() => {
    if (localStorage.getItem('accessToken')) {
      setIsLoggedIn(true);
    }
  }, []);

  const handleLogin = () => { setIsLoggedIn(true); setShowRegister(false); };
  const handleLogout = () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    setIsLoggedIn(false);
  };

  if (isLoggedIn) {
    return (
      <div style={{ maxWidth: '900px', margin: '0 auto', fontFamily: 'Arial' }}>
        <h1 style={{ textAlign: 'center' }}>Painel Protegido (JWT)</h1>
        <UserInfo onLogout={handleLogout} />
        {/* Aqui viria o CadastroForm se ele enviasse o token */}
      </div>
    );
  }

  return (
    <div style={{ fontFamily: 'Arial' }}>
      {showRegister ? (
        <Register onSwitchToLogin={() => setShowRegister(false)} />
      ) : (
        <Login onLogin={handleLogin} switchToRegister={() => setShowRegister(true)} />
      )}
    </div>
  );
}

export default App;