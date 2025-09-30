import { NavigationItem } from '@/types'

export const navigation: NavigationItem[] = [
  {
    name: 'Chat',
    href: '/',
  },
  {
    name: 'Persona',
    href: '/persona',
  },
  {
    name: 'Spellbook',
    href: '/spellbook',
  },
  { name: 'History', href: '/history' },
]

export type NavigationItemType = (typeof navigation)[number]
