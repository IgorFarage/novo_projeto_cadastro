import React, { useState, useEffect } from 'react';

// Componentes de Autenticação
import Login from './components/Login';
import Register from './components/Register';

// Componentes da Aplicação (Header e Leads - mantivemos caso queira usar depois)
import UserInfo from './components/UserInfo';

// --- NOVOS COMPONENTES DA LOJA ---
import ProductList from './components/ProductList';
import CartSidebar from './components/CartSidebar';

// Você pode remover ou comentar estes dois se não for usar a tela de Leads agora
// import CadastroForm from './components/CadastroForm';
// import ListaBitrix from './components/ListaBitrix';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [showRegister, setShowRegister] = useState(false);

  // Verifica token ao iniciar
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
      <div style={{ display: 'flex', flexDirection: 'column', height: '100vh', fontFamily: 'Arial' }}>

        {/* 1. TOPO: Header Fixo */}
        <header style={{
          padding: '10px 20px',
          background: '#333',
          color: '#fff',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          boxShadow: '0 2px 5px rgba(0,0,0,0.1)'
        }}>
          <h1 style={{ margin: 0, fontSize: '1.2rem' }}>Minha Loja Bitrix</h1>
          <UserInfo onLogout={handleLogout} />
        </header>

        {/* 2. CONTEÚDO PRINCIPAL: Layout Flexível (Lado a Lado) */}
        <div style={{ display: 'flex', flexGrow: 1, overflow: 'hidden', background: '#f4f4f4' }}>

          {/* ESQUERDA: Catálogo de Produtos (Ocupa o espaço restante) */}
          <main style={{ flex: 1, overflowY: 'auto', padding: '20px' }}>
            <ProductList />
          </main>

          {/* DIREITA: Carrinho (Largura fixa) */}
          <aside style={{
            width: '350px',
            background: '#fff',
            borderLeft: '1px solid #ddd',
            boxShadow: '-2px 0 10px rgba(0,0,0,0.05)',
            zIndex: 10
          }}>
            <CartSidebar />
          </aside>

        </div>
      </div>
    );
  }

  // --- TELA DE ACESSO (QUANDO NÃO LOGADO) ---
  // (Mantive exatamente igual ao seu original)
  return (
    <div style={{ fontFamily: 'Arial' }}>
      <h1 style={{ textAlign: 'center', marginTop: '50px' }}>Portal de Acesso</h1>
      {showRegister ? (
        <Register onSwitchToLogin={() => setShowRegister(false)} />
      ) : (
        <Login onLogin={handleLogin} switchToRegister={() => setShowRegister(true)} />
      )}
    </div>
  );
}

export default App;