import React from 'react';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import App from '../App';
import { AuthProvider } from '../context/AuthContext';
import { CustomizationProvider } from '../context/CustomizationContext';

// Mock para a API para evitar chamadas de rede nos testes de UI
vi.mock('../services/api', () => ({
  default: {
    get: vi.fn(() => Promise.resolve({ data: {} })),
    post: vi.fn(() => Promise.resolve({ data: {} })),
  },
}));

describe('App Routing', () => {
  it('renders login page for the root route when not authenticated', () => {
    render(
      <MemoryRouter initialEntries={['/']}>
        <CustomizationProvider>
          <AuthProvider>
            <App />
          </AuthProvider>
        </CustomizationProvider>
      </MemoryRouter>
    );

    // Como a rota '/' é protegida, o usuário é redirecionado para '/login'
    expect(screen.getByRole('heading', { name: /login/i })).toBeInTheDocument();
  });
});
