import React, { useState } from 'react';
import api from '../../services/api';

const ImportScanForm = () => {
    const [tool, setTool] = useState('burpsuite');
    const [file, setFile] = useState(null);
    const [message, setMessage] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        const formData = new FormData();
        formData.append('file', file);

        try {
            await api.post(`/scans/import?tool=${tool}`, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            setMessage('Scan importado com sucesso!');
        } catch (error) {
            setMessage('Erro ao importar o scan.');
        }
    };

    return (
        <div>
            <h2>Importar Scan</h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Ferramenta:</label>
                    <select value={tool} onChange={(e) => setTool(e.target.value)}>
                        <option value="burpsuite">BurpSuite</option>
                    </select>
                </div>
                <div>
                    <label>Arquivo:</label>
                    <input type="file" onChange={(e) => setFile(e.target.files[0])} />
                </div>
                <button type="submit">Importar</button>
            </form>
            {message && <p>{message}</p>}
        </div>
    );
};

export default ImportScanForm;
