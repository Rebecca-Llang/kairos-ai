import React from 'react'
import { Link } from 'react-router-dom'
import { navigation } from '@/constants/navigation'
import { useNavigation } from '@/hooks/useNavigation'

const Header: React.FC = () => {
  const { activeTab, items } = useNavigation(navigation)

  return (
    <header className="bg-gradient-to-r from-primary-50 to-accent-blue/10 border-b border-border">
      <div className="container mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          <h1 className="text-xl font-bold text-primary-800 dark:text-primary-200">
            Kairos AI
          </h1>
          <nav className="flex items-center space-x-6">
            {items.map((item) => (
              <Link
                key={item.href}
                to={item.href}
                className={`text-sm font-medium transition-all duration-200 ${
                  activeTab === item.name
                    ? 'text-primary-600 dark:text-primary-400 font-bold'
                    : 'text-muted-foreground hover:text-accent-purple'
                }`}
              >
                {item.name}
              </Link>
            ))}
          </nav>
        </div>
      </div>
    </header>
  )
}

export default Header
