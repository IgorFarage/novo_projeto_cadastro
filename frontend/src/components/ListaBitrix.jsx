import React, { useEffect, useState } from 'react';

function ListaBitrix() {
    const [leads, setLeads] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    const fetchBitrixData = async () => {
        const token = localStorage.getItem('accessToken');

        try {
            // Chama o NOSSO Django, não o Bitrix direto
            const response = await fetch('http://127.0.0.1:8000/api/cadastro/bitrix-list/', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`, // Segurança JWT
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                const data = await response.json();
                setLeads(data);
            } else {
                setError('Falha ao carregar dados do Bitrix.');
            }
        } catch (err) {
            setError('Erro de conexão com o servidor.');
        } finally {
            setLoading(false);
        }
    };

    // Carrega ao abrir a página
    useEffect(() => {
        fetchBitrixData();
    }, []);

    if (loading) return <p>Carregando dados do CRM...</p>;
    if (error) return <p style={{ color: 'red' }}>{error}</p>;

    return (
        <div style={{ marginTop: '30px', border: '1px solid #ccc', padding: '20px', borderRadius: '8px' }}>
            <h3>📊 Leads Vindos do Bitrix24 (Tempo Real)</h3>
            <button onClick={fetchBitrixData} style={{ marginBottom: '10px', padding: '5px 10px' }}>🔄 Atualizar</button>

            {leads.length === 0 ? (
                <p>Nenhum lead encontrado no Bitrix.</p>
            ) : (
                <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                    <thead>
                        <tr style={{ background: '#f4f4f4', textAlign: 'left' }}>
                            <th style={{ padding: '8px' }}>ID</th>
                            <th style={{ padding: '8px' }}>Título</th>
                            <th style={{ padding: '8px' }}>Nome</th>
                            <th style={{ padding: '8px' }}>Status</th>
                            <th style={{ padding: '8px' }}>Data</th>
                        </tr>
                    </thead>
                    <tbody>
                        {leads.map((lead) => (
                            <tr key={lead.ID} style={{ borderBottom: '1px solid #eee' }}>
                                <td style={{ padding: '8px' }}>{lead.ID}</td>
                                <td style={{ padding: '8px', fontWeight: 'bold' }}>{lead.TITLE}</td>
                                <td style={{ padding: '8px' }}>{lead.NAME} {lead.LAST_NAME}</td>
                                <td style={{ padding: '8px' }}>
                                    <span style={{
                                        background: lead.STATUS_ID === 'NEW' ? '#e6f7ff' : '#eee',
                                        padding: '4px 8px', borderRadius: '4px', fontSize: '0.9em'
                                    }}>
                                        {lead.STATUS_ID}
                                    </span>
                                </td>
                                <td style={{ padding: '8px' }}>{new Date(lead.DATE_CREATE).toLocaleDateString('pt-BR')}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
    );
}

export default ListaBitrix;