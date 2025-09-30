import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { Header, Footer } from './index';
import Chat from '@/pages/Chat';
import Persona from '@/pages/Persona';
import Spellbook from '@/pages/Spellbook';
import History from '@/pages/History';

const Layout: React.FC = () => {
  return (
    <div className='min-h-screen flex flex-col'>
      <Header />
      <main className='flex-1'>
        <Routes>
          <Route path='/' element={<Chat />} />
          <Route path='/persona' element={<Persona />} />
          <Route path='/spellbook' element={<Spellbook />} />
          <Route path='/history' element={<History />} />
        </Routes>
      </main>
      <Footer />
    </div>
  );
};

export default Layout;
