import React from 'react';
import { navigation } from '@/constants/navigation';
import { useNavigation } from '@/hooks/useNavigation';
import { contact } from '@/constants/contact';

import { Link } from 'react-router-dom';

const Footer: React.FC = () => {
  const { items } = useNavigation(navigation);

  return (
    <footer className='bg-dark-matter border-t border-gray-700 mt-8 constellation-bg'>
      <div className='container mx-auto px-4 sm:px-6 py-6 sm:py-8'>
        <div className='grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 sm:gap-8'>
          <div>
            <h3 className='text-sm font-semibold text-starlight mb-3 sm:mb-4'>
              Navigation
            </h3>
            <nav className='flex flex-col space-y-2'>
              {items.map(item => (
                <Link
                  key={item.href}
                  to={item.href}
                  className='text-sm text-moonbeam hover:text-nebula transition-colors duration-200 py-1'
                >
                  {item.name}
                </Link>
              ))}
            </nav>
          </div>

          <div>
            <h3 className='text-sm font-semibold text-starlight mb-3 sm:mb-4'>
              Connect
            </h3>
            <div className='space-y-2'>
              {contact.map(item => {
                const Icon = item.icon;
                return (
                  <Link
                    key={item.link}
                    to={item.link}
                    className='flex items-center space-x-3 text-sm text-moonbeam hover:text-nebula transition-colors duration-200 group py-1'
                  >
                    <Icon className='w-4 h-4 group-hover:text-nebula transition-colors duration-200' />
                    <span>{item.title}</span>
                  </Link>
                );
              })}
            </div>
          </div>

          <div className='sm:col-span-2 lg:col-span-1'>
            <h3 className='text-sm font-semibold text-starlight mb-3 sm:mb-4'>
              About Kairos
            </h3>
            <p className='text-sm text-moonbeam mb-3 sm:mb-4 leading-relaxed'>
              An AI companion for creative, introspective, and emotionally
              intelligent conversations.
            </p>
            <div className='space-y-1'>
              <p className='text-xs text-moonbeam'>
                Built with 💜 by Rebecca Lang
              </p>
              <p className='text-xs text-moonbeam'>
                © 2024 Kairos AI. All rights reserved.
              </p>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
