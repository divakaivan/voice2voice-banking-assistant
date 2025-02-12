import { render, screen } from '@testing-library/react';
import Status from '../components/Status';

describe('Status Component', () => {
  test('renders message prop correctly', () => {
    const testMessage = 'This is a test message';
    
    render(<Status message={testMessage} />);
    
    const messageElement = screen.getByText(testMessage);
    expect(messageElement).toBeInTheDocument();
  });

  test('renders nothing if no message prop is passed', () => {
    render(<Status/>);

    const messageElement = screen.queryByText(/./);
    expect(messageElement).toBeNull();
  });
});
