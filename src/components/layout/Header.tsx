import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { navigation } from '@/constants/navigation';
import { useNavigation } from '@/hooks/useNavigation';

const Header: React.FC = () => {
  const { activeTab, items } = useNavigation(navigation);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  return (
    <header className='bg-dark-matter border-b border-gray-700 constellation-bg'>
      <div className='container mx-auto px-4 sm:px-6 py-3 sm:py-4'>
        <div className='flex items-center justify-between'>
          <h1 className='text-lg sm:text-xl font-bold text-starlight animate-float'>
            Kairos AI
          </h1>

          {/* Desktop Navigation */}
          <nav className='hidden md:flex items-center space-x-6'>
            {items.map(item => (
              <Link
                key={item.href}
                to={item.href}
                className={`text-sm font-medium transition-all duration-200 ${
                  activeTab === item.name
                    ? 'text-message-text font-bold bg-user-message px-3 py-1 rounded-lg shadow-glow'
                    : 'text-gray-300 hover:text-white hover:bg-gray-700 px-3 py-1 rounded-lg'
                }`}
              >
                {item.name}
              </Link>
            ))}
          </nav>

          {/* Mobile Menu Button */}
          <button
            className='md:hidden p-2 text-moonbeam hover:text-nebula transition-colors'
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            aria-label='Toggle mobile menu'
          >
            <svg
              className='w-6 h-6'
              fill='none'
              stroke='currentColor'
              viewBox='0 0 24 24'
            >
              {isMobileMenuOpen ? (
                <path
                  strokeLinecap='round'
                  strokeLinejoin='round'
                  strokeWidth={2}
                  d='M6 18L18 6M6 6l12 12'
                />
              ) : (
                <path
                  strokeLinecap='round'
                  strokeLinejoin='round'
                  strokeWidth={2}
                  d='M4 6h16M4 12h16M4 18h16'
                />
              )}
            </svg>
          </button>
        </div>

        {/* Mobile Navigation */}
        {isMobileMenuOpen && (
          <nav className='md:hidden mt-4 pb-4 border-t border-gray-700 pt-4'>
            <div className='flex flex-col space-y-3'>
              {items.map(item => (
                <Link
                  key={item.href}
                  to={item.href}
                  className={`text-sm font-medium transition-all duration-200 py-2 px-3 rounded-lg ${
                    activeTab === item.name
                      ? 'text-message-text font-bold bg-user-message shadow-glow'
                      : 'text-gray-300 hover:text-white hover:bg-gray-700'
                  }`}
                  onClick={() => setIsMobileMenuOpen(false)}
                >
                  {item.name}
                </Link>
              ))}
            </div>
          </nav>
        )}
      </div>
    </header>
  );
};

export default Header;
