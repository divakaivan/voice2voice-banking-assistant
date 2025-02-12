import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import ChatContainer from '../components/ChatContainer';

describe('ChatContainer Component', () => {
  test('renders chat messages correctly', () => {
    const messages = [
      { sender: 'Agent', message: 'Hello! How can I help you?' },
      { sender: 'User', message: 'I need support with my order.' }
    ];

    render(<ChatContainer chatMessages={messages} />);

    expect(screen.getByText(/Agent/i)).toBeInTheDocument();
    expect(screen.getByText(/Hello! How can I help you\?/i)).toBeInTheDocument();
    expect(screen.getByText(/User/i)).toBeInTheDocument();
    expect(screen.getByText(/I need support with my order\./i)).toBeInTheDocument();
  });
});
