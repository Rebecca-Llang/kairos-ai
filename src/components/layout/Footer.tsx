import React from 'react';
import { navigation } from '@/constants/navigation';
import { useNavigation } from '@/hooks/useNavigation';
import { contact } from '@/constants/contact';

import { Link } from 'react-router-dom';

const Footer: React.FC = () => {
  const { items } = useNavigation(navigation);

  return (
    <footer className='bg-dark-matter border-t border-gray-700 mt-8 constellation-bg'>
      <div className='container mx-auto px-6 py-4'>
        <div className='grid grid-cols-1 md:grid-cols-3 gap-4'>
          <div>
            <h3 className='text-sm font-semibold text-starlight mb-2'>
              Navigation
            </h3>
            <nav className='flex flex-col space-y-1'>
              {items.map(item => (
                <Link
                  key={item.href}
                  to={item.href}
                  className='text-sm text-moonbeam hover:text-nebula transition-colors duration-200'
                >
                  {item.name}
                </Link>
              ))}
            </nav>
          </div>

          <div>
            <h3 className='text-sm font-semibold text-starlight mb-2'>
              Connect
            </h3>
            <div className='space-y-1'>
              {contact.map(item => {
                const Icon = item.icon;
                return (
                  <Link
                    key={item.link}
                    to={item.link}
                    className='flex items-center space-x-3 text-sm text-moonbeam hover:text-nebula transition-colors duration-200 group'
                  >
                    <Icon className='w-4 h-4 group-hover:text-nebula transition-colors duration-200' />
                    <span>{item.title}</span>
                  </Link>
                );
              })}
            </div>
          </div>

          <div>
            <h3 className='text-sm font-semibold text-starlight mb-2'>
              About Kairos
            </h3>
            <p className='text-sm text-moonbeam mb-2'>
              An AI companion for creative, introspective, and emotionally
              intelligent conversations.
            </p>
            <p className='text-xs text-moonbeam'>
              Built with 💜 by Rebecca Lang
            </p>
            <p className='text-xs text-moonbeam mt-1'>
              © 2024 Kairos AI. All rights reserved.
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
