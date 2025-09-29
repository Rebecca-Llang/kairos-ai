import { Contact } from '@/types'
import { MdEmail } from 'react-icons/md'
import { FaLinkedin } from 'react-icons/fa'
import { FaGithub } from 'react-icons/fa'

export const contact: Contact[] = [
  {
    title: 'Email',
    details: 'rebeccalang50@gmail.com',
    icon: MdEmail,
    link: '/contact-me',
  },
  {
    title: 'LinkedIn',
    link: 'https://www.linkedin.com/in/rebecca-lang-nz/',
    icon: FaLinkedin,
    details: 'linkedin.com/in/rebecca-lang-nz',
  },
  {
    title: 'Github',
    link: 'https://github.com/Rebecca-Llang',
    icon: FaGithub,
    details: 'github.com/Rebecca-Llang',
  },
]
