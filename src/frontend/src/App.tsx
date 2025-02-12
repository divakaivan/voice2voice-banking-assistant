import React, { useState, useRef, useEffect, FC } from 'react';
import Header from './components/Header.tsx';
import Status from './components/Status.tsx';
import RecordingButton from './components/RecordingButtons.tsx';
import ChatContainer from './components/ChatContainer.tsx';
import './App.css'; // Add the required CSS for layout
import welcomeLlama from './welcome_llama.png'; // Import your image

const App: FC = () => {
  const [statusMessage, setStatusMessage] = useState<string>('Click to start recording');
  const [isRecording, setIsRecording] = useState<boolean>(false);
  const [buttonDisabled, setButtonDisabled] = useState<boolean>(false);
  const [chatMessages, setChatMessages] = useState<Array<{ sender: string; message: string }>>([]);

  const websocketRef = useRef<WebSocket | null>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioContextRef = useRef<AudioContext | null>(null);
  const audioQueueRef = useRef<Array<ArrayBuffer>>([]);
  const isPlayingRef = useRef<boolean>(false);

  const initializeWebSocket = (): void => {
    const ws: WebSocket = new WebSocket(`ws://localhost:8000/voice_stream`);
    ws.binaryType = 'arraybuffer';

    ws.onopen = () => {
      setStatusMessage('Ready to talk');
      setButtonDisabled(false);
    };

    ws.onmessage = (event: MessageEvent) => {
      if (event.data instanceof ArrayBuffer) {
        const arrayBuffer: ArrayBuffer = event.data;
        if (arrayBuffer.byteLength > 0) {
          setButtonDisabled(true);
          audioQueueRef.current.push(arrayBuffer);
          if (!isPlayingRef.current) {
            isPlayingRef.current = true;
            processAudioQueue();
          }
        }
      } else if (typeof event.data === 'string') {
        const sender: string = event.data.slice(0, 5);
        const content: string = event.data.slice(6);
        displayChatMessage(sender, content);
        if (sender.toLowerCase() === 'agent') {
          setTimeout(() => {
            setButtonDisabled(false);
            setStatusMessage('Ready to talk');
          }, 500);
        }
      }
    };

    ws.onerror = (error: Event) => {
      console.error('WebSocket error:', error);
      setStatusMessage('WebSocket error occurred.');
      setButtonDisabled(true);
    };

    ws.onclose = () => {
      setStatusMessage('Connection closed. Reconnecting...');
      setButtonDisabled(true);
      setTimeout(() => {
        initializeWebSocket();
      }, 1000);
    };

    websocketRef.current = ws;
  };

  const processAudioQueue = (): void => {
    if (audioQueueRef.current.length === 0) {
      isPlayingRef.current = false;
      return;
    }

    const arrayBuffer: ArrayBuffer = audioQueueRef.current.shift()!;

    if (!audioContextRef.current) {
      audioContextRef.current = new (window.AudioContext || window.AudioContext)();
    }

    if (audioContextRef.current) {
      audioContextRef.current.decodeAudioData(arrayBuffer).then((audioBuffer: AudioBuffer) => {
        const source: AudioBufferSourceNode = audioContextRef.current!.createBufferSource();
        source.buffer = audioBuffer;
        if (audioContextRef.current) {
          source.connect(audioContextRef.current.destination);
        }
        source.onended = () => {
          processAudioQueue();
        };
        source.start(0);
      }).catch((error: Error) => {
        console.error('Error decoding audio data:', error);
        processAudioQueue();
      });
    }
  };

  const displayChatMessage = (sender: string, message: string): void => {
    setChatMessages(prevMessages => [...prevMessages, { sender, message }]);
  };

  const handleToggleRecording = async (): Promise<void> => {
    if (!isRecording) {
      // Start recording
      try {
        const stream: MediaStream = await navigator.mediaDevices.getUserMedia({ audio: true });
        setStatusMessage('Recording...');
        setIsRecording(true);

        const mimeType: string = 'audio/webm;codecs=opus';
        
        if (!MediaRecorder.isTypeSupported(mimeType)) {
          throw new Error(`${mimeType} is not supported on your browser.`);
        }

        const mediaRecorder: MediaRecorder = new MediaRecorder(stream, { mimeType });
        mediaRecorderRef.current = mediaRecorder;
        
        const recordedChunks: Blob[] = [];
        
        mediaRecorder.ondataavailable = (event: BlobEvent): void => { 
          if (event.data.size > 0) {
            recordedChunks.push(event.data); 
          }
        }; 

        mediaRecorder.onstop = (): void => { 
          const audioBlob: Blob = new Blob(recordedChunks, { type: mimeType }); 
          setStatusMessage('Processing...'); 
          sendAudioData(audioBlob); 
        }; 

        mediaRecorder.start(); 
      } catch (err: any) {  
        console.error('Error accessing microphone:', err);  
        setStatusMessage('Error: ' + err.message);  
        setIsRecording(false);
        setButtonDisabled(false);
      } 
    } else {
      // Stop recording
      setIsRecording(false);
      if (mediaRecorderRef.current) {   
        mediaRecorderRef.current.stop();   
        setButtonDisabled(true);
        setStatusMessage('Processing...');   
      } 
    }
  }; 

  const sendAudioData = (audioBlob: Blob): void => {
    if (websocketRef.current && websocketRef.current.readyState === WebSocket.OPEN) {
      setStatusMessage('Sending audio...');
      audioBlob.arrayBuffer().then((arrayBuffer: ArrayBuffer) => {
        websocketRef.current?.send(arrayBuffer);
        setStatusMessage('Waiting for response...');
        isPlayingRef.current = false;
      });
    } else {
      setStatusMessage('Connection lost. Please refresh.');
      setButtonDisabled(true);
    }
  };

  useEffect(() => {
    initializeWebSocket();
  
    return () => {
      if (websocketRef.current && websocketRef.current.readyState === WebSocket.OPEN) {
        websocketRef.current.close();
      }
    };
  }, []);

  return (
    <div className="container">
      <div className="main-content">
        <Header />
        <Status message={statusMessage} />
        <RecordingButton
          onToggle={handleToggleRecording}
          isRecording={isRecording}
          disabled={buttonDisabled}
          className={isRecording ? 'recording' : ''}
        />
        {/* Speech Bubble and Image */}
        <div className="relative flex items-center justify-center mt-4">          
          {/* Llama Image */}
          <img src={welcomeLlama} alt="Llama" className="welcome-llama" />
        </div>
      </div>
      <div className="chat-container">
        <ChatContainer chatMessages={chatMessages} />
      </div>
    </div>
  ); 
};

export default App;
