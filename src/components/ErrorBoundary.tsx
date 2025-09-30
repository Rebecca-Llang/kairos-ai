import React, { Component } from 'react';

interface Props {
  children: React.ReactNode;
}

interface State {
  hasError: boolean;
}

class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(): State {
    return { hasError: true };
  }

  componentDidCatch(error: Error) {
    console.error('App crashed:', error);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className='min-h-screen flex items-center justify-center bg-deep-space constellation-bg'>
          <div className='text-center animate-twinkle'>
            <h1 className='text-2xl font-bold text-starlight mb-4 text-glow'>
              Something went wrong
            </h1>
            <p className='text-moonbeam mb-6'>
              Kairos encountered an error and needs to restart.
            </p>
            <button
              onClick={() => window.location.reload()}
              className='px-4 py-2 bg-nebula text-white rounded-md hover:bg-indigo-600 shadow-glow hover:shadow-glow-lg transition-colors'
            >
              Reload Page
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
