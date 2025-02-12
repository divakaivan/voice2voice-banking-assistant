import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import RecordingButtons from '../components/RecordingButtons';

describe('RecordingButtons Component', () => {
  test('renders both buttons', () => {
    render(<RecordingButtons onStart={() => {}} onStop={() => {}} startDisabled={false} stopDisabled={false} />);
    expect(screen.getByText('Start Voice Message')).toBeInTheDocument();
    expect(screen.getByText('Stop Voice Message')).toBeInTheDocument();
  });

  test('calls onStart when Start button is clicked', () => {
    const onStartMock = jest.fn();
    render(<RecordingButtons onStart={onStartMock} onStop={() => {}} startDisabled={false} stopDisabled={false} />);
    fireEvent.click(screen.getByText('Start Voice Message'));
    expect(onStartMock).toHaveBeenCalledTimes(1);
  });

  test('calls onStop when Stop button is clicked', () => {
    const onStopMock = jest.fn();
    render(<RecordingButtons onStart={() => {}} onStop={onStopMock} startDisabled={false} stopDisabled={false} />);
    fireEvent.click(screen.getByText('Stop Voice Message'));
    expect(onStopMock).toHaveBeenCalledTimes(1);
  });

  test('disables Start button when startDisabled is true', () => {
    render(<RecordingButtons onStart={() => {}} onStop={() => {}} startDisabled={true} stopDisabled={false} />);
    expect(screen.getByText('Start Voice Message')).toBeDisabled();
  });

  test('disables Stop button when stopDisabled is true', () => {
    render(<RecordingButtons onStart={() => {}} onStop={() => {}} startDisabled={false} stopDisabled={true} />);
    expect(screen.getByText('Stop Voice Message')).toBeDisabled();
  });
});