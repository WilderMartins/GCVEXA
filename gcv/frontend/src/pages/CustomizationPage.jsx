import React, { useState } from 'react';
import { useCustomization } from '../context/CustomizationContext';

const CustomizationPage = () => {
  const { customization, updateCustomization } = useCustomization();
  const [title, setTitle] = useState(customization.app_title);
  const [logo, setLogo] = useState(null);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        // O resultado inclui o prefixo 'data:image/png;base64,'
        // Precisamos remover isso antes de enviar para o backend.
        const base64String = reader.result.split(',')[1];
        setLogo(base64String);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await updateCustomization({
        app_title: title,
        logo_base64: logo,
      });
      alert('Customization updated successfully!');
    } catch (error) {
      alert('Failed to update customization.');
    }
  };

  return (
    <div>
      <h1>Application Customization</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Application Title</label>
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />
        </div>
        <div>
          <label>Logo (PNG)</label>
          <input type="file" accept="image/png" onChange={handleFileChange} />
        </div>
        <button type="submit">Save Changes</button>
      </form>
    </div>
  );
};

export default CustomizationPage;
