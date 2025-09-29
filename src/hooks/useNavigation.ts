import { useState, useEffect } from 'react'
import { useLocation } from 'react-router-dom'
import { NavigationItem } from '@/types'

export const useNavigation = (items: NavigationItem[]) => {
  const location = useLocation()
  const [activeTab, setActiveTab] = useState<string>(items[0]?.name || '')

  // Sync activeTab with current route
  useEffect(() => {
    const currentItem = items.find((item) => item.href === location.pathname)
    if (currentItem) {
      setActiveTab(currentItem.name)
    }
  }, [location.pathname, items])

  const getActiveItem = () => {
    return items.find((item) => item.name === activeTab)
  }

  const setActiveByHref = (href: string) => {
    const item = items.find((i) => i.href === href)
    if (item) setActiveTab(item.name)
  }

  return {
    activeTab,
    setActiveTab,
    getActiveItem,
    setActiveByHref,
    items,
  }
}
