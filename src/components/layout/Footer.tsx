import React from 'react'
import { navigation } from '@/constants/navigation'
import { useNavigation } from '@/hooks/useNavigation'
import { contact } from '@/constants/contact'

import { Link } from 'react-router-dom'

const Footer: React.FC = () => {
  const { items } = useNavigation(navigation)

  return (
    <footer className="bg-gradient-to-r from-primary-50 to-accent-blue/10 border-t border-border mt-8">
      <div className="container mx-auto px-6 py-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <h3 className="text-sm font-semibold text-primary-700 dark:text-primary-300 mb-2">
              Navigation
            </h3>
            <nav className="flex flex-col space-y-1">
              {items.map((item) => (
                <Link
                  key={item.href}
                  to={item.href}
                  className="text-sm text-muted-foreground hover:text-primary-600 dark:hover:text-primary-400 transition-colors duration-200"
                >
                  {item.name}
                </Link>
              ))}
            </nav>
          </div>

          <div>
            <h3 className="text-sm font-semibold text-primary-700 dark:text-primary-300 mb-2">
              Connect
            </h3>
            <div className="space-y-1">
              {contact.map((item) => {
                const Icon = item.icon
                return (
                  <Link
                    key={item.link}
                    to={item.link}
                    className="flex items-center space-x-3 text-sm text-muted-foreground hover:text-accent-purple hover:text-primary-600 dark:hover:text-primary-400 transition-colors duration-200 group"
                  >
                    <Icon className="w-4 h-4 group-hover:text-accent-purple transition-colors duration-200" />
                    <span>{item.title}</span>
                  </Link>
                )
              })}
            </div>
          </div>

          <div>
            <h3 className="text-sm font-semibold text-primary-700 dark:text-primary-300 mb-2">
              About Kairos
            </h3>
            <p className="text-sm text-muted-foreground mb-2">
              An AI companion for creative, introspective, and emotionally
              intelligent conversations.
            </p>
            <p className="text-xs text-muted-foreground">
              Built with 💜 by Rebecca Lang
            </p>
            <p className="text-xs text-muted-foreground mt-1">
              © 2024 Kairos AI. All rights reserved.
            </p>
          </div>
        </div>
      </div>
    </footer>
  )
}

export default Footer
